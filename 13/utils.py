import ast
import copy
import pathlib
from typing import List


def get_lists(filepath: pathlib.Path) -> List[List[int]]:
    """Auxilary function to get the required data in listformats.

    A list of lists is returned. The logic to pair every other two lists will be
    implemented later on.
    """
    with open(filepath, "r") as f:
        data = f.read().splitlines()
        lists = [ast.literal_eval(row) for row in data if row != ""]
    return lists


def lists_are_in_order(list_left, list_right):
    """Auxilary function to compare lists."""

    list_left = copy.deepcopy(list_left)
    list_right = copy.deepcopy(list_right)

    # Find out how far we can loop without exceeding any of the lists
    n_list_left = len(list_left)
    n_list_right = len(list_right)
    n = min(n_list_left, n_list_right)

    # Iterate through the list, comparing each element
    for i in range(n):

        # If both values are integers
        if type(list_left[i]) == int and type(list_right[i]) == int:
            if list_left[i] < list_right[i]:  # In order
                return True
            elif list_left[i] > list_right[i]:  # Not in order
                return False

        # If both values are lists
        elif type(list_left[i]) == list and type(list_right[i]) == list:
            in_order = lists_are_in_order(list_left[i], list_right[i])
            if in_order is None:
                continue  # No decision possible yet
            elif in_order:
                return True
            elif not in_order:
                return False

        # If only left value is list (we make right value a list)
        elif type(list_left[i]) == list and type(list_right[i]) == int:
            in_order = lists_are_in_order(list_left[i], [list_right[i]])
            if in_order is None:
                continue  # No decision possible yet
            elif in_order:
                return True
            elif not in_order:
                return False

        # If only right value is list (we make left value a list)
        elif type(list_left[i]) == int and type(list_right[i]) == list:
            in_order = lists_are_in_order([list_left[i]], list_right[i])
            if in_order is None:
                continue  # No decision possible yet
            elif in_order:
                return True
            elif not in_order:
                return False

    # If the previous checks did not determine the result, the list lengths will
    if n_list_left < n_list_right:  # In order
        return True
    elif n_list_left > n_list_right:  # Not in order
        return False
    else:
        return None


def merge(arr, l, m, r):
    """
    Reference: https://www.geeksforgeeks.org/python-program-for-merge-sort/#:~:text=Merge%20Sort%20is%20a%20Divide,assumes%20that%20arr%5Bl..
    """
    n1 = m - l + 1
    n2 = r - m

    # create temp arrays
    L = [0] * (n1)
    R = [0] * (n2)

    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    # Merge the temp arrays back into arr[l..r]
    i = 0  # Initial index of first subarray
    j = 0  # Initial index of second subarray
    k = l  # Initial index of merged subarray

    while i < n1 and j < n2:
        # THE NEXT 2 LINES ARE WHERE WE CUSTOMIZE THE MERGE SORT ALGORITHM
        in_order = lists_are_in_order(L[i], R[j])
        if in_order is None or in_order:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def merge_sort(arr, l=None, r=None):

    if l is None:
        l = 0
    if r is None:
        r = len(arr) - 1

    if l < r:

        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        m = l + (r - l) // 2

        # Sort first and second halves
        merge_sort(arr, l, m)
        merge_sort(arr, m + 1, r)
        merge(arr, l, m, r)
