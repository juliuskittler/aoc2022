"""2022, Day 2, Part 2"""
from typing import List
import pathlib

def solution(opponent: List, player: List) -> int:
    # Check inputs
    assert len(player) == len(opponent)
    assert all([x in ["A", "B", "C"] for x in opponent])
    assert all([x in ["X", "Y", "Z"] for x in player])

    # Initialize useful variables
    n = len(player)
    result_score_dict = {"X": 0, "Y": 3, "Z": 6}
    base_score_dict = {
        "A": {
            "X": 3, # Opponent plays rock, we need to loose -> Scissors (3)
            "Y": 1, # Opponent plays rock, we need to draw -> Rock (1)
            "Z": 2  # Opponent plays rock, we need to win -> Paper (2)
        }, 
        "B": {
            "X": 1, # Opponent plays paper, we need to loose -> Rock (1)
            "Y": 2, # Opponent plays paper, we need to draw -> Paper (2)
            "Z": 3  # Opponent plays paper, we need to win -> Scissors (3)
        }, 
        "C": {
            "X": 2, # Opponent plays scissors, we need to loose -> Paper (2)
            "Y": 3, # Opponent plays scissors, we need to draw -> Scissors (3)
            "Z": 1  # Opponent plays scissors, we need to win -> Rock (1)
        }
    }
    total_score = 0

    # Iterate through all games, compute their scores and sum them up
    for i in range(n):
        
        # Compute the score of the current game
        result_score = result_score_dict[player[i]]
        base_score = base_score_dict[opponent[i]][player[i]] 
        score = base_score + result_score
        
        # Compute the sum of the scores across all games
        total_score += score

    return total_score


if __name__ == "__main__":
    
    # Input data
    filepath = pathlib.Path("02/input.txt")
    with open(filepath) as f:
        my_list  = f.read().splitlines() 
        opponent = [x[0] for x in my_list]
        player   = [x[-1] for x in my_list]
        
    # Result
    print(solution(opponent, player)) # correct: 14610

    # Test 1
    opponent_test = ["A", "B", "C"]
    player_test = ["Y", "X", "Z"]
    expected = 12
    assert solution(opponent_test, player_test) == expected

    # Test 2
    opponent_test = ["A", "B", "C"]
    player_test = ["X", "Y", "Z"]
    expected = 15 # (0+3) + (3+2) + (6+1)
    assert solution(opponent_test, player_test) == expected

    # Test 3
    opponent_test = ["A", "B", "C"]
    player_test = ["Z", "Z", "Z"]
    expected = 24 # (6+1) + (6+2) + (6+3)
    assert solution(opponent_test, player_test) == expected