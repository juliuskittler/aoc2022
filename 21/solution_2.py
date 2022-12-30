"""2022, day 21, part 2.

- Initially, we need to understand which of the 2 monkeys in the root operation can be
influenced by what the human 'humn' says. The monkey that cannot be influenced is fixed.
We can compute the number for this monkey as before with our recursive get_number
function. This number will be our 'target'. The other monkey that can be influenced is
variable. It's number will be our 'x' that we need to find.
- For the monkey that is variable, we recursively compute the 'x' (which will then
become the new target during the next recursion step) until we have reached 'humn'.
"""


import pathlib
from typing import Dict

from utils import get_action_dict


class Solution:
    def __init__(self, action_dict: Dict, verbose: bool = False):
        self.action_dict = action_dict
        self.verbose = verbose

    def get_solution(self) -> int:
        """Main function to return the solution for the problem."""
        # Find out which monkey is dependent on humn. This also adds the dependency
        # information for each monkey to our action_dict.
        dependent_mky_l = self._is_dependent_on_humn(self.action_dict["root"]["mky_l"])
        dependent_mky_r = self._is_dependent_on_humn(self.action_dict["root"]["mky_r"])

        # Get the value that should be returned by the monkey which is dependent on humn
        if dependent_mky_l:
            target = self._get_number(self.action_dict["root"]["mky_r"])
            _ = self._get_number(
                self.action_dict["root"]["mky_l"]
            )  # run this for later
            dependent_mky = self.action_dict["root"]["mky_l"]
        elif dependent_mky_r:
            target = self._get_number(self.action_dict["root"]["mky_l"])
            _ = self._get_number(
                self.action_dict["root"]["mky_r"]
            )  # run this for later
            dependent_mky = self.action_dict["root"]["mky_r"]

        if self.verbose:
            print("Target: {}".format(target))

        # Find number that humn has to say in order to make the monkey that is dependent
        # on humn return the same value as the monkey that is not dependent on humn.
        result = int(self._get_required_output(target, dependent_mky))
        return result

    def _is_dependent_on_humn(self, monkey: str) -> bool:
        """Auxilary function to find out if the input monkey is dependent on humn.

        This function also adds the dependency information to our action_dict.
        """
        # Find out if the current monkey is dependent on humn
        if monkey == "humn":
            is_dependent = True
        elif self.action_dict[monkey]["num"] is not None:
            is_dependent = False
        else:
            dependent_mky_l = self._is_dependent_on_humn(
                self.action_dict[monkey]["mky_l"]
            )
            dependent_mky_r = self._is_dependent_on_humn(
                self.action_dict[monkey]["mky_r"]
            )
            is_dependent = dependent_mky_l or dependent_mky_r

        # Add dependency information to our action_dict
        self.action_dict[monkey]["is_dependent"] = is_dependent
        return is_dependent

    def _get_number(self, monkey: str) -> int:
        """Auxilary function go get the number for a particular monkey.

        This function works recursively and returns the number regardless of whether
        an operation needs to be conducted or if the number for the monkey is directly
        available. This function also adds the number information to our action_dict.
        """
        if self.action_dict[monkey]["num"] is not None:
            number = self.action_dict[monkey]["num"]
        else:
            number_mky_l = self._get_number(self.action_dict[monkey]["mky_l"])
            number_mky_r = self._get_number(self.action_dict[monkey]["mky_r"])
            operator = self.action_dict[monkey]["operator"]
            if operator == "+":
                number = number_mky_l + number_mky_r
            elif operator == "*":
                number = number_mky_l * number_mky_r
            elif operator == "-":
                number = number_mky_l - number_mky_r
            elif operator == "/":
                number = number_mky_l / number_mky_r

            # Add number information to our action_dict if it was computed
            self.action_dict[monkey]["num"] = number

        return number

    def _get_required_output(self, target: int, monkey: str) -> int:

        # Find out which of the two monkeys is dependent on humn. Only one of the
        # monkeys can be dependent on humn.
        mky_l = self.action_dict[monkey]["mky_l"]
        mky_r = self.action_dict[monkey]["mky_r"]
        dependent_mky_l = self.action_dict[mky_l]["is_dependent"]
        dependent_mky_r = self.action_dict[mky_r]["is_dependent"]

        # We keep the number of the monkey that is not dependent on humn as fixed.
        if dependent_mky_l:
            dependent_mky = mky_l
            fixed_num = self.action_dict[mky_r]["num"]
        elif dependent_mky_r:
            fixed_num = self.action_dict[mky_l]["num"]
            dependent_mky = mky_r
        else:
            print(self.action_dict[monkey])

        # Compute the new target depending on the operation
        if self.action_dict[monkey]["operator"] == "+":  # order does not matter
            new_target = target - fixed_num
            if self.verbose:
                print("{}: {} = {} - {} ".format(mky_r, new_target, target, fixed_num))
        elif self.action_dict[monkey]["operator"] == "*":  # order does not matter
            new_target = target / fixed_num
            if self.verbose:
                print("{}: {} = {} / {} ".format(mky_r, new_target, target, fixed_num))
        elif self.action_dict[monkey]["operator"] == "-":  # order does matter
            if dependent_mky_l:
                new_target = fixed_num + target
                if self.verbose:
                    print(
                        "{}: {} = {} + {} ".format(mky_l, new_target, fixed_num, target)
                    )
            elif dependent_mky_r:
                new_target = fixed_num - target
                if self.verbose:
                    print(
                        "{}: {} = {} + {} ".format(mky_r, new_target, fixed_num, target)
                    )
        elif self.action_dict[monkey]["operator"] == "/":  # order does matter
            if dependent_mky_l:
                new_target = target * fixed_num
                if self.verbose:
                    print(
                        "{}: {} = {} * {} ".format(mky_l, new_target, target, fixed_num)
                    )
            elif dependent_mky_r:
                new_target = target / fixed_num
                if self.verbose:
                    print(
                        "{}: {} = {} / {} ".format(mky_r, new_target, target, fixed_num)
                    )

        # If the dependent monkey is humn, return its result
        if dependent_mky == "humn":
            return new_target
        # Else, keep recursing until we reach humn
        else:
            return self._get_required_output(new_target, dependent_mky)


if __name__ == "__main__":

    filepath = pathlib.Path("21/input.txt")
    action_dict = get_action_dict(filepath)

    print(Solution(action_dict).get_solution())  # correct:

    # Test 1
    filepath = pathlib.Path("21/input_test_1.txt")
    action_dict_test = get_action_dict(filepath)
    expected = 301
    assert Solution(action_dict_test).get_solution() == expected
