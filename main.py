import argparse
import sys
import os
from time import time

from StatespaceParser import StatespaceParser
from StatespaceVisualiser import StatespaceVisualiser
from CausalReducer import CausalReducer


def main():
    parser = argparse.ArgumentParser(description="Statespace Visualiser.")

    parser.add_argument('--short', action="store_true", help='Turn on shortened statespace mode')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input statespace file')
    args = parser.parse_args()

    statespace_file_path = args.input
    directory = os.path.dirname(statespace_file_path)
    statespace_name = os.path.splitext(os.path.basename(statespace_file_path))[0]

    start_time = time()
    statespace = StatespaceParser.parse(statespace_file_path)
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
    StatespaceVisualiser.visualise(statespace, directory, statespace_name)
    StatespaceVisualiser.visualise(causal_statespace, directory, statespace_name + "_causal")
    end_time = time()
    print(f"Rendering time: {end_time - start_time:.4f} seconds")


def get_statespace_name() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "Batteries"

main()
