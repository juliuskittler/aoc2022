import pathlib
import re
from typing import Dict


def get_monkey_dict(filepath: pathlib.Path) -> Dict:
    with open(filepath, "r") as f:
        lines = f.read().splitlines()
        lines = [line.strip() for line in lines]

    monkey_dict = dict()
    for line in lines:
        if line.startswith("Monkey "):
            current_monkey = int(re.findall(r"\d+", line)[0])
            monkey_dict[current_monkey] = dict()
        elif line.startswith("Starting items: "):
            items = [int(item) for item in re.findall(r"\d+", line)]
            monkey_dict[current_monkey]["items"] = items
        elif line.startswith("Operation: "):
            # We assume that there is only "*" or "+"
            if "+" in line:
                operator = "+"
            elif "*" in line:
                operator = "*"
            else:
                raise ValueError
            monkey_dict[current_monkey]["op_operator"] = operator
            # We assume that if there is no number, we multiply or sum
            # with 'old'. E.g.: 'old + old' or 'old * old'.
            number = re.findall(r"\d+", line)
            if len(number) == 0:
                number = "old"
            elif len(number) == 1:
                number = int(number[0])
            else:
                raise ValueError
            monkey_dict[current_monkey]["op_number"] = number
        elif line.startswith("Test: "):
            # We assume that the test always checks for divisibility
            if not "divisible" in line:
                raise ValueError
            else:
                divisor = int(re.findall(r"\d+", line)[0])
                monkey_dict[current_monkey]["test_divisor"] = divisor
        elif line.startswith("If true: "):
            target = int(re.findall(r"\d+", line)[0])
            monkey_dict[current_monkey]["test_true_target"] = target
        elif line.startswith("If false: "):
            target = int(re.findall(r"\d+", line)[0])
            monkey_dict[current_monkey]["test_false_target"] = target

    return monkey_dict
