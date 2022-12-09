"""2022, Day 2, Part 1"""
import pathlib
from typing import List


def solution(opponent: List[str], player: List[str]) -> int:
    # Check inputs
    assert len(player) == len(opponent)
    assert all([x in ["A", "B", "C"] for x in opponent])
    assert all([x in ["X", "Y", "Z"] for x in player])

    # Initialize useful variables
    n = len(player)
    base_score_dict = {"X": 1, "Y": 2, "Z": 3}
    result_score_dict = {
        "A": {
            "X": 3,  # draw (Rock, Rock)
            "Y": 6,  # win  (Rock, Paper) -> paper wins (you)
            "Z": 0,  # loss (Rock, Scissors) -> rock wins (opponent)
        },
        "B": {
            "X": 0,  # loss (Paper, Rock) -> paper wins (opponent)
            "Y": 3,  # draw (Paper, Paper)
            "Z": 6,  # win  (Paper, Scissors) -> scissors wins (you)
        },
        "C": {
            "X": 6,  # win (Scissors, Rock) -> rock wins (you)
            "Y": 0,  # loss (Scissors, Paper) -> scissors wins (opponent)
            "Z": 3,  # draw (Scissors, Scissors)
        },
    }
    total_score = 0

    # Iterate through all games, compute their scores and sum them up
    for i in range(n):

        # Compute the score of the current game
        result_score = result_score_dict[opponent[i]][player[i]]
        base_score = base_score_dict[player[i]]
        score = base_score + result_score

        # Compute the sum of the scores across all games
        total_score += score

    return total_score


if __name__ == "__main__":

    # Input data
    filepath = pathlib.Path("02/input.txt")
    with open(filepath, "r") as f:
        my_list = f.read().splitlines()
        opponent = [x[0] for x in my_list]
        player = [x[-1] for x in my_list]

    # Result
    print(solution(opponent, player))  # correct: 9241

    # Test 1
    opponent_test = ["A", "B", "C"]
    player_test = ["Y", "X", "Z"]
    expected = 15  # (6+2) + (0+1) + (3+3)
    assert solution(opponent_test, player_test) == expected

    # Test 2
    opponent_test = ["A", "B", "C"]
    player_test = ["X", "Y", "Z"]
    expected = 15  # (3+1) + (3+2) + (3+3)
    assert solution(opponent_test, player_test) == expected

    # Test 3
    opponent_test = ["A", "B", "C"]
    player_test = ["Z", "Z", "Z"]
    expected = 18  # (6+3) + (0+3) + (3+3)
    assert solution(opponent_test, player_test) == expected
