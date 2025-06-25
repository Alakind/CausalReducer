from typing import Dict, List
from collections import deque
import copy

from model.state import State
from model.transition import Transition

class CausalReducer:
    statespace: Dict[str, State] = {}
    causal_transitions: Dict[str, Transition] = {}
    causal_transitions_refined: Dict[str, Transition] = {}
    state_transition_traces: Dict[str, List[List[Transition]]] = {}

    bfs_queue = deque([])

    def reduce_to_causal(self, statespace: Dict[str, State], is_short=False) -> Dict[str, State]:
        self.statespace = statespace

        for state in self.statespace.values():
            if state.is_hazardous:
                self.reduce_single_haz_state(state)
                self.state_transition_traces = {}

        causal_statespace = self.get_causal_statespace(self.causal_transitions)
        return causal_statespace

    def get_causal_statespace(self, transitions: Dict[str, Transition]) -> Dict[str, State]:
        causal_statespace: Dict[str, State] = {}

        for transition in transitions.values():
            if not transition.state_from_id in causal_statespace.keys():
                self.add_causal_state(causal_statespace, transition.state_from_id)
            if not transition.state_to_id in causal_statespace.keys():
                self.add_causal_state(causal_statespace, transition.state_to_id)

            state_to = causal_statespace[transition.state_to_id]
            state_from = causal_statespace[transition.state_from_id]

            if not transition in state_to.transitions_target:
                state_to.transitions_target.append(transition)
            if not transition in state_from.transitions:
                state_from.transitions.append(transition)

        return causal_statespace

    def add_causal_state(self, causal_statespace: Dict[str, State], state_id: str):
        new_state: State = copy.deepcopy(self.statespace[state_id])

        new_state.transitions = []
        new_state.transitions_target = []

        causal_statespace[state_id] = new_state

    def reduce_single_haz_state(self, bad_state: State):
        self.reverse_bfs_step(bad_state, [])

        while self.bfs_queue:
            (next_state, trace) = self.bfs_queue.popleft()
            self.reverse_bfs_step(next_state, trace)

    def refine_causal_transitions(self, current_state: State, causal_statespace: Dict[str, State], is_short=False):
        if is_short and current_state.is_hazardous:
            return

        for transition in current_state.transitions:
            if transition.id in self.causal_transitions_refined.keys():
                continue
            self.causal_transitions_refined[transition.id] = transition

            self.refine_causal_transitions(causal_statespace[transition.state_to_id], causal_statespace, is_short)

    def reverse_bfs_step(self, current_state: State, trace: List[Transition]):
        if current_state.id in self.state_transition_traces:
            if self.is_trace_subset(trace, self.state_transition_traces[current_state.id]):
                return
        else:
            self.state_transition_traces[current_state.id] = []

        self.state_transition_traces[current_state.id].append(trace.copy())
        
        if current_state.is_initial:
            self.add_causal_transitions(trace)
            return
        
        for transition in current_state.transitions_target:
            self.bfs_queue.append((self.statespace[transition.state_from_id], trace + [transition]))

    def add_causal_transitions(self, transitions: List[Transition]):
        for transition in transitions:
            if transition.id not in self.causal_transitions.keys():
                self.causal_transitions[transition.id] = transition

    def is_trace_subset(self, current_trace: List[Transition], traces: List[List[Transition]]):
        for trace in traces:
            if self.is_one_subset_of_other(current_trace, trace):
                return True
        return False

    def is_one_subset_of_other(self, transitions_A: List[Transition], transitions_B: List[Transition]):
        short_trace = transitions_A
        long_trace = transitions_B
        if len(transitions_A) > len(transitions_B):
            short_trace = transitions_B
            long_trace = transitions_A


        current_transition_index = 0
        for transition_B in long_trace:
            if current_transition_index >= len(short_trace):
                return True

            transition_A = short_trace[current_transition_index]
            if (transition_A.message.owner == transition_B.message.owner
                    and transition_A.message.sender == transition_B.message.sender
                    and transition_A.message.value == transition_B.message.value):
                current_transition_index += 1
        
        if current_transition_index >= len(short_trace):
            return True

        return False
