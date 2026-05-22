
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
race.telemetry.lap_times.head()
race.telemetry.pit_stops.head()
race.telemetry.events.head()

# pit stops ##########################################################
real_stops = race.telemetry.pit_stops[race.telemetry.pit_stops['lap']>0]
pit_stop_table = real_stops.sort_values('lap')

# # lap times ##########################################################
real_laps = race.telemetry.lap_times[race.telemetry.lap_times['Lap']>0]
lap_times_table = real_laps.sort_values('Lap')

# # caution flags ##########################################################
caution_flag_laps = race.results.cautions[race.results.cautions['start_lap']>0]
caution_table = caution_flag_laps.sort_values('start_lap')

# # lap by lap leaders ##########################################################
lap_by_lap_leaders = race.results.lead_changes.head()
lap_leaders_sorted = lap_by_lap_leaders.sort_values('start_lap')

# # loop data ##########################################################
loop_data = race.driver_data.drivers
loop_table_sorted = loop_data.sort_values('driver_id')

# # race events ##########################################################
race.telemetry.events['Lap'] = pd.to_numeric(race.telemetry.events['Lap'], errors='coerce')
race_events = race.telemetry.events[race.telemetry.events['Lap'] > 0]
events_table_sorted = race_events.sort_values('Lap')

green_laps = race.telemetry.events.loc[
    race.telemetry.events['Flag'] == 'Green',
    ['Lap']
]

pit_stops = race.telemetry.pit_stops.loc[
    race.telemetry.pit_stops['driver_name'] == 'Denny Hamlin',
    ['lap']
]

print(pit_stops)