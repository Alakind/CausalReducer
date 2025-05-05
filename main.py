from pprint import pprint
import sys

from StatespaceParser import StatespaceParser
from StatespaceVisualiser import StatespaceVisualiser


def main():
    statespace_name = get_statespace_name()
    statespace = StatespaceParser.parse(f"./statespaces/{statespace_name}.statespace")

    pprint("State")
    pprint(statespace)

    StatespaceVisualiser.visualise(statespace, statespace_name)


def get_statespace_name() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "Batteries"

main()
