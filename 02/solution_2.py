"""2022, day 2, part 2: https://adventofcode.com/2022/day/2."""
import pathlib


def solution(filepath: pathlib.Path) -> int:

    with open(filepath, "r") as f:
        my_list = f.read().splitlines()
        opponent = [x[0] for x in my_list]
        player = [x[-1] for x in my_list]

    # Check inputs
    assert len(player) == len(opponent)
    assert all([x in ["A", "B", "C"] for x in opponent])
    assert all([x in ["X", "Y", "Z"] for x in player])

    # Initialize useful variables
    n = len(player)
    result_score_dict = {"X": 0, "Y": 3, "Z": 6}
    base_score_dict = {
        "A": {
            "X": 3,  # Opponent plays rock, we need to loose -> Scissors (3)
            "Y": 1,  # Opponent plays rock, we need to draw -> Rock (1)
            "Z": 2,  # Opponent plays rock, we need to win -> Paper (2)
        },
        "B": {
            "X": 1,  # Opponent plays paper, we need to loose -> Rock (1)
            "Y": 2,  # Opponent plays paper, we need to draw -> Paper (2)
            "Z": 3,  # Opponent plays paper, we need to win -> Scissors (3)
        },
        "C": {
            "X": 2,  # Opponent plays scissors, we need to loose -> Paper (2)
            "Y": 3,  # Opponent plays scissors, we need to draw -> Scissors (3)
            "Z": 1,  # Opponent plays scissors, we need to win -> Rock (1)
        },
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

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 14610

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 12
    assert solution(filepath) == expected
