
"""
Observed Climate Parameters Analysis
Project: Climate Change Analysis

Purpose:
Comparison of observed climate parameters with climatological
normals and generation of monthly anomaly charts.

Privacy:
- Input Excel data remain on the local computer.
- Station names are anonymized in published figures.
- No geographic coordinates are used or exported.

Author: Leila Rashidian
"""

import re
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# --------------------------------------------------
# 1. Select local Excel file
# --------------------------------------------------

root = tk.Tk()
root.withdraw()

selected_file = filedialog.askopenfilename(
    title="Select your climate Excel file",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)

if not selected_file:
    raise SystemExit("No Excel file selected.")

DATA_FILE = Path(selected_file)

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "Figures" / "Observed_Climate"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Read Excel data
# --------------------------------------------------

df = pd.read_excel(DATA_FILE, sheet_name="Sheet1")

parameters = {
    "Precipitation": {
        "observed": "rrr24",
        "normal": "n_rrr24",
        "unit": "mm"
    },
    "Mean Temperature": {
        "observed": "tm_m",
        "normal": "n_tm_m",
        "unit": "°C"
    },
    "Maximum Temperature": {
        "observed": "tmax_m",
        "normal": "n_tmax_m",
        "unit": "°C"
    },
    "Minimum Temperature": {
        "observed": "tmin_m",
        "normal": "n_tmin_m",
        "unit": "°C"
    },
    "Relative Humidity": {
        "observed": "umm",
        "normal": "n_umm",
        "unit": "%"
    },
    "Evaporation": {
        "observed": "evt_s",
        "normal": "n_evt_s",
        "unit": "mm"
    }
}


# --------------------------------------------------
# 3. Validate data structure
# --------------------------------------------------

required_columns = ["station_name", "month"]

for item in parameters.values():
    required_columns.extend([
        item["observed"],
        item["normal"]
    ])

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        "Missing required Excel columns: "
        + ", ".join(missing_columns)
    )

for col in required_columns[2:]:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# --------------------------------------------------
# 4. Prepare monthly order
# --------------------------------------------------

month_order = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
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
    ["station_name", "_month_order"]
)


# --------------------------------------------------
# 5. Anonymize station names
# --------------------------------------------------

stations = sorted(df["station_name"].dropna().unique())

station_labels = {
    station: f"Station_{i + 1:02d}"
    for i, station in enumerate(stations)
}


# --------------------------------------------------
# 6. Generate comparison and anomaly charts
# --------------------------------------------------

for station in stations:

    station_data = df[
        df["station_name"] == station
    ].copy()

    station_data = station_data.sort_values(
        "_month_order"
    )

    station_label = station_labels[station]

    months = station_data["month"].astype(str).tolist()

    x = np.arange(len(months))
    width = 0.38

    for parameter, info in parameters.items():

        observed = station_data[info["observed"]]
        normal = station_data[info["normal"]]

        # Calculate anomaly consistently
        anomaly = observed - normal

        valid = observed.notna() & normal.notna()

        if not valid.any():
            continue

        # ------------------------------------------
        # A. Observed vs climatological normal
        # ------------------------------------------

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            x - width / 2,
            normal,
            width,
            label="Climatological Normal",
            color="red",
            alpha=0.75
        )

        ax.bar(
            x + width / 2,
            observed,
            width,
            label="Observed",
            color="steelblue",
            alpha=0.85
        )

        ax.set_title(
            f"{parameter} - {station_label}",
            fontsize=13,
            fontweight="bold"
        )

        ax.set_xlabel("Month")
        ax.set_ylabel(f"{parameter} ({info['unit']})")

        ax.set_xticks(x)
        ax.set_xticklabels(months, rotation=45)

        ax.legend()
        ax.grid(axis="y", alpha=0.25)

        plt.tight_layout()

        filename = (
            f"{station_label}_"
            f"{parameter.replace(' ', '_')}_Comparison.png"
        )

        plt.savefig(
            OUTPUT_DIR / filename,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()


        # ------------------------------------------
        # B. Monthly anomalies
        # ------------------------------------------

        fig, ax = plt.subplots(figsize=(10, 5))

        colors = [
            "steelblue" if value >= 0 else "tomato"
            for value in anomaly.fillna(0)
        ]

        ax.bar(
            x,
            anomaly,
            color=colors,
            alpha=0.85
        )

        ax.axhline(
            0,
            color="black",
            linewidth=0.9
        )

        ax.set_title(
            f"{parameter} Anomaly - {station_label}",
            fontsize=13,
            fontweight="bold"
        )

        ax.set_xlabel("Month")
        ax.set_ylabel(f"Anomaly ({info['unit']})")

        ax.set_xticks(x)
        ax.set_xticklabels(months, rotation=45)

        ax.grid(axis="y", alpha=0.25)

        plt.tight_layout()

        filename = (
            f"{station_label}_"
            f"{parameter.replace(' ', '_')}_Anomaly.png"
        )

        plt.savefig(
            OUTPUT_DIR / filename,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()


# --------------------------------------------------
# 7. Completion message
# --------------------------------------------------

print("Climate analysis completed successfully.")
print(f"Number of stations: {len(stations)}")
print(f"Output directory: {OUTPUT_DIR}")
print("Station names were anonymized in all figures.")
print("Original Excel data were not modified.")
