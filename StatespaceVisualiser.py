from graphviz import Digraph
from typing import Dict

from model.state import State


class StatespaceVisualiser:

    @staticmethod
    def visualise(statespace: Dict[str, State], statespace_name: str = "my_graph", open: bool = True):
        dot = StatespaceVisualiser.get_dot_representation(statespace)        

        dot.render(directory='graphs', filename=statespace_name, format='png', cleanup=True)

        if open:
            dot.view()

    @staticmethod
    def get_dot_representation(statespace: Dict[str, State]):
        dot = Digraph()

        visited = set()

        def visit(state_id: str):
            state = statespace[state_id]

            if state.id in visited:
                return
            
            visited.add(state.id)
            dot.node(state.id)

            for transition in state.transitions:
                dot.edge(state.id, transition.state_to_id)
                visit(transition.state_to_id)

        for state in statespace:
            visit(state)

        return dot

