# Climate Change Analysis Project

This project provides a comprehensive climate change analysis using Python and GIS, focusing on CMIP6 scenarios. It includes statistical trend analysis, time series visualization, and spatial mapping of multiple climate parameters.

## Project Structure

climate_change_analysis/
├── analysis.py                ← Mann-Kendall & Sen trend analysis
├── plot_trends.ipynb          ← Jupyter Notebook for temperature scenario plotting
├── data/
│    ├── data_observation.csv  ← Observational climate data
│    └── SSP370_surface_temp.nc← NetCDF model output for surface temperature
├── results/
│    ├── MK_Sen_results.csv    ← Statistical results output
│    ├── Surface_Temperature_SSP126_Trend.png
│    └── Surface_Temperature_SSP126_Trend.pdf
├── README.md                  ← This file

## Features
- Mann-Kendall & Sen trend analysis for multiple climate parameters
- Time series plotting with trend lines
- GIS mapping for spatial visualization
- Flexible structure to add more regions or climate variables

## How to Use
1. Place your data files in the data/ folder.
2. Run analysis.py for statistical trend analysis.
3. Open plot_trends.ipynb in Jupyter Notebook to visualize time series and trend lines.
4. Output files (CSV, PNG, PDF) will be saved in the results/ folder.

## Contact
For collaboration or inquiries, contact me via:
- LinkedIn: [Leila Rashidian]  
- Email: Lrashidiyan@yahoo.com
