from dataclasses import dataclass

@dataclass
class Transition:
    sender: str
    owner: str
    state_from_id: str
    state_to_id: str
    title: str
