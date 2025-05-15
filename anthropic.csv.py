import pandas as pd
import numpy as np
import csv


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
                top_seven.append(data[j][i])

        # Extract bottom 3 predictions (rows 10-12)
        for j in range(10, 13):
            if j < len(data) and i < len(data[j]):
                bottom_three.append(data[j][i])

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


def calculate_scores(predictions, results):
    """Calculate scores based on the provided rules."""
    scores = {}

    for contestant, prediction in predictions.items():
        score = 0

        # Get actual results
        actual_top_seven = results['top_seven']
        actual_bottom_three = results['relegated'] + [results['bottom']]

        # 1 point for predicting the champions correctly
        if prediction['top_seven'] and prediction['top_seven'][0] == actual_top_seven[0]:
            score += 1

        # Points for correctly predicting teams in the top positions
        # For each tier (top 2, top 3, etc.), check if teams are in that tier

        # 1 point for each team in top 2 that was predicted in any order in top 2
        for team in prediction['top_seven'][:2]:
            if team in actual_top_seven[:2]:
                score += 1

        # 1 point for each team in top 3 that was predicted in any order in top 3
        for team in prediction['top_seven'][:3]:
            if team in actual_top_seven[:3]:
                score += 1

        # 1 point for each team in top 4 that was predicted in any order in top 4
        for team in prediction['top_seven'][:4]:
            if team in actual_top_seven[:4]:
                score += 1

        # 1 point for each team in top 5 that was predicted in any order in top 5
        for team in prediction['top_seven'][:5]:
            if team in actual_top_seven[:5]:
                score += 1

        # 1 point for each team in top 6 that was predicted in any order in top 6
        for team in prediction['top_seven'][:6]:
            if team in actual_top_seven[:6]:
                score += 1

        # 1 point for each team in top 7 that was predicted in any order in top 7
        for team in prediction['top_seven']:
            if team in actual_top_seven:
                score += 1

        # 1 point for each team in bottom 3 that was predicted in any order
        for team in prediction['bottom_three']:
            if team in actual_bottom_three:
                score += 1

        # 1 point for bottom being correct in addition to the points for being in the bottom 3
        if prediction['bottom_three'] and prediction['bottom_three'][-1] == results['bottom']:
            score += 1

        scores[contestant] = score

    return scores


def main():
    # Load predictions, final results, and expected scores
    predictions = load_predictions('predictions1.csv')
    results = load_final_results('final1.csv')
    expected_scores = load_expected_scores('expected1.csv')

    # Calculate scores
    calculated_scores = calculate_scores(predictions, results)

    # Print calculated scores
    print("Calculated Scores:")
    for contestant, score in calculated_scores.items():
        print(f"{contestant}: {score}")

    # Compare with expected scores
    print("\nScore Verification:")
    all_match = True
    for contestant, expected_score in expected_scores.items():
        calculated_score = calculated_scores.get(contestant, None)
        match = calculated_score == expected_score
        if not match:
            all_match = False
        print(f"{contestant}: Calculated={calculated_score}, Expected={expected_score}, Match={match}")

    print(f"\nAll scores match expected values: {all_match}")


if __name__ == "__main__":
    main()