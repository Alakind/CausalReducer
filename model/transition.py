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

    @property
    def id(self) -> str:
        return (
            self.state_from_id + "_" +
            self.state_to_id + "_" +
            self.message.sender + "_" +
            self.message.owner +
            self.message.value)
