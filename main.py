import argparse
import sys
import os
from time import time

from StatespaceParser import StatespaceParser
from StatespaceVisualiser import StatespaceVisualiser
from CausalReducer import CausalReducer
from StatespaceSaver import StatespaceSaver


def main():
    parser = argparse.ArgumentParser(description="Statespace Visualiser.")

    parser.add_argument('--short', action="store_true", help='Turn on shortened statespace mode')
    parser.add_argument('--visualise', action="store_true", help='Visualise state space after reduction')
    parser.add_argument('--time', action="store_true", help='Logs the time spent on different stages of execution')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input statespace file')
    args = parser.parse_args()

    statespace_file_path = args.input
    directory = os.path.dirname(statespace_file_path)
    statespace_name = os.path.splitext(os.path.basename(statespace_file_path))[0]

    # Parsing
    start_time = time()
    statespace = StatespaceParser.parse(statespace_file_path)
    parsing_time = time() - start_time
    print("Statespace parsed")
    print(f"Full statespace size: {len(statespace)} states")

    # Causal analysis
    causal_reducer = CausalReducer()
    start_time = time()
    causal_statespace = causal_reducer.reduce_to_causal(statespace, is_short=args.short)
    analysis_time = time() - start_time
    print("Causality analysis complete")
    print(f"Casual statespace size: {len(causal_statespace)} states")

    # Visualisation
    if args.visualise:
        start_time = time()
        StatespaceVisualiser.visualise(statespace, directory, statespace_name)
        StatespaceVisualiser.visualise(causal_statespace, directory, statespace_name + "_causal")
        visualisation_time = time() - start_time
        
    # Saving
    start_time = time()
    StatespaceSaver.save_statespace(causal_statespace, statespace_file_path)
    saving_time = time() - start_time

    if args.time:
        print(f"Parsing time: {saving_time:.4f} seconds")
        print(f"Causal analysis time: {analysis_time:.4f} seconds")
        if args.visualise: print(f"Rendering time: {visualisation_time:.4f} seconds")
        print(f"Saving statespace time: {saving_time:.4f} seconds")

def get_statespace_name() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "Batteries"

main()
