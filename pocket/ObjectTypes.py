import sys
import pygame
import random
from types import MethodType
from operator import xor
# from image import *
import constants

# todo: class Street, PoliceDepartment
# class for all buttons and prompts?
# when draw, return a surface object at each level
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


class Token:
    def __init__(self, screen, name, display_name, image, location=None):
        self.name = name
        self.display_name = display_name
        self.image = image
        self.location = location
        self.show = False
        self.screen = screen

    def __str__(self):
        return "Token: " + self.name

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location

    def get_image(self):
        return self.image

    def draw(self):
        pass


class Tile(Token):  # todo: need a method to set direction and check witness
    def __init__(self, name, display_name, hourglass_num, image):
        super(Tile, self).__init__(name, display_name, None, (0, 0))
        self.hourglass_num = hourglass_num
        self.direction = 0
        self.head = True  # false for tail
        self.suspect = 1
        self.is_seen = 0
        self.images = [pygame.image.load(image[0]).convert(), pygame.image.load(image[1]).convert()]
        self.flip_image()

    def __str__(self):
        return "Tile: " + super(Tile, self).__str__()

    def set_location(self, location):
        super(Tile, self).set_location(location)

    def get_location(self):
        return super(Tile, self).get_location()

    def rotate(self):  # counterclockwise
        self.direction += 1
        self.direction %= 4

    def flip_image(self):
        self.image = self.images[int(self.head)]

    def set_direction(self, direction):
        self.direction = direction

    def mark_suspect(self, susp):  # todo: not so clear here
        self.suspect = susp

    def flip(self):
        self.head = not self.head
        self.flip_image()

    def get_image(self):
        return pygame.transform.rotate(self.image, self.direction * 90)


class Detective(Token):
    def __init__(self, name, display_name, location, image):
        super(Detective, self).__init__(name, display_name, pygame.image.load(image).convert_alpha(), location)
        self.init_location = location

    def set_location(self, location):
        super(Detective, self).set_location(location % 12)

    def get_location(self, bias=0):
        return (super(Detective, self).get_location() + bias) % 12

    def can_reach(self, loc, view_range=2):
        if loc < self.location:
            loc += 12
        return 0 < loc - self.location < view_range + 1

    def go_back(self):
        self.location = self.init_location


class Button(Token):
    def __init__(self, name, display_name, callback, size=(100, 50)):
        super(Button, self).__init__(name, display_name, None, 0)
        self.callback = callback
        self.size = size

    def set_location(self, location):
        super(Button, self).set_location(location)
        self.update_image()

    def get_location(self):
        return super(Button, self).get_location()

    def update_image(self):
        # no need for rect, black background is enough
        # pygame.Rect(self.location * button_size[0], 0, button_size[0], button_size[1])
        self.image = pygame.Surface(self.size)
        self.image.fill(constants.black)
        font = pygame.font.Font(constants.font, 15)
        self.image.blit(font.render(self.display_name, True, constants.white, (0, 0)), (20, 5))


class ActionCards(Token):
    def __init__(self, name, display_name, location, image):
        super(ActionCards, self).__init__(name, display_name, pygame.image.load(image).convert_alpha(), location)
        self.used = False
        self.head = False
        self.callback = name

    def set_location(self, location):
        super(ActionCards, self).set_location(location)

    def get_location(self):
        return super(ActionCards, self).get_location()


class Hourglass(Token):
    def __init__(self, name, display_name, location, image, turn):
        super(Hourglass, self).__init__(name, display_name, pygame.image.load(image).convert_alpha(), location)
        self.turn = turn

    def set_location(self, location):
        super(Hourglass, self).set_location(location)

    def get_location(self):
        return super(Hourglass, self).get_location()
