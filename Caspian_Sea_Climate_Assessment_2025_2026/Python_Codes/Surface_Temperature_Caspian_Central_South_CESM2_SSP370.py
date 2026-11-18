# -*- coding: utf-8 -*-
"""
Projected surface temperature over the Caspian Sea
Model: CESM2 | Scenario: SSP3-7.0 (SSP370)

Select the local NetCDF file for either the central or southern Caspian Sea.
Raw NetCDF data and geographic coordinates are not exported.
"""

import os
import re
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

import netCDF4 as nc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


# ==========================================================
# Select a local NetCDF file and identify the Caspian region
# ==========================================================
root = tk.Tk()
root.withdraw()

his_file = filedialog.askopenfilename(
    title="Select CESM2 SSP3-7.0 NetCDF file (Caspian Sea)",
    filetypes=[("NetCDF files", "*.nc"), ("All files", "*.*")]
)

if not his_file:
    raise SystemExit("No NetCDF file was selected.")

region = simpledialog.askstring(
    "Caspian Sea region",
    "Enter the region name (e.g. Caspian_Central or Caspian_South):"
)

if not region or not region.strip():
    raise SystemExit("A region name is required.")

region = region.strip()
region_tag = re.sub(r"[^A-Za-z0-9_-]+", "_", region).strip("_")
if not region_tag:
    region_tag = "Caspian_Sea"


# ==========================================================
# Read surface temperature (ts) and time from NetCDF
# ==========================================================
def read_ts(file_path):
    with nc.Dataset(file_path, "r") as ds:
        if "ts" not in ds.variables:
            raise KeyError("The NetCDF file does not contain the variable 'ts'.")
        if "time" not in ds.variables:
            raise KeyError("The NetCDF file does not contain the variable 'time'.")

        ts_var = ds.variables["ts"]
        time_var = ds.variables["time"]

        if ts_var.ndim < 1 or ts_var.dimensions[0] != time_var.dimensions[0]:
            raise ValueError(
                "The first dimension of 'ts' must correspond to the NetCDF time dimension."
            )

        ts_data = np.ma.filled(ts_var[:], np.nan).astype(float)
        time_values = time_var[:]
        time_units = time_var.units
        calendar = getattr(time_var, "calendar", "standard")
        temperature_units = getattr(ts_var, "units", "").strip()

    # Convert NetCDF dates to regular monthly timestamps.
    time_values = nc.num2date(
        time_values,
        units=time_units,
        calendar=calendar,
        only_use_cftime_datetimes=True
    )
    dates = pd.to_datetime([
        pd.Timestamp(year=int(t.year), month=int(t.month), day=15)
        for t in time_values
    ])

    # Average over every spatial dimension; retain the time dimension.
    if ts_data.ndim > 1:
        ts_mean = np.nanmean(ts_data, axis=tuple(range(1, ts_data.ndim)))
    else:
        ts_mean = ts_data

    ts_mean = np.asarray(ts_mean, dtype=float).reshape(-1)

    if len(dates) != len(ts_mean):
        raise ValueError("The time coordinate and temperature series have different lengths.")

    # Convert units explicitly; do not silently assume an unknown unit.
    unit_norm = temperature_units.lower().replace(" ", "").replace("_", "")
    if unit_norm in ("k", "kelvin", "degreesk", "degreek"):
        ts_mean_c = ts_mean - 273.15
    elif unit_norm in (
        "c", "degc", "degreec", "degreesc", "degreecelsius",
        "degreescelsius", "celsius"
    ):
        ts_mean_c = ts_mean
    else:
        raise ValueError(
            "Unrecognized or missing units for 'ts': {!r}. "
            "Expected Kelvin (K) or degrees Celsius (°C).".format(temperature_units)
        )

    return dates, ts_mean_c


dates_ts, ts_model = read_ts(his_file)

# Remove missing values before trend analysis.
valid = np.isfinite(ts_model) & ~pd.isna(dates_ts)
dates_ts = dates_ts[valid]
ts_model = ts_model[valid]

if len(ts_model) < 3:
    raise ValueError("At least three valid monthly temperature values are required.")

# ==========================================================
# Linear trend (monthly data): convert slope to °C per decade
# ==========================================================
x_num = np.arange(len(ts_model), dtype=float)
slope, intercept, r_value, p_value, std_err = linregress(x_num, ts_model)

slope_per_decade = slope * 120.0
trend_line = intercept + slope * x_num
r_squared = r_value ** 2

# ==========================================================
# Plot time series and trend
# ==========================================================
plt.figure(figsize=(14, 6))

plt.plot(
    dates_ts,
    ts_model,
    color="#1f77b4",
    linewidth=1.8,
    label="Surface Temperature (°C)"
)

plt.plot(
    dates_ts,
    trend_line,
    color="red",
    linestyle="--",
    linewidth=2,
    label=(
        "Linear trend: {:+.3f} °C/decade | R²={:.3f} | p={:.3g}"
        .format(slope_per_decade, r_squared, p_value)
    )
)

plt.title(
    "Projected Surface Temperature – {} (CESM2, SSP3-7.0)".format(region),
    fontsize=15,
    fontweight="bold"
)
plt.xlabel("Year", fontsize=13)
plt.ylabel("Surface Temperature (°C)", fontsize=13)
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.45)
plt.legend(fontsize=10)
plt.tight_layout()

# ==========================================================
# Save figures in the project Figures folder
# ==========================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.normpath(
    os.path.join(script_dir, "..", "Figures", "Surface_Temperature")
)
os.makedirs(output_dir, exist_ok=True)

base_name = "Surface_Temperature_{}_CESM2_SSP370".format(region_tag)
png_path = os.path.join(output_dir, base_name + ".png")
pdf_path = os.path.join(output_dir, base_name + ".pdf")

plt.savefig(png_path, dpi=300, bbox_inches="tight")
plt.savefig(pdf_path, bbox_inches="tight")
plt.show()

print("\nAnalysis completed.")
print("Region: {}".format(region))
print("Model: CESM2 | Scenario: SSP3-7.0")
print("Valid monthly records: {}".format(len(ts_model)))
print("Linear trend: {:+.4f} °C/decade".format(slope_per_decade))
print("R-squared: {:.4f}".format(r_squared))
print("p-value: {:.6g}".format(p_value))
print("PNG output: {}".format(png_path))
print("PDF output: {}".format(pdf_path))
print("No raw NetCDF data or geographic coordinates were exported.")
