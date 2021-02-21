import sys

# use pythonic getter and setter, which is @property and @p.setter

import constants
from GameBoard import GameBoard
from ObjectTypes import *
import pygame


class GameEngine:
    def __init__(self, log_file="log.txt"):
        pygame.init()
        self.game_board = GameBoard()
        # have player objects here

    def run(self):
        # clock = pygame.time.Clock()
        while True:
            # clock.tick(60)
            self.handle_events()
            # self.update_buttons()
            self.game_board.draw()
            pygame.display.flip()
            # pygame.time.wait(500)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.game_board.click(pygame.mouse.get_pos())
            elif event.type == pygame.KEYUP:
                self.game_board.press(event.key)

    def log(self, *message):
        self.message = " ".join([str(i) for i in message])
