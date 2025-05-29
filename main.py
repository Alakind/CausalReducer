from pprint import pprint
import sys

from StatespaceParser import StatespaceParser
from StatespaceVisualiser import StatespaceVisualiser
from CausalReducer import CausalReducer


def main():
    statespace_name = get_statespace_name()
    statespace = StatespaceParser.parse(f"./statespaces/{statespace_name}.statespace")

    print("Statespace parsed")
    print(f"Full statespace size: {len(statespace)} states")

    causal_reducer = CausalReducer()
    causal_statespace = causal_reducer.reduce_to_causal(statespace)
    print("Causality analysis complete")

    StatespaceVisualiser.visualise(statespace, statespace_name)
    StatespaceVisualiser.visualise(causal_statespace, statespace_name + "_causal")


def get_statespace_name() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "Batteries"

main()
