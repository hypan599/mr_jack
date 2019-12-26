import sys
import pygame
import random
from types import MethodType
from operator import xor
# from image import *
import constants


# maybe: use pythonic getter and setter
# todo: hourglass change to 2 columns
# todo: actions -> choose target then save



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
    def __init__(self, name, display_name, image, location=None):
        self.name = name
        self.display_name = display_name
        self.image = image
        self.location = location

    def __str__(self):
        return "Token: " + self.name

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location

    def get_image(self):
        return self.image


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


class GameEngine:
    def __init__(self, log_file="log.txt"):
        # pygame surface related
        pygame.init()
        self.window_dimension = 1560, 920
        self.streets_dimension = 1060, 920
        self.side_dimension = 500, 920
        self.button_size = 100, 50
        self.screen = pygame.display.set_mode(self.window_dimension, 0, 32)
        self.background_image = pygame.image.load(constants.background_image).convert()
        self.message = ""

        # game status flags
        self.game_turn = None  # None is before start, otherwise integer.
        self.action_chosen = False
        self.num_action_chosen = 0
        self.target_chosen = False
        self.num_targets = 0
        self.target1 = None
        self.target2 = None
        self.clickable = []

        # jack related flags
        self.jack_status = None
        self.witness = None
        self.mouse_position = None
        self.toggle_show_jack = False
        self.jack = None

        # load static
        self.detectives = []
        self.tiles = []
        self.all_buttons = {}
        self.buttons = []
        self.actions = []
        self.hourglasses = []
        self.current_actions = [True, True, True, True]
        for detective in constants.detectives:
            self.detectives.append(Detective(*detective))
        for tile in constants.tiles:
            self.tiles.append(Tile(*tile))
        for button in constants.buttons:
            button = list(button) + [self.button_size]
            self.all_buttons[button[0]] = Button(*button)
        for i in range(1, 9):
            self.hourglasses.append(Hourglass(constants.hourglass[0], constants.hourglass[1], i, constants.hourglass[2], i))
        for i in range(4):
            self.actions.append([])
            self.actions[-1].append(ActionCards(*constants.actions[2 * i]))
            self.actions[-1].append(ActionCards(*constants.actions[2 * i + 1]))
        self.shuffle_actions()
        self.shuffle_tiles_location()
        self.tile_mouse_on_img = pygame.image.load(constants.tile_mouse_on).convert_alpha()
        self.action_mouse_on_img = pygame.image.load(constants.action_mouse_on).convert_alpha()
        self.detective_mouse_on_img = pygame.image.load(constants.detective_mouse_on).convert_alpha()
        print("initialization finish")

    def shuffle_tiles_location(self):
        shuffled_locations = random.sample(constants.available_tile_locations, 9)
        for idx, tile in enumerate(self.tiles):
            tile.set_location(shuffled_locations[idx])
            for i in range(random.randint(0, 3)):
                tile.rotate()

    def shuffle_actions(self):
        for i in range(len(self.actions)):
            self.current_actions[i] = random.random() > 0.5

    def update_buttons(self):
        if self.game_turn is not None:
            available_buttons = ["reveal", "cancel", "confirm", "start"]
        else:
            available_buttons = ["start"]

        assert (len(available_buttons) < 5)
        self.buttons.clear()
        for idx, btn_name in enumerate(available_buttons):
            btn_obj = self.all_buttons[btn_name]
            btn_obj.set_location(idx)
            self.buttons.append(btn_obj)

    def cleanup(self):
        self.message = None

    def is_clickable(self, click_type, click_location):
        return True

    def draw_board(self):
        # each time redraw every pixel is slow, but not matter in this board game :)
        mouse_position = pygame.mouse.get_pos()
        hover_type, hover_location = self.get_mouse_location(mouse_position)  # check availability for
        if hover_type in ["detectives", "tiles", "actions"]:
            self.screen.blit(self.draw_streets(hover_type, hover_location), (0, 0))
            self.screen.blit(self.draw_side(), (self.streets_dimension[0], 0))
        else:
            self.screen.blit(self.draw_streets(), (0, 0))
            self.screen.blit(self.draw_side(hover_type, hover_location), (self.streets_dimension[0], 0))

    def draw_streets(self, hover_type=None, hover_location=None):
        # todo: do not hard code margin and padding
        surface = pygame.Surface(self.streets_dimension)
        surface.blit(self.background_image, (0, 0))
        # blit tiles
        for idx, tile in enumerate(self.tiles):
            surface.blit(tile.get_image(), (lambda x: (100 + 240 * x[0], 100 + 240 * x[1]))(tile.get_location()))
            if hover_type == "tiles" and hover_location == idx:
                surface.blit(self.tile_mouse_on_img, (lambda x: (100 + 240 * x[0], 100 + 240 * x[1]))(tile.get_location()))
        # blit detectives
        positions_for_detective = [(170, 0), (410, 0), (650, 0), (820, 170), (820, 410), (820, 650),
                                   (650, 820), (410, 820), (170, 820), (0, 650), (0, 410), (0, 170)]
        for detective in self.detectives:
            surface.blit(detective.image, positions_for_detective[detective.get_location()])
            if hover_type == "detectives" and hover_location == detective.get_location():
                surface.blit(self.detective_mouse_on_img, positions_for_detective[detective.get_location()])
        # blit actions
        actions_to_show = [self.actions[i][int(self.current_actions[i])] for i in range(len(self.current_actions))]
        for idx, action in enumerate(actions_to_show):
            surface.blit(action.image, (940, 100 * action.get_location()))
            if hover_type == "actions" and hover_location == idx:
                surface.blit(self.action_mouse_on_img, (940, 100 * action.get_location()))
        # blit hourglasses
        for hourglass in self.hourglasses:
            surface.blit(hourglass.get_image(), (950, 400 + 60 * hourglass.get_location()))
        return surface

    def draw_side(self, hover_type=None, hover_location=None):
        surface = pygame.Surface((self.window_dimension[0] - self.streets_dimension[0], self.streets_dimension[1]))
        font = pygame.font.Font(constants.font, 15)
        # buttons
        for button in self.buttons:
            # print(button.get_location())
            surface.blit(button.image, (self.button_size[0] * button.get_location(), 0))
        # prompts:
        if self.message:
            surface.blit(font.render(self.message, True, constants.white, (0, 0)), (0, 350))
        # reveal jack
        if self.toggle_show_jack:
            surface.blit(font.render("Jack is.", True, constants.white, (0, 0)), (0, 650))
        # every person's visibility,
        if self.game_turn is not None:
            for idx, tile in enumerate(self.tiles):
                # make this location based on their location on map, may have translation issue
                text = font.render("{0}: {1}可见".format(tile.display_name, " " if tile.is_seen else "不"), True, constants.white, (0, 0))
                surface.blit(text, (0, 680 + idx * 25))
        # turn and stage info
        if self.game_turn is not None:
            turn_prompt = "第{0}回合, 第{1}轮, {2}行动".format(self.game_turn,
                                                        self.num_action_chosen + 1,
                                                        "Jack " if self.game_turn % 2 else "Detective ")
            surface.blit(font.render(turn_prompt, True, constants.white, (0, 0)), (0, 550))
        # jack and detective marker number,
        # jack's status,
        # game room prompt
        return surface

    def run(self):
        # clock = pygame.time.Clock()
        while True:
            # clock.tick(60)
            self.handle_events()
            self.update_buttons()
            self.draw_board()
            pygame.display.flip()
            # pygame.time.wait(500)

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

    def get_mouse_location(self, mouse_position):
        """
        only street tiles, detectives, action tiles, and button area is click-able
        """
        mouse_type, mouse_location = "invalid", 0
        if mouse_position[0] < self.streets_dimension[0]:
            if mouse_position[0] < 920:
                if mouse_position[0] < 100:
                    if 170 < mouse_position[1] < 270:
                        mouse_type, mouse_location = "detectives", 11
                    elif 410 < mouse_position[1] < 510:
                        mouse_type, mouse_location = "detectives", 10
                    elif 650 < mouse_position[1] < 750:
                        mouse_type, mouse_location = "detectives", 9
                elif mouse_position[0] > 820:
                    if 170 < mouse_position[1] < 270:
                        mouse_type, mouse_location = "detectives", 3
                    elif 410 < mouse_position[1] < 510:
                        mouse_type, mouse_location = "detectives", 4
                    elif 650 < mouse_position[1] < 750:
                        mouse_type, mouse_location = "detectives", 5
                elif mouse_position[1] < 100:
                    if 170 < mouse_position[0] < 270:
                        mouse_type, mouse_location = "detectives", 0
                    elif 410 < mouse_position[0] < 510:
                        mouse_type, mouse_location = "detectives", 1
                    elif 650 < mouse_position[0] < 750:
                        mouse_type, mouse_location = "detectives", 2
                elif mouse_position[1] > 820:
                    if 170 < mouse_position[0] < 270:
                        mouse_type, mouse_location = "detectives", 8
                    elif 410 < mouse_position[0] < 510:
                        mouse_type, mouse_location = "detectives", 7
                    elif 650 < mouse_position[0] < 750:
                        mouse_type, mouse_location = "detectives", 6
                else:  # tiles area
                    x = (mouse_position[0] - 100) // 240
                    y = (mouse_position[1] - 100) // 240
                    for idx, p in enumerate(self.tiles):
                        if p.get_location() == (x, y):
                            mouse_type, mouse_location = "tiles", idx
            else:  # action cards
                if mouse_position[1] < 400:
                    mouse_type, mouse_location = "actions", mouse_position[1] // 100
        else:  # click in side area
            mouse_position = mouse_position[0] - self.streets_dimension[0], mouse_position[1]
            if mouse_position[1] < self.button_size[1]:  # click on some button
                button_clicked = mouse_position[0] // 100
                if button_clicked < len(self.buttons):
                    mouse_type, mouse_location = "buttons", button_clicked
        return mouse_type, mouse_location

    def click(self):
        mouse_position = pygame.mouse.get_pos()
        click_type, click_location = self.get_mouse_location(mouse_position)

        if click_type == "detectives":
            print("click detective", click_location)
        elif click_type == "tiles":
            print("click tile", click_location)
            self.tiles[click_location].rotate()
        elif click_type == "buttons":
            getattr(self, self.buttons[click_location].callback)()
        elif click_type == "actions":
            getattr(self, self.actions[click_location][int(self.current_actions[click_location])].callback)()
        print("mouse clicked:", mouse_position)

    def check_jack_visibility(self):
        # todo: need to modify tile class
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
        self.log("joker")

    def move_one_detective(self, subject, max_steps):
        # todo: check for existing detectives
        subject.set_location(subject.get_location() + 1)
        self.log("moving: " + subject.display_name)

    def rotate(self):
        print("rorate")

    def exchange(self):
        pass

    def alibi(self):
        pass

    # below are function for button callbacks
    def start_game(self):  # including start and restart
        if self.game_turn is None:
            self.game_turn = 1
            self.log("game started!")

    def confirm(self):
        print("confirm")

    def cancel(self):
        print("cancel")

    def checkpoint(self):
        pass

    def reveal(self):
        self.toggle_show_jack = not self.toggle_show_jack

    def log(self, *message):
        self.message = " ".join([str(i) for i in message])
