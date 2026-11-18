# CMIP6 Climate Projections for Bushehr and the Persian Gulf Region

**Prepared by:** Leila Rashidian  
**Focus:** Regional climate projections, NetCDF processing, trend analysis, and scientific visualization

## Project Overview

This project presents selected CMIP6-based climate projection analyses for Bushehr on the northern coast of the Persian Gulf. It combines a curated set of scientific diagrams with Python workflows for processing monthly NetCDF model output and visualizing projected changes in surface temperature and precipitation.

The project is focused on the selected model data and study-area files used in the analysis. It should not be interpreted as a complete assessment of the entire Persian Gulf basin.

## Study Area

The study focuses on Bushehr and the adjacent northern Persian Gulf region, as represented by the input model grid used for each analysis.

## Variables, Models, and Scenarios

| Climate variable | CMIP6 model | Scenario | NetCDF variable |
|---|---|---|---|
| Surface temperature | CESM2 | SSP3-7.0 (SSP370) | `ts` |
| Precipitation | CNRM | SSP5-8.5 (SSP585) | `pr` |

## Analysis Workflow

### Surface temperature

- Reads monthly surface temperature (`ts`) from a local NetCDF file.
- Converts Kelvin to degrees Celsius when the variable units indicate Kelvin.
- Calculates a spatial mean, applying cosine-latitude weights when a compatible one-dimensional latitude coordinate is available.
- Estimates a linear trend and reports the trend slope in °C per decade, R², and p-value.
- Saves the time-series figure in PNG and PDF formats.

### Precipitation

- Reads monthly precipitation (`pr`) and the time coordinate from a local NetCDF file.
- Converts supported precipitation-rate units to monthly totals in mm/month using the number of days in each month.
- Calculates a spatial mean, applying cosine-latitude weights when a compatible one-dimensional latitude coordinate is available; otherwise, it uses an arithmetic spatial mean.
- Estimates a linear trend and reports the slope in mm/decade, R², and p-value.
- Saves the time-series figure in PNG and PDF formats.

**Spatial interpretation note:** The precipitation script averages all grid cells contained in the supplied NetCDF file. It does not apply a Bushehr administrative boundary mask or independently crop the file to the city boundary. The temperature script also assumes that the supplied NetCDF grid represents the intended study area. The spatial coverage of each input file must therefore be checked before interpreting the results as representative of Bushehr.

## Python Scripts

- [Surface temperature — CESM2 SSP370](Python_Codes/Surface_Temperature_Bushehr_CESM2_SSP370.py)
- [Precipitation — CNRM SSP585](Python_Codes/Precipitation_Bushehr_CNRM_SSP585.py)

## Running the Scripts

### Requirements

The scripts use:

- Python 3
- `netCDF4`
- `numpy`
- `pandas` (precipitation workflow)
- `matplotlib`
- `scipy`

Install the required packages with:

```bash
pip install netCDF4 numpy pandas matplotlib scipy
```

### Input files

The current scripts use local NetCDF paths defined in their **USER SETTINGS / input file** sections. Before running a script, update `NC_FILE` to the location of the corresponding NetCDF file on your computer.

The input files must contain the expected variable and a valid time coordinate:

- Temperature: `ts` and `time`; temperature units must be recognized as Kelvin or degrees Celsius.
- Precipitation: `pr` and `time`; the precipitation variable must have a supported `units` attribute.

Run a script from the repository or your Python environment:

```bash
python Python_Codes/Surface_Temperature_Bushehr_CESM2_SSP370.py
python Python_Codes/Precipitation_Bushehr_CNRM_SSP585.py
```

### Output

Figures are saved locally, relative to each script, in:

- `Figures/Surface_Temperature/`
- `Figures/Precipitation/`

The scripts generate PNG and PDF figures. These local outputs are not automatically uploaded to GitHub.

## Main Project Output

- [Curated CMIP6 climate projection diagrams (PDF)](../Persian%20Gulf%20CMIP6%20scenario%20diagrams.pdf)

## Interpretation and Limitations

- CMIP6 scenario results are conditional projections, not deterministic predictions.
- Results depend on the selected climate model, scenario pathway, temporal coverage, and spatial extent of the input grid.
- A spatial average over a supplied grid should not be described as a city-specific estimate unless the grid selection and spatial representativeness have been verified.
- Trend statistics (slope, R², and p-value) summarize the selected model time series; they do not quantify the full range of climate-model uncertainty.
- Projected model output must be distinguished from observed station records and climatological normals.

## Data Availability and Privacy

Original NetCDF datasets, precise point coordinates, and sensitive station-location metadata are not included in this public repository. Input data remain on the user's local computer. Only reviewed scripts, documentation, and selected public-facing figures are shared.

## Repository Structure

```text
Persian_Gulf_CMIP6_Climate_Projections/
├── README.md
├── Methodology.md
├── Python_Codes/
│   ├── Surface_Temperature_Bushehr_CESM2_SSP370.py
│   └── Precipitation_Bushehr_CNRM_SSP585.py
└── Figures/
    └── README.md
```

---

*Prepared for scientific communication and professional research portfolio purposes.*
