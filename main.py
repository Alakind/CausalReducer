import argparse
import sys
from time import time

from StatespaceParser import StatespaceParser
from StatespaceVisualiser import StatespaceVisualiser
from CausalReducer import CausalReducer


def main():
    parser = argparse.ArgumentParser(description="Statespace Visualiser.")

    parser.add_argument('--short', type=bool, default=False, help='Turn on shortened statespace mode')
    parser.add_argument('--statespace', type=str, required=True, help='Input statespace')
    args = parser.parse_args()

    statespace_name = args.statespace

    start_time = time()
    statespace = StatespaceParser.parse(f"./statespaces/{statespace_name}.statespace")
    end_time = time()

    print("Statespace parsed")
    print(f"Parsing time: {end_time - start_time:.4f} seconds")
    print(f"Full statespace size: {len(statespace)} states")

    causal_reducer = CausalReducer()
    start_time = time()
    causal_statespace = causal_reducer.reduce_to_causal(statespace, is_short=args.short)
    end_time = time()
    print("Causality analysis complete")
    print(f"Causal analysis time: {end_time - start_time:.4f} seconds")
    print(f"Casual statespace size: {len(causal_statespace)} states")

    start_time = time()
    StatespaceVisualiser.visualise(statespace, statespace_name)
    StatespaceVisualiser.visualise(causal_statespace, statespace_name + "_causal")
    end_time = time()
    print(f"Rendering time: {end_time - start_time:.4f} seconds")


def get_statespace_name() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "Batteries"

main()
