#!/usr/bin/env python3
"""CapillAir daily analysis: is the VMC earning its keep, and is the cavedio behaving
like a damped thermal mass or just tracking ambient?  Reads the 5-min CSV.
"""
import csv, sys, datetime, math
from pathlib import Path
CSV = Path.home()/"projects/CapillAir/data/climate.csv"
FLOW = 200.0            # m3/h, assumed VMC flow; scale results linearly if measured
# The cavedio unit was mounted ~08:40 carrying indoor heat and took ~90 min to reach
# shaft temperature. Damping/lag stats before this are meaningless, so they start here.
SETTLE_FROM = sys.argv[1] if len(sys.argv) > 1 else "09:30"

def f(r, k):
    try: return float(r[k])
    except (ValueError, KeyError, TypeError): return None

rows = [r for r in csv.DictReader(CSV.open())]
today = datetime.date.today().isoformat()
rows = [r for r in rows if r["ts"].startswith(today)]
if not rows:
    print("no rows for today"); sys.exit(1)

print(f"=== CapillAir — {today}, {rows[0]['ts'][11:16]} to {rows[-1]['ts'][11:16]} "
      f"({len(rows)} samples) ===\n")

# --- hourly table -------------------------------------------------------------
H = {}
for r in rows:
    H.setdefault(r["ts"][11:13], []).append(r)
def mean(rs, k):
    v = [f(r, k) for r in rs]; v = [x for x in v if x is not None]
    return sum(v)/len(v) if v else None
def fmt(x, w=7, d=2): return f"{x:{w}.{d}f}" if x is not None else " "*(w-1)+"-"

print("  h   ambient  cavedio   d(cav-amb)   indoor  d(cav-ind)   VMC_W   SoggPT  printroom")
for hh in sorted(H):
    rs = H[hh]
    amb, cav = mean(rs, "out_t"), mean(rs, "out_real_t")
    ind, sg, pr = mean(rs, "env_t"), mean(rs, "sogg_pt"), mean(rs, "printroom_t")
    dca = cav-amb if (cav is not None and amb is not None) else None
    dci = cav-ind if (cav is not None and ind is not None) else None
    w = 0.335*FLOW*dci if dci is not None else None
    print(f"  {hh}  {fmt(amb)}  {fmt(cav)}   {fmt(dca,8)}    {fmt(ind)}  {fmt(dci,8)}  {fmt(w,7,0)}  {fmt(sg)}  {fmt(pr)}")

# --- the falsifiable claim ----------------------------------------------------
st = [r for r in rows if r["ts"][11:16] >= SETTLE_FROM]
amb = [(r["ts"][11:16], f(r,"out_t")) for r in st if f(r,"out_t") is not None]
cav = [(r["ts"][11:16], f(r,"out_real_t")) for r in st if f(r,"out_real_t") is not None]
print(f"\n=== PREDICTION UNDER TEST: cavedio = damped lagged mass, not a tracker "
      f"(from {SETTLE_FROM}, post-settle) ===")
if amb and cav:
    amax = max(amb, key=lambda x: x[1]); cmax = max(cav, key=lambda x: x[1])
    aspan = max(x[1] for x in amb)-min(x[1] for x in amb)
    cspan = max(x[1] for x in cav)-min(x[1] for x in cav)
    print(f"  ambient  range {min(x[1] for x in amb):.1f} .. {max(x[1] for x in amb):.1f}  (span {aspan:.2f})  peak at {amax[0]}")
    print(f"  cavedio  range {min(x[1] for x in cav):.1f} .. {max(x[1] for x in cav):.1f}  (span {cspan:.2f})  peak at {cmax[0]}")
    if aspan > 0.5:
        print(f"  DAMPING  = 1 - {cspan:.2f}/{aspan:.2f} = {(1-cspan/aspan)*100:.0f}%   "
              f"(high = behaves like a mass; ~0 = just tracks outdoor air)")
    print(f"  gap at ambient peak: cavedio {cmax[1]:.2f} vs ambient {amax[1]:.2f} = {cmax[1]-amax[1]:+.2f} C")

# --- energy ------------------------------------------------------------------
tot = n = 0
for r in rows:
    c, i = f(r,"out_real_t"), f(r,"env_t")
    if c is None or i is None: continue
    tot += 0.335*FLOW*(c-i); n += 1
if n:
    hrs = n*5/60
    print(f"\n=== VMC ENERGY so far ({hrs:.1f} h at an assumed {FLOW:.0f} m3/h) ===")
    print(f"  mean {tot/n:+.0f} W  ->  {tot/n*hrs/1000:+.2f} kWh  ({'COOLING' if tot<0 else 'HEATING'} the house)")
    print(f"  scale linearly if the real flow differs: at 400 m3/h it is {tot/n*2:+.0f} W")

# --- printer room, third SHT40 probe ------------------------------------------
def abs_hum(T, RH):
    """g/m3 from T (C) and RH (%). The CapillAir nodes compute this on-device; the
    P1S node does not, so derive it here rather than reflash a heater controller."""
    if T is None or RH is None: return None
    es = 610.94*math.exp(17.625*T/(T+243.04))
    return 2.1667*(RH/100*es)/(T+273.15)

pr = [(r["ts"][11:16], f(r,"printroom_t"), f(r,"printroom_rh"),
       r.get("p1s_heater",""), r.get("p1s_auto","")) for r in rows]
pr = [x for x in pr if x[1] is not None]
if pr:
    heated = [x for x in pr if x[3] == "on" or x[4] == "on"]
    print(f"\n=== PRINTER ROOM (P1S chamber probe, {len(pr)} samples) ===")
    if heated:
        print(f"  WARNING: heater/auto ON for {len(heated)} samples — those are chamber, not room")
    t0, t1 = pr[0], pr[-1]
    ah0, ah1 = abs_hum(t0[1], t0[2]), abs_hum(t1[1], t1[2])
    print(f"  {t0[0]} {t0[1]:.2f} C  AH {ah0:.2f}   ->   {t1[0]} {t1[1]:.2f} C  AH {ah1:.2f}"
          f"   (swing {max(x[1] for x in pr)-min(x[1] for x in pr):.2f} C)")
    ind = [f(r,"env_t") for r in rows if f(r,"env_t") is not None]
    if ind:
        print(f"  vs indoor swing {max(ind)-min(ind):.2f} C — the printer room is the "
              f"{'flattest' if (max(x[1] for x in pr)-min(x[1] for x in pr)) < (max(ind)-min(ind)) else 'more variable'} zone")

# --- moisture ----------------------------------------------------------------
d = [f(r,"out_real_ah")-f(r,"env_ah") for r in rows
     if f(r,"out_real_ah") is not None and f(r,"env_ah") is not None]
if d:
    print(f"\n=== MOISTURE: intake - indoor absolute humidity ===")
    print(f"  mean {sum(d)/len(d):+.2f} g/m3, range {min(d):+.2f} .. {max(d):+.2f}  "
          f"({'VMC humidifies' if sum(d)/len(d) > 0.1 else ('VMC dries' if sum(d)/len(d) < -0.1 else 'neutral')})")
