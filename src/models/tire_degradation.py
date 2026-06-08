import pandas as pd
from pynascar import Schedule, Race, set_options, get_settings
from pynascar.driver import DriversData
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Enable local caching for faster repeated runs
set_options(cache_enabled=True, cache_dir=".cache/", df_format="parquet")

# Series: 1=Cup, 2=Xfinity, 3=Trucks
year = 2025
series_id = 1
race_id = 5553 
    
# Schedules
schedule = Schedule(year, series_id)
schedule.data.head()

martinsville_races = schedule.data[schedule.data['track_name'].str.contains('Martinsville', na=False)]

# Race data (use reload=True to force network fetch even if cached)
race = Race(year, series_id, race_id, reload=True)

'''
Filter to clean green-flag laps for one driver
Compute "laps since last pit stop" for each lap
Plot lap_time vs laps_since_pit
Fit a curve (linear or exponential)
The curve's slope = degradation rate, residuals = noise/std dev
'''

TRACK_LENGTH_MI = 0.526
lap_times = race.telemetry.lap_times.copy()   # explicit copy you own
lap_times['lap_time_sec'] = (TRACK_LENGTH_MI * 3600) / lap_times['lap_speed']

hamlin_clean = lap_times.loc[
    (lap_times['driver_name'] == 'Denny Hamlin') &
    (lap_times['lap_speed'] > 85),
    ['Lap', 'lap_speed', 'lap_time_sec']
]

"""
Compute "laps since last pit stop" for each lap
"""

# sorting thru pit stops
# Make a clean copy with proper dtypes
pit_stops_df = race.telemetry.pit_stops.copy()
pit_stops_df['lap'] = pd.to_numeric(pit_stops_df['lap'], errors='coerce').astype('Int64')

hamlin_pits = pit_stops_df[
    (pit_stops_df['driver_name'] == 'Denny Hamlin') &
    (pit_stops_df['lap'] > 0)
]['lap'].sort_values().tolist()

hamlin_pits_df = pd.DataFrame({'pit_lap': hamlin_pits}).astype('Int64')

# sorting thru green laps
hamlin_clean['Lap'] = pd.to_numeric(hamlin_clean['Lap'], errors='coerce')
hamlin_clean = hamlin_clean.dropna(subset=['Lap'])
hamlin_clean['Lap'] = hamlin_clean['Lap'].astype('Int64')
hamlin_clean = hamlin_clean.sort_values('Lap')

#merging both data frames
merged = pd.merge_asof(
    hamlin_clean,
    hamlin_pits_df,
    left_on='Lap',
    right_on='pit_lap',
    direction='backward'
)
merged['tire_age'] = merged['Lap'] - merged['pit_lap'].fillna(0)


slope, intercept, r_value, p_value, std_err = stats.linregress(
    merged['tire_age'], merged['lap_time_sec']
)
print(f"Fresh tire baseline: {intercept:.3f} seconds")
print(f"Degradation rate: {slope:.4f} sec/lap")
print(f"R² (fit quality): {r_value**2:.3f}")
print(f"R² (linear fit): {r_value**2:.3f}")
predicted = intercept + slope * merged['tire_age']
residuals = merged['lap_time_sec'] - predicted
noise_std = residuals.std()
print(f"Residual std dev: {noise_std:.3f} seconds")

x_fit = np.linspace(0, 125, 100)
y_fit = intercept + slope * x_fit

plt.scatter(merged['tire_age'], merged['lap_time_sec'], alpha=0.4)
plt.plot(x_fit, y_fit, 'r-', linewidth=2,
         label=f'Linear fit: y = {intercept:.2f} + {slope:.4f}x')
plt.xlabel('Tire Age (laps since last pit stop)')
plt.ylabel('Lap Time (seconds)')
plt.title('Hamlin — Tire Degradation with Linear Fit')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
