class Player:
    def __init__(self, is_human=None):
        self.is_human = is_human
        self.tokens = []


class Jack(Player):
    def __init__(self):
        super(Jack, self).__init__()
        self.real_jack = None


class Investigator(Player):
    def __init__(self):
        super(Investigator, self).__init__()
        self.characters_with_alibi = []