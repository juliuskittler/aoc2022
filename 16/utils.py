import pathlib
import re
from typing import List


def get_valve_info(filepath: pathlib.Path) -> List[List]:
    """Auxilary function to return a list of three lists.

    The three lists are [flow_rates, dest_valves, targ_valves].
    """
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

        flow_rates = list()
        dest_valves = list()
        targ_valves = list()

        for line in lines:

            # Extract data
            flow_rate = int(re.findall("flow rate=(-?\d+)", line)[0])
            dest_valve = line.split(" ")[1]

            if "lead to valves" in line:
                targ_valve = line.split("lead to valves ")[1].split(", ")
            elif "leads to valve" in line:
                targ_valve = [line.split("leads to valve ")[1]]

            # Store data in a list
            flow_rates.append(flow_rate)
            dest_valves.append(dest_valve)
            targ_valves.append(targ_valve)

    return [flow_rates, dest_valves, targ_valves]
