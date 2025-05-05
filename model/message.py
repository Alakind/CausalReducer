from dataclasses import dataclass

@dataclass
class Message:
    sender: str
    owner: str
    value: str
