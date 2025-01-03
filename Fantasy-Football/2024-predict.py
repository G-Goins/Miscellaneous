import pandas as pd
import numpy as np

data = pd.read_csv('/Users/grantgoins/Desktop/Miscellaneous/Fantasy-Football/offense_yearly_data.csv')
data_2023 = data[data['season'] == 2023]

# Replace 'inf' with NaN
data_2023['ppr_fp_ps'].replace([np.inf, -np.inf], np.nan, inplace=True)

# Drop rows with NaN values in 'ppr_fp_ps'
cleaned_data_2023 = data_2023.dropna(subset=['ppr_fp_ps'])

# Ensure the column is numeric
cleaned_data_2023['ppr_fp_ps'] = pd.to_numeric(cleaned_data_2023['ppr_fp_ps'])

# Now you can sort the cleaned data
sorted_data_2023 = cleaned_data_2023.sort_values(by='ppr_fp_ps', ascending=False)

# Simulate the draft
def simulate_draft(sorted_data, num_rounds=16, min_players=12):
    draft_order = list(range(1, 13))  # 12 teams in the league
    team_picks = []
    total_teams = len(draft_order)
    pick_position = 5  # Your draft position

    # Positional requirements
    required_positions = {
        'QB': 2,
        'RB': 3,
        'WR': 3,
        'TE': 2
    }
    position_counts = {
        'QB': 0,
        'RB': 0,
        'WR': 0,
        'TE': 0
    }

    for round_num in range(1, num_rounds + 1):
        if round_num % 3 == 0:  # Third-round reversal
            draft_order.reverse()

        available_players = sorted_data.copy()
        
        # Prioritize WRs if positional minimums are met
        if all(position_counts[pos] >= req for pos, req in required_positions.items()):
            available_players = available_players[available_players['position'] == 'WR']
        else:
            # Filter players to ensure minimum requirements are met
            for position, min_required in required_positions.items():
                if position_counts[position] < min_required:
                    # Filter to only include players of this position
                    available_players = available_players[available_players['position'] == position]
                    break

        # Calculate the index of the player you would pick based on the draft position
        current_pick_index = (round_num - 1) * total_teams + pick_position - 1

        # Ensure there are enough players left
        if len(available_players) > current_pick_index:
            pick = available_players.iloc[current_pick_index]
            team_picks.append(pick)

            # Update position counts
            position_counts[pick['position']] += 1

            # Remove players picked by other teams before your turn
            sorted_data = sorted_data.drop(sorted_data.index[:current_pick_index + 1])
        else:
            print(f"Not enough players left to pick in round {round_num}.")
            break

        # Stop if you have drafted at least 12 players
        if len(team_picks) >= min_players:
            break

    return team_picks

# Run multiple simulations
def run_simulations(sorted_data, num_simulations=1000):
    all_picks = []

    for _ in range(num_simulations):
        sorted_data_copy = sorted_data.copy()  # Ensure each simulation is independent
        simulation_result = simulate_draft(sorted_data_copy)
        all_picks.append(simulation_result)

    return all_picks

# Analyze the simulation results
def analyze_simulations(all_simulations):
    pick_counts = {}

    for simulation in all_simulations:
        for pick in simulation:
            player_name = pick['name']
            if player_name in pick_counts:
                pick_counts[player_name] += 1
            else:
                pick_counts[player_name] = 1

    # Sort players by how often they were picked in the simulations
    sorted_picks = sorted(pick_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_picks

# Example usage with 2023 data:
all_simulations_2023 = run_simulations(sorted_data_2023)
best_picks_2023 = analyze_simulations(all_simulations_2023)

# Display the best picks
for player, count in best_picks_2023:
    print(f"{player}: picked {count} times")