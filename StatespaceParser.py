import xml.etree.ElementTree as ET
from typing import Dict

from model.state import State
from model.actor import Actor
from model.variable import Variable
from model.message import Message
from model.transition import Transition

class StatespaceParser:

    @staticmethod
    def parse(filename: str) -> Dict[str, State]:
        try:
            tree = ET.parse(filename)
        except FileNotFoundError as e:
            print("The statespace was not found.")
            raise e
        root = tree.getroot()

        states = {}

        for child in root:
            if child.tag == "state":
                new_state = StatespaceParser.get_state(child)
                states[new_state.id] = new_state
            elif child.tag == "transition":
                new_transition = StatespaceParser.get_transition(child)
                state_from_id = new_transition.state_from_id
                states[state_from_id].transitions.append(new_transition)
        
        return states

    @staticmethod
    def get_state(state_element: ET.Element) -> State:
        id = state_element.attrib["id"]
        new_state = State(id=id, actors=[], transitions=[])

        for child in state_element:
            if child.tag == "rebec":
                new_actor = StatespaceParser.get_actor(child)
                new_state.actors.append(new_actor)

        return new_state

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

        new_transition = Transition(
            sender=sender,
            owner=owner,
            state_from_id=state_from_id,
            state_to_id=state_to_id,
            title=title
        )

        return new_transition
