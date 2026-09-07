# CapillAir

Instrumenting passive cooling in a three-storey Italian house, to find out what actually
moves heat out of it — and to drive a window open/close advisor from the answer.

Short version: the mechanical heat-recovery ventilation unit everyone assumes is doing the
work contributes about 100 W. The unpowered chimney the house already had, and which nobody
had measured, contributes about ten times that.

## What was measured

**The intake shaft is a thermal flywheel.** The VMC draws from a shaded west cavedio at
interrato level. Across a day when outdoor air swung 24.0 → 29.9 °C, the shaft moved 0.49 °C
— **75% damping**, and it sat 5.6 °C *below* ambient at the afternoon peak. It is a large
shaded mass, not a tracker, which makes it an excellent intake precisely when it matters.

**So the bypass stays open all day.** A heat exchanger tempers incoming air *toward* indoor
temperature, so when the intake is already colder than indoors, running it through the core
destroys 75–80% of the benefit. The intuitive "close the bypass when it's hot outside" is
backwards here, because the intake never sees outdoor air.

**The passive stack dominates.** `cavedio → interrato → stairwell → piano primo → out` runs
on a 2.97 °C gradient, ≈0.67 Pa, ≈1160 m³/h, **≈1090 W** — against the VMC's ≈100 W. The
whole thing needs no fan; the only operational lever is whether a high exit is open.

**But it is a channel, not a house-wide sweep.** This is the correction that matters most.
Over one full night the house mean fell 1.19 °C, and two thirds of that arrived only after a
*piano terra* window was opened — a second inlet, not a bigger gradient. The control that
proves it: **taverna**, same level as the interrato but with no opening of its own, lost
0.3 °C in eleven hours while cucina lost 2.0, and stayed flat within 0.2 °C across 18 h.
Rooms hanging off the corridor get essentially nothing. The warmest rooms were the ones the
stack missed.

## The window rule

Three attempts; the first two failed in ways worth keeping:

1. **Closing on the live coolest room does not work.** Open windows couple rooms to outdoor
   air, so as outdoor climbs the rooms climb with it and the threshold runs away from the
   number chasing it. The call ran ~84 min late and gave back ~0.8 °C.
2. **Latching the threshold alone reopens into the morning ramp**, because the *open* side
   still keyed off live rooms, which warm too.
3. **A 1 h trend guard is fooled by a plateau** in that ramp.

Final rule, verified by replaying the real CSV before deploying:

- **OPEN** when outdoor < min(warmest room − 1.0, coolest room − 0.3) **and** falling ≥ 0.3 °C
  over a sustained 2 h. Over 2 h the morning ramp is unambiguously up and the evening fall
  unambiguously down.
- **CLOSE** when outdoor rises above the **banked minimum** — the lowest temperature actually
  reached this cycle, persisted to disk, so the target cannot drift upward.
- **The interrato and cavedio never close.** The cavedio is below the house all day.
- Rain gates the *open* transition only, and never forces a close: the best cooling gradient
  of the whole campaign (−6.6 °C) was measured during rain.

It fails **closed**: without trend history it stays shut. A missed open costs one evening; a
wrong open imports heat into a house that spent all night cooling.

## Layout

| path | what |
|---|---|
| `log_climate.py` | polls Home Assistant every 5 min → `data/climate.csv` |
| `bin/vmcwatch.py` | the live advisor; notifies open/close through HA |
| `analyse.py` | rolling 24 h analysis (`analyse.py 48` for 48 h) |
| `esphome/` | ESPHome nodes: ambient, cavedio/VMC intake, north-face outdoor, plus two SHT41 device targets (battery Seeed XIAO C3, USB SuperMini C3) |
| `HANDOFF.md` | running session log, including the errors |
| `RECIPE.md` | build notes for the sensor nodes |

Analysis windows are **rolling**, not calendar-day: the night purge straddles midnight and a
`startswith(today)` filter silently discarded half of it.

## Two traps worth stealing

**Reference frames.** Three different "outdoor" numbers exist in the CSV and confusing them
caused six separate errors: `north_t` is true measured outdoor, `out_real_t` is the **cavedio**
despite the name, and `out_t` is the *forecast* (coarse, ran +1.4 °C high). Damping was
reported as 82–93% for two sessions because it had been computed against the forecast rather
than the real north node; it is 75%. Before quoting any "outdoor" figure, resolve the column
back to the entity behind it.

**Watts at altitude.** Every figure here is corrected for 290 m — ×0.942 against the
sea-level 0.335 constant.

## Note on the published data

`data/climate.csv` carries the thermal and humidity channels and the window state. The
occupancy covariates the study logged for confound-masking — motion, presence, garage door —
were removed from this repository and from its history, along with the WiFi SSIDs, because
they describe a particular house rather than the physics. Nothing in the analysis reads them.
Sensor credentials live in `esphome/secrets.yaml`, which was never committed.
