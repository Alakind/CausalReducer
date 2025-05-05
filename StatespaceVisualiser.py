from graphviz import Digraph
from typing import Dict

from model.state import State


class StatespaceVisualiser:

    @staticmethod
    def visualise(statespace: Dict[str, State]):
        dot = StatespaceVisualiser.get_dot_representation(statespace)        

        dot.render('my_graph', format='png', cleanup=True)
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
                dot.edge(state.id, transition.state_to)
                visit(transition.state_to)

        for state in statespace:
            visit(state)

        return dot

