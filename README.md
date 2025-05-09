# Sunlight Estimator

This script calculates the amount of direct sunlight passing through a window based on location, date, and obstructions.

## Features
- Computes solar positions using `pvlib`.
- Estimates sunlight visibility through a window with specified azimuth and obstruction parameters.
- Outputs a summary of sunlight hours and visualizes the data with a plot.

## Requirements
- Python 3.8+
- Required libraries: `pandas`, `numpy`, `pvlib`, `matplotlib`, `pytz`

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt