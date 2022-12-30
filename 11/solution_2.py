"""2022, day 11, part 2: https://adventofcode.com/2022/day/11.

- The main concern here is overflow. The worry levels of the items get HUGE!
- Hence, we need to store the worry level more efficiently.
- Ultimately, the only aspect that matters is the divisibility.
- If we take a look at the divisors, we notice that all of them are prime numbers:
    - Test input: 23, 19, 13, 17
    - Problem input: 13, 19, 11, 17, 3, 7, 5, 2
- Prime numbers are whole numbers greater than 1 that cannot be exactly divided by any
whole number other than itself and 1.
- This means that the least common multiple (LCM) of a list of prime numbers is simply
the product of all the prime numbers in the list.
- If we take the modulo of an item's worry level with the LCM, we maintain the
divisibility with all of the prime numbers.
"""

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
    n_rounds = 10000
    n_monkeys = len(monkey_dict)
    inspected_items_per_monkey = [0 for _ in range(n_monkeys)]

    # Compute least common multiple of the test divisors
    lcm = 1
    for monkey_idx in monkey_dict.keys():
        test_divisor = monkey_dict[monkey_idx]["test_divisor"]
        lcm *= test_divisor

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

                # Divide by LCM
                new_item = new_item % lcm

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
        # print_round_idx = [0, 19, 999, 1999, 2999, 3999, 4999, 7999, 8999, 8999, 9999]
        # if round_idx in print_round_idx:
        #     print("\nRound: {}".format(round_idx+1))
        #     print(inspected_items_per_monkey)

    # Compute the 'level of monkey business'
    inspected_items_per_monkey.sort()
    lomb = inspected_items_per_monkey[-1] * inspected_items_per_monkey[-2]
    return lomb


if __name__ == "__main__":

    filepath = pathlib.Path("11/input.txt")
    monkey_dict = get_monkey_dict(filepath)
    print(solution(monkey_dict))  # correct: 19457438264

    # Test 1
    filepath = pathlib.Path("11/input_test_1.txt")
    monkey_dict_test = get_monkey_dict(filepath)
    expected = 2713310158
    assert solution(monkey_dict_test) == expected
