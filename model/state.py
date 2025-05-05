from dataclasses import dataclass
from typing import List
from model.actor import Actor
from model.transition import Transition

@dataclass
class State:
    id: str
    actors: List[Actor]
    transitions: List[Transition]
