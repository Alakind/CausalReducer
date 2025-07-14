import xml.etree.ElementTree as ET
from typing import Dict, Set, List
import os

from StatespaceParser import StatespaceParser
from model.state import State

class StatespaceSaver:

    @staticmethod
    def save_statespace(statespace: Dict[str, State], statespace_file_path: str = ""):
        directory = os.path.dirname(statespace_file_path)
        statespace_name = os.path.splitext(os.path.basename(statespace_file_path))[0]

        state_ids = StatespaceSaver._get_state_ids(statespace)
        transition_ids = StatespaceSaver._get_transition_ids(statespace)

        tree = ET.parse(statespace_file_path)
        root = tree.getroot()

        filtered_items = StatespaceSaver._get_filtered_items(
            root, state_ids, transition_ids
        )

        new_root = ET.Element('transitionsystem')
        for item in filtered_items:
            new_root.append(item)
        new_tree = ET.ElementTree(new_root)
        new_tree.write(f'{directory}/{statespace_name}_causal.statespace', encoding='utf-8')

    @staticmethod
    def _get_state_ids(statespace: Dict[str, State]) -> Set[str]:
        state_ids = set()
        for state in statespace.values():
            state_ids.add(state.id)
        return state_ids

    @staticmethod
    def _get_transition_ids(statespace: Dict[str, State]) -> Set[str]:
        transition_ids = set()
        for state in statespace.values():
            for transition in state.transitions:
                transition_ids.add(transition.id)
        return transition_ids
    
    @staticmethod
    def _get_filtered_items(
        root: ET.Element,
        state_ids: set[str],
        transition_ids: set[str]
    ) -> List[ET.Element]:
        filtered_items = []
        for child in root:
            if child.tag == "state":
                id = child.attrib["id"]
                if id in state_ids:
                    filtered_items.append(child)
            elif child.tag == "transition":
                transition = StatespaceParser.get_transition(child)
                if transition.id in transition_ids:
                    filtered_items.append(child)
        return filtered_items
