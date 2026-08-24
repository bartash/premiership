# On cygwin:
#  source C:/cygwin64/home/ac9/git/pycharm_projects/premiership/.venv/Scripts/activate
import sys

import csv

expected_teams = {
    "Arsenal",
    "Bournemouth",
    "Brentford",
    "Brighton",
    "Burnley",
    "Chelsea",
    "Everton",
    "Fulham",
    "Leeds",
    "Ipswich",
    "Leicester",
    "Liverpool",
    "Luton",
    "Man City",
    "Man Utd",
    "Newcastle",
    "Norwich City",
    "Forest",
    "Palace",
    "Sheffield United",
    "Southampton",
    "Spurs",
    "Sunderland",
    "Villa",
    "Watford",
    "West Ham",
    "Wolves",
}

def validate_team_name(team, filename):
    """Avoid bad data my checking team name is canonical
    May need to update this as teams are promoted or relegated"""
    debug(False, f"validate {team} in {filename}")
    if not team in expected_teams:
        print(f"Bad team {team} in {filename}")
        exit(1)

def load_predictions(filename):
    """Load predictions from CSV file."""
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Extract contestant names (first row)
    contestants = data[0]

    # Create a dictionary for each contestant with their predictions
    predictions = {}
    for i, contestant in enumerate(contestants):
        top_seven = []
        bottom_three = []

        # Extract top 7 predictions (rows 1-7)
        for j in range(1, 8):
            if j < len(data) and i < len(data[j]):
                team = data[j][i]
                if contestant:
                    validate_team_name(team, filename)
                top_seven.append(team)

        # Extract bottom 3 predictions (rows 10-12)
        for j in range(10, 13):
            if j < len(data) and i < len(data[j]):
                team = data[j][i]
                if contestant:
                    validate_team_name(team, filename)
                bottom_three.append(team)

        predictions[contestant] = {
            'top_seven': top_seven,
            'bottom_three': bottom_three
        }

    return predictions


def load_final_results(filename):
    """Load final results from CSV file."""
    results = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            category, team = row
            validate_team_name(team, filename)

            if category == 'Champions':
                if 'top_seven' not in results:
                    results['top_seven'] = []
                results['top_seven'].append(team)
            elif category in ['2nd', '3rd', '4th', '5th', '6th', '7th']:
                if 'top_seven' not in results:
                    results['top_seven'] = []
                results['top_seven'].append(team)
            elif category == 'relegated':
                if 'relegated' not in results:
                    results['relegated'] = []
                results['relegated'].append(team)
            elif category == 'bottom':
                results['bottom'] = team

    return results


def load_expected_scores(filename):
    """Load expected scores from CSV file."""
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Extract contestant names (first row) and scores (second row)
    contestants = data[0]
    scores = [int(score) for score in data[1]]

    # Create a dictionary mapping contestants to their expected scores
    expected_scores = {}
    for i, contestant in enumerate(contestants):
        if i < len(scores):
            expected_scores[contestant] = scores[i]

    return expected_scores


def debug(print_debug, str):
    if print_debug:
        print(str)

def calculate_scores(predictions, results, print_debug, print_summary):
    """Calculate scores based on the provided rules."""
    scores = {}

    for contestant, prediction in predictions.items():
        score = 0

        # Get actual results
        actual_top_seven = results['top_seven']
        actual_bottom_three = results['relegated'] + [results['bottom']]

        # 1 point for predicting the champions correctly
        place_1 = 0
        if prediction['top_seven'] and prediction['top_seven'][0] == actual_top_seven[0]:
            debug(print_debug, f"{contestant} successfully predicts champions {actual_top_seven[0]}")
            score += 1
            place_1 += 1
        if print_summary:
            print(f"{contestant} champions score {place_1}")

        # Points for correctly predicting teams in the top positions
        # For each tier (top 2, top 3, etc.), check if teams are in that tier

        # 1 point for each team in top 2 that was predicted in any order in top 2
        place_2 = 0
        for team in prediction['top_seven'][:2]:
            if team in actual_top_seven[:2]:
                debug(print_debug, f"{contestant} successfully predicts {team} in top 2")
                score += 1
                place_2 += 1
        if print_summary:
            print(f"{contestant} place 2 score   {place_2}")

        # 1 point for each team in top 3 that was predicted in any order in top 3
        place_3 = 0
        for team in prediction['top_seven'][:3]:
            if team in actual_top_seven[:3]:
                debug(print_debug, f"{contestant} successfully predicts {team} in top 3")
                score += 1
                place_3 += 1
        if print_summary:
            print(f"{contestant} place 3 score   {place_3}")

        # 1 point for each team in top 4 that was predicted in any order in top 4
        place_4 = 0
        for team in prediction['top_seven'][:4]:
            if team in actual_top_seven[:4]:
                debug(print_debug, f"{contestant} successfully predicts {team} in top 4")
                score += 1
                place_4 += 1
        if print_summary:
            print(f"{contestant} place 4 score   {place_4}")

        # 1 point for each team in top 5 that was predicted in any order in top 5
        place_5 = 0
        for team in prediction['top_seven'][:5]:
            if team in actual_top_seven[:5]:
                debug(print_debug, f"{contestant} successfully predicts {team} in top 5")
                score += 1
                place_5 += 1
        if print_summary:
            print(f"{contestant} place 5 score   {place_5}")

        # 1 point for each team in top 6 that was predicted in any order in top 6
        place_6 = 0
        for team in prediction['top_seven'][:6]:
            if team in actual_top_seven[:6]:
                debug(print_debug, f"{contestant} successfully predicts {team} in top 6")
                score += 1
                place_6 += 1
        if print_summary:
            print(f"{contestant} place 6 score   {place_6}")

        # 1 point for each team in top 7 that was predicted in any order in top 7
        place_7 = 0
        for team in prediction['top_seven']:
            if team in actual_top_seven:
                debug(print_debug, f"{contestant} successfully predicts {team} in top 7")
                score += 1
                place_7 += 1
        if print_summary:
            print(f"{contestant} place 7 score   {place_7}")

        # 1 point for each team in bottom 3 that was predicted in any order
        bottom_3 = 0
        for team in prediction['bottom_three']:
            if team in actual_bottom_three:
                debug(print_debug, f"{contestant} successfully predicts {team} in bottom 3")
                score += 1
                bottom_3 += 1
        if print_summary:
            print(f"{contestant} bottom 3 score  {bottom_3}")

        # 1 point for bottom being correct in addition to the points for being in the bottom 3
        last = 0
        if prediction['bottom_three'] and prediction['bottom_three'][-1] == results['bottom']:
            debug(print_debug, f"{contestant} successfully predicts {team} is bottom")
            score += 1
            last += 1
        if print_summary:
            print(f"{contestant} last    score   {last}")


        scores[contestant] = score

    return scores


def print_sorted_scores(scores):
    """Print scores in descending order (highest first)."""
    print("\nScores in Descending Order:")
    # Sort scores by value in descending order
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Print the sorted scores
    for i, (contestant, score) in enumerate(sorted_scores, 1):
        print(f"{i}. {contestant}: {score}")


def main():
    # Load predictions, final results, and expected scores
    verify(predictions__csv='predictions_2023_2024.csv', results='final_2023_2024.csv', expected='expected_2023_2024.csv')
    verify(predictions__csv='predictions_2024_2025.csv', results='final_2024_2025.csv', expected='expected_2024_2025.csv')
    verify(predictions__csv='predictions_2025_2026.csv', results='final_2025_2026.csv', expected='expected_2025_2026.csv')

    print(f"\nLoad 2024/2025")

    predictions = load_predictions('predictions_2025_2026.csv')
    results = load_final_results('final_2025_2026.csv')
    calculated_scores = calculate_scores(predictions, results, False, True)

    # Print calculated scores
    print("Calculated Scores for 2025/2026:")
    # Print scores in descending order
    print_sorted_scores(calculated_scores)


def verify(predictions__csv, results, expected):
    print_debug = False

    predictions = load_predictions(predictions__csv)
    results = load_final_results(results)
    expected_scores = load_expected_scores(expected)

    # Calculate scores
    calculated_scores = calculate_scores(predictions, results, print_debug, False)

    # Print calculated scores
    print(f"Calculated Scores for {predictions__csv}")
    for contestant, score in calculated_scores.items():
        debug(print_debug, f"{contestant}: {score}")

    # Compare with expected scores
    all_match = True
    err_str=None
    for contestant, expected_score in expected_scores.items():
        calculated_score = calculated_scores.get(contestant, None)
        match = calculated_score == expected_score
        if not match:
            all_match = False
            err_str = f"{contestant}: Calculated={calculated_score}, Expected={expected_score}, Match={match}"
        debug(print_debug, err_str)

    if not all_match:
        print("error in verification on {predictions__csv} {expected} files with results: {results}".
              format(predictions__csv=predictions__csv, expected=expected, results=results))
        print(err_str)
        sys.exit()
    print(f"All scores match expected values: {all_match}")




if __name__ == "__main__":
    main()