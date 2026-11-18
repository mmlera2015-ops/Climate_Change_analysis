# Climate Assessment of the Iranian Caspian Sea Coast — Water Year 2025–2026

## Project Overview

This project assesses climate conditions along the southern coast of the Caspian Sea during the 2025–2026 water year (1 October 2025–30 September 2026), using observations from eight synoptic meteorological stations: Anzali, Ramsar, Nowshahr, Babolsar, Sari, Torkaman, Bandar-e Gaz, and Amirabad.

Observed conditions are compared with corresponding climatological normals for selected temperature and water-cycle variables.

## Key Findings

- **Mean air temperature:** Positive anomalies were reported at all eight stations, ranging from **+1.5°C to +2.9°C**. The simple average station anomaly was approximately **+2.2°C**.
- **Maximum air temperature:** Positive anomalies were reported at all stations, ranging from **+1.9°C to +3.0°C**.
- **Minimum air temperature:** The current analysis indicates negative anomalies at all eight stations, with a simple average anomaly of approximately **−2.7°C**. This contrasting pattern requires additional quality control and verification before firm interpretation.
- **Precipitation:** Strong spatial variability was observed. Anzali, Nowshahr, and Babolsar were above their respective normals, while the other five stations were below normal. The simple average across the eight stations was approximately **0.4% below normal**.
- **Evaporation:** Estimates were above normal at seven stations. However, some missing monthly observations were replaced with corresponding monthly climatological normals; evaporation results therefore require cautious interpretation.

## Why This Matters

The results highlight the importance of assessing temperature, precipitation, and evaporation together when examining climate conditions along the Iranian Caspian coast. Coastal station observations provide useful regional context, but they do not by themselves quantify changes in Caspian Sea level. A basin-scale water-balance assessment must also consider river inflow, precipitation directly over the sea, and evaporation from the sea surface.

## Project Contents

- `README.md`: project overview and principal findings.
- `Methodology.md`: data period, variables, comparison approach, and limitations.
- `Figures/`: selected, publication-ready figures will be added after final quality checks. Station identifiers should be anonymized in public figures where appropriate.


## CMIP6 Climate Projection Analysis — Central and Southern Caspian Sea

In addition to the observational assessment above, this repository includes a separate, model-based analysis of projected surface temperature and precipitation at selected locations in the central and southern Caspian Sea. These scenario-based analyses are distinct from the 2025–2026 coastal-station bulletin.

### Variables, Models, and Scenarios

| Variable | CMIP6 model | Scenario | NetCDF variable |
|---|---|---|---|
| Surface temperature | CESM2 | SSP3-7.0 (SSP370) | `ts` |
| Precipitation | CNRM | SSP5-8.5 (SSP585) | `pr` |

The scripts are designed to process a selected local NetCDF file for either the central or southern Caspian Sea location. They do not publish or require uploading the source NetCDF data to this repository.

### Analysis Workflow

- Read monthly model data and the associated time coordinate from NetCDF.
- Convert surface temperature from Kelvin to degrees Celsius when the file units indicate Kelvin.
- Convert precipitation to monthly millimetres using the units specified in the source file.
- Calculate a linear trend and report its slope, coefficient of determination (R²), and p-value.
- Generate time-series plots with fitted linear trends and save figure files locally in PNG and PDF formats.

Trend slopes are expressed in °C per decade for surface temperature and mm/month per decade for precipitation. Results should be interpreted in the context of the selected model, emissions scenario, spatial sampling, and model uncertainty. They are projections, not observations or a basin-wide estimate.

### Python Scripts

- [Surface temperature — CESM2 SSP370](Python_Codes/Surface_Temperature_Caspian_Central_South_CESM2_SSP370.py)
- [Precipitation — CNRM SSP585](Python_Codes/Precipitation_Caspian_Central_South_CNRM_SSP585.py)

### Running the Scripts

1. Install Python and the required packages: `netCDF4`, `numpy`, `pandas`, `matplotlib`, and `scipy`.
2. Run the relevant script in a Python environment.
3. Use the file-selection dialog (where provided) to select the NetCDF file stored on your computer.
4. Enter a short location label when prompted, such as `Caspian_Central` or `Caspian_South`.
5. The generated figures are saved locally in the corresponding `Figures` subfolder relative to the script location.

The exact NetCDF variable names and units must be available in the input files. The scripts validate supported units and may stop with an error if units are missing or unsupported.

### Data Availability and Privacy

Original NetCDF files, precise point coordinates, and sensitive station/location metadata are not included in this public repository. Only the analysis scripts and non-sensitive project documentation are shared. Generated figures are local outputs unless separately reviewed and intentionally added to the repository.


## Important Limitations

1. The simple average of the eight stations is not an area-weighted estimate for the entire Iranian coast or the Caspian Sea basin.
2. Minimum-temperature anomalies show an unusual contrast with the positive mean- and maximum-temperature anomalies and should be checked against the original observations and calculation procedures.
3. Some evaporation values include climatological substitutions for missing monthly observations. They should not be interpreted as fully observation-based annual totals.
4. Coastal station evaporation is not equivalent to evaporation from the Caspian Sea surface.

## Prepared by

**Leila Rashidian**  
Climate Change and Climate Data Analysis

---

*This project summary describes station-based climate analysis. Conclusions about Caspian Sea level changes require integration with hydrological and sea-surface water-balance data.*
