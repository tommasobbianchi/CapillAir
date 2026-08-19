# CapillAir — evaporative cooling column

**Printed enclosure, bought cellulose pad.** Replaces the earlier wood-PLA and salt-leach recipes.
Reasoning and the demolition of the old approach: `REVIEW_fable_porous_fdm.md`.

---

## 1. What it is

- A **hexagonal column** ~35 cm across and ~50 cm tall, standing on a water reservoir.
- Air is drawn **inward through all six wet sides**, cooled ~9 °C, and blown **up and out of the top**.
- **You print the enclosure. You buy the wet part.** No filament touches the water as a working
  surface.
- **~1000 W of cooling for ~20 W of electricity.** No compressor, no refrigerant, no gas.

## 2. Why the column shape wins (and it is not the chimney)

The original argument for a tube was the chimney effect. That was wrong — with a fan, buoyancy is
irrelevant. The real reason is **face area**:

| form | face area | face velocity | pad depth | efficiency | pressure drop |
|---|---|---|---|---|---|
| flat pad 200×300 mm | 0.06 m² | 1.50 m/s | **200 mm** | 85 % | 9.7 Pa |
| **hex column, side 173 mm** | **0.311 m²** | **0.29 m/s** | **50 mm** | **91 %** | **0.5 Pa** |

- Six sides give **5× the face area** in a *smaller* footprint.
- That drops face velocity to **0.29 m/s**, and low face velocity is what buys efficiency.
- So a **50 mm pad outperforms a 200 mm flat one**, with **20× less pressure drop** — which means a
  slow, quiet, cheap fan.
- Bonus: it draws from **360°**, so there is no "front" to point at anything, and it reads as a
  piece of furniture rather than a machine.

## 3. **Can you get CELdek in a tube or vase shape? Yes — three ways**

**(a) Buy a curved pad. These are a stock item.** Tower / "desert" evaporative coolers (Symphony,
Bajaj, Honeywell and the many clones) are built exactly like this — a vertical curved honeycomb
cellulose pad, a water pump, and an axial fan. Replacement pads are sold as spare parts, typically
**€10–25**, in curved or three-panel sets. Search "tower cooler honeycomb pad replacement". This is
the cheapest route and it is purpose-made for the job.

**(b) Build a polygon from flat slabs — recommended.** Six flat CELdek slabs in a hexagon give you a
"tube" with none of the drawbacks. Flat slabs are the standard product, cut easily with a bread knife
or a fine saw, and a hexagon prints as six identical flat panels. **This is the design below.**

**(c) Do NOT try to bend a rigid CELdek block.** The block is corrugated sheets laminated with resin
and cured stiff — bending it cracks the laminations and opens the channels unevenly. The individual
flexible sheets are not sold separately.

An octagon is slightly rounder if you prefer the look; the maths is the same, you just print 8
narrower panels.

## 4. Geometry

| | |
|---|---|
| Shape | regular hexagon |
| Panel width (hex side) | **173 mm** |
| Height of the pad section | **300 mm** |
| Across the flats / across the corners | 300 mm / **346 mm** |
| Pad thickness | **50 mm** |
| Central bore | **200 mm** |
| Pad face area | 0.311 m² |
| Airflow | 320 m³/h |
| Face velocity / bore velocity | 0.29 m/s / 2.8 m/s |
| Pressure drop | **0.5 Pa** (negligible) |
| Efficiency | 91 % floor, expect >95 % in practice |

- **Printed panels are 173 × 300 mm — fits any 200 mm bed.** Six identical parts.
- Cellulose needed: **six slabs of 173 × 300 × 50 mm.** One standard CELdek sheet or two tower-cooler
  replacement pads will cover it.

## 5. Performance, your 14:00–20:00 window

At Bologna's representative summer dew point of 16 °C:

| hour | outdoor | **supply air** | ΔT | cooling | water |
|---|---|---|---|---|---|
| 14:00 | 31.0 °C | **22.2 °C** | 8.8 | 915 W | 1.35 L/h |
| 16:00 | 32.0 °C | **22.6 °C** | 9.4 | 976 W | 1.44 L/h |
| 18:00 | 32.5 °C | **22.8 °C** | 9.7 | 1007 W | 1.49 L/h |
| 20:00 | 32.0 °C | **22.6 °C** | 9.4 | 976 W | 1.44 L/h |
| 22:00 | 28.0 °C | **20.9 °C** | 7.1 | 734 W | 1.08 L/h |

- **~7 L/day evaporated**, ~10 L/day including bleed, on a 6-hour duty.
- **Electricity: ~0.12 kWh/day ≈ €0.03.** About **€3 for a whole summer**; the same cooling from a
  COP-3 split AC is ~€40.

## 5b. **The room will NOT be 22 °C. Read this before building anything.**

**22 °C is the temperature of the air coming out of the machine. It is not the room temperature.**
The room settles wherever the cooling balances the heat coming in:

> **T_room = T_supply + (heat gains) / 104 W per °C**

| room heat gains | **1 unit** (320 m³/h) | 2 units | 3 units |
|---|---|---|---|
| 300 W | **25.4 °C** | 23.9 °C | 23.5 °C |
| 500 W | **27.3 °C** | 24.9 °C | 24.1 °C |
| 800 W | **30.2 °C** | 26.4 °C | 25.1 °C |
| 1100 W | **33.1 °C** | 27.8 °C | 26.0 °C |

A typical 16 m² Bologna room in the evening: walls giving back stored heat 300–600 W, people
100–200 W, computer and lights 100–300 W. **So 500–1100 W is the realistic band, and one unit puts
the room at 27–33 °C.** Against a do-nothing baseline of ~32 °C that is somewhere between **5 °C
better and no better at all.** Everything hinges on the gains — which is why you measure them first
(§11a) rather than print anything.

### Windows WIDE open is the worst case — and it may be what you have now

- A fan-forced unit **pressurises the room**. If the machine pushes 320 m³/h in and only **one window
  is cracked** as an exhaust, the room is at positive pressure and outdoor air **does not flow in**.
  The room is then fed *only* by the cooled air.
- **Windows wide open destroys this.** Outdoor air short-circuits straight in and you are just mixing
  32 °C air back into the room as fast as you cool it.
- **Correct setup: everything shut except one small opening on the far side of the room, as an
  exhaust.** Not "open the windows" — the opposite.

### What actually makes it feel cold: the air on your skin

ASHRAE 55 "cooling effect" of elevated air speed:

| air speed on you | feels cooler by |
|---|---|
| 0.6 m/s | 1.7 °C |
| 0.9 m/s | 2.2 °C |
| **1.2 m/s** | **2.9 °C** |
| 1.5 m/s | 3.4 °C |

Sitting **in** the 22.5 °C stream at ~1.2 m/s, in a 28 °C room: local air 22.5 °C plus ~2.9 °C of
air-movement effect → **feels like 20–22 °C**.

> **This is a personal cooler. Point it at yourself.** Trying to chill 43 m³ of air against a masonry
> wall that is radiating heat back at you is the losing game. Cooling the person is the winning one.

### The highest-value use: night flushing

Your 19:00–20:00 indoor peak **is the walls giving back the day's heat**. Run the unit overnight and
you pull that heat *out of the structure*, so the next day starts lower:

| hour | outdoor | room | structure cooling |
|---|---|---|---|
| 22:00 | 28 °C | 30.5 °C | 259 W |
| 01:00 | 24 °C | 29 °C | 519 W |
| 04:00 | 22 °C | 27.5 °C | 571 W |

**8 hours overnight removes ~7 kWh from the walls — roughly 4× what the afternoon session takes out
of the air alone — for about €0.04 of electricity.** And after ~01:00 you can run the **fan alone**
with the pump off, because outdoor air is already cold enough. That is free cooling *and* the drying
cycle at the same time.

## 6. Shopping list

| item | notes | ~cost |
|---|---|---|
| Cellulose cooler pad | CELdek slab, or 2× tower-cooler replacement pads | €15–35 |
| PETG filament | ~1 kg for the enclosure. **Not PLA** — it lives in water. | €20 |
| 200 mm axial fan | or a 200 mm duct/inline fan. Only needs ~1 Pa, so pick for quiet. | €15–25 |
| Submersible pump | aquarium type, 200–400 L/h, 3–5 W | €10 |
| Silicone tube | to suit the pump outlet | €3 |
| Mechanical plug timer | runs the drying cycle automatically (§9) | €5 |
| Float valve | optional, for unattended top-up | €8 |
| **Total** | | **€70–105** |

## 7. What to print (PETG throughout)

**Six side panels** (173 × 300 mm each)

- An open frame, not a solid wall — it must not block airflow. Think a picture frame with a coarse
  grid or a few horizontal ribs across it.
- **Target 85 %+ open area.** Every square centimetre of frame is pad you are not using.
- A slot or lip on the inner face to hold the 50 mm pad, so the pad drops in and lifts out.
- Vertical edges: a simple tongue-and-groove or a screw boss so panels join into the hexagon.

**Base / sump**

- Holds 15–20 L, houses the pump, and carries the column.
- **It must drain completely** — put the drain at the true low point and slope the floor to it. This
  is the part that matters most for hygiene, more than the pad. Do not design a puddle you cannot
  empty.
- Print in sections and seal the joints, or print one piece if your bed allows.

**Top ring / water header**

- A closed hexagonal ring tube sitting on top of the pad, **1.5 mm holes on 10 mm pitch, facing
  down**.
- Oversize the holes and let it dribble. **Even distribution matters far more than flow rate** — one
  dry lane down a pad is directly lost cooling.

**Fan shroud / top cap**

- Holds the 200 mm fan over the bore, **pulling air up and out**.
- Pulling (not pushing) keeps the pad under slight negative pressure so drips stay inside.
- A lip or small louvre at the outlet so nothing splashes out.

**Print settings**: PETG, 240 °C / 80 °C bed, 3 perimeters, 20 % infill on frames, 100 % on the sump
walls. Nothing here is fussy — no vase mode, no exotic geometry, no wood filler, no post-processing.

## 8. Assembly

1. Sump on the floor, pump inside, tube up one corner.
2. Six panels joined into the hexagon, standing on the sump.
3. Six pad slabs dropped into the panel slots.
4. Header ring on top, connected to the pump tube.
5. Fan shroud and fan on top, blowing up.
6. **Fan and pump on separate switches.** Non-negotiable — the drying cycle in §9 is "pump off, fan
   on", and you cannot do it if they share a plug. Put the **pump** on the timer.

## 9. Drying — the three different jobs that share the word

### 9a. Drying the pad (operation) — this is the mould and bacteria control

- **Why**: mould needs water, food and warmth. Cellulose is food and summer is warmth; **water is the
  only one you control**. Spores need many hours of continuous free water to establish. Break that
  daily and they cannot.
- **Pump off, fan on, 30–60 minutes at the end of every run.** The fan strips the free water film off
  the pad. Costs about 2 Wh.
- **Set the timer so the pump stops an hour before you do.** Then it is automatic and there is
  nothing to remember.
- **The duty cycle already does most of the work.** You run this 14:00–20:00, so the pad is dry
  ~18 h/day anyway. The forced hour just guarantees it starts each day from *dry*, not *damp*.
- **Empty the sump.** This matters more than the pad. The pad air-dries on its own; a tray of warm
  standing water does not, and that is the actual bacterial reservoir in every evaporative cooler.
  Drain it whenever the unit will sit unused for more than a day — which is why §7 insists the drain
  is a plug pull and not a bucket-and-sponge job.
- **Bleed the water.** Everything that evaporates leaves its minerals behind. Left alone the sump
  concentrates until it scales the pad shut. **Dump and refill the sump daily in heavy use** — that
  handles the minerals and the hygiene in one move.
- **End of season**: pull the pads, air-dry them fully, store dry or replace. Scrub and dry the sump
  and header.

### 9b. Drying the filament (before printing)

- PETG is hygroscopic — wet PETG strings badly and prints weak layers.
- **45–55 °C for 4–6 hours** before printing. Store in a drybox.
- Much less critical than it was for wood-PLA, and there are no clogging problems.

### 9c. Drying the room air (the dehumidifier question)

- Your instinct that dehumidifiers are cheap and low-power is right. **But never run one in the same
  closed room as this cooler.**
  - This cooler moves heat from *sensible* to *latent* — the room's total heat is unchanged, the
    thermometer just reads lower.
  - A dehumidifier moves it straight back, **and adds its own wattage as heat on top**.
  - Both at once in a sealed room = the water goes round in a circle and **the room gets hotter**.
- **Time-multiplex them instead:**
  - **14:00–20:00, hot and dry** → cooler on, **window open**, dehumidifier off.
  - **Late night, muggy** → cooler off, **window closed**, dehumidifier on. It cannot lower the
    temperature, but cutting the humidity is exactly what makes a 27 °C night bearable.
  - **Never both at once.**

## 10. Operating rules

- **Run 14:00 → 20:00.** It delivers 22–23 °C supply air across the whole window and does not weaken
  toward the end — Bologna's dew point stays flat while the temperature stays high.
- **Keep going past 20:00 if the room is still hot.** It gets *stronger* into the evening, because
  the outdoor air it feeds on keeps cooling while your walls stay warm.
- **After ~01:00: pump off, fan on.** By then plain outdoor air is within ~3 °C of what the wet pad
  delivers, so the water stops earning its keep — and this doubles as the drying cycle.
- **Window open whenever the pump runs.**
- **Dump and refill the sump daily** in heavy use.
- **Replace the pads each season** (~€15).

## 11a. **Measure first — the M5 sensor campaign**

Two M5 units (ENV IV / SHT40 class, ±0.2 °C, ±1.8 % RH) logging indoor + outdoor. Do this **before
printing anything.** It answers whether this project is worth building at all.

### Sensor hygiene — do these or the data is worthless

- **Cross-calibrate first.** Put both sensors side by side for an hour, log, and record the offset.
  You will be computing differences of 2–5 °C between two units; a 0.4 °C uncorrected offset makes
  efficiency numbers meaningless. Apply the offset in software, and re-check monthly.
- **Shield from radiation.** A sensor in sunlight, or facing a hot wall or window, reads several
  degrees high. Use a white shield with airflow through it, or at minimum a shaded, ventilated spot.
- **Keep it off the M5 core.** The ESP32 and the display self-heat by 1–3 °C. Put the sensor on a
  cable, away from the body, and sleep between readings.
- **Log at 1 min.** You want the shape of the day, not fast transients.
- **Warning for later:** measuring the machine's supply air means putting an RH sensor in a ~95 % RH
  stream. Water will condense on it. SHT sensors recover but drift after repeated wetting — use a
  cheap sacrificial one there, and rely on **temperature** for the efficiency number.

### Test 1 — the baseline week (no hardware needed)

Log indoor and outdoor for a week. You get, for free:

- **The real dew point profile over 14:00–20:00.** This sets the hard ceiling. Everything in §5
  assumed 16 °C — verify it. Compute dew point from T and RH, and plot it: it should be nearly flat
  across the day while temperature swings.
- **The real indoor/outdoor lag.** Confirms the masonry story and tells you the true best hour to run.
- **How far indoor tracks outdoor with the windows as you currently use them.**

### Test 2 — **the decisive one: measure your room's heat gain**

This is the single number that decides everything in §5b, and you can measure it with a **box fan you
already own** — no cooler required.

1. Close everything except **one small opening on the far side of the room** (exhaust only).
2. Put the fan in a window blowing **outdoor air in**, at a known airflow. Rated flow is fine;
   an anemometer is better. Call it V m³/h.
3. Wait for steady state (30–60 min), then log for an hour.
4. **Heat gain Q = 0.335 × V × (T_room − T_outdoor)**  [watts, V in m³/h, ΔT in °C]

Then read your answer straight off the table in §5b:

| measured gain | verdict |
|---|---|
| **under ~400 W** | Build it. One unit lands the room around 24–26 °C. |
| **400–700 W** | Build it, expect 26–28 °C room and rely on pointing it at yourself. |
| **700–1000 W** | One unit is marginal. Size up, or treat it as a personal cooler only. |
| **over ~1000 W** | Fix the gains first — shutters, external shading, insulate the roof. No evaporative unit of this size will win against that, and neither will a cheap AC. |

Run this test at **19:00–20:00**, at your peak, not in the morning.

### Test 3 — sanity-check the ceiling before you commit

From the same logs, for each hour of your window compute the wet-bulb from T and RH and check
`T_outdoor − T_wetbulb`. If it is consistently **above 8 °C**, §5 holds. If it is routinely under
5 °C, the climate assumption is wrong and we redesign.

## 11b. First checks once it is built

1. **Water film, pump only, no fan.** Look at all six faces. You want a continuous wet film with **no
   dry lanes**. If you see one, tighten the header hole spacing or raise the pump flow.
2. **Cooling.** Thermometer at a side face and at the top outlet, hygrometer outside.
   `efficiency = (T_in − T_out) / (T_in − T_wetbulb)`. **Target above 0.85.**
3. **Water balance.** Mark the sump level, measure the drop per hour. Cross-check against
   `Q = litres/hour × 0.68 kW per L/h`. (1 g/h of evaporation = 0.68 W. Note the common slip:
   g/h × 2.45 kJ/g gives kJ/h — divide by 3.6 for watts.)

## 12. If the open window is ever unacceptable

The upgrade is an **indirect** evaporative cooler: the wet air stream goes out the window and never
touches the air you breathe, so no moisture is added and the room can stay sealed. Real M-cycle
products achieve **45–75 W of electricity per kW of cooling** (5–7× better than a split AC).

**That is the one place where printing the wet part genuinely earns its keep**, because an indirect
exchanger needs alternating wet and dry channels sealed against each other in one piece — a geometry
you cannot buy as a pad and cannot line with an insert. It is next summer's project. Build this one
first; it is a weekend.
