# -*- coding: utf-8 -*-
"""
Monthly surface temperature projection for Bushehr
Model: CESM2 | Scenario: SSP3-7.0 (SSP370)

The NetCDF input is assumed to contain the study-area grid.
No geographic coordinates or station locations are printed or exported.
"""

import os
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import linregress

# ---------------------------------------------------------------------
# Input file (local path; do not upload the NetCDF data to the repository)
# ---------------------------------------------------------------------
NC_FILE = (
    r"E:\WORK-2025\Scenario\Bushehr\Surface temperature"
    r"\CESM2\SSP.370\370.nc"
)

# Output directory is relative to this script's location.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.normpath(
    os.path.join(SCRIPT_DIR, "..", "Figures", "Surface_Temperature")
)
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_STEM = "Surface_Temperature_Bushehr_CESM2_SSP370"

# ---------------------------------------------------------------------
# Read and validate NetCDF data
# ---------------------------------------------------------------------
if not os.path.isfile(NC_FILE):
    raise FileNotFoundError(
        "Input NetCDF file was not found. Update NC_FILE to the local file path."
    )

with nc.Dataset(NC_FILE, "r") as dataset:
    if "ts" not in dataset.variables:
        raise KeyError("Variable 'ts' was not found in the NetCDF file.")

    ts_var = dataset.variables["ts"]
    ts_data = np.ma.filled(np.ma.asarray(ts_var[:]), np.nan).astype(float)

    if ts_data.ndim != 3:
        raise ValueError(
            "Expected 'ts' to have three dimensions: (time, lat, lon). "
            "Please check the NetCDF variable dimensions."
        )

    time_var = dataset.variables.get("time")
    if time_var is None:
        raise KeyError("A 'time' coordinate is required to build the monthly series.")

    time_values = np.asarray(time_var[:])
    time_units = getattr(time_var, "units", None)
    if not time_units:
        raise ValueError("The NetCDF time variable has no 'units' attribute.")

    calendar = getattr(time_var, "calendar", "standard")
    dates = nc.num2date(
        time_values,
        units=time_units,
        calendar=calendar,
        only_use_cftime_datetimes=False,
        only_use_python_datetimes=True
    )

    # Use latitude weights when a compatible 1-D latitude coordinate exists.
    # Coordinates are used internally only; they are not printed or exported.
    latitudes = None
    if "lat" in dataset.variables:
        lat_candidate = np.asarray(dataset.variables["lat"][:])
        if lat_candidate.ndim == 1 and lat_candidate.size == ts_data.shape[1]:
            latitudes = lat_candidate.astype(float)

    units = str(getattr(ts_var, "units", "")).strip().lower()

# ---------------------------------------------------------------------
# Convert temperature to degrees Celsius
# ---------------------------------------------------------------------
if units in ("k", "kelvin", "degrees_k", "degree_k"):
    ts_celsius = ts_data - 273.15
elif units in ("degc", "degree_celsius", "degrees_celsius", "celsius", "°c"):
    ts_celsius = ts_data.copy()
else:
    # CMIP6 surface temperature (ts) is normally stored in Kelvin.
    # Do not silently guess when the units are absent or unexpected.
    raise ValueError(
        "Unrecognized temperature units: {!r}. "
        "Expected Kelvin (K) or degrees Celsius.".format(units)
    )

# ---------------------------------------------------------------------
# Spatial mean for each time step
# ---------------------------------------------------------------------
if latitudes is not None and np.all(np.isfinite(latitudes)):
    weights = np.cos(np.deg2rad(latitudes))
    weights = np.clip(weights, 0.0, None)
    weights_2d = weights[:, np.newaxis]
    valid = np.isfinite(ts_celsius)
    numerator = np.nansum(ts_celsius * weights_2d[np.newaxis, :, :], axis=(1, 2))
    denominator = np.sum(valid * weights_2d[np.newaxis, :, :], axis=(1, 2))
    with np.errstate(invalid="ignore", divide="ignore"):
        monthly_mean = numerator / denominator
else:
    monthly_mean = np.nanmean(ts_celsius, axis=(1, 2))

monthly_mean = np.asarray(monthly_mean, dtype=float)
date_numbers = mdates.date2num(list(dates))
valid_time = np.isfinite(monthly_mean) & np.isfinite(date_numbers)

if np.count_nonzero(valid_time) < 3:
    raise ValueError("Not enough valid monthly values to calculate a reliable trend.")

monthly_mean = monthly_mean[valid_time]
date_numbers = date_numbers[valid_time]
plot_dates = [dates[i] for i in np.flatnonzero(valid_time)]

# ---------------------------------------------------------------------
# Linear trend: monthly slope converted to degrees Celsius per decade
# ---------------------------------------------------------------------
time_index = np.arange(monthly_mean.size, dtype=float)
trend = linregress(time_index, monthly_mean)
slope_per_decade = trend.slope * 120.0
trend_line = trend.intercept + trend.slope * time_index

print("Study area: Bushehr")
print("Model: CESM2")
print("Scenario: SSP3-7.0 (SSP370)")
print("Valid monthly records: {}".format(monthly_mean.size))
print("Linear trend: {:.3f} °C/decade".format(slope_per_decade))
print("R-squared: {:.3f}".format(trend.rvalue ** 2))
print("p-value: {:.4g}".format(trend.pvalue))

# ---------------------------------------------------------------------
# Plot and save
# ---------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    plot_dates,
    monthly_mean,
    color="steelblue",
    linewidth=1.2,
    label="Monthly mean surface temperature"
)
ax.plot(
    plot_dates,
    trend_line,
    color="darkred",
    linestyle="--",
    linewidth=2,
    label="Linear trend: {:.3f} °C/decade".format(slope_per_decade)
)

ax.set_title(
    "Surface Temperature Projection – Bushehr\nCESM2 | SSP3-7.0 (SSP370)",
    fontsize=13
)
ax.set_xlabel("Year")
ax.set_ylabel("Surface temperature (°C)")
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
ax.xaxis.set_major_locator(mdates.YearLocator(10))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
fig.autofmt_xdate()
fig.tight_layout()

png_path = os.path.join(OUTPUT_DIR, OUTPUT_STEM + ".png")
pdf_path = os.path.join(OUTPUT_DIR, OUTPUT_STEM + ".pdf")
fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(pdf_path, bbox_inches="tight")
plt.show()

print("PNG saved to: {}".format(png_path))
print("PDF saved to: {}".format(pdf_path))
