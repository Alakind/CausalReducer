from graphviz import Digraph
from typing import Dict

from model.state import State


class StatespaceVisualiser:

    @staticmethod
    def visualise(statespace: Dict[str, State], directory: str = "", statespace_name: str = "my_graph", open_file: bool = True):
        dot = StatespaceVisualiser.get_dot_representation(statespace)        
        dot.engine = 'dot'

        print("Rendering...")

        dot.render(directory=directory, filename=statespace_name, format='png', cleanup=True)

        print("Done!")

        if open_file:
            dot.view()

    @staticmethod
    def get_dot_representation(statespace: Dict[str, State]):
        dot = Digraph(format='png')

        visited = set()

        def visit(state_id: str):
            state = statespace[state_id]

            if state.id in visited:
                return
            
            visited.add(state.id)
            color = "black"
            if state.is_hazardous:
                color = "red"
            elif state.is_initial:
                color = "blue"
            dot.node(state.id, color=color)

            for transition in state.transitions:
                from_id = state.id
                to_id = transition.state_to_id
                dot.edge(from_id, to_id, label=f"{transition.sender}->{transition.owner}.{transition.message.value}")
                visit(transition.state_to_id)

        i = 1
        for state in statespace:
            visit(state)
            i += 1

        return dot

