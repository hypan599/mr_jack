import sys
import pygame
import random
from types import MethodType
from operator import xor
# from image import *
import constants


class Tile:
    def __init__(self, name, display_name, hourglass_num, image):
        self.name = name
        self.display_name = display_name
        self.hourglass_num = hourglass_num
        self.direction = 0
        self.location = 0, 0
        self.head = True  # false for tail

        self.suspect = 1
        self.is_seen = 0

        # todo: seems better to do this using picture rotation?
        # todo: add a tail picture for all tile
        self.image = pygame.image.load(image).convert()

    def __str__(self):
        return "Tile: " + self.name

    def rotate(self, direction=0):
        if direction:
            self.direction = direction
        else:
            self.direction = (self.direction + 1) % 4

    def set_direction(self, direction):
        self.direction = direction

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location

    def mark_suspect(self, susp):
        self.suspect = susp


class Detective:
    def __init__(self, name, display_name, location, image):
        self.name = name
        self.display_name = display_name
        self.init_location = location
        self.location = location
        self.image = pygame.image.load(image).convert_alpha()

    def get_location(self, bias=0):
        return (self.location + bias) % 12

    def can_reach(self, loc, view_range=2):
        if loc < self.location:
            loc += 12
        return 0 < loc - self.location < view_range + 1

    def go_back(self):
        self.location = self.init_location


# todo: make general buttons and change based on game status
class Button:
    def __init__(self, name, display_name, location, callback, disabled):
        self.name = name
        self.display_name = display_name
        self.location = location
        self.callback = callback
        self.disabled = disabled


class ActionCards:
    def __init__(self, name, location):
        self.name = name
        self.used = False
        self.side = True
        self.location = location
        self.image = [0, 1]

    # def get_image(self):
    #     if self.side:
    #         return action_card_images[self.name[-1] + "f"]
    #     else:
    #         return action_card_images[self.name[-1] + "b"]
        # after reorganize static images
        # return self.image[int(self.side)]

    def get_location(self):
        return self.location

    def throw(self):
        self.side = random.randint(0, 1) == 1
        self.used = False

    def turn_over(self):
        self.side = not self.side
        self.used = False


class GameEngine:
    def __init__(self, log_file="log.txt"):
        # pygame surface related
        pygame.init()
        self.window_dimension = 1560, 920
        self.streets_dimension = 1060, 920
        self.screen = pygame.display.set_mode(self.window_dimension, 0, 32)
        self.background_image = pygame.image.load(constants.background_image).convert()
        self.log = open(log_file, "w")

        # setup
        self.detectives = self.add_detectives()
        self.tiles = self.add_tiles()
        self.shuffle_tiles()
        self.all_buttons = self.init_all_buttons()
        self.buttons = []
        self.button_size = 100, 50

        # game status related
        self.game_started = False
        self.game_turn = None
        self.game_stage = None
        self.game_action = None
        self.curr_status = None
        self.curr_player = None
        self.witness = None
        self.mouse_position = None

        print("initialization finish")

    def add_detectives(self):
        detectives = []
        for detective in constants.detectives:
            detectives.append(Detective(*detective))
        return detectives

    def shuffle_tiles(self):
        shuffled_locations = random.sample(constants.available_tile_locations, 9)
        for idx, tile in enumerate(self.tiles):
            tile.set_location(shuffled_locations[idx])

    def add_tiles(self):
        tiles = []
        for tile in constants.tiles:
            tiles.append(Tile(*tile))
        return tiles

    def init_all_buttons(self):
        all_buttons = []
        return all_buttons

    def update_buttons(self):
        pass

    def cleanup(self):
        self.log.close()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            # clock.tick(60)
            self.handle_events()
            self.draw_board()
            pygame.display.flip()
            # pygame.time.wait(500)

    def draw_buttons(self):
        pass

    def draw_board(self):
        # each time redraw every pixel is slow,
        # but not matter in this board game :)
        self.screen.blit(self.draw_streets(), (0, 0))
        self.screen.blit(self.draw_side(), (self.streets_dimension[0], 0))
        print("drawing board finish")

    def draw_streets(self):
        # todo: do not hard code margin and padding
        surface = pygame.Surface(self.streets_dimension)
        surface.blit(self.background_image, (0, 0))
        # blit tiles
        for tile in self.tiles:
            surface.blit(tile.image, (lambda x: (100 + 240 * x[0], 100 + 240 * x[1]))(tile.get_location()))
        # blit detectives
        positions_for_detective = [(170, 0), (410, 0), (650, 0), (820, 170), (820, 410), (820, 650),
                                   (650, 820), (410, 820), (170, 820), (0, 650), (0, 410), (0, 170)]
        for detective in self.detectives:
            surface.blit(detective.image, positions_for_detective[detective.get_location()])
        # blit hourglasses

        return surface

    def draw_side(self):
        surface = pygame.Surface((self.window_dimension[0]-self.streets_dimension[0], self.streets_dimension[1]))
        # buttons
        for button in self.buttons:
            area = (lambda x: (x * self.button_size[0], self.button_size[1]))(button.location)
            pygame.draw.rect(surface, constants.grey, area)
            surface.blit(pygame.font.render(button.prompt, True, constants.white, (0, 0)),
                         (area[0] + 20, area[1] + 5))

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.cleanup()
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.click()
            # elif event.type == pygame.KEYDOWN:
            #     self.doKeyDown(event.key)

    def click(self):
        self.mouse_position = pygame.mouse.get_pos()
        print("mouse clicked:", self.mouse_position)

    def check_jack_visibility(self):
        pass

    # below are actions created for 8 action cards
    # actions are not this simple, also includes "available mouse location" stuff
    def move1(self):
        self.move_one_detective(self.detectives[0], 2)

    def move2(self):
        self.move_one_detective(self.detectives[1], 2)

    def move3(self):
        self.move_one_detective(self.detectives[2], 2)

    def joker(self):  # named after same action in real game
        pass

    def move_one_detective(self, subject, max_steps):
        pass

    def rotate(self):
        pass

    def exchange(self):
        pass

    def alibi(self):
        pass

    # below are function for button callbacks
    def start_game(self):  # including start and restart
        pass

    def confirm(self):
        pass

    def cancel(self):
        pass

    def checkpoint(self):
        pass