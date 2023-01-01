"""2022, day 25, part 1: https://adventofcode.com/2022/day/25."""
import pathlib


def snafu_to_decimal(snafu: str) -> int:
    """Auxilary function to convert snafu to decimal."""
    assert type(snafu) == str

    # Initialize useful variables
    snafu_rev = reversed(snafu)
    decimal = 0

    # Iterate through each position in snafu string from right to left (small to large)
    for i, val in enumerate(snafu_rev):
        factor = 5 ** (i)  # 5 to the power of i
        if val == "-":
            decimal = decimal - 1 * factor
        elif val == "=":
            decimal = decimal - 2 * factor
        else:
            decimal = decimal + int(val) * factor

    return decimal


def decimal_to_snafu(decimal: int) -> str:
    """Auxilary function to convert decimal to snafu."""
    assert type(decimal) == int

    # Find the starting point, the largest required power of 5.
    # If we divide the decimal with 5 ^ (largest required power of 5), the result should
    # be smaller or equal 2 as 2 is the largest factor that we have in the snafu system.
    start_reached = False
    max_power_of_base_5 = -1
    while not start_reached:
        max_power_of_base_5 += 1
        if decimal / (5**max_power_of_base_5) <= 2:
            start_reached = True

    # We start by finding the large snafu digits, working ourselves from left to right
    snafu = []  # represent snafu as a list of its digits
    decimal_sum = 0

    for power_of_base_5 in range(max_power_of_base_5, -1, -1):

        max_remaining_sum = sum([2 * (5**pwr) for pwr in range(power_of_base_5)])
        decimal_delta = decimal - decimal_sum

        # Increase value if current decimal is smaller than needed
        if decimal_delta > 0:
            if max_remaining_sum >= decimal_delta:
                snafu.append("0")
            elif (decimal_delta - max_remaining_sum) / (5**power_of_base_5) <= 1:
                snafu.append("1")
                decimal_sum += 5**power_of_base_5
            elif (decimal_delta - max_remaining_sum) / (5**power_of_base_5) <= 2:
                snafu.append("2")
                decimal_sum += 2 * (5**power_of_base_5)
        # Decrease value if current decimal is larger than needed
        elif decimal_delta < 0:
            if max_remaining_sum >= abs(decimal_delta):
                snafu.append("0")
            elif (decimal_delta + max_remaining_sum) / (5**power_of_base_5) >= -1:
                snafu.append("-")
                decimal_sum -= 5**power_of_base_5
            elif (decimal_delta + max_remaining_sum) / (5**power_of_base_5) >= -2:
                snafu.append("=")
                decimal_sum -= 2 * (5**power_of_base_5)
        else:
            snafu.append("0")

    # Remove trailing 0s at the beginning and return result
    i = 0
    while snafu[i] == "0":
        i += 1
    snafu = snafu[i:]

    # Return snafu as string
    snafu_str = "".join(snafu)
    return snafu_str


def solution(filepath: pathlib.Path) -> str:

    with open(filepath, "r") as f:
        snafu_list = f.read().splitlines()

    # Convert all snafu values to decimal values and sum them up
    decimal = sum([snafu_to_decimal(snafu) for snafu in snafu_list])

    # Convert sum of decimal values to snafu value
    snafu = decimal_to_snafu(decimal)
    return snafu


if __name__ == "__main__":

    dirpath = pathlib.Path(__file__).parent.resolve()

    # Puzzle
    filepath = dirpath / "input.txt"
    print(solution(filepath))  # correct: 2-=2==00-0==2=022=10

    # Test case 1
    filepath = dirpath / "input_test_1.txt"
    expected = "2=-1=0"
    assert solution(filepath) == expected

    # Test cases for auxilary functions
    snafu_list = [
        "1",
        "2",
        "1=",
        "1-",
        "10",
        "11",
        "12",
        "2=",
        "2-",
        "20",
        "1=0",
        "1-0",
        "1=11-2",
        "1-0---0",
        "1121-1110-1=0",
    ]
    decimal_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 2022, 12345, 314159265]
    matches = [snafu_to_decimal(s) == d for s, d in zip(snafu_list, decimal_list)]
    assert all
    assert all([decimal_to_snafu(d) == s for s, d in zip(snafu_list, decimal_list)])

    snafu_list = [
        "1=-0-2",
        "12111",
        "2=0=",
        "21",
        "2=01",
        "111",
        "20012",
        "112",
        "1=-1=",
        "1-12",
        "12",
        "1=",
        "122",
    ]
    decimal_list = [1747, 906, 198, 11, 201, 31, 1257, 32, 353, 107, 7, 3, 37]
    assert all([snafu_to_decimal(s) == d for s, d in zip(snafu_list, decimal_list)])
    assert all([decimal_to_snafu(d) == s for s, d in zip(snafu_list, decimal_list)])
