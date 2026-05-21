import pandas as pd
from pynascar import Schedule, Race, set_options, get_settings
from pynascar.driver import DriversData
import numpy as np
import matplotlib.pyplot as plt

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

real_laps = race.telemetry.lap_times[race.telemetry.lap_times['Lap']>0]
lap_times_table = real_laps.sort_values('Lap')
lap_speeds = race.telemetry.lap_times.loc[
    race.telemetry.lap_times['driver_name'] == 'Denny Hamlin',
    ['Lap', 'lap_speed']
]

lap_speeds = lap_speeds.sort_values('Lap')

# 
plt.scatter(x= lap_speeds['Lap'], y= lap_speeds['lap_speed'], alpha=0.3)
plt.ylabel('Speed')
plt.xlabel('Lap')
plt.title('Hamilin Times')
plt.grid(True, alpha=0.3)
plt.show()


# Need to 