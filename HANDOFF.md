# CapillAir — session handoff, 2026-08-19 12:30

## What survives this reboot

`Linger=yes` is set, so **user systemd timers restart automatically**. Verified before exit.

| what | where | cadence | survives reboot |
|---|---|---|---|
| `capillair-climate.timer` | nativedev | 5 min → `data/climate.csv` | **yes** |
| `capillair-window.timer` | nativedev | 10 min → window state to HA via MQTT | **yes** |
| `capillair-report.timer` | nativedev | 13/17/20/23:00 → `reports/*.txt` | **yes** |
| `capillair-env` (Atom, first floor) | WiFi → HA | 30 s | yes, independent |
| `capillair-out` (Atom, cavedio) | WiFi → HA | 30 s | yes, independent |
| CapillAir dashboard | HAOS | — | yes |
| **Claude session Monitor** | session | 5 min | **NO — dies, re-arm if wanted** |

Nothing needs restarting by hand. `systemctl --user list-timers | grep capillair` to confirm after boot.

## The result so far — the hypothesis held

**Claim under test:** the west cavedio is a large shaded thermal mass, so it damps and lags
ambient rather than tracking it — which would make it an excellent VMC intake in the afternoon.

**Confirmed, decisively** (09:33–12:23, post-settle):

```
ambient  24.0 -> 29.9   span 5.90 C   peak 11:58
cavedio  25.7 -> 26.2   span 0.49 C   peak 10:38
DAMPING  92%
gap at ambient peak: cavedio 26.22 vs ambient 29.90 = -3.68 C
```

The shaft moved half a degree while outdoors moved six. It crossed from *warmer* than ambient
(+1.56 at 09:00) to *colder* (−3.68 at 12:00) and keeps pulling ahead.

**VMC contribution:** −67 W mean over 5.2 h (−0.34 kWh), currently −97 W, at an **assumed
200 m³/h**. Scales linearly — real flow is still unmeasured. It is also **drying** the house
(−0.27 g/m³ mean), so no moisture penalty.

**Bypass OPEN is correct** and my earlier advice to close it in the day was wrong: it assumed the
intake saw ambient. With an intake colder than indoors, the heat exchanger would destroy 75–80%
of the benefit.

## Day timeline (2026-08-19)

- 07:13 windows closed after the overnight purge (upper floors −1.8 to −2.0 °C; interrato −0.3)
- ~08:00 VMC crossed into cooling
- ~10:15–10:55 **ambient passed indoor — free-cooling window closed**, garage door became a liability
- 12:00 ambient 29.9, cavedio 26.0, VMC −97 W

## Open items

1. **Measure the real VMC airflow.** Every wattage here is `×(flow/200)`. Until it's measured, the
   magnitude is indicative, not quantitative.
2. **North-face ambient sensor.** `weather.forecast_home` is a *forecast*, refreshing in coarse
   steps — ambient jumped 26.6→28.5 in five minutes at 10:55. The single most decision-relevant
   number in the system is currently not measured. Second Atom, north face, shaded, 30–50 cm off
   the wall, 1.5–2 m up.
3. Two unrelated binary sensors are unreliable. Tracked separately, out of scope here.
4. **Confounds are larger than the signal.** Occupancy (+200…300 W), wet mopping (−680 W transient,
   +5 g/m³). Hence the method pivot: measure the VMC's *driving force* (`T_cavedio − T_indoor`,
   immune to occupancy) rather than trying to extract its footprint from the house curve.
   Activity covariates are logged for masking.
5. **P1S chamber probe is conditional.** Valid as a room proxy only while heater/auto are off —
   both logged and flagged on the dashboard.

## Files

```
~/projects/CapillAir/
  RECIPE.md                    evaporative cooling column design (printed enclosure + bought pad)
  REVIEW_fable_porous_fdm.md   demolition of the original salt-leach/gypsum proposal
  log_climate.py               5-min logger, self-migrates when columns change
  analyse.py                   analysis; arg = post-settle start time, default 09:30
  data/climate.csv             38 columns
  reports/                     timer snapshots (gitignored)
  esphome/capillair-out.yaml   cavedio node, RH offset +4.879 documented inline
  esphome/secrets.yaml         REAL CREDENTIALS — gitignored, never commit
```

**OTA to the cavedio node needs a tunnel** (nativedev is on Tailscale, node is on the home LAN):

```bash
cd ~/projects/CapillAir/esphome
sshpass -p "$HAOS_PASS" ssh -N -L 3232:192.168.0.184:3232 hassio@100.71.237.68 &
TPID=$!; sleep 4
esphome run capillair-out.yaml --device 127.0.0.1     # `run`, NOT `upload` — upload does not compile
kill $TPID
```

`esphome upload` pushes the *existing* binary and reports success without applying yaml changes.
That cost a round trip today.

## Next check

`capillair-report.timer` fires at 13:00, 17:00, 20:00, 23:00 into `reports/`. The 20:00 and 23:00
ones matter most: they cover the evening peak and the start of the night purge.
