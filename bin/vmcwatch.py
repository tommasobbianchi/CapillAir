#!/usr/bin/env python3
"""Watch for the two decisions that actually need acting on:
   1. WHEN TO OPEN THE WINDOWS  — outdoor colder than indoor, measured, plus a
      moisture check so we don't trade heat for humidity.
   2. WHEN TO CLOSE THEM        — outdoor climbing back past indoor.
Plus VMC regime changes and sensor health. Ambient comes from the NORTH SENSOR
(measured), not weather.forecast_home, which ran +1.4 C high and steps coarsely.
"""
import json, time, urllib.request, sys
from pathlib import Path
TOK = (Path.home()/".local/share/capillair-window/env").read_text().split("HA_TOKEN=")[1].split("\n")[0]
OPEN_MARGIN  = 1.0   # only worth opening once outdoor is this far BELOW the warmest room
HYST         = 0.3   # keeps the open threshold strictly below the close threshold
BANK = Path.home()/".local/share/capillair-window/banked_min.json"
# The ONLY rain signal available: weather.forecast_home. There is no physical rain sensor
# on this house. It is coarse and laggy -- on 2026-08-20 it read "rainy" at 20:04 as rain
# began, then flipped back to "cloudy" at 20:59 while it was still raining. So it is used
# ONLY to suppress a new open and to warn once; it never forces a close. Which windows are
# sheltered is the user's knowledge, not a number we hold.
RAIN = {"rainy", "pouring", "lightning-rainy", "hail", "snowy-rainy"}

def states():
    r = urllib.request.Request("http://100.71.237.68:8123/api/states",
                               headers={"Authorization": "Bearer " + TOK})
    return {e["entity_id"]: e for e in json.load(urllib.request.urlopen(r, timeout=25))}
def notify(title, msg):
    """Push through Home Assistant. The whole point of running this as a service is
    that the alert must arrive whether or not a Claude session is up."""
    for svc, payload in (("telegram", {"title": title, "message": msg}),
                         ("mobile_app_pixel_9a", {"title": title, "message": msg})):
        try:
            r = urllib.request.Request(
                "http://100.71.237.68:8123/api/services/notify/" + svc,
                data=json.dumps(payload).encode(),
                headers={"Authorization": "Bearer " + TOK, "Content-Type": "application/json"},
                method="POST")
            urllib.request.urlopen(r, timeout=20)
        except Exception as e:
            print(f"    [notify {svc} failed: {type(e).__name__}]")


def num(s, e):
    v = s[e]["state"]
    return None if v in ("unavailable", "unknown") else float(v)

prev_open = None; prev_rain = False; last = 0; last_rain_warn = 0; fails = 0
hist = []   # (epoch, outdoor) for the last hour, to tell the morning ramp from the evening fall
while True:
    try:
        s = states(); fails = 0
        out  = num(s, "sensor.capillair_north_temperatura")
        cav  = num(s, "sensor.capillair_out_temperatura")
        # Compare against the WARMEST OCCUPIED ROOM, not the ENV IV: that node reads
        # 1.44 C cooler than the bedrooms on average (0.77-1.89 range), so using it said
        # "keep shut" while the rooms people are in were already gaining. Caught 2026-08-19
        # when the windows were opened at 20:30 and were right to be.
        rooms = [num(s, e) for e in (
            "sensor.temperatura_rilevata_camera1_piano_primo",
            "sensor.temperatura_rilevata_camera2_piano_primo",
            "sensor.temperatura_rilevata_soggiorno_piano_terra",
            "sensor.temperatura_rilevata_cucina_piano_terra")]
        rooms = [x for x in rooms if x is not None]
        env  = num(s, "sensor.capillair_env_iv_temperatura")
        ind  = max(rooms) if rooms else env          # window decision: warmest room
        # VMC delta stays referenced to the ENV IV: its supply mixes house-wide, and
        # switching reference mid-day would break comparability with the whole log.
        cond = s.get("weather.forecast_home", {}).get("state", "")
        raining = cond in RAIN
        oah  = num(s, "sensor.capillair_north_umidita_assoluta")
        iah  = num(s, "sensor.capillair_env_iv_umidita_assoluta")
        cah  = num(s, "sensor.capillair_out_umidita_assoluta")
        if out is None:
            print(f"[{time.strftime('%H:%M')}] ALERT north sensor offline — cannot judge windows")
            sys.stdout.flush(); time.sleep(300); continue
        # ASYMMETRIC thresholds, deliberately:
        #   OPEN  on the WARMEST room  — the hot rooms gain first, and opening early
        #         costs nothing while outdoor is below them.
        #   CLOSE on the COOLEST CONNECTED room — the rooms that actually got cooled are
        #         the ones you are about to spoil. Every minute past their crossover
        #         re-heats exactly the rooms the night's purge paid for.
        #         This replaced the house MEAN on 2026-08-20. The mean was dragged up by
        #         taverna and studio, which have NO opening of their own and which the
        #         purge never reached (taverna: -0.3 C in 11 h while cucina did -2.0).
        #         Waiting for the mean spoils the good rooms to chase rooms that are not
        #         on the circuit at all. `rooms` below is already the connected set.
        house_mean = sum(rooms)/len(rooms) if rooms else ind
        coolest = min(rooms) if rooms else ind
        # LATCHED, not live. Closing on the LIVE coolest room does not work: open windows
        # couple the rooms to outdoor air, so as outdoor climbs the rooms climb with it and
        # the threshold runs away from the very number that is chasing it. Measured
        # 2026-08-20: 07:20 close>28.2, 08:50 close>28.8 — the target moved up 0.6 C in 90
        # min while the house was actively being heated, and the call came ~1 h late.
        # The right target is the BEST temperature actually banked this cycle: a fixed
        # number that outdoor can genuinely overtake.
        try:    banked = json.loads(BANK.read_text())["min"]
        except Exception: banked = coolest
        gap = out - ind                      # vs warmest occupied room
        # Hysteresis: the open threshold must stay strictly BELOW the close threshold or
        # the two rules fight. With a 1.5 C spread across the house, `warmest - 1.0` sits
        # ABOVE `coolest`, which would open and close on alternating polls.
        close_thr = banked
        # Opening still keys off the LIVE rooms — the second term stops the two rules
        # fighting when the house spread exceeds OPEN_MARGIN.
        open_thr  = min(ind - OPEN_MARGIN, coolest - HYST)
        # ...but a temperature test alone reopens into the MORNING RAMP: once shut, the
        # rooms warm, open_thr rises to meet the climbing outdoor air, and the rule invites
        # you to open at 28.4 having just closed at 28.0. Replay 2026-08-20 did exactly
        # that at 08:21. Opening is only ever right on the EVENING FALL, so require the
        # outdoor trend to be flat or downward.
        # A 1 h window is not enough: a plateau in the morning ramp reads as flat and
        # reopened the windows at 08:51 in replay. Over 2 h the morning ramp is
        # unambiguously up and the evening fall unambiguously down.
        hist.append((time.time(), out))
        hist[:] = [h for h in hist if time.time() - h[0] <= 7200]
        span = time.time() - hist[0][0]
        trend = (out - hist[0][1]) if span >= 5400 else None   # None = not enough history
        falling = trend is not None and trend <= -0.3
        # SEED FROM REALITY, not from the rule. On a restart prev_open is None, and deriving
        # it from the open rule asks "would I open now?", which in a rising morning is False
        # even with the windows wide open -- so the morning CLOSE would never fire. The
        # camera classifier knows the actual state; fall back to the rule only if it doesn't.
        if prev_open is None:
            w = s.get("sensor.piano_primo_finestra", {}).get("state", "")
            if w in ("aperta", "vasistas"): prev_open = True
            elif w == "chiusa":             prev_open = False
            print(f"[{time.strftime('%H:%M')}] seeded windows={'OPEN' if prev_open else 'shut'} "
                  f"from classifier state '{w or 'unavailable'}'")
        if prev_open:                        # currently open -> close on the BANKED min
            should_open = out < close_thr
        else:                                # currently shut -> open only on a real fall.
            # No history yet (restart) => stay shut. Fails closed: a missed open costs one
            # evening, a wrong open imports heat into a house that spent all night cooling.
            # Rain gates the shut->open transition ONLY. It deliberately does not appear in
            # the prev_open branch: rain does not force a close. The 2026-08-20 rain gave the
            # best cooling of the campaign (-6.6 C gradient), so auto-closing on it would
            # have thrown away the best hours we have measured.
            should_open = out < open_thr and falling and not raining
        if prev_open and coolest < banked:   # still open and still improving -> bank it
            banked = coolest
            BANK.write_text(json.dumps({"min": banked, "at": time.strftime("%Y-%m-%dT%H:%M")}))
        if prev_open is not None and should_open != prev_open:
            if should_open:
                wet = "will HUMIDIFY" if (oah or 0) > (iah or 0) else "will also DRY"
                # Do NOT blanket-recommend the low opening: this basement often sits BELOW
                # outdoor air, and opening it then imports heat into the coolest part of the
                # house. Check the actual interrato temperature first.
                intr = num(s, "sensor.temperatura_rilevata_camera_interrato")
                if intr is not None and out > intr:
                    where = (f"Open HIGH (piano primo) only. NOT the interrato yet: it is {intr:.1f} C, "
                             f"{out-intr:+.1f} C BELOW outdoor — opening it now imports heat. "
                             f"Add the low opening once outdoor drops under {intr:.1f}.")
                else:
                    where = ("Open LOW (interrato/garage) AND HIGH (piano primo) — the pair is what "
                             "drives the stack; flow scales with sqrt(house mean - outdoor).")
                m = (f"Esterno {out:.1f} vs stanza piu calda {ind:.1f} ({gap:+.1f}C). "
                     f"Umidita est/int {oah:.1f}/{iah:.1f} g/m3 - {wet}. {where}")
                banked = coolest        # new purge cycle: bank restarts from here
                BANK.write_text(json.dumps({"min": banked, "at": time.strftime("%Y-%m-%dT%H:%M")}))
                print(f"[{time.strftime('%H:%M')}] *** OPEN THE WINDOWS *** {m}")
                notify("APRIRE LE FINESTRE", m)
            else:
                m = (f"Esterno {out:.1f} ha superato il minimo notturno {banked:.1f} "
                     f"(media casa {house_mean:.1f}). CHIUDERE PIANO PRIMO E PIANO TERRA. "
                     f"Lasciare aperto interrato/cavedio: il cavedio ({cav:.1f}) sta sotto "
                     f"la casa tutto il giorno e tira il camino.")
                notify("CHIUDERE IL PIANO PRIMO", m)
                print(f"[{time.strftime('%H:%M')}] *** CLOSE TOP + PIANO TERRA *** outdoor {out:.1f} has passed "
                      f"the coolest connected room {coolest:.1f} (mean {house_mean:.1f}). LEAVE THE INTERRATO/CAVEDIO OPEN — the cavedio is "
                      f"below the house all day and drives the passive stack. Closing the top is about WIND, "
                      f"not temperature: the stack is ~0.7 Pa and a 13 km/h breeze is 7.6 Pa, so an open top "
                      f"window stops being a reliable exhaust.")
        # Warn ONCE when rain starts with the windows open. Not a close instruction: only
        # the user knows which openings are sheltered.
        # The forecast flip-flops (rainy -> cloudy -> rainy inside one shower), so a bare
        # edge-trigger warned 3x for one event in replay. One warning per 3 h.
        if raining and not prev_rain and prev_open and time.time() - last_rain_warn > 10800:
            last_rain_warn = time.time()
            m = (f"PIOGGIA ({cond}) con le finestre aperte. Esterno {out:.1f}, casa {ind:.1f}. "
                 f"Chiudere o mettere a vasistas SOLO le finestre esposte - l'aria di pioggia "
                 f"raffredda bene, non chiudere tutto.")
            print(f"[{time.strftime('%H:%M')}] *** RAIN with windows open *** {cond}, outdoor {out:.1f}")
            notify("PIOGGIA - FINESTRE APERTE", m)
        prev_rain = raining
        prev_open = should_open
        if time.time() - last > 5400:
            v = f"{cav-env:+.2f}" if (cav is not None and env is not None) else "?"
            tr = "n/a" if trend is None else f"{trend:+.1f}"
            print(f"[{time.strftime('%H:%M')}] outdoor {out:.1f} | indoor {ind:.1f} ({gap:+.1f}) | "
                  f"cavedio {cav:.1f} (VMC {v}C vs ENV IV {env:.1f}) | AH out {oah:.1f} cav {cah:.1f} ind {iah:.1f} | "
                  f"thr open<{open_thr:.1f} close>{close_thr:.1f} (banked {banked:.1f}, 2h trend {tr}) | "
                  f"windows: {'OPEN' if should_open else 'keep shut'}")
            last = time.time()
    except Exception as e:
        fails += 1
        # Was `fails in (3, 10)` — a NameError on 2026-08-20 crashed every poll and stayed
        # invisible for 15 min. Report the first one immediately, then throttle.
        if fails == 1 or fails in (3, 10) or fails % 50 == 0:
            print(f"[{time.strftime('%H:%M')}] ALERT polling failed {fails}x: {type(e).__name__} {e}")
    sys.stdout.flush(); time.sleep(300)
