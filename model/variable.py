from dataclasses import dataclass

@dataclass
class Variable:
    name: str
    type: str
    value: any
