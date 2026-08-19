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
OPEN_MARGIN  = 1.0   # only worth opening once outdoor is this far BELOW indoor
CLOSE_MARGIN = 0.0   # close as soon as it comes back up to indoor

def states():
    r = urllib.request.Request("http://100.71.237.68:8123/api/states",
                               headers={"Authorization": "Bearer " + TOK})
    return {e["entity_id"]: e for e in json.load(urllib.request.urlopen(r, timeout=25))}
def notify(title, msg):
    """Push through Home Assistant. The whole point of running this as a service is
    that the alert must arrive whether or not a Claude session is up."""
    for svc, payload in (("telegram", {"title": title, "message": msg}),
                         ("mobile_app_pixel_9a_tommy", {"title": title, "message": msg})):
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

prev_open = None; last = 0; fails = 0
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
        oah  = num(s, "sensor.capillair_north_umidita_assoluta")
        iah  = num(s, "sensor.capillair_env_iv_umidita_assoluta")
        cah  = num(s, "sensor.capillair_out_umidita_assoluta")
        if out is None:
            print(f"[{time.strftime('%H:%M')}] ALERT north sensor offline — cannot judge windows")
            sys.stdout.flush(); time.sleep(300); continue
        # ASYMMETRIC thresholds, deliberately:
        #   OPEN  on the WARMEST room  — the hot rooms gain first, and opening early
        #         costs nothing while outdoor is below them.
        #   CLOSE on the HOUSE MEAN    — stop before the average room starts importing
        #         heat. Closing on the warmest room would run hours too late; closing
        #         at dawn (the traditional habit) runs ~4 h too early. Measured
        #         2026-08-19: outdoor passed the mean at 11:58, the house was shut 07:13.
        house_mean = sum(rooms)/len(rooms) if rooms else ind
        gap = out - ind                      # vs warmest occupied room
        if prev_open:                        # currently open -> close on the MEAN
            should_open = out < house_mean
        else:                                # currently shut -> open on the WARMEST
            should_open = gap <= -OPEN_MARGIN
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
                print(f"[{time.strftime('%H:%M')}] *** OPEN THE WINDOWS *** {m}")
                notify("APRIRE LE FINESTRE", m)
            else:
                m = (f"Esterno {out:.1f} ha superato la media casa {house_mean:.1f}. "
                     f"CHIUDERE SOLO IL PIANO PRIMO. Lasciare aperto interrato/cavedio: "
                     f"il cavedio ({cav:.1f}) sta sotto la casa tutto il giorno e tira il camino.")
                notify("CHIUDERE IL PIANO PRIMO", m)
                print(f"[{time.strftime('%H:%M')}] *** CLOSE THE TOP (piano primo) *** outdoor {out:.1f} has passed "
                      f"the house mean {house_mean:.1f}. LEAVE THE INTERRATO/CAVEDIO OPEN — the cavedio is "
                      f"below the house all day and drives the passive stack. Closing the top is about WIND, "
                      f"not temperature: the stack is ~0.7 Pa and a 13 km/h breeze is 7.6 Pa, so an open top "
                      f"window stops being a reliable exhaust.")
        prev_open = should_open
        if time.time() - last > 5400:
            v = f"{cav-env:+.2f}" if (cav is not None and env is not None) else "?"
            print(f"[{time.strftime('%H:%M')}] outdoor {out:.1f} | indoor {ind:.1f} ({gap:+.1f}) | "
                  f"cavedio {cav:.1f} (VMC {v}C vs ENV IV {env:.1f}) | AH out {oah:.1f} cav {cah:.1f} ind {iah:.1f} | "
                  f"windows: {'OPEN' if should_open else 'keep shut'}")
            last = time.time()
    except Exception as e:
        fails += 1
        if fails in (3, 10): print(f"[{time.strftime('%H:%M')}] ALERT polling failed {fails}x: {type(e).__name__} {e}")
    sys.stdout.flush(); time.sleep(300)
