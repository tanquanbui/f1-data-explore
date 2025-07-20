# verstappen_wdc_scenarios.py
import fastf1
from fastf1.ergast import Ergast

SEASON = 2025
ROUND = 12  # After British GP
TOTAL_ROUNDS = 24
REMAINING_ROUNDS = TOTAL_ROUNDS - ROUND
MAX_POINTS_PER_RACE = 25
def get_driver_standings(season, round_):
    ergast = Ergast()
    response = ergast.get_driver_standings(season, round_)

    if len(response) == 0:
        raise ValueError("No standings data found.")

    standings = response.iloc[0]

    print(f"\nTop drivers after Round {round_}:")
    for entry in standings[:10]:
        name = entry.driver['familyName']
        points = float(entry.points)
        print(f"{name}: {points} pts")

    return {entry.driver['familyName']: float(entry.points) for entry in standings}

def simulate_wdc_scenarios():
    current = get_driver_standings(SEASON, ROUND)

    # Extract only the contenders
    try:
        verstappen_current = current['Verstappen']
        norris_current = current['Norris']
        piastri_current = current['Piastri']
    except KeyError:
        raise KeyError("Could not find one of the required drivers: Verstappen, Norris, or Piastri")

    max_points_remaining = REMAINING_ROUNDS * MAX_POINTS_PER_RACE
    results = {}

    print("\nSimulating Verstappen win scenarios...")
    for verstappen_points_earned in range(max_points_remaining, 180, -10):  # explore from perfect to 180
        verstappen_total = verstappen_current + verstappen_points_earned

        norris_required = verstappen_total - norris_current - 1
        piastri_required = verstappen_total - piastri_current - 1

        scenario = 'Possible' if norris_required <= max_points_remaining and piastri_required <= max_points_remaining else 'Unlikely'

        results[verstappen_points_earned] = {
            'Verstappen Total': verstappen_total,
            'Norris Max Allowed': round(norris_required, 1),
            'Piastri Max Allowed': round(piastri_required, 1),
            'Scenario': scenario
        }

    return results

if __name__ == '__main__':
    scenarios = simulate_wdc_scenarios()
    print("\nVerstappen WDC Scenarios (Points earned in last 12 races):")
    for pts, data in scenarios.items():
        print(f"\n✅ Verstappen earns {pts} pts → Total = {data['Verstappen Total']}")
        print(f"   ⛔ Norris must score ≤ {data['Norris Max Allowed']} pts")
        print(f"   ⛔ Piastri must score ≤ {data['Piastri Max Allowed']} pts")
        print(f"   📌 Scenario: {data['Scenario']}")

