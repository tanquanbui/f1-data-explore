## Formula 1 Championship Tools (2021–2025)

This repository contains two Python tools powered by FastF1 for simulating and visualizing Formula 1 races and championship scenarios:

1. WDC Scenarios Simulator – Calculates how Max Verstappen can still win the 2025 World Drivers’ Championship.
2. Abu Dhabi 2021 Race Animation – Animates the iconic 2021 Abu Dhabi Grand Prix using real telemetry and lap data.

## Project Structure

.
├── cache/                        # FastF1 cache directory (auto-created)
├── verstappen_wdc_scenarios.py  # 2025 WDC simulation for Verstappen
├── abu_dhabi_2021_race.py       # 2021 race animation using telemetry
└── README.md

## Requirements

Install all dependencies:

    pip install fastf1 matplotlib pandas numpy

## Script 1: Verstappen WDC Scenario Simulator

File: verstappen_wdc_scenarios.py

This script simulates scenarios in which Max Verstappen can become the 2025 World Champion after Round 12 (British GP), based on his performance in the remaining 12 races.

What It Does:
- Fetches 2025 season standings after Round 12 using Ergast API.
- Calculates Verstappen's possible point totals from the remaining races.
- Determines how many points his main rivals (Norris, Piastri) can score without surpassing him.
- Labels scenarios as 'Possible' or 'Unlikely'.

To Run:

    python verstappen_wdc_scenarios.py

Example output:

    ✅ Verstappen earns 250 pts → Total = 495.0
       ⛔ Norris must score ≤ 289.0 pts
       ⛔ Piastri must score ≤ 284.0 pts
       📌 Scenario: Possible

## Script 2: Abu Dhabi 2021 Race Animation

File: abu_dhabi_2021_race.py

This script animates the Abu Dhabi 2021 Grand Prix using real driver telemetry. It visualizes driver positions, tyre compounds, current laps, and DNF status on a live track map.

What It Does:
- Loads telemetry and lap data from the final 2021 race.
- Shows all drivers moving around the track in real-time.
- Updates a live leaderboard with current lap, tyre compound, and DNF info.

To Run:

    python abu_dhabi_2021_race.py

To save the animation as a video (optional), uncomment the following line in the script:

    # anim.save("abu_dhabi_2021_race.mp4", fps=60, dpi=200)

## Notes

- The 'cache/' directory will be created automatically and stores race data locally after the first fetch.
- Both scripts use FastF1, which pulls data from Ergast and F1 telemetry endpoints.
- Internet is required for the initial data fetch.

## License

MIT License – feel free to use, modify, and share.
 f1-data-explore
