# Leila Rashidian

## Senior Climate Change Expert | Climate Data Analyst | Marine Climatology

**Climate Change Assessment | CMIP6 & SSP Scenarios | Python | GIS | Climate Modelling | Marine and Polar Climatology**

## Professional Profile

I am a climate change and climate data professional with more than 23 years of overall professional experience, including approximately 14 years of specialized experience in climate change research, marine climatology, climate data analysis, and scientific project coordination.

My areas of expertise include climate scenario analysis (CMIP6, RCP and SSP pathways), climate trend and variability assessment, marine and coastal climatology, climate modelling, and GIS-based spatial analysis. I use Python, R, MATLAB, GIS, and climate and ocean modelling tools to process, analyse, interpret, and visualize climate and oceanographic data.

My professional and research experience covers the Caspian Sea, Persian Gulf, Gulf of Oman, Indian Ocean, Arctic, and Antarctic regions.

I am registered as an expert reviewer in the IPCC Seventh Assessment Report (AR7), Working Group II review process. I reviewed eight chapters and submitted formal technical comments through the official review platform. This repository does not contain confidential review material.

## Repository Overview

This repository presents selected examples of my work in climate data analysis, climate scenario assessment, and scientific visualization. It is intended as a professional portfolio and a starting point for reproducible analysis.

### 1. Observed Climate Parameters Analysis Using Python

**Script:** [Python_Codes/Observed_Climate_Parameters.py](Python_Codes/Observed_Climate_Parameters.py)

This Python workflow compares observed monthly meteorological parameters with their corresponding climatological normals and generates comparison and anomaly charts.

**Climate parameters**
- Precipitation
- Mean temperature
- Maximum temperature
- Minimum temperature
- Relative humidity
- Evaporation

**Methodology and outputs**
- Reads a locally selected Excel workbook.
- Checks that the required data columns are available.
- Organizes monthly values by station.
- Calculates anomalies as observed values minus climatological normals.
- Generates observed-versus-normal comparison charts and monthly anomaly charts.
- Uses anonymized station labels in the figures.

**Data privacy:** Original observational datasets are not included in this public repository. The script reads the user's local Excel file; station names are anonymized in generated figures, and station coordinates are neither required nor published.

### 2. CMIP6 Climate Scenario Analysis – Persian Gulf

This project presents selected climate scenario analysis outputs for the Persian Gulf region. The accompanying PDF contains scientific diagrams prepared to communicate projected climate conditions under CMIP6 scenarios.

[View CMIP6 Scenario Diagrams – Persian Gulf (PDF)](Persian%20Gulf%20CMIP6%20scenario%20diagrams.pdf)

The scenario work reflects the use of climate model projections, SSP pathways, data processing, and scientific visualization for regional climate assessment.

### 3. Caspian Sea Climate Assessment and CMIP6 Scenario Analysis

The Caspian Sea work is organized as a dedicated project with two distinct components:

- **Observed coastal climate assessment (2025–2026):** analysis of meteorological observations and climatological normals along the Iranian Caspian coast. The project page documents the study scope, methodology, findings, and important data limitations.
- **CMIP6 scenario analysis:** selected central and southern Caspian Sea locations are analysed using model output for surface temperature (CESM2, SSP3-7.0) and precipitation (CNRM, SSP5-8.5). Python scripts read local NetCDF files and generate time-series and trend figures.

The observational station assessment and model-based scenario analysis are separate analyses and should not be interpreted as a single continuous dataset or as a basin-wide assessment.

[Open the Caspian Sea project and methodology](Caspian_Sea_Climate_Assessment_2025_2026/README.md)

**Scenario analysis scripts:**
- [Surface temperature — CESM2 SSP370](Caspian_Sea_Climate_Assessment_2025_2026/Python_Codes/Surface_Temperature_Caspian_Central_South_CESM2_SSP370.py)
- [Precipitation — CNRM SSP585](Caspian_Sea_Climate_Assessment_2025_2026/Python_Codes/Precipitation_Caspian_Central_South_CNRM_SSP585.py)

Original NetCDF files and precise point coordinates are not included in the public repository.

### 4. Persian Gulf CMIP6 Climate Projections

A dedicated project page for the Bushehr / Persian Gulf CMIP6 scenario diagrams, with project documentation and methodology.

[Open the Persian Gulf project](Persian_Gulf_CMIP6_Climate_Projections/README.md)

## Repository Structure

```text
Climate_Change_analysis/
├── Python_Codes/
│   └── Observed_Climate_Parameters.py
├── Persian Gulf CMIP6 scenario diagrams.pdf
├── Persian_Gulf_CMIP6_Climate_Projections/
│   ├── README.md
│   ├── Methodology.md
│   └── Figures/
│       └── README.md
├── Caspian_Sea_Climate_Assessment_2025_2026/
│   ├── README.md
│   ├── Methodology.md
│   ├── Python_Codes/
│   │   ├── Surface_Temperature_Caspian_Central_South_CESM2_SSP370.py
│   │   └── Precipitation_Caspian_Central_South_CNRM_SSP585.py
│   └── Figures/
│       └── README.md
├── Leila_Rashidian_International_CV.pdf
├── requirements.txt
└── README.md
```

The repository also contains selected supporting figures and professional documents. Original observational datasets and station coordinates are not published.

## How to Run the Python Analysis

### Requirements

- Python 3
- pandas
- NumPy
- Matplotlib
- openpyxl

Install the required packages:

```bash
pip install -r requirements.txt
```

### Input Excel workbook

The script opens a file-selection window so that the input workbook can remain on your local computer. The workbook must contain a worksheet named `Sheet1` and the required columns below:

- `station_name`, `month`
- Observed values: `rrr24`, `tm_m`, `tmax_m`, `tmin_m`, `umm`, `evt_s`
- Corresponding normal values: `n_rrr24`, `n_tm_m`, `n_tmax_m`, `n_tmin_m`, `n_umm`, `n_evt_s`

Run the script from the repository directory:

```bash
python Python_Codes/Observed_Climate_Parameters.py
```

Select your local Excel workbook when prompted. The generated figures are saved automatically in:

```text
Figures/Observed_Climate/
```

The original Excel workbook is not modified or uploaded by the script.

## Tools and Technologies

Python | Pandas | NumPy | Matplotlib | Excel | NetCDF | R | MATLAB | ArcGIS | RegCM4 | WRF | SWAN | MIKE 21

## Research Interests

- Climate change impacts, risks, and adaptation
- CMIP6 climate projections and SSP scenarios
- Climate variability and long-term trend analysis
- Marine and coastal climatology
- Oceanographic and wave modelling
- Polar climate research
- GIS-based climate analysis and visualization

## International CV

[View International CV (PDF)](Leila_Rashidian_International_CV.pdf)

## Contact and Collaboration

I welcome opportunities for international research collaboration, climate data analysis, marine and coastal climate assessment, and project-based scientific consultancy, including remote assignments.

- **LinkedIn:** [Leila Rashidian](https://www.linkedin.com/in/leila-rashidian-5a8512315/)
- **GitHub:** [Climate Change Analysis](https://github.com/mmlera2015-ops/Climate_Change_analysis)
