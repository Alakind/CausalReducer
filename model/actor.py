from dataclasses import dataclass
from typing import List
from model.variable import Variable
from model.message import Message

@dataclass
class Actor:
    name: str
    variables: List[Variable]
    queue: List[Message]
