# Hostile review — "porous FDM evaporative cooling" proposal

Reviewer: Claude Opus 5. Date 2026-08-16. Target: the Fable document proposing salt-leached /
wood-filled / plaster-coated FDM parts as a cheap substitute for TU Graz's fired-clay TPMS cubes,
with a stated goal of ">=85% of the porosity / temp degrees lowering".

**Verdict up front.** The document's *engineering conclusion* (a cheap FDM part can perform close to
the fired ceramic) is probably right. **Every reason it gives for that conclusion is wrong**, it
optimises two variables that are already oversupplied by 10-90x, it never touches the one variable
that actually binds the result, and the target "85% of 7 degC" is **physically impossible in
Campania** regardless of material. Three of the four proposed material routes carry a slow
self-destruct that the document does not mention.

---

## 0. What the source actually says (measured facts — do not re-theorise)

From the TU Graz primary release (Stavric, Institute of Architecture and Media, 04.08.2026) and
its syndication:

- Cubes ~23 cm side, clay, TPMS internal geometry, **fired at low temperature** for high porosity.
- Sawdust + fungal mycelium burned out during firing to create the micro/macro pore network.
- *"In a controlled experimental setup, a temperature drop of almost seven degrees Celsius was
  measured **in the immediate vicinity** of the water-filled cube"*, in a **hot attic** at TU Graz.
- Project funded by **aws under the *proof of concept* programme**; the cooling-wall integration is
  a **Master's thesis** (Kristijan Ristoski).

**What is NOT published anywhere**: ambient temperature, ambient RH, airflow, sensor distance, test
duration, water consumption, number of replicates, control condition. **No peer-reviewed paper
exists.** The 7 degC has no stated methodology.

That is the first and largest problem with the whole proposal: it treats a press-release number
from a proof-of-concept grant as a performance specification to hit at 85%.

---

## 1. The attacks that land

### A1 — "85% of 7 degC" is an unfalsifiable target, and in Campania it is impossible

Evaporative cooling cannot go below the **wet-bulb temperature**. That is a hard thermodynamic
ceiling, independent of material, porosity, geometry and cleverness. Computed (Stull 2011):

| Condition | T | RH | T_wb | **max possible dT** | 7 degC needs |
|---|---|---|---|---|---|
| Graz attic, hot dry day | 32 | 35% | 21.0 | **11.0 degC** | 64% of ceiling |
| Graz attic, typical | 28 | 45% | 19.7 | **8.3 degC** | 85% of ceiling |
| Campania coast, summer | 32 | 65% | 26.6 | **5.4 degC** | **131% — impossible** |
| Campania coast, muggy | 30 | 75% | 26.4 | **3.6 degC** | **193% — impossible** |
| Inland IT, dry spell | 34 | 40% | 23.7 | **10.3 degC** | 68% of ceiling |

So "6 degC, realistic" as the document states is **not** realistic at the intended location. On a
muggy coastal day a *perfect* device — infinite surface, perfect wick, 100% saturation — tops out at
3.6 degC. Any prototype measured in Campania in August and compared against a number measured in a
Graz attic in a dry spell is comparing two different climates, not two materials.

Further: "in the immediate vicinity" is a proximity measurement. Hold a thermocouple 1 cm from *any*
wetted surface and you read something close to the wet-bulb temperature — a wet sponge, a wet towel,
a terracotta pot. The 7 degC does not characterise the cube; it characterises the boundary layer.
**It is not a material figure of merit and cannot be used as an 85% target.**

### A2 — The proposal optimises surface area and capillarity. Both are already oversupplied. The binding constraint is air exchange, and it is never mentioned.

Computed for the exact geometry the document recommends (OD 135 / bore 70 / H 175 mm, gyroid 20%,
10 mm cell, eps = 0.40, r = 25 um):

| Quantity | Value |
|---|---|
| Wetted internal + external surface | **0.34 m2** |
| Capillary *supply* capacity (Darcy, 15 cm lift, net 2601 Pa driving) | **~820 g/h** |
| Surface-limited evaporation ceiling (free-surface correlation, 30 degC/50% RH) | 126 g/h = 86 W |
| **Airflow-limited evaporation, bore at 0.05 m/s (natural convection)** | **9 g/h = 6 W** |
| **Airflow-limited, bore at 0.1 m/s** | **19 g/h = 13 W** |
| **Airflow-limited, bore at 0.2 m/s (optimistic chimney)** | **38 g/h = 26 W** |
| Airflow-limited, bore at 1.5 m/s (**small fan**) | 284 g/h = **193 W** |

Read those rows together:

- **Capillary supply exceeds actual demand by 20-90x.** The document's entire Route-1 apparatus —
  compounding your own filament, 55 wt% NaCl, 48 h leaching, NaOH etching, in-situ gypsum
  nucleation — exists to improve a variable that has ~an order of magnitude of headroom already.
  A wet cotton rope would keep that surface wet.
- **Surface area exceeds what the air can absorb by ~7x** at natural-convection airflow. Adding
  micro-porosity adds surface the air never reaches, because the air inside the lattice saturates
  within the first few centimetres. The "very large surface area" language in the TU Graz release
  (and the whole TPMS justification) is marketing physics for the natural-convection case.
- **The one lever with real authority is air exchange.** 0.05 -> 1.5 m/s is a **32x** swing in
  cooling power. A 1 W USB fan beats every material innovation in the document combined.

This is the central failure of the proposal. It is a materials-science answer to a fluid-mechanics
problem.

### A3 — Gypsum dissolves. Routes 1-refined and 3 have a built-in self-destruct.

CaSO4·2H2O solubility is ~2.0-2.4 g/L. The document proposes gypsum in **permanent contact with
continuously flowing, continuously evaporating water** — the single worst service condition for it.

Literature is unambiguous: the **softening coefficient of pure gypsum plaster is 0.30-0.40** (ratio
of compressive strength after 24 h immersion to dry strength), which is precisely why gypsum is
excluded from wet and outdoor construction. Strength falls ~1/3 on wetting and keeps falling with
immersion time; wet creep proceeds by pressure-solution (dissolve at grain boundary, diffuse,
reprecipitate).

Worse than the strength loss is the **transport**: in an evaporating system, dissolved sulfate
migrates *to the evaporating face* and precipitates there. That is the standard scaling failure of
evaporative coolers. Your pores will crust over from the outside in. Add Italian tap water (hard,
carbonate-rich) and you get CaCO3 scale on top of the CaSO4 scale.

Fired ceramic is insoluble. That is not incidental to why TU Graz used it.

This kills **Route 3 outright** and kills the "elegant part" of the refined M1 formulation.

### A4 — The in-situ hemihydrate rehydration trick will not do what is claimed

Three independent problems:
1. Only the hemihydrate **exposed at a pore wall** is accessible. At 9.3 vol% loading, randomly
   dispersed in a 55 vol% PLA matrix, the accessible fraction is a small minority of that 9.3%.
2. Hemihydrate dehydrates to anhydrite III at 150-180 degC and to the **poorly-rehydratable
   anhydrite II above ~180-200 degC**. The M1 compounding pass and the printer hotend both operate
   in or above that window — **twice**. The proposal's instruction to "feed calcined plaster
   (hemihydrate)" therefore converts it to the one phase that will not do the job.
3. Whatever dihydrate needles do form then **dissolve away** per A3.

The document itself flags the expansion-cracking risk. The cracking risk is the *least* of it.

### A5 — Biofouling / Legionella is a showstopper for indoor use and is not mentioned once

A permanently wet, warm (25-40 degC), enormous-surface-area, low-flow, porous substrate in an
occupied room is a textbook microbial amplifier. The **CDC explicitly lists "evaporative air
coolers"** among the equipment that grows *Legionella* absent active control. **VDI 2047-2** covers
"evaporative cooling systems and apparatus where water is trickled or sprayed over a surface" and
requires design for draining, cleaning and biofilm limitation; **VDI 6022** sets airborne germ and
Legionella limits for humidifier water. The literature is blunt about the material choice:
*"Non-porous materials are commonly used, as they are easy to maintain and safer in terms of
microbial risk."* Direct evaporative cooling (air in contact with water) is the higher-risk
configuration versus indirect.

The decisive asymmetry versus the ceramic is that **neither sanitisation route is open to PLA**:

- **Thermal** — thermal disinfection is 60-70 degC. PLA's Tg is ~55-60 degC. The part deforms
  before the water gets hot enough to kill anything.
- **Chemical** — bleach/hypochlorite **accelerates PLA hydrolysis**. Sanitising the part destroys
  the part.

A fired ceramic cube can be baked, boiled or bleached. And Route 2 actively adds **sawdust/wood
flour** — a carbon nutrient source — into a permanently wet part. That is culture medium.

If this is ever placed indoors, this is the objection that ends the project, not the porosity.

### A6 — PLA is the wrong polymer, and there may be no right one

Tg ~55-60 degC, HDT (0.45 MPa) ~50-55 degC. The demonstrated use case is **a hot attic** and the
proposed one is an Italian summer facade. Attic air routinely exceeds 45-50 degC. The part is a ~11%
effective solid-fraction lattice (20% infill x 60% remaining solid after leaching) **loaded with its
own weight in water**. It will creep and sag, and it will do so exactly when it is supposed to be
working.

The hydrolysis half is worse than the proposal's "a season or two": accelerated ageing of PLLA
showed **~50% molecular-weight loss after three months at 40 degC**, and ~41.6% after 5.5 months in
water. The proposed **NaOH etch deliberately generates carboxyl/hydroxyl surface groups** (confirmed
by XPS in the etching literature) exactly at the pore walls where the water is — so the treatment
that makes it wick is also the treatment that makes it dissolve.

**And the substitution is not easy.** PETG's HDT (~70-75 degC) is only marginally better and PETG
also hydrolyses; PA hydrolyses and warps; PP and PVDF are chemically robust but **hydrophobic**,
which defeats the entire purpose. There is no common FDM filament that is simultaneously printable,
hydrophilic, hydrolysis-resistant and creep-resistant at 60 degC. This is not a "pick a better
filament" problem — it is a structural argument that the FDM material palette does not contain a
solution.

*(Nuance retained — see B2: the thin-walled open geometry does suppress the classic bulk-erosion
autocatalysis, so the mechanism is milder than I first claimed. The measured absolute rates above
are what matter, and they are fast.)*

### A7 — Hydrophobic recovery is not addressed

The document banks on NaOH etching taking PLA from ~70-90 deg to ~40-50 deg contact angle. Surface
treatments on polymers are well known to **recover hydrophobicity** over days-to-weeks as chains
reorient. Alkaline hydrolysis removes material rather than merely functionalising it, so recovery
should be slower than for plasma — but the document asserts the improved wetting as permanent
without evidence. This needs measurement at t = 0, 1 week, 1 month, not assertion.

### A8 — Unit error in the one quantitative instruction given

*"evaporation rate in g/h x 2.45 kJ/g gives you watts of cooling directly"*. It gives **kJ/h**;
divide by 3.6. **1 g/h = 0.68 W**, not 2.45 W. The document's only proposed measurement protocol
overstates cooling power by **3.6x**. Small error, but it is in the sentence that tells you how to
validate everything else.

### A9 — YAGNI: the industrialised answer already exists and is better on every axis

Corrugated cellulose evaporative pads (CELdek/Kuul class) reach **85-95% saturation efficiency**,
have a **5-8 year service life**, are engineered for low air-side pressure drop, and are designed to
be replaced when they foul. Cost is tens of euro per panel. An unglazed terracotta pot costs 5 euro.

Given A2 — that the result is airflow-limited, not surface-limited — a corrugated pad plus a small
fan will beat a salt-leached gyroid column by an order of magnitude in W per euro and per litre of
water. The FDM route buys **geometric and aesthetic freedom**, and it buys **research novelty**
(the document is right that TPMS + porogen-leached FDM for evaporative cooling appears
uncharacterised). It does not buy cooling performance.

That is a legitimate reason to build it. It is not the reason the document gives.

---

## 2. Attacks that DID NOT survive — where the proposal is right and I was wrong

Stated so this review is usable rather than merely hostile.

### B1 — Salt-leaching a 25-35 mm wall: I expected this to be fatal. It is not. (Kimi got this wrong too.)

The scaffold literature says complete removal of salt from the centre **becomes difficult above
~2 mm**, and the NIST protocol uses warm water 2 h **plus 5 days** at room temperature. On the face
of it a 25-35 mm wall is hopeless — which is what I assumed, and what the second opinion also
concluded ("*diffusion of NaCl through tortuous FDM bead interstices... 24-48 h is a fantasy*").

**Both of us were wrong about the geometry.** The salt is *inside the extruded bead*, not migrating
through interstices between beads, and the proposal prints an **open gyroid at 15-25% infill with
1 perimeter**. The polymer diffusion path is therefore the bead half-thickness — **~0.2-0.6 mm,
wetted from both sides** — which is 3-10x *inside* the literature's 2 mm limit. Leaching is feasible.
The 24-48 h figure is still optimistic (NIST's 5 days is the honest number), but that is a schedule
error, not a physics failure.

**This converts into a hard design rule the document does not state**: any solid region is a leaching
dead zone. The document's own "solid foot ring for the bottom 10 mm" is exactly such a zone, and it
sits at the waterline where the wick must start. Same for any solid top/bottom layer or
multi-perimeter wall. **No feature may exceed ~2 mm of continuous solid.**

Newly conceded to the second opinion: **leaching causes shrinkage and warpage**. A 150-200 mm
column will not come out of the bath the shape it went in.

### B2 — PLA hydrolysis autocatalysis: my *mechanism* was wrong, my *conclusion* was right.

Autocatalysis in PLA is a *bulk-erosion* phenomenon — acidic degradation products accumulate inside
thick parts and accelerate the reaction. In a thin-walled, continuously flushed open structure those
products **wash away**, suppressing autocatalysis. So the porous geometry works in the proposal's
favour, and I withdraw "autocatalysis makes it far faster".

But the measured rates settle it anyway: **~50% Mw loss in 3 months at 40 degC**. The document's
"a season or two" is roughly one season optimistic. See A6.

### B3 — Filler loading / printability: feasible. (Second opinion is wrong here — it didn't convert wt% to vol%.)

The second opinion called the formulation "feedstock fantasy", citing a printability collapse above
**45-50 vol% solids**. But it then applied that threshold to the proposal's **weight** percentages.
Converting (NaCl 2.16 vs PLA 1.24 g/cm3):

| Formulation | vol% filler |
|---|---|
| PLA 45 / NaCl 55 wt% (headline) | **41.2 vol%** |
| PLA 50 / NaCl 50 wt% | **36.5 vol%** |
| PLA 40 / NaCl 45 / hemihydrate 15 wt% (refined) | **44.9 vol% total** (35.6 NaCl + 9.3 hemi) |

All three land **at or under** the 45-50 vol% ceiling that same source gives, and published FDM work
has **printed 50 vol% Al2O3/PLA filament** (60 vol% extrudable but too brittle to print). They are
also comfortably above the ~29 vol% continuum percolation threshold, so an interconnected leachable
network is plausible. Printability is at the brittle edge, not beyond it.

Two caveats the document underrates and which the second opinion is right about: NaCl crystals are
angular and **abrasive** (hardened nozzle mandatory, M1 screw/barrel is a consumable), and NaCl
**deliquesces at ~75% RH** — a filament left in Italian summer air gives erratic extrusion and steam
popping. Chloride pitting of the hotend, which I raised, is **not** a real concern: SCC needs an
aqueous electrolyte under sustained tensile stress, not a 200 degC transient. The chloride risk is
residual salt in the finished part attacking tray hardware and fittings.

**Also conceded**: the document's throwaway mention of **PVA or icing sugar** as alternative porogens
is not viable — PVA decomposes near 200 degC and sugar caramelises and chars at PLA extrusion
temperatures. NaCl is the only one of the three that survives the hotend.

### B4 — Capillary rise: the document's 20-30 cm is about right.

h = 2·gamma·cos(theta)/(rho·g·r): at r = 25 um and theta = 45 deg you get 42 cm; at 50 um/70 deg,
10 cm. The 20-30 cm working figure and the "cap module height at 15-20 cm, stack with per-tier drip
feed" recommendation are sound.

### B5 — The macro-shape recommendation (vertical tube in a tray) is correct, for the wrong reason.

The document justifies the tube by surface area and chimney effect. Surface area is irrelevant
(A2). But the **chimney effect is exactly right** — and by A2 it is in fact the *only* thing in the
document that touches the binding constraint. The tube is the right shape because it is the only
proposed geometry that moves air. Maximise bore draw (taller bore, warm exit, low internal flow
resistance), not lattice surface.

---

## 2b. Further failure modes neither the document nor my first pass listed

From the independent second opinion (Kimi Code), verified against the physics above:

1. **Structural integrity of a 1-perimeter, 0-top/bottom gyroid after leaching.** The remaining PLA
   struts are weakly fused beads with minimal contact area, and leaching removes 40% of what little
   material there is. Wet + warm + self-loaded = interlayer delamination and collapse. This is a
   *stronger* objection than creep, because it does not need attic temperatures.
2. **Pore flooding.** Evaporation needs a *thin film* exposed to moving air. A 40-60% open-porosity
   sponge below the capillary rise height is **saturated**, not filmed — a water-filled pore
   evaporates poorly. The optimum wetness is partial, and nothing in the design controls it.
3. **No blow-down / bleed strategy.** Every real evaporative cooler bleeds water to stop the
   reservoir concentrating dissolved solids. With no bleed, the tray concentrates minerals until it
   scales the part shut. Compounding with A3.
4. **Residual NaOH.** The document says "dip in NaOH, rinse" without specifying neutralisation. Caustic
   carry-over into the tray is a pH shock, a hazard, and a hydrolysis accelerator.
5. **The chimney effect at 150-200 mm is negligible.** Stack effect scales with height and dT. A
   20 cm bore will not self-ventilate meaningfully — which is precisely what A2 shows numerically
   (0.05 m/s natural convection = 6 W). The one feature aimed at the binding constraint is too small
   to move it.
6. **Water consumption and tray sizing are unspecified.** At the airflow-limited rates in A2 a single
   column drinks 0.2-0.9 L/day passively, and 2.3-6.8 L/day if you add the fan that makes it work. A
   2-3 cm tray is a toy; refill interval must be designed, not assumed.
7. **Fire/electrical load.** A combustible printed lattice in an attic alongside a pump and fan.
   Commercial cellulose pads carry flame and rot inhibitors; a printed PLA part carries neither.
8. **M1 R1 tolerance reality.** It is a desktop filament extruder, not a precision compounder.
   Holding ±0.05 mm diameter with ~40 vol% abrasive filler is optimistic.

---

## 3. What I would actually do

1. **Stop targeting "85% of 7 degC."** It is a proximity reading from an unpublished proof-of-concept
   with no stated conditions. Replace with a defensible metric: **saturation efficiency**
   eta = (T_dry_in - T_dry_out)/(T_dry_in - T_wb), measured on air passing *through* the bore, with
   RH and face velocity logged. That is the industry-standard figure, comparable against the 85-95%
   of a cellulose pad, and it is climate-independent.
2. **Run the control first, before compounding anything.** Print the same gyroid column in plain
   PLA, wrap it in a cotton/microfibre sleeve dipped in the tray, put it on a scale, and measure
   g/h and eta. If a cheap wick already hits eta ~0.6-0.8 — and per A2 it very likely will, because
   the system is airflow-limited — then Route 1 has nothing to prove and the entire filament project
   is answering a question that isn't being asked.
3. **Then measure the airflow sensitivity**, 0 / 0.5 / 1.5 m/s. Confirm the 32x span. This one
   experiment determines whether any material work is worth doing.
4. **If the numbers say the material matters** (they probably won't), go to Route 1 — but with:
   no gypsum in any form (A3/A4), NaCl as the only porogen (B3), all solid features under 2 mm and
   no solid foot ring (B1), a 5-day leach not 48 h (B1), hardened nozzle + drybox (B3), and contact
   angle re-measured at t=0 / 1 week / 1 month (A7). **Note that A6 leaves you without a good
   polymer**: PLA creeps and hydrolyses, PETG only slightly better, PP/PVDF are hydrophobic. Treat
   the part as a seasonal consumable and say so, or the polymer question sinks it later.
5. **Never put it indoors** without a sanitisation plan (A5) — and note that PLA admits neither
   thermal nor chemical sanitisation, so "a plan" means a different material. Outdoor facade /
   terrace only.
6. **Frame it honestly**: this is a research + architectural-form project. The evaporation physics
   was solved by a corrugated cellulose pad decades ago. The novel contribution is TPMS +
   porogen-leached FDM as a *characterised* material system, which is real and publishable — and
   that framing survives every attack above, whereas "cheap AC replacement" does not.

### Where the second opinion and I differ

Kimi Code's verdict is flatly **"stop — buy a cellulose pad, a pump and a fan; if you want a pretty
object, print a shell around a commercial pad."** On the engineering merits that is correct and I do
not argue with it.

My one amendment: **do step 2 and step 3 first anyway** — the plain-PLA-plus-cotton-sleeve control
and the airflow sweep. They cost an afternoon and no compounding, and they are the experiments that
either confirm the airflow-limited result (in which case Kimi is right and you have your own data
proving it, which is worth more than a review) or falsify my A2 analysis (in which case the material
work is justified after all). Do not skip straight to compounding filament, and do not skip straight
to giving up. Measure the one thing that decides it.

---

## Sources

- [TU Graz — Develops a Cooling Ceramic Wall to Combat Urban Heat (primary)](https://www.tugraz.at/en/news/article/cooling-ceramic-wall)
- [EurekAlert syndication](https://www.eurekalert.org/news-releases/1138659)
- [3Dnatives coverage](https://www.3dnatives.com/en/3d-printed-cooling-cubes-05082026/)
- [Effect of salt leaching process parameters on 3D porous PLA scaffolds (PubMed)](https://pubmed.ncbi.nlm.nih.gov/41231772/)
- [Porogen Leaching — ScienceDirect Topics](https://www.sciencedirect.com/topics/engineering/porogen-leaching)
- [Rheological Characterization and Printability of PLA-Al2O3 Filaments for FDM (Materials 2022)](https://doi.org/10.3390/ma15238399)
- [A review on PLA with different fillers used as a filament in 3D printing](https://www.sciencedirect.com/science/article/abs/pii/S221478532106329X)
- [Legionella risk in evaporative cooling systems and breaches in H&S compliance](https://www.sciencedirect.com/science/article/pii/S1438463919308934)
- [Challenges and future directions in evaporative cooling: balancing sustainable cooling with microbial safety](https://www.sciencedirect.com/science/article/abs/pii/S036013232401134X)
- [Kinetics of Hydrolytic Degradation of PLA](https://link.springer.com/article/10.1007/s10924-012-0547-x)
- [Hydrolysis of PLA and PCL: Autocatalysis](https://link.springer.com/article/10.1023/A:1022826528673)
- [Study on mechanical strength and water resistance of gypsum plaster (softening coefficient)](https://www.sciencedirect.com/science/article/pii/S2214509521000619)
- [Wet creep of gypsum plaster — pressure-solution mechanism](https://www.sciencedirect.com/science/article/abs/pii/S0008884614001100)
- [Munters CELdek evaporative cooling media specifications](https://piec.com/celdek/)
- [Munters CELdek product sheet (>85%, 88-92% at 100-150 mm depth)](https://www.munters.com/globalassets/inriver/resources/ps_celdek_202204_en.pdf)
- [Performance insights into cooling pad materials in hot and humid climates](https://www.sciencedirect.com/science/article/pii/S2949821X2600164X)

Added by the second opinion (Kimi Code), verified where noted:

- [CDC — Legionella control, other devices incl. evaporative air coolers](https://www.cdc.gov/control-legionella/php/toolkit/other-devices-module.html)
- [VDI 2047-2 (evaporative cooling systems — hygiene) sample text](https://www.normsplash.com/Samples/DIN/398717568/VDI-2047-Blatt-2-2019-en-de.pdf)
- [VDI 6022 — hygiene inspection of ventilation systems (overview)](https://www.ventomaxx.de/en/blog/vdi-6022-hygiene-inspection-of-ventilation-systems/)
- [Salt-leaching: complete removal difficult above ~2 mm (Biomaterials)](https://www.sciencedirect.com/science/article/pii/S0142961205011762)
- [NIST scaffold fabrication tutorial — 2 h warm + 5 days leach](https://www.nist.gov/document/scaffold-fabrication-tutorialpdf)
- [Ceramic FDM feedstock >45 vol% brittle/hard to feed (Springer)](https://link.springer.com/content/pdf/10.1007/978-3-030-54334-1_21)
- [Metal MEX feedstock limited to 50-60 vol% by filament brittleness (Metals 2022)](https://www.mdpi.com/2075-4701/12/3/429)
- [PLA/nano-HAp printability collapse above 50 wt% (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10007491/)
- [PLLA seawater ageing: ~50% Mw loss in 3 months at 40 degC (Biomimetics)](https://www.mdpi.com/2311-5629/7/2/42)
- [NaOH etching of PLA — XPS confirms C=O / C-OH increase (Schneider et al., PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7464172/)
- [Hemihydrate -> anhydrite III/II transition temperatures (Ceramics 2025)](https://www.mdpi.com/2571-6131/8/3/83)
- [Calcium sulfate solubility ~2.53 g/L at 25 degC (ScienceDirect Topics)](https://www.sciencedirect.com/topics/engineering/calcium-sulfate)
- [NaCl deliquescence ~75% RH (Experts@Minnesota)](https://experts.umn.edu/en/publications/effect-of-relative-humidity-on-corrosion-of-steel-under-sea-salt-/)

Kimi session (resumable): `kimi -r session_3922f5bd-c92b-4b81-8bd9-551e0067380a`
