import sys
import random
from types import MethodType
import platform
from operator import xor

# todo: use pythonic getter and setter, which is @property and @p.setter
# todo: hourglass change to 2 columns
# todo: actions -> choose target then save
# todo: let the street be empty before game starts

# todo: detective is clickable when
from ObjectTypes import *


class GameEngine:
    def __init__(self, log_file="log.txt"):
        # pygame surface related
        pygame.init()
        # move size related to GameBoard
        self.window_dimension = 1560, 920 # todo: detect os
        self.streets_dimension = 1060, 920
        self.side_dimension = 500, 920
        self.button_size = 100, 50
        self.screen = pygame.display.set_mode(self.window_dimension, 0, 32)  # inject this object into token
        self.background_image = pygame.image.load(constants.background_image).convert()
        self.message = ""

        # game status flags
        self.game_turn = None  # None is before start, otherwise integer.
        self.action_chosen = False
        self.num_action_chosen = 0
        self.target_chosen = True
        self.num_targets = 0
        self.target1 = None
        self.target2 = None
        self.clickable = {}

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
            self.actions[-1].append(ActionToken(*constants.actions[2 * i]))
            self.actions[-1].append(ActionToken(*constants.actions[2 * i + 1]))
        self.shuffle_actions()
        self.shuffle_tiles_location()
        self.tile_mouse_on_img = pygame.image.load(constants.tile_mouse_on).convert_alpha()
        self.action_mouse_on_img = pygame.image.load(constants.action_mouse_on).convert_alpha()
        self.detective_mouse_on_img = pygame.image.load(constants.detective_mouse_on).convert_alpha()
        print("initialization finish")

    # move to GameBoard
    def shuffle_tiles_location(self):
        shuffled_locations = random.sample(constants.available_tile_locations, 9)
        for idx, tile in enumerate(self.tiles):
            tile.location = shuffled_locations[idx]
            for i in range(random.randint(0, 3)):
                tile.rotate()
    def shuffle_actions(self):
        for i in range(len(self.actions)):
            self.current_actions[i] = random.random() > 0.5

    # keep in engine for now
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

    # move to GameBoard
    def cleanup(self):
        self.message = None

    # move to GameBoard.draw
    def is_clickable(self, click_type, click_location):
        return click_location in self.clickable.get(click_type, [])

    # move to GameBoard.draw
    def draw_board(self):
        # each time redraw every pixel is slow, but not matter in this board game :)
        mouse_position = pygame.mouse.get_pos()
        hover_type, hover_location = self.get_mouse_location(mouse_position)  # check availability for
        if hover_type in ["detectives", "tiles", "actions"] and self.is_clickable(hover_type, hover_location):
            self.screen.blit(self.draw_streets(hover_type, hover_location), (0, 0))
            self.screen.blit(self.draw_side(), (self.streets_dimension[0], 0))
        else:
            self.screen.blit(self.draw_streets(), (0, 0))
            self.screen.blit(self.draw_side(hover_type, hover_location), (self.streets_dimension[0], 0))
    def draw_streets(self, hover_type=None, hover_location=None): # todo: should be method of each object
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
        font = pygame.font.Font(constants.FONT, 15)
        # buttons
        for button in self.buttons:
            # print(button.get_location())
            surface.blit(button.image, (self.button_size[0] * button.get_location(), 0))
        # prompts:
        if self.message:
            surface.blit(font.render(self.message, True, constants.WHITE, (0, 0)), (0, 350))
        # reveal jack
        if self.toggle_show_jack:
            surface.blit(font.render("Jack is.", True, constants.WHITE, (0, 0)), (0, 650))
        # every person's visibility,
        if self.game_turn is not None:
            for idx, tile in enumerate(self.tiles):
                # make this location based on their location on map, may have translation issue
                text = font.render("{0}: {1}可见".format(tile.display_name, " " if tile.is_seen else "不"), True, constants.WHITE, (0, 0))
                surface.blit(text, (0, 680 + idx * 25))
        # turn and stage info
        if self.game_turn is not None:
            turn_prompt = "第{0}回合, 第{1}轮, {2}行动".format(self.game_turn,
                                                        self.num_action_chosen + 1,
                                                        "Jack " if self.game_turn % 2 else "Detective ")
            surface.blit(font.render(turn_prompt, True, constants.WHITE, (0, 0)), (0, 550))
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

    # pass absolute mouse position to GameBoard
    # move the logic to GameBoard
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
        self.target_chosen = False
        self.clickable["detectives"] = [
            (self.detectives[0].get_location() + 1) % 12,
            (self.detectives[0].get_location() + 2) % 12,
        ]
        # self.move_one_detective(self.detectives[0], 2)

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
