from dataclasses import dataclass

@dataclass
class Transition:
    sender: str
    owner: str
    state_from: str
    state_to: str
    title: str
