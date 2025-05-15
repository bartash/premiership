#  source C:/cygwin64/home/ac9/git/pycharm_projects/premiership/.venv/Scripts/activate

import pandas as pd
import io


# Provided CSV data
csv_data = """🏆,Conor,Nathan,Patrick,Google docs AI assistant,Luke,Russ,Gavin,Andrew,Mike,Little Conor
Champions,Man City,Man City,Man City,Man City,Man City,Man Utd,Arsenal,Arsenal,Man City,Man City
2nd,Arsenal,Man Utd,Arsenal,Liverpool,Man Utd,Arsenal,Man City,Man City,Liverpool,Arsenal
3rd,Liverpool,Arsenal,Liverpool,Chelsea,Arsenal,Man City,Man Utd,Liverpool,Arsenal,Man Utd
4th,Man Utd,Liverpool,Man United,Arsenal,Liverpool,Newcastle,Liverpool,Chelsea,Chelsea,Chelsea
5th,Chelsea,Newcastle,Newcastle,Man Utd,Newcastle,Chelsea,Chelsea,Man Utd,Man Utd,Liverpool
6th,Newcastle,Chelsea,Chelsea,Spurs,Aston Villa,Liverpool,Newcastle,Newcastle,Newcastle,Newcastle
7th,Spurs,Aston Villa,Aston Villa,West Ham,Chelsea,Aston Villa,Spurs,Aston Villa,Aston Villa,Brighton
,,,,,,,,,,
,,,,,,,,,,
relegated,Nottingham Forest,Everton,Nottingham Forest,Norwich City,Wolves,Burnley,Everton,Everton,Everton,Everton
relegated,Sheffield United,Sheffield United,Luton Town,Watford,Luton,Sheffield,Luton,Luton,Wolves,Sheffield United
20th,Luton,Luton,Sheffield United,Leeds United,Sheffield United,Luton,Sheffield United,Sheffield United,Luton,Luton 
"""

# Actual results
actual_results = {
    "Champions": "Man City",
    "2nd": "Arsenal",
    "3rd": "Liverpool",
    "4th": "Aston Villa",
    "5th": "Spurs",
    "6th": "Chelsea",
    "7th": "Newcastle",
    "relegated": ["Luton", "Burnley", "Sheffield United"], #Order doesn't matter for these
    "bottom": "Sheffield United"
}

# Read the CSV data into a pandas DataFrame
# Use a try-except block for robustness in reading CSV
try:
    df = pd.read_csv(io.StringIO(csv_data))
except Exception as e:
    print(f"Error reading CSV data: {e}")
    exit()

# Rename the first column to 'Prediction' for easier access
df.rename(columns={df.columns[0]: 'Prediction'}, inplace=True)

# Extract player names
players = df.columns[1:].tolist()

# Initialize scores
scores = {player: 0 for player in players}

# --- Scoring Logic ---

# 1. Actual top N teams (lists for ordered comparison where needed, sets for unordered)
actual_top_positions = [
    actual_results["Champions"],
    actual_results["2nd"],
    actual_results["3rd"],
    actual_results["4th"],
    actual_results["5th"],
    actual_results["6th"],
    actual_results["7th"]
]

# 2. Actual relegated teams (order doesn't matter, so use a set)
actual_relegated_set = set(actual_results["relegated"])


for player in players:
    player_predictions_df = df[['Prediction', player]].copy()
    player_predictions_df.set_index('Prediction', inplace=True)
    # Ensure we handle cases where a player might not have a prediction for a category
    # by converting to a dictionary with a default value (e.g., None or an empty string)
    player_predictions = player_predictions_df[player].to_dict()

    # Helper to safely get prediction
    def get_prediction(category, index=None):
        pred = player_predictions.get(category)
        if isinstance(pred, pd.Series): # Handles multiple 'relegated' rows
            try:
                return pred.iloc[index] if index is not None and index < len(pred) else (pred.iloc[0] if index is None and len(pred)>0 else None) # return first if no index and series is not empty
            except IndexError:
                return None
        return pred

    # --- Top 7 Scoring ---
    # 1 point for predicting the champions correctly
    if get_prediction('Champions') == actual_results["Champions"]:
        scores[player] += 1

    # 1 point for each of top N that were predicted in any order (N=2 to 7)
    predicted_top_n_teams = []
    for i, pos_key in enumerate(["Champions", "2nd", "3rd", "4th", "5th", "6th", "7th"]):
        predicted_team = get_prediction(pos_key)
        if predicted_team: # Only add if a prediction was made
             predicted_top_n_teams.append(predicted_team)

        if i >= 1: # For top 2, top 3, ..., top 7
            actual_slice = set(actual_top_positions[:i+1])
            predicted_slice = set(predicted_top_n_teams[:i+1]) # Use current list of predicted teams
            scores[player] += len(actual_slice.intersection(predicted_slice))


    # --- Relegation Scoring ---
    predicted_relegated_teams_list = []
    # The CSV has two 'relegated' rows and one '20th' row.
    # We need to extract these carefully.
    relegated_preds = player_predictions.get('relegated')
    if isinstance(relegated_preds, pd.Series):
        for team in relegated_preds:
            if pd.notna(team) and team:
                 predicted_relegated_teams_list.append(team)
    elif pd.notna(relegated_preds) and relegated_preds: # If it's a single value (should not happen with current CSV structure but good for safety)
        predicted_relegated_teams_list.append(relegated_preds)

    bottom_pred = get_prediction('20th')
    if pd.notna(bottom_pred) and bottom_pred:
        predicted_relegated_teams_list.append(bottom_pred)

    # Ensure unique teams if a player somehow predicted the same team in multiple relegation slots
    predicted_relegated_set = set(predicted_relegated_teams_list)


    # 1 point for each of bottom 3 that were predicted in any order
    correct_relegated_predictions = len(predicted_relegated_set.intersection(actual_relegated_set))
    scores[player] += correct_relegated_predictions

    # 1 point for bottom being correct
    if get_prediction('20th') == actual_results["bottom"]:
        scores[player] += 1

# Print the scores
print("--- Final Scores ---")
# Sort scores dictionary by value (score) in descending order
sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
for player_name, score in sorted_scores:
    print(f"{player_name}: {score} points")
