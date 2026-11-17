
"""
Observed Climate Parameters Analysis
Project: Climate Change Analysis
Description:
Comparison of observed climate parameters with climatological
normals and generation of anomaly charts for each station.

Author: Leila Rashidian
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re

# --------------------------------------------------
# 1. Define project directories
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "Climate_Data" / "sep.xlsx"

OUTPUT_DIR = PROJECT_DIR / "Figures" / "Observed_Climate"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Read climate dataset
# --------------------------------------------------

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Input file not found: {DATA_FILE}"
    )

df = pd.read_excel(DATA_FILE, sheet_name="Sheet1")

# --------------------------------------------------
# 3. Define climate parameters
# --------------------------------------------------

parameters = {
    "Precipitation": {
        "observed": "rrr24",
        "normal": "n_rrr24",
        "anomaly": "anomaly-rcp",
        "unit": "mm"
    },
    "Mean Temperature": {
        "observed": "tm_m",
        "normal": "n_tm_m",
        "anomaly": "anomaly-tm",
        "unit": "°C"
    },
    "Maximum Temperature": {
        "observed": "tmax_m",
        "normal": "n_tmax_m",
        "anomaly": "anomaly-tmax",
        "unit": "°C"
    },
    "Minimum Temperature": {
        "observed": "tmin_m",
        "normal": "n_tmin_m",
        "anomaly": "anomaly-tmin",
        "unit": "°C"
    },
    "Relative Humidity": {
        "observed": "umm",
        "normal": "n_umm",
        "anomaly": "anomaly-hum",
        "unit": "%"
    },
    "Evaporation": {
        "observed": "evt_s",
        "normal": "n_evt_s",
        "anomaly": "anomaly-eve",
        "unit": "mm"
    }
}

# --------------------------------------------------
# 4. Check required columns
# --------------------------------------------------

required_columns = ["station_name", "month"]

for item in parameters.values():
    required_columns.extend([
        item["observed"],
        item["normal"]
    ])

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns in Excel file: {missing_columns}"
    )

# Convert climate data to numeric values
for item in parameters.values():
    for col in [item["observed"], item["normal"],
                item["anomaly"]]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )

# --------------------------------------------------
# 5. Sort months
# --------------------------------------------------

month_order = {
    "January": 1, "February": 2, "March": 3,
    "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9,
    "October": 10, "November": 11, "December": 12
}

def month_number(value):
    if pd.isna(value):
        return 99
    text = str(value).strip()
    if text in month_order:
        return month_order[text]
    try:
        return int(float(text))
    except ValueError:
        return month_order.get(text.capitalize(), 99)

df["_month_order"] = df["month"].apply(month_number)

df = df.sort_values(
    ["station_name", "_month_order"],
    ascending=[True, False]
)

# --------------------------------------------------
# 6. Generate climate comparison charts
# --------------------------------------------------

def safe_filename(name):
    return re.sub(r'[^\w\-]+', '_', str(name))

stations = df["station_name"].dropna().unique()

for station in stations:

    station_data = df[
        df["station_name"] == station
    ].copy()

    station_data = station_data.sort_values(
        "_month_order", ascending=False
    )

    months = station_data["month"].astype(str)

    for parameter, info in parameters.items():

        observed_col = info["observed"]
        normal_col = info["normal"]
        anomaly_col = info["anomaly"]
        unit = info["unit"]

        observed = station_data[observed_col]
        normal = station_data[normal_col]

        # Calculate anomalies when available in the dataset
        if anomaly_col in station_data.columns:
            anomaly = station_data[anomaly_col]
        else:
            anomaly = observed - normal

        # ------------------------------------------
        # A. Observed vs Normal chart
        # ------------------------------------------

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            months, normal,
            label="Climatological Normal",
            color="red", alpha=0.75
        )

        ax.bar(
            months, observed,
            label="Observed",
            color="steelblue", alpha=0.85
        )

        ax.set_title(
            f"{parameter} - {station}",
            fontsize=13, fontweight="bold"
        )

        ax.set_xlabel("Month")
        ax.set_ylabel(f"{parameter} ({unit})")

        ax.legend()
        ax.grid(axis="y", alpha=0.25)

        plt.xticks(rotation=45)
        plt.tight_layout()

        filename = (
            f"{safe_filename(station)}_"
            f"{safe_filename(parameter)}_Comparison.png"
        )

        plt.savefig(
            OUTPUT_DIR / filename,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        # ------------------------------------------
        # B. Climate anomaly chart
        # ------------------------------------------

        fig, ax = plt.subplots(figsize=(10, 5))

        colors = [
            "steelblue" if pd.notna(value) and value >= 0
            else "tomato"
            for value in anomaly
        ]

        ax.bar(
            months, anomaly,
            color=colors, alpha=0.85
        )

        ax.axhline(
            0, color="black",
            linewidth=0.9
        )

        ax.set_title(
            f"{parameter} Anomaly - {station}",
            fontsize=13, fontweight="bold"
        )

        ax.set_xlabel("Month")
        ax.set_ylabel(f"Anomaly ({unit})")

        ax.grid(axis="y", alpha=0.25)

        plt.xticks(rotation=45)
        plt.tight_layout()

        filename = (
            f"{safe_filename(station)}_"
            f"{safe_filename(parameter)}_Anomaly.png"
        )

        plt.savefig(
            OUTPUT_DIR / filename,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

# --------------------------------------------------
# 7. Finish
# --------------------------------------------------

print("Climate analysis completed successfully.")
print(f"Output directory: {OUTPUT_DIR}")
print(f"Number of stations: {len(stations)}")
print("All comparison and anomaly charts were generated.")
