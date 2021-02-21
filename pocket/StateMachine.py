from transitions import Machine
import yaml


def convert_state_config(states_config):
    states = []
    transitions = []
    state_properties = {}
    for state in states_config["states"]:
        states.append(state["name"])
        for trans in state["transitions"]:
            transitions.append([trans["trigger"], state["name"], trans["dest"]])
        state_properties[state["name"]] = {
            "buttons": state["buttons"],
            "clickable": state["clickable"],
        }
    return states, transitions, state_properties


class JackStateHelper:
    def __init__(self):
        states_config = yaml.safe_load(open("states.yaml", "r"))
        states, transitions, state_properties = convert_state_config(states_config)
        self.state_properties=state_properties
        self.machine = Machine(model=self, states=states, transitions=transitions)

        self.clickables = []
        self.buttons = []



    def set_clickable(self, clickables=[], buttons=[]):
        self.clickables = clickables
        self.buttons = buttons
