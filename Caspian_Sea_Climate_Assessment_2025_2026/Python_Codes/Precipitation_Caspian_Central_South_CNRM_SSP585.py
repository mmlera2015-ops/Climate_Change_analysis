# -*- coding: utf-8 -*-
"""
Monthly precipitation time series for the Caspian Sea study points.

Model: CNRM
Scenario: SSP5-8.5 (SSP585)

Use this same script for either the central or southern Caspian point.
Select the corresponding NetCDF file when prompted and enter the point name.
The script does not print, plot, or export latitude/longitude coordinates.
Do not upload the original NetCDF files to the public repository.
"""

import os
import calendar
import tkinter as tk
from tkinter import filedialog

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import linregress


MODEL = "CNRM"
SCENARIO = "SSP5-8.5 (SSP585)"
VARIABLE = "pr"


def choose_netcdf_file():
    """Open a file picker so local file paths do not need to be hard-coded."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(
        title="Select the Caspian Sea NetCDF file",
        filetypes=[("NetCDF files", "*.nc"), ("All files", "*.*")]
    )
    root.destroy()
    if not path:
        raise FileNotFoundError("No NetCDF file was selected.")
    return path


def convert_to_mm_per_month(values, units, dates):
    """Convert common CMIP precipitation units to monthly totals."""
    unit = str(units).strip().lower().replace(" ", "")
    days = np.array([
        getattr(t, "daysinmonth", calendar.monthrange(t.year, t.month)[1])
        for t in dates
    ], dtype=float)

    if unit in ("kgm-2s-1", "kg/m2/s", "kgm**-2s**-1"):
        return values * 86400.0 * days
    if unit in ("mm/day", "mmd-1", "mmd^-1", "mmday-1"):
        return values * days
    if unit in ("mm/month", "mmmonth-1", "kgm-2month-1"):
        return values
    if unit in ("m/s", "ms-1"):
        return values * 1000.0 * 86400.0 * days

    raise ValueError(
        "Unsupported or missing precipitation units: {!r}. "
        "Check the NetCDF 'pr' units before proceeding.".format(units)
    )


def main():
    region = input(
        "Enter study point (Central Caspian or Southern Caspian): "
    ).strip()

    if not region:
        raise ValueError("A study-point name is required.")

    nc_file = choose_netcdf_file()
    if not os.path.isfile(nc_file):
        raise FileNotFoundError("The selected NetCDF file does not exist.")

    with nc.Dataset(nc_file, "r") as ds:
        if VARIABLE not in ds.variables:
            raise KeyError("Variable 'pr' was not found in the selected file.")
        if "time" not in ds.variables:
            raise KeyError("A 'time' variable is required in the NetCDF file.")

        pr_var = ds.variables[VARIABLE]
        pr = np.ma.filled(np.ma.asarray(pr_var[:]), np.nan).astype(float)
        time_var = ds.variables["time"]

        dates = nc.num2date(
            time_var[:],
            units=time_var.units,
            calendar=getattr(time_var, "calendar", "standard"),
            only_use_cftime_datetimes=True
        )
        units = getattr(pr_var, "units", "")

    if pr.ndim == 1:
        pr_mean = pr
    elif pr.ndim >= 2:
        # The supplied files represent individual study points.
        # Average any remaining spatial dimensions without exposing coordinates.
        pr_mean = np.nanmean(pr.reshape(pr.shape[0], -1), axis=1)
    else:
        raise ValueError("Unexpected dimensions for precipitation variable 'pr'.")

    if len(dates) != len(pr_mean):
        raise ValueError("Time dimension and precipitation data length do not match.")

    pr_mm_month = convert_to_mm_per_month(pr_mean, units, dates)

    valid = np.isfinite(pr_mm_month)
    if np.count_nonzero(valid) < 3:
        raise ValueError("At least three valid monthly values are required.")

    pr_mm_month = pr_mm_month[valid]
    valid_dates = [dates[i] for i in np.flatnonzero(valid)]
    plot_dates = [
        mdates.date2num(
            __import__("datetime").datetime(int(t.year), int(t.month), 15)
        )
        for t in valid_dates
    ]

    x = np.arange(len(pr_mm_month), dtype=float)
    result = linregress(x, pr_mm_month)
    trend = result.intercept + result.slope * x
    trend_per_decade = result.slope * 120.0
    r_squared = result.rvalue ** 2

    print("Study point: {}".format(region))
    print("Model: {}".format(MODEL))
    print("Scenario: {}".format(SCENARIO))
    print("Valid monthly records: {}".format(len(pr_mm_month)))
    print("Linear trend: {:.3f} mm/month per decade".format(trend_per_decade))
    print("R-squared: {:.3f}".format(r_squared))
    print("p-value: {:.4g}".format(result.pvalue))

    safe_region = "_".join(region.strip().split()).replace("/", "-")
    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "Figures", "Precipitation"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_stem = "Precipitation_{}_{}_SSP585".format(safe_region, MODEL)

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(
        plot_dates,
        pr_mm_month,
        linewidth=1.8,
        label="Monthly precipitation – {}".format(region)
    )
    ax.plot(
        plot_dates,
        trend,
        "r--",
        linewidth=2,
        label="Linear trend: {:.2f} mm/month per decade (R²={:.2f})".format(
            trend_per_decade, r_squared
        )
    )

    ax.set_title(
        "Projected Precipitation – {} ({}; {})".format(
            region, MODEL, SCENARIO
        ),
        fontsize=15,
        fontweight="bold"
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Precipitation (mm/month)")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.YearLocator(10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.autofmt_xdate()
    fig.tight_layout()

    png_path = os.path.join(output_dir, output_stem + ".png")
    pdf_path = os.path.join(output_dir, output_stem + ".pdf")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.show()

    print("PNG saved: {}".format(png_path))
    print("PDF saved: {}".format(pdf_path))


if __name__ == "__main__":
    main()
