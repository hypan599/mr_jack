from StateMachine import *
import yaml


def main(state_helper):
    print("cancel1")
    state_helper.to_Joker()
    print(state_helper.state)
    state_helper.cancel()
    print(state_helper.state)

    print("cancel2")
    state_helper.to_Joker2()
    print(state_helper.state)
    state_helper.cancel()
    print(state_helper.state)

    print("Finish")


if __name__ == "__main__":
    states_config = yaml.safe_load(open("states.yaml", "r"))
    print(states_config)
    state_helper = JackStateHelper()
    print(dir(state_helper))
    # main(state_helper)