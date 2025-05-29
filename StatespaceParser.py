import xml.etree.ElementTree as ET
from typing import Dict

from model.state import State
from model.actor import Actor
from model.variable import Variable
from model.message import Message
from model.transition import Transition

class StatespaceParser:
    states: Dict[str, State] = {}

    @staticmethod
    def parse(filename: str) -> Dict[str, State]:
        try:
            tree = ET.parse(filename)
        except FileNotFoundError as e:
            print("The statespace was not found.")
            raise e
        root = tree.getroot()

        StatespaceParser.states = {}

        # i = 1
        for child in root:
            if child.tag == "state":
                new_state = StatespaceParser.get_state(child)
                StatespaceParser.states[new_state.id] = new_state
            elif child.tag == "transition":
                new_transition = StatespaceParser.get_transition(child)
                state_from_id = new_transition.state_from_id
                state_to_id = new_transition.state_to_id
                StatespaceParser.states[state_from_id].transitions.append(new_transition)
                StatespaceParser.states[state_to_id].transitions_target.append(new_transition)
        
        return StatespaceParser.states

    @staticmethod
    def get_state(state_element: ET.Element) -> State:
        id = state_element.attrib["id"]

        propositions_string = state_element.attrib["atomicpropositions"]
        is_hazardous = StatespaceParser._is_hazardous(propositions_string)

        is_initial = id == "0"

        new_state = State(id=id, actors=[], transitions=[], transitions_target=[], is_hazardous=is_hazardous, is_initial=is_initial)


        for child in state_element:
            if child.tag == "rebec":
                new_actor = StatespaceParser.get_actor(child)
                new_state.actors.append(new_actor)

        return new_state
    
    @staticmethod
    def _is_hazardous(propositions_string: str) -> bool:
        for proposition in propositions_string.split(","):
            if proposition.startswith("haz"):
                return True
        return False


    @staticmethod
    def get_actor(actor_element: ET.Element) -> State:
        actor_name = actor_element.attrib["name"]
        new_actor = Actor(name=actor_name, variables=[], queue=[])

        for child in actor_element:
            if child.tag == "statevariables":
                for variable in child:
                    name = variable.attrib["name"]
                    type = variable.attrib["type"]
                    value = variable.text
                    new_variable = Variable(name=name, type=type, value=value)
                    new_actor.variables.append(new_variable)
            if child.tag == "queue":
                for message in child:
                    sender = message.attrib["sender"]
                    owner = actor_name
                    value = message.text
                    new_message = Message(sender=sender, owner=owner, value=value)
                    new_actor.queue.append(new_message)

        return new_actor

    @staticmethod
    def get_transition(transition_element: ET.Element) -> Transition:
        state_from_id = transition_element.attrib["source"]
        state_to_id = transition_element.attrib["destination"]

        for child in transition_element:
            sender = child.attrib["sender"]
            owner = child.attrib["owner"]
            title = child.attrib["title"]

        message = StatespaceParser.get_message_from_transition(
            sender,
            owner,
            state_from_id,
            state_to_id,
            title
        )

        new_transition = Transition(
            sender=sender,
            owner=owner,
            state_from_id=state_from_id,
            state_to_id=state_to_id,
            title=title,
            message=message,
            id=(state_from_id + "_" + state_to_id + "_" + message.value)
        )

        return new_transition
    
    @staticmethod
    def get_message_from_transition(
        sender: str,
        owner: str,
        state_from_id: str,
        state_to_id: str,
        title: str
    ) -> Message:
        if state_from_id not in StatespaceParser.states.keys():
            raise Exception("Parsing error. Transition is declared before the state")
        state_from = StatespaceParser.states[state_from_id]
        for actor in state_from.actors:
            # Get actor, who initiated the transition
            if actor.name == owner:
                # Get first message in a queue (the one, being handled)
                first_message = actor.queue[0]
                if (
                    StatespaceParser.is_message_equals_transition_title(first_message.value, title)
                    and sender == first_message.sender
                    and owner == first_message.owner
                ):
                    message = Message(sender=sender, owner=owner, value=first_message.value)

                    return message

        raise Exception("Parsing error. Transition is not found in the actor message queue")

    @staticmethod
    def is_message_equals_transition_title(message_value: str, transition_title: str) -> bool:
        message_title = message_value.split('(')[0].upper()

        return message_title == transition_title
