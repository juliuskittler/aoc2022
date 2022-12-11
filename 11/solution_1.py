import copy
import pathlib
from typing import Dict

from utils import get_monkey_dict


def solution(monkey_dict: Dict) -> int:
    # Required so that the input outside this function remains the same even if we
    # call the function. After using copy.deepcopy, we can call the function multiple
    # times with the same 'monkey_dict' input and the output will always be the same
    monkey_dict = copy.deepcopy(monkey_dict)

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

    filepath = pathlib.Path("11/input.txt")
    monkey_dict = get_monkey_dict(filepath)
    print(solution(monkey_dict))  # correct: 110220

    # Test 1
    filepath = pathlib.Path("11/input_test_1.txt")
    monkey_dict_test = get_monkey_dict(filepath)
    expected = 10605
    assert solution(monkey_dict_test) == expected
