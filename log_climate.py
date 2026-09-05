#!/usr/bin/env python3
"""Append one row of house-climate state to a CSV. Run from a systemd timer.

Why a local poller and not HA template sensors: weather.* attributes are not kept by
the recorder, and today's VMC experiment is unreadable without a logged OUTDOOR trace
to normalise against. This touches nothing in the HA config. ponytail: one file, one
timer, plain CSV.
"""
import csv, datetime, json, os, urllib.request
from pathlib import Path

HA = "http://100.71.237.68:8123"
TOK = os.environ.get("HA_TOKEN") or (Path.home()/".local/share/capillair-window/env").read_text().split("HA_TOKEN=")[1].split("\n")[0]
OUT = Path.home()/"projects/CapillAir/data/climate.csv"

SENSORS = {
    "env_t": "sensor.capillair_env_iv_temperatura",
    "env_rh": "sensor.capillair_env_iv_umidita",
    "env_ah": "sensor.capillair_env_iv_umidita_assoluta",
    "env_dew": "sensor.capillair_punto_di_rugiada",
    "env_p": "sensor.capillair_env_iv_pressione",
    "camera1_p1": "sensor.temperatura_rilevata_camera1_piano_primo",
    "camera2_p1": "sensor.temperatura_rilevata_camera2_piano_primo",
    "sogg_pt": "sensor.temperatura_rilevata_soggiorno_piano_terra",
    "cucina_pt": "sensor.temperatura_rilevata_cucina_piano_terra",
    "interrato": "sensor.temperatura_rilevata_camera_interrato",
    "taverna": "sensor.temperatura_rilevata_taverna",
    "studio": "sensor.temperatura_rilevata_studio",
    "garage_air": "sensor.fibaro_door_sensor_basculante_air_temperature",
    # printer room next to the permanently-open cavedio door (P1S chamber atom:
    # lagged/offset proxy for that room, heater off = tracks ambient there)
    "printroom_t": "sensor.controller_camera_p1s_temperatura_camera",
    "printroom_rh": "sensor.controller_camera_p1s_umidita_camera",
    # The P1S probe is INSIDE the print chamber. It only proxies the room while the
    # heater and auto-control are off and nothing is printing; log those so invalid
    # intervals can be excluded instead of silently polluting the room series.
    "p1s_heater": "switch.controller_camera_p1s_resistenza_riscaldatore",
    "p1s_fan": "switch.controller_camera_p1s_ventola_riscaldatore",
    "p1s_auto": "switch.controller_camera_p1s_controllo_automatico_camera",
    # real measured outdoor, replacing the forecast once it is mounted on the north face
    # north-face true ambient (UNCALIBRATED until co-located with capillair-env)
    "north_t": "sensor.capillair_north_temperatura",
    "north_rh": "sensor.capillair_north_umidita",
    "north_ah": "sensor.capillair_north_umidita_assoluta",
    "north_p": "sensor.capillair_north_pressione",
    "north_wifi": "sensor.capillair_north_segnale_wifi",
    "out_real_t": "sensor.capillair_out_temperatura",
    "out_real_rh": "sensor.capillair_out_umidita",
    "out_real_ah": "sensor.capillair_out_umidita_assoluta",
    "out_real_p": "sensor.capillair_out_pressione",
    "window_p1": "sensor.piano_primo_finestra",
    # The occupancy covariates that used to sit here (motion, presence, garage door)
    # are NOT logged in the published version of this project: they describe a specific
    # house rather than the physics. They mattered because people (~100 W + ~50 g/h each)
    # and wet-mopping (several hundred W transient) are BIGGER than the VMC effect being
    # measured -- which is exactly why the method pivoted to the VMC's DRIVING FORCE
    # (T_cavedio - T_indoor), immune to occupancy, instead of the whole-house curve.
}

def get(path):
    r = urllib.request.Request(HA + path, headers={"Authorization": "Bearer " + TOK})
    return json.load(urllib.request.urlopen(r, timeout=30))

def main():
    states = {e["entity_id"]: e for e in get("/api/states")}
    row = {"ts": datetime.datetime.now().isoformat(timespec="seconds")}
    for k, eid in SENSORS.items():
        s = states.get(eid)
        row[k] = s["state"] if s else ""
    w = states.get("weather.forecast_home")
    a = w["attributes"] if w else {}
    # the whole point of this file: an outdoor trace the recorder does not keep
    row["out_t"] = a.get("temperature", "")
    row["out_rh"] = a.get("humidity", "")
    row["out_dew"] = a.get("dew_point", "")
    row["out_p"] = a.get("pressure", "")
    row["out_wind"] = a.get("wind_speed", "")
    row["out_cond"] = w["state"] if w else ""

    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Adding a sensor changes the column set. Appending under a stale header silently
    # misaligns every later row, so migrate the file instead of assuming it matches.
    old_rows, old_hdr = [], None
    if OUT.exists():
        with OUT.open(newline="") as f:
            rd = csv.DictReader(f)
            old_hdr = rd.fieldnames
            if old_hdr != list(row):
                old_rows = list(rd)
    if old_hdr is not None and old_hdr != list(row):
        with OUT.open("w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(row), restval="")
            wr.writeheader()
            for r in old_rows:
                wr.writerow({k: r.get(k, "") for k in row})
            wr.writerow(row)
        print(f"schema changed: migrated {len(old_rows)} rows to {len(row)} columns")
        return
    with OUT.open("a", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(row), restval="")
        if old_hdr is None:
            wr.writeheader()
        wr.writerow(row)
    print(f"{row['ts']} in={row['env_t']} out={row['out_t']} win={row['window_p1']}")

if __name__ == "__main__":
    main()
