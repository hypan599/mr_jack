import pygame
import constants

# todo: class Street, PoliceDepartment
# class for all buttons and prompts?
# when draw, return a surface object at each level


### classes for player
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


### base classes
class GroupBase:
    def __init__(self, screen=None):
        self.objects = []
        self.screen = screen

    def draw(self):
        raise NotImplementedError('subclasses must override draw()!')

    # shuffle logic is special for each group
    def shuffle(self):
        raise NotImplementedError('subclasses must override shuffle()!')

    def reset(self):
        for i in self.objects:
            i.reset()

class TokenBase:
    def __init__(self, name, display_name, image, location=0):
        self.name = name
        self.display_name = display_name
        self.image = image
        self.location = location
        self.show = False
        # self.screen = screen

    def __str__(self):
        return "Token: " + self.name


class Tile(TokenBase):  # todo: need a method to set direction and check witness
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

    def rotate(self):  # counterclockwise
        self.direction += 1
        self.direction %= 4

    def flip_image(self):
        self.image = self.images[int(self.head)]

    def mark_suspect(self, susp):  # todo: not so clear here
        self.suspect = susp

    def flip(self):
        self.head = not self.head
        self.flip_image()

    def get_image(self):
        return pygame.transform.rotate(self.image, self.direction * 90)


class Street(GroupBase):
    def __init__(self):
        super().__init__()
        for obj_config in constants.tiles:
            self.objects.append(Tile(*obj_config))

    def draw(self):
        pass

    def shuffle(self):
        pass


class Detective(TokenBase):
    def __init__(self, name, display_name, location, image):
        super().__init__(name, display_name, pygame.image.load(image).convert_alpha(), location)
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


class PoliceDepartment(GroupBase):
    def __init__(self):
        super().__init__()
        for obj_config in constants.detectives:
            self.objects.append(Tile(*obj_config))

    def draw(self):
        pass

    def shuffle(self):
        pass


class Button(TokenBase):
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
        self.image.fill(constants.BLACK)
        font = pygame.font.Font(constants.FONT, 15)
        self.image.blit(font.render(self.display_name, True, constants.WHITE, (0, 0)), (20, 5))


class ActionToken(TokenBase):
    def __init__(self, name, display_name, location, image):
        super(ActionToken, self).__init__(name, display_name, pygame.image.load(image).convert_alpha(), location)
        self.used = False
        self.head = False
        self.callback = name

    def set_location(self, location):
        super(ActionToken, self).set_location(location)

    def get_location(self):
        return super(ActionToken, self).get_location()


class AllActionTokens(GroupBase):
    def __init__(self):
        super().__init__()
        for obj_config in constants.actions:
            self.objects.append(Tile(*obj_config))

    def draw(self):
        pass

    def shuffle(self):
        pass


class Hourglass(TokenBase):
    def __init__(self, name, display_name, location, image, turn):
        super(Hourglass, self).__init__(name, display_name, pygame.image.load(image).convert_alpha(), location)
        self.turn = turn

    def set_location(self, location):
        super(Hourglass, self).set_location(location)

    def get_location(self):
        return super(Hourglass, self).get_location()


class AllHourglasses(GroupBase):
    pass


class GameBoard():
    def __init__(self):
        print("load all from config file")
        self.street = Street()
        self.police_department = PoliceDepartment()
        # pygame related
        self.background_image = pygame.image.load(constants.background_image).convert()
        # init game board size



    def mouse_on(self, mos_pos):
        pass
