import pygame

from ObjectTypes import *
from StateMachine import JackStateHelper
from constants import *


class GameBoard():
    def __init__(self):
        # init game board size
        self.dimension = Dimension("MEDIUM")
        self.state_helper = JackStateHelper()

        # pygame init
        self.font = pygame.font.Font(FONT, 15)
        self.text_color = WHITE
        self.screen = pygame.display.set_mode((self.dimension.window_width, self.dimension.window_height), 0, 32)
        self.background_image = pygame.image.load(
            os.path.join(IMAGE_ROOT, BACKGROUND_IMAGE)).convert()  # todo: resize background
        self.log = ""

        # elements on gameboard
        self.street = Street(self.dimension)
        self.police_department = PoliceDepartment(self.dimension)
        self.actions = AllActionTokens(self.dimension)
        self.hourglass = Hourglass(**HOURGALSS)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        surface = pygame.Surface((self.dimension.game_area_width, self.dimension.window_height))
        surface.blit(self.background_image, (0, 0))
        self.street.draw(surface, mouse_pos)
        self.police_department.draw(surface, mouse_pos)
        self.actions.draw(surface, mouse_pos)
        self.screen.blit(surface, (0, 0))

        surface = pygame.Surface(
            (self.dimension.window_width - self.dimension.game_area_width, self.dimension.window_height))
        surface.fill(BLACK)
        self.draw_visible(surface)
        self.screen.blit(surface, (self.dimension.game_area_width, 0))

    def draw_visible(self, surface):
        visible = set()
        for d in self.police_department.objects:
            visible |= self.street.get_visible_from(self.police_department.positions[d.location])

        text_height = 25
        tile_prompt = "{0}:  {1}  {2}"
        seen = lambda x: u"暴露" if x in visible else u"隐藏"
        for idx, tile in enumerate(self.street.objects):
            surface.blit(self.font.render(tile_prompt.format(tile.display_name, seen(tile), tile.location), True,
                                          self.text_color, (0, 0)),
                         (0, 550 + text_height * idx))

    def draw_side(self, hover_type=None, hover_location=None):
        surface = pygame.Surface((self.window_dimension[0] - self.streets_dimension[0], self.streets_dimension[1]))
        font = pygame.font.Font(FONT, 15)
        # buttons
        for button in self.buttons:
            # print(button.get_location())
            surface.blit(button.image, (self.button_size[0] * button.get_location(), 0))
        # prompts:
        if self.log:
            surface.blit(font.render(self.message, True, WHITE, (0, 0)), (0, 350))
        return surface
        # reveal jack
        if self.toggle_show_jack:
            surface.blit(font.render("Jack is.", True, WHITE, (0, 0)), (0, 650))
        # every person's visibility,
        if self.game_turn is not None:
            for idx, tile in enumerate(self.tiles):
                # make this location based on their location on map, may have translation issue
                text = font.render("{0}: {1}可见".format(tile.display_name, " " if tile.is_seen else "不"), True, WHITE,
                                   (0, 0))
                surface.blit(text, (0, 680 + idx * 25))
        # turn and stage info
        if self.game_turn is not None:
            turn_prompt = "第{0}回合, 第{1}轮, {2}行动".format(self.game_turn,
                                                        self.num_action_chosen + 1,
                                                        "Jack " if self.game_turn % 2 else "Detective ")
            surface.blit(font.render(turn_prompt, True, WHITE, (0, 0)), (0, 550))
        # jack and detective marker number,
        # jack's status,
        # game room prompt
        return surface

    # should this be in game board or in streets?
    def shuffle(self):
        self.street.shuffle()

    def shuffle_actions(self):
        self.actions.shuffle()

    def mouse_on(self, mouse_pos):
        pass

    def click(self, mouse_pos):
        # figure out what is clicked
        # return clicked object
        return 0, 1

    def press(self, key):
        print("Key ", key, " is pressed!")