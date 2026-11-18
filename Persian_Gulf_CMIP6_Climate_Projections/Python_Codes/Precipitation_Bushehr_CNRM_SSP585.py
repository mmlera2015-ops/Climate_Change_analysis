# -*- coding: utf-8 -*-
"""
Monthly precipitation projection for Bushehr
Model: CNRM | Scenario: SSP5-8.5

Input: NetCDF variable 'pr' with dimensions (time, lat, lon).
The script converts precipitation rates to monthly totals (mm/month),
calculates a linear trend (mm/decade), and saves PNG and PDF figures.

IMPORTANT:
- Confirm that the NetCDF file covers the intended Bushehr study area.
- The script averages all grid cells in the file; it does not apply a
  geographic mask or crop to a Bushehr boundary.
- The precipitation unit is read from the NetCDF variable attributes.
"""

import os
import warnings
from datetime import datetime

import netCDF4 as nc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


# ============================================================
# USER SETTINGS
# ============================================================

NC_FILE = (
    r"E:\WORK-2025\Scenario\Bushehr\Precipitation"
    r"\CNRM\SSP.585\585.nc"
)

VARIABLE_NAME = "pr"
MODEL_NAME = "CNRM"
SCENARIO_NAME = "SSP5-8.5"
STUDY_AREA = "Bushehr"

# Output is saved in the project's Figures/Precipitation folder.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(
    os.path.join(SCRIPT_DIR, "..", "Figures", "Precipitation")
)

# ============================================================
# FUNCTIONS
# ============================================================

def convert_to_monthly_mm(values, units, days_in_month):
    """Convert common precipitation-rate units to mm/month."""
    unit = str(units).strip().lower()
    unit = unit.replace("**", "^").replace(" ", "")
    unit = unit.replace("−", "-")

    values = np.asarray(values, dtype=float)
    days = np.asarray(days_in_month, dtype=float)

    if unit in (
        "kgm-2s-1", "kgm^-2s^-1", "kg/m2/s",
        "kgm-2sec-1", "kgm^-2sec^-1",
        "mm/s", "mms-1", "mms^-1"
    ):
        return values * 86400.0 * days

    if unit in ("mm/day", "mmd-1", "mmd^-1", "mmday-1"):
        return values * days

    if unit in ("mm/month", "mmmonth-1", "mmmonth^-1"):
        return values

    if unit in ("mm",):
        warnings.warn(
            "The NetCDF unit is 'mm'. The values are treated as monthly totals. "
            "Please verify the temporal meaning of this unit."
        )
        return values

    raise ValueError(
        "Unsupported precipitation unit: {!r}. "
        "Check the 'units' attribute of the NetCDF variable '{}' "
        "and add the correct conversion before proceeding.".format(
            units, VARIABLE_NAME
        )
    )


def calculate_spatial_mean(data, dataset):
    """
    Calculate a cosine-latitude-weighted mean when a 1-D latitude
    coordinate is available; otherwise use an arithmetic mean.
    """
    lat_name = None
    for candidate in ("lat", "latitude", "LATITUDE"):
        if candidate in dataset.variables:
            lat_name = candidate
            break

    if lat_name is None:
        warnings.warn(
            "No 1-D latitude coordinate was found. "
            "Using an arithmetic spatial mean."
        )
        return np.nanmean(data, axis=(1, 2))

    lat = np.asarray(dataset.variables[lat_name][:], dtype=float)

    if lat.ndim != 1 or data.ndim != 3 or data.shape[1] != lat.size:
        warnings.warn(
            "Latitude coordinate is not compatible with (time, lat, lon). "
            "Using an arithmetic spatial mean."
        )
        return np.nanmean(data, axis=(1, 2))

    weights = np.cos(np.deg2rad(lat))
    weights = np.clip(weights, 0.0, None)[None, :, None]

    valid = np.isfinite(data)
    weighted_values = np.where(valid, data * weights, 0.0)
    valid_weights = np.where(valid, weights, 0.0)

    numerator = np.sum(weighted_values, axis=(1, 2))
    denominator = np.sum(valid_weights, axis=(1, 2))

    with np.errstate(divide="ignore", invalid="ignore"):
        result = numerator / denominator

    result[denominator == 0] = np.nan
    return result


# ============================================================
# CHECK INPUT FILE
# ============================================================

if not os.path.isfile(NC_FILE):
    raise FileNotFoundError(
        "NetCDF file was not found. Please check NC_FILE:\n{}".format(NC_FILE)
    )

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# READ NETCDF DATA
# ============================================================

with nc.Dataset(NC_FILE, mode="r") as ds:
    print("NetCDF variables:", list(ds.variables.keys()))

    if VARIABLE_NAME not in ds.variables:
        raise KeyError(
            "Variable '{}' was not found. Available variables: {}".format(
                VARIABLE_NAME, list(ds.variables.keys())
            )
        )

    if "time" not in ds.variables:
        raise KeyError("The NetCDF file does not contain a 'time' variable.")

    pr_var = ds.variables[VARIABLE_NAME]
    time_var = ds.variables["time"]

    pr_units = getattr(pr_var, "units", None)
    if pr_units is None:
        raise ValueError(
            "The precipitation variable has no 'units' attribute. "
            "Unit conversion cannot be performed safely."
        )

    # Preserve masked/fill values as NaN.
    pr_raw = np.ma.filled(pr_var[:], np.nan).astype(float)

    if pr_raw.ndim != 3:
        raise ValueError(
            "Expected a 3-D precipitation array (time, lat, lon), "
            "but received shape {}.".format(pr_raw.shape)
        )

    time_cf = nc.num2date(
        time_var[:],
        units=time_var.units,
        calendar=getattr(time_var, "calendar", "standard"),
        only_use_cftime_datetimes=False,
        only_use_python_datetimes=False
    )

    # Extract year and month. Day 15 is used only as a plotting timestamp.
    dates = pd.to_datetime([
        datetime(int(t.year), int(t.month), 15) for t in time_cf
    ])

    # Spatial average across the grid cells in this NetCDF file.
    pr_mean_rate = calculate_spatial_mean(pr_raw, ds)

# ============================================================
# CONVERT TO MONTHLY PRECIPITATION TOTAL (mm/month)
# ============================================================

days_in_month = dates.days_in_month.to_numpy(dtype=float)

pr_mm_month = convert_to_monthly_mm(
    pr_mean_rate,
    pr_units,
    days_in_month
)

# ============================================================
# VALID DATA AND LINEAR TREND
# ============================================================

valid = np.isfinite(pr_mm_month)

if np.count_nonzero(valid) < 3:
    raise ValueError(
        "Fewer than three valid monthly precipitation values are available; "
        "a reliable linear trend cannot be calculated."
    )

dates_valid = dates[valid]
precip_valid = pr_mm_month[valid]

# Time expressed in years from the first valid observation.
elapsed_years = (
    (dates_valid - dates_valid[0]).days.to_numpy(dtype=float) / 365.2425
)

slope_per_year, intercept, r_value, p_value, std_err = linregress(
    elapsed_years, precip_valid
)

slope_per_decade = slope_per_year * 10.0
trend = intercept + slope_per_year * elapsed_years
r_squared = r_value ** 2

print("\n========== TREND RESULTS ==========")
print("Model: {}".format(MODEL_NAME))
print("Scenario: {}".format(SCENARIO_NAME))
print("Variable: {}".format(VARIABLE_NAME))
print("Original units: {}".format(pr_units))
print("Valid monthly values: {}".format(len(precip_valid)))
print("Linear trend: {:.3f} mm/decade".format(slope_per_decade))
print("R-squared: {:.4f}".format(r_squared))
print("p-value: {:.4g}".format(p_value))
print("===================================\n")

# ============================================================
# PLOT
# ============================================================

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    dates_valid.to_numpy(),
    precip_valid,
    linewidth=1.8,
    label="Monthly precipitation"
)

ax.plot(
    dates_valid.to_numpy(),
    trend,
    "r--",
    linewidth=2.0,
    label=(
        "Linear trend: {:.2f} mm/decade (R² = {:.3f})"
        .format(slope_per_decade, r_squared)
    )
)

ax.set_title(
    "Projected Monthly Precipitation in {} ({} – {})".format(
        STUDY_AREA, MODEL_NAME, SCENARIO_NAME
    ),
    fontsize=15,
    fontweight="bold"
)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Precipitation (mm/month)", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.45)
ax.legend()
fig.autofmt_xdate()
fig.tight_layout()

# ============================================================
# SAVE FIGURES
# ============================================================

base_name = "Precipitation_{}_{}_SSP585_Trend".format(
    STUDY_AREA, MODEL_NAME
)

png_path = os.path.join(OUTPUT_DIR, base_name + ".png")
pdf_path = os.path.join(OUTPUT_DIR, base_name + ".pdf")

fig.savefig(png_path, dpi=300, bbox_inches="tight")
fig.savefig(pdf_path, bbox_inches="tight")

print("PNG saved to:", png_path)
print("PDF saved to:", pdf_path)

plt.show()
