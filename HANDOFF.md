# CapillAir — handoff, 2026-08-19 22:40

## THE HEADLINE: the passive loop dwarfs the VMC, and I missed it all day

The house already runs a passive cooling circuit that owes nothing to the VMC:

```
cavedio (26.8 C)  ->  interrato  ->  stairwell  ->  piano primo  -> out
```

Driven by the cavedio sitting **below the house 24 h a day**, not by outdoor air.

| mechanism | flow | power |
|---|---|---|
| **passive cavedio stack** | ~1160 m³/h | **~1090 W** |
| VMC (bypass open, cavedio intake) | ~200 m³/h assumed | ~100 W |

I spent the day characterising the intake of the **smaller** mechanism while the bigger one
ran unmeasured, because I assumed a sealed house. The garage–cavedio door and the interrato
are open permanently; the only missing piece was a **top exit**.

**Evidence it is real:** when the piano primo opened at 20:30, three rooms flipped sign
within minutes — Camera1 P1 −0.06 → **−0.35 °C/h**, Camera2 +0.10 → **−0.24**, Soggiorno
+0.11 → **−0.23**. And the interrato sits at 28.6 while the taverna, *same level*, is 30.0:
the interrato sensor is standing in the incoming cool stream.

## Window rule (now a service, notifies by itself)

**Asymmetric on purpose:**

- **OPEN** when outdoor < warmest occupied room − 1 °C. The hot rooms gain first and early
  opening costs nothing. Tonight that was ~20:15–20:30.
- **CLOSE** when outdoor > **house mean**. Today that was **11:58**. The house was actually
  shut at **07:13 — about four hours early**, losing the coolest cheapest hours of the day.
- **The interrato/cavedio never closes.** Only the top closes, and that is about **wind, not
  temperature**: the stack is ~0.7 Pa, a 13 km/h breeze is 7.6 Pa, so an open top window
  stops being a reliable exhaust. *This part is reasoned, not measured — the open question.*

`capillair-windows.service` (systemd user, `Restart=always`, linger on) notifies via HA →
Telegram + Pixel. Both tested. It survives session end and reboot.

## Reference-frame errors I made today — the pattern worth remembering

Four times I picked a sensor for convenience instead of asking what the number represents:

1. **Bypass**: told him to close it in the day, assuming the intake saw ambient. It sees the
   cavedio, which is *colder* than indoors — closing it would destroy 75–80% of the benefit.
2. **Window reference**: built the rule on the ENV IV, which runs **1.44 °C cooler than the
   bedrooms** (0.77–1.89 range). It said "keep shut" while the occupied rooms were gaining.
   His wife opened at 20:30 and was right; my alert fired at 20:53.
3. **VMC delta**: when I fixed (2) I dragged the VMC baseline onto the warmest room too,
   inflating −1.94 °C into −3.60. Its supply mixes house-wide → belongs on the ENV IV.
4. **Stack inlet**: computed the stack against *outdoor* (29.6) when the inlet is the
   **cavedio** (26.9). A 12× error in flow, 40× in power. He said "the chimney effect is
   strong" and he was right.

Also: I patched the watcher while it was running and it kept emitting old numbers for 90
minutes. **Editing a file does not reload a running process.**

## Measured results

```
DAMPING 82-93%   ambient span 9.40 C -> cavedio span 0.49-1.66 C
gap at ambient peak: cavedio 27.4 vs ambient 33.4 = -6.0 C
VMC: -71 W mean over 9.8 h = -0.70 kWh; moisture NEUTRAL over the day (+0.06 g/m3)
altitude 290 m (station 976.6 vs sea-level 1010.9) -> every watt is x0.942 vs the
  sea-level 0.335 constant; analyse.py now derives it from the barometer
evaporative ceiling gain from altitude: +0.06..0.15 C — negligible, does not change RECIPE.md
```

## Hardware

| node | board | notes |
|---|---|---|
| `capillair-env` | Atom Lite (ESP32-PICO) | first floor, reference for calibration |
| `capillair-out` | Atom Lite | cavedio, VMC intake. **RH +4.879 offset applied in firmware** |
| `capillair-north` | **AtomS3 (ESP32-S3)** | north face. I2C GPIO2/1, USB-CDC, no LED. **RH UNCALIBRATED** |
| P1S chamber probe | Atom Lite + SHT4x | printer room. Valid only while heater/auto off and NOT printing |

**OTA needs a tunnel** (nativedev is on Tailscale, nodes are on the home LAN):

```bash
cd ~/projects/CapillAir/esphome
sshpass -p "$HAOS_PASS" ssh -N -L 3232:192.168.0.184:3232 hassio@100.71.237.68 &
TPID=$!; sleep 4
esphome run capillair-out.yaml --device 127.0.0.1    # `run`, NOT `upload` — upload does not compile
kill $TPID
```

## Services (all survive reboot, linger on)

| unit | cadence |
|---|---|
| `capillair-climate.timer` | 5 min → `data/climate.csv` (43 cols) |
| `capillair-window.timer` | 10 min → window classifier → MQTT → HA |
| `capillair-report.timer` | 13/17/20/23:00 → `reports/` |
| `capillair-windows.service` | continuous, notifies open/close |

## Open items, priority order

1. **The passive loop is unquantified.** ~1 kW is a calculation, not a measurement. It is the
   dominant mechanism and deserves the instrumentation the VMC got.
2. **Real VMC airflow** still assumed at 200 m³/h. Everything scales linearly.
3. **North sensor humidity uncalibrated** — 30 min beside `capillair-env`, then apply its own
   offset. Do NOT inherit capillair-out's +4.879.
4. **North sensor has no radiation shield** — double Stevenson printing. Baseline banked in
   `data/north_unshielded_until.txt` so the step change measures the radiative error.
5. **Close threshold (house mean) is a judgement, not validated.** Tomorrow is the first test.
6. **Wind-vs-stack argument is theoretical.** Test: leave the top on vasistas through a calm
   afternoon and see whether the stack holds direction.
7. Two unrelated binary sensors are unreliable. Tracked separately, out of scope here.
8. Two unrelated binary sensors are unreliable. Tracked separately, out of scope here.

## Tomorrow

**Leave everything open overnight and through the morning.** The service will say when to
close the top (~11:00–12:00, on the measured mean). Interrato and cavedio stay open always.
