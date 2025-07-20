import os
import fastf1
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.offsetbox import AnchoredText

# Setup FastF1 cache
os.makedirs('cache', exist_ok=True)
fastf1.Cache.enable_cache('cache')

# Load Abu Dhabi 2021 Race
session = fastf1.get_session(2021, 22, 'R')
session.load()

# Total race laps
total_laps = session.laps['LapNumber'].max()

# Extract track outline using fastest lap
reference_lap = session.laps.pick_fastest()
reference_tel = reference_lap.get_telemetry()
track_x = reference_tel['X'].values
track_y = reference_tel['Y'].values

# Collect telemetry data for all drivers
drivers = session.drivers
driver_data = {}

for drv in drivers:
    laps = session.laps.pick_drivers(drv).reset_index()
    x_all, y_all, time_all = [], [], []

    for _, lap in laps.iterrows():
        tel = lap.get_telemetry()
        x_all.extend(tel['X'].values)
        y_all.extend(tel['Y'].values)
        time_all.extend(tel['Time'].dt.total_seconds().values)

    if x_all and y_all:
        driver_data[drv] = {
            'abbr': session.get_driver(drv)['Abbreviation'],
            'x': np.array(x_all),
            'y': np.array(y_all),
            'time': np.array(time_all)
        }

# Normalize time for all drivers
start_time = min(d['time'][0] for d in driver_data.values())
for d in driver_data.values():
    d['time'] -= start_time

# Setup plot
fig = plt.figure(figsize=(16, 16))
ax = fig.add_axes([0.05, 0.05, 0.9, 0.9])
ax.axis('off')

# Track boundaries
all_x = np.concatenate([d['x'] for d in driver_data.values()])
all_y = np.concatenate([d['y'] for d in driver_data.values()])
margin_x = (all_x.max() - all_x.min()) * 0.02
margin_y = (all_y.max() - all_y.min()) * 0.02
ax.set_xlim(all_x.min() - margin_x, all_x.max() + margin_x)
ax.set_ylim(all_y.min() - margin_y, all_y.max() + margin_y)

# Draw circuit layout
ax.plot(track_x, track_y, color='black', linewidth=1.5, alpha=0.6, zorder=0)

# Create driver markers and labels
for drv, d in driver_data.items():
    d['dot'], = ax.plot([], [], 'o', markersize=6, label=d['abbr'], zorder=1)
    d['label'] = ax.text(0, 0, d['abbr'], fontsize=7, ha='center', va='bottom')

# Leaderboard box
leaderboard_box = AnchoredText("", loc='upper right', prop=dict(size=9), frameon=True, bbox_to_anchor=(1, 1))
ax.add_artist(leaderboard_box)

# Determine animation frame count
max_frames = max(len(d['x']) for d in driver_data.values())

# Update function
def update(frame):
    current_states = []

    for drv, d in driver_data.items():
        if frame < len(d['x']):
            # Driver is active
            x, y = d['x'][frame], d['y'][frame]
            d['dot'].set_data(x, y)
            d['label'].set_position((x, y + 1.5))

            # Get current lap/compound
            current_time = d['time'][frame]
            lap_df = session.laps.pick_drivers(drv)
            current_lap = lap_df[lap_df['Time'] <= pd.to_timedelta(current_time, unit='s')].sort_values('Time').tail(1)

            compound = current_lap['Compound'].values[0] if not current_lap.empty else "Unknown"
            lap_number = current_lap['LapNumber'].values[0] if not current_lap.empty else 0

            current_states.append({
                'abbr': d['abbr'],
                'distance': current_time,
                'tyre': compound,
                'lap': lap_number,
                'status': 'Running'
            })

        else:
            # DNF: hide dot and label
            d['dot'].set_data([], [])
            d['label'].set_position((0, 0))

            current_states.append({
                'abbr': d['abbr'],
                'distance': float('-inf'),
                'tyre': '',
                'lap': '',
                'status': 'DNF'
            })

    # Sort by distance (active drivers first)
    sorted_states = sorted(current_states, key=lambda x: -x['distance'])

    # Determine current lap
    active_laps = [s['lap'] for s in sorted_states if s['status'] == 'Running' and isinstance(s['lap'], (int, np.integer))]
    current_lap_display = max(active_laps) if active_laps else '?'

    # Format leaderboard text
    leaderboard_text = f"Lap {current_lap_display} / {total_laps}\n"
    for i, s in enumerate(sorted_states):
        if s['status'] == 'DNF':
            leaderboard_text += f"{i+1}. {s['abbr']} (DNF)\n"
        else:
            leaderboard_text += f"{i+1}. {s['abbr']} ({s['tyre']})\n"

    leaderboard_box.txt.set_text(leaderboard_text)

    return [d['dot'] for d in driver_data.values()] + [d['label'] for d in driver_data.values()] + [leaderboard_box]

# Animate
anim = animation.FuncAnimation(fig, update, frames=max_frames, interval=15, blit=True)
plt.show()

# Save (optional)
# anim.save("abu_dhabi_2021_race.mp4", fps=60, dpi=200)

