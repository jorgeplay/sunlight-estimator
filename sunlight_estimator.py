import pandas as pd
import numpy as np
from pvlib import solarposition, location
from datetime import datetime
import pytz
import matplotlib.pyplot as plt

# --- 1. Define your location and date ---
latitude = 60.1695
longitude = 24.9354
tz = 'Europe/Helsinki'
date = pd.Timestamp(datetime.now().date()).tz_localize(tz)

# --- 2. Define window and obstruction ---
window_azimuth_center = 230  # degrees (southwest)
window_azimuth_range = 30    # degrees on each side
min_azimuth = window_azimuth_center - window_azimuth_range
max_azimuth = window_azimuth_center + window_azimuth_range

obstacle_height = 9     # meters (approx. 3 stories)
obstacle_distance = 10  # meters
min_solar_elevation = np.degrees(np.arctan(obstacle_height / obstacle_distance))  # ~42°

# --- 3. Set up location and compute solar positions ---
site = location.Location(latitude, longitude, tz=tz)
times = pd.date_range(start=date, end=date + pd.Timedelta(days=1), freq='5min', tz=tz)
solpos = site.get_solarposition(times)

# --- 4. Apply sunlight visibility conditions ---
in_window_azimuth = solpos['azimuth'].between(min_azimuth, max_azimuth)
above_obstruction = solpos['elevation'] > min_solar_elevation
sunlit = in_window_azimuth & above_obstruction
sunlit_times = times[sunlit]

# --- 5. Output text summary ---
if not sunlit_times.empty:
    start_time = sunlit_times[0]
    end_time = sunlit_times[-1]
    sunlit_minutes = len(sunlit_times) * 5
    sunlit_hours = sunlit_minutes / 60

    print(f"Estimated direct sunlight through window today: {sunlit_hours:.2f} hours")
    print(f"Direct sunlight starts at: {start_time.strftime('%H:%M')}")
    print(f"Direct sunlight ends at:   {end_time.strftime('%H:%M')}")
else:
    print("No direct sunlight through the window today (due to orientation or obstructions).")

# --- 6. Plot the solar data ---
plt.figure(figsize=(10, 6))

# Plot solar elevation
plt.plot(times, solpos['elevation'], label='Solar Elevation (°)', color='orange')

# Plot obstruction elevation limit
plt.axhline(y=min_solar_elevation, color='gray', linestyle='--', label=f'Obstruction Limit ({min_solar_elevation:.1f}°)')

# Highlight sunlit times
plt.fill_between(times, 0, 90, where=sunlit, color='yellow', alpha=0.3, label='Direct Sunlight Through Window')

# Labels and formatting
plt.title('Direct Sunlight Window – Helsinki Today')
plt.xlabel('Time of Day')
plt.ylabel('Elevation (degrees)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show plot
plt.show()
