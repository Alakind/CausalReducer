import xml.etree.ElementTree as ET
from pprint import pprint

from StatespaceParser import StatespaceParser
from StatespaceVisualiser import StatespaceVisualiser


def main():
    statespace = StatespaceParser.parse("./statespaces/Batteries.statespace")

    pprint("State")
    pprint(statespace)

    StatespaceVisualiser.visualise(statespace)


main()
