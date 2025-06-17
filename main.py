import argparse
import sys

from StatespaceParser import StatespaceParser
from StatespaceVisualiser import StatespaceVisualiser
from CausalReducer import CausalReducer


def main():
    parser = argparse.ArgumentParser(description="Statespace Visualiser.")

    parser.add_argument('--short', type=bool, default=False, help='Turn on shortened statespace mode')
    parser.add_argument('--statespace', type=str, required=True, help='Input statespace')
    args = parser.parse_args()

    statespace_name = args.statespace
    statespace = StatespaceParser.parse(f"./statespaces/{statespace_name}.statespace")

    print("Statespace parsed")
    print(f"Full statespace size: {len(statespace)} states")

    causal_reducer = CausalReducer()
    causal_statespace = causal_reducer.reduce_to_causal(statespace, is_short=args.short)
    print("Causality analysis complete")

    StatespaceVisualiser.visualise(statespace, statespace_name)
    StatespaceVisualiser.visualise(causal_statespace, statespace_name + "_causal")


def get_statespace_name() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "Batteries"

main()
