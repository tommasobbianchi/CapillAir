# CapillAir — handoff, 2026-08-20 15:30

## THE HEADLINE: the stack is a CHANNEL, not a house-wide sweep

Yesterday's handoff said a ~1090 W passive cavedio loop cools the house. Half right.
The loop is real, but **it only cools rooms that have their own opening.**

Measured overnight 2026-08-19/20, windows open 20:30 -> 09:15:

```
house mean  29.96 -> 28.77   = -1.19 C
  of which  20:30-00:30  -0.15 C   (top + interrato only)
            00:30-07:00  -0.78 C   (after a PIANO TERRA window was opened)
```

Four hours with a 3.4 C deficit produced **-0.02 C/h**. The purge had stalled. Opening a
piano terra window restarted it and cucina went to **-0.83 C/h**.

**Taverna is the control that proves it.** Same level as the interrato, no opening of its
own: **-0.3 C in eleven hours** while cucina did -2.0. It is now flat to within 0.2 C
across 18 h — decoupled from both the purge and the daytime load.

```
cavedio -> interrato -> stairwell -> piano primo -> out
                          ^
        rooms hang off this and get NOTHING unless they have their own opening
```

Caveat kept honest: the PT opening and the outdoor crossover happened within an hour of
each other, so tonight's data cannot fully separate them. Taverna is the evidence that the
opening mattered. A second night puts a number on it.

## The window rule (rewritten this session, committed 9de651c)

**CLOSE on the coolest CONNECTED room, latched to the minimum banked this cycle.**

Three attempts were needed; the first two are instructive:

1. **Live coolest room does not work.** Open windows couple rooms to outdoor air, so the
   threshold climbs with the number chasing it: 28.2 at 07:20, 28.8 at 08:50. The call ran
   ~84 min late and gave back ~0.8 C. Now latched to `banked_min.json`.
2. **Latching alone reopens into the morning ramp**, because the OPEN threshold still keys
   off live rooms and they warm too. Replay reopened at 28.4 having closed at 28.0.
3. **A 1 h trend guard is fooled by a plateau** in the ramp (reopened 08:51, trend -0.0).
   Now requires a sustained **2 h fall of >= 0.3 C**.

Replay over the real CSV now yields exactly two flips: open 20:55, close 07:51.
The old rule closed at 09:15 — the fix is worth ~0.8 C.

**OPEN** on the warmest room -1 C, clamped by coolest -0.3 (hysteresis), AND a 2 h fall.
**Interrato/cavedio NEVER close.** Cavedio ran 27.1-28.1 while ambient hit 33.0.

## Reference-frame errors — the pattern that keeps recurring

Yesterday logged four. This session added two more, same class:

5. **Reported `out_real_t` as "outdoor" for six hours.** It is `capillair_out` = the
   **cavedio**. True outdoor is `north_t`. Every table from 00:53 to 05:50 was mislabelled.
   The conclusions survived (the cavedio is the stack inlet, so it was the right reference
   by accident) but the "outdoor bottomed at 25.9" call was wrong — that was the damped
   cavedio; real ambient was 30.0 at 20:00 and still falling at 05:00.
6. **Then "corrected" a non-error**: flagged yesterday's flat morning north readings as a
   mis-deployed sensor. Same mistake again — that column was the cavedio, and flat ~26 all
   morning is exactly the damping already measured.

**`analyse.py` also compared the cavedio against the FORECAST, not the north node**, while
the table above it used north. Damping is **75%**, not the 82-93% previously reported.

## Measured

```
DAMPING 75%   (vs measured north node; the old 82-93% was against the forecast)
gap at ambient peak: cavedio 27.74 vs ambient 33.34 = -5.60 C
VMC over 23.9 h: mean -82 W = -1.96 kWh cooling; moisture -0.15 g/m3 (DRIES)
daytime with everything sealed: house +1.29 C against a 7.6 C outdoor swing
altitude 290 m -> every watt is x0.942 vs the sea-level 0.335 constant
```

## Operational faults found

- **A duplicate advisor ran all night.** Launched as a foreground Bash process in the
  previous session (22:19), still executing pre-fix code, emitting a second conflicting
  advice stream. Killed by PID. **Never leave a watcher running from a Bash tool call.**
- **Silent crash loop.** A NameError crashed every poll for ~10 min invisibly, because the
  handler only spoke at the 3rd and 10th failure. Now the first failure reports immediately.
- **Service exited once unexplained** (14:10:22, restart counter 1, no traceback, no ALERT
  line) — so it exited OUTSIDE the try block, pointing at `states()`/HTTP, not the logic.
  `Restart=always` covered it. **The restart wiped the 2 h trend history**, and the open
  rule fails closed without it — a restart near the evening crossover silently delays the
  open. Trend history should be persisted like `banked_min.json`.
- `pgrep -c -f vmcwatch` counts your own shell. Use `ps -eo pid,cmd | grep "[v]mcwatch"`.

## Services (all survive reboot, linger on)

| unit | cadence |
|---|---|
| `capillair-climate.timer` | 5 min -> `data/climate.csv` (43 cols) |
| `capillair-window.timer` | 10 min -> classifier -> MQTT -> HA |
| `capillair-report.timer` | 13/17/20/23:00 -> `reports/` |
| `capillair-windows.service` | continuous, notifies open/close -> `reports/windows.log` |

`analyse.py` now takes a **rolling 24 h** window (`analyse.py 48` for 48 h), not the
calendar day — the night purge straddles midnight and `startswith(today)` discarded half.

## Open items, priority order

1. **Give taverna its own opening and measure it.** The cleanest test of the channel model,
   and taverna is the warmest room in the house.
2. **Persist the advisor's 2 h trend history** so a restart cannot silently block the open.
3. **Diagnose the 14:10 exit** — outside the try block, so `states()`/urllib.
4. **The passive loop is still unquantified.** ~1 kW is a calculation, not a measurement.
5. **Real VMC airflow** still assumed at 200 m3/h. Everything scales linearly.
6. **North sensor humidity uncalibrated** — 30 min beside `capillair-env`, its OWN offset.
   Do NOT inherit capillair-out's +4.879.
7. **North sensor has no radiation shield** — double Stevenson printing; baseline banked in
   `data/north_unshielded_until.txt`.
8. **Wind-vs-stack argument is untestable**: `out_wind` is the forecast entity, flat at
   20.9 km/h all night. It measures nothing. Needs a real anemometer or drop the argument.
9. Two unrelated binary sensors are unreliable. Tracked separately, out of scope here.
10. **No git remote configured** — `848e810` and `9de651c` have never left this machine.

## Tonight

Open when north < ~29.7 AND falling 0.3 C over 2 h (yesterday: 20:55). **Include the piano
terra window** — it was worth two thirds of last night's cooling. Interrato/cavedio stay open.
