from dataclasses import dataclass

from model.message import Message

@dataclass
class Transition:
    sender: str
    owner: str

    state_from_id: str
    state_to_id: str

    title: str
    message: Message

    id: str
