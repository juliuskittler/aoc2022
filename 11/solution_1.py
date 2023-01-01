"""2022, day 11, part 1: https://adventofcode.com/2022/day/11."""

import pathlib

from utils import get_monkey_dict


def solution(filepath: pathlib.Path) -> int:

    monkey_dict = get_monkey_dict(filepath)

    # Initialize useful variables
    n_rounds = 20
    n_monkeys = len(monkey_dict)
    inspected_items_per_monkey = [0 for _ in range(n_monkeys)]

    # Let monkeys inspect and throw items for n_rounds
    for round_idx in range(n_rounds):
        for monkey_idx in monkey_dict.keys():
            for item in monkey_dict[monkey_idx]["items"]:

                # Compute new worry level due to inspection
                op_operator = monkey_dict[monkey_idx]["op_operator"]
                op_number = monkey_dict[monkey_idx]["op_number"]
                if op_number == "old":
                    op_number = item
                if op_operator == "+":
                    new_item = item + op_number
                elif op_operator == "*":
                    new_item = item * op_number

                # Compute new worry level due to monkey boredom
                new_item = new_item // 3  # using floor division (always rounding down)

                # Conduct test and send the item to the next monkey
                test_divisor = monkey_dict[monkey_idx]["test_divisor"]
                if new_item % test_divisor == 0:
                    target = monkey_dict[monkey_idx]["test_true_target"]
                else:
                    target = monkey_dict[monkey_idx]["test_false_target"]
                monkey_dict[target]["items"].append(new_item)

                # Set items of the monkey to an empty list
                monkey_dict[monkey_idx]["items"] = list()

                # Update number of inspected items of the monkey
                inspected_items_per_monkey[monkey_idx] += 1

        # # Debugging
        # print("\nRound: {}".format(round_idx+1))
        # for monkey_idx in monkey_dict.keys():
        #     print("Monkey {}: {}".format(monkey_idx, monkey_dict[monkey_idx]["items"]))

    # Compute the 'level of monkey business'
    inspected_items_per_monkey.sort()
    lomb = inspected_items_per_monkey[-1] * inspected_items_per_monkey[-2]
    return lomb


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 110220

    # Test 1
    filepath = dirpath / "input_test_1.txt"
    expected = 10605
    assert solution(filepath) == expected
