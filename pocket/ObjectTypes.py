import random
import pygame
from constants import *


class Dimension:
    def __init__(self, size):
        _d = DIMENSIONS[size]
        self.window_height = _d["WindowHeight"]
        self.window_width = _d["WindowWidth"]
        self.tile_size = _d["TileSize"]
        self.tile_padding = _d["TilePadding"]
        self.tile_margin = (self.window_height - self.tile_size * 3 - self.tile_padding) // 2

        self.action_size = _d["ActionSize"]
        self.action_padding = _d["ActionPadding"]
        self.action_margin = _d["ActionMargin"]
        self.action_width = self.action_size + self.action_margin * 2

        self.button_height = _d["ButtonHeight"]
        self.game_area_width = self.window_height + self.action_width


class GroupBase:
    def __init__(self):
        self.objects = []
        self.can_hover = True

    def draw(self, surface, mouse_pos):
        raise NotImplementedError('subclasses must override draw()!')

    # shuffle logic is special for each group
    def shuffle(self):
        raise NotImplementedError('subclasses must override shuffle()!')

    def reset(self):
        for i in self.objects:
            i.reset()

    def size(self):
        return len(self.objects)

    def is_mouse_in(self, mouse_pos, obj_pos, obj_size):
        return obj_pos[0] < mouse_pos[0] < obj_pos[0] + obj_size \
               and obj_pos[1] < mouse_pos[1] < obj_pos[1] + obj_size


class TokenBase:
    def __init__(self, name, display_name, image, location):
        self.name = name
        self.display_name = display_name
        self.image = image
        self.location = location
        self.show = False

    def __str__(self):
        return "Token: " + self.name

    def reset(self):
        raise NotImplementedError('subclasses must override reset()!')


class Tile(TokenBase):
    def __init__(self, name, display_name, hourglass_num, head_image, tail_image, wall_blocked):
        super(Tile, self).__init__(name, display_name, None, (0, 0))
        self.hourglass_num = hourglass_num
        self.head = True  # false for tail
        self.is_suspect = 1
        self.is_visible = 0
        self.images = [pygame.image.load(os.path.join(IMAGE_ROOT, IMAGE_TILES, tail_image)).convert(),
                       pygame.image.load(os.path.join(IMAGE_ROOT, IMAGE_TILES, head_image)).convert()]
        self.location = None
        self.pixel_loc = None
        self.direction = 0
        self.wall_blocked = wall_blocked

    def __str__(self):
        return "Tile: " + super(Tile, self).__str__()

    def rotate(self, count):  # counterclockwise
        self.direction += count
        self.direction %= 4
        self.set_tile_image(pygame.transform.rotate(self.get_tile_image(), count * 90))

    def flip(self):
        self.head = not self.head

    def get_tile_image(self):
        return self.images[int(self.head)]

    def set_tile_image(self, image):
        self.images[int(self.head)] = image

    def random_direction(self):
        self.rotate(random.randint(0, 3))

    def reset(self):
        pass


class Street(GroupBase):
    def __init__(self, dimension):
        super().__init__()
        self.dimension = dimension
        self.available_tile_locations = [(i, j) for i in range(3) for j in range(3)]
        random.shuffle(self.available_tile_locations)
        self.hover_image = pygame.image.load(os.path.join(IMAGE_ROOT, IMAGE_TILES, TILE_MOUSE_ON)).convert_alpha()

        for idx, loc in enumerate(self.available_tile_locations):
            tile = Tile(**TILES[idx])
            tile.random_direction()
            tile.location = loc
            tile.pixel_loc = (dimension.tile_margin + (dimension.tile_padding + dimension.tile_size) * loc[0],
                              dimension.tile_margin + (dimension.tile_padding + dimension.tile_size) * loc[1])
            self.objects.append(tile)

    def draw(self, surface, mouse_pos):
        for obj in self.objects:
            obj_pos = obj.pixel_loc
            surface.blit(obj.get_tile_image(), obj.pixel_loc)
            # if obj in self.game_state.clickable and self.is_mouse_in(mouse_pos, obj_pos, self.dimension.tile_size):
            if self.is_mouse_in(mouse_pos, obj_pos, self.dimension.tile_size):
                surface.blit(self.hover_image, obj_pos)

    def shuffle(self):
        dimension = self.dimension
        random.shuffle(self.available_tile_locations)
        for idx, loc in enumerate(self.available_tile_locations):
            self.objects[idx].location = loc
            self.objects[idx].pixel_loc = (
                dimension.tile_margin + (dimension.tile_padding + dimension.tile_size) * loc[0],
                dimension.tile_margin + (dimension.tile_padding + dimension.tile_size) * loc[1])

    def get_affected(self, position):
        if position[0] == 0:
            from_direction = 1  # "left"
            offset = position[1]
        elif position[0] == self.dimension.window_height - self.dimension.tile_margin:
            from_direction = 3  # "right"
            offset = position[1]
        elif position[1] == 0:
            from_direction = 0  # "up"
            offset = position[0]
        else:  # position[1] == self.dimension.window_height - self.dimension.tile_margin:
            from_direction = 2  # "down"
            offset = position[0]
        offset = (offset - self.dimension.tile_margin // 2 - self.dimension.tile_size // 2) \
                 // (self.dimension.tile_padding + self.dimension.tile_size)
        if from_direction == 0:
            affected = [(offset, i) for i in range(3)]
        elif from_direction == 1:
            affected = [(i, offset) for i in range(3)]
        elif from_direction == 2:
            affected = [(offset, i) for i in range(2, -1, -1)]
        else:  # from_direction == 3
            affected = [(i, offset) for i in range(2, -1, -1)]
        return from_direction, affected

    def get_visible_from(self, position):
        from_direction, affected = self.get_affected(position)

        loc2tile = {o.location: o for o in self.objects}
        get_opposite = lambda x: 4 - x if x // 2 else 2 - x
        visible = set()
        for loc in affected:
            tile = loc2tile[loc]
            view_from = (from_direction - tile.direction) % 4
            opposite = get_opposite(view_from)
            if view_from in tile.wall_blocked:
                break  # can see nothing
            elif opposite in tile.wall_blocked:
                visible.add(tile)
                break  # can see only him self
            else:
                visible.add(tile)
        return visible


class Detective(TokenBase):
    def __init__(self, name, display_name, start_position, image):
        super().__init__(name, display_name,
                         pygame.image.load(os.path.join(IMAGE_ROOT, IMAGE_DETECTIVES, image)).convert_alpha(),
                         start_position)
        self.init_location = start_position

    def advance(self, step=1):
        self.location += step
        self.location %= 12

    def reset(self):
        self.location = self.init_location


class PoliceDepartment(GroupBase):
    def __init__(self, dimension):
        super().__init__()
        for obj_config in DETECTIVES:
            self.objects.append(Detective(**obj_config))
        self.dimension = dimension
        self.hover_image = pygame.image.load(os.path.join(IMAGE_ROOT, IMAGE_DETECTIVES, DETECTIVE_MOUSE_ON)).convert_alpha()

        x0 = dimension.tile_margin // 2 + dimension.tile_size // 2
        xs = [x0 + i * (dimension.tile_padding + dimension.tile_size) for i in (0, 1, 2)]
        y = dimension.window_height - dimension.tile_margin
        positions = []
        positions += [(x, 0) for x in xs]
        positions += [(y, x) for x in xs]
        positions += [(x, y) for x in reversed(xs)]
        positions += [(0, x) for x in reversed(xs)]
        self.positions = positions

    def draw(self, surface, mouse_pos):
        for obj in self.objects:
            obj_pos = self.positions[obj.location]
            surface.blit(obj.image, obj_pos)
            if obj_pos[0] < mouse_pos[0] < obj_pos[0] + self.dimension.tile_margin \
                    and obj_pos[1] < mouse_pos[1] < obj_pos[1] + self.dimension.tile_margin:
                surface.blit(self.hover_image, obj_pos)

    def shuffle(self):
        pass

    def advance(self, idx):
        if idx <3:
            self.objects[idx].advance()


class Button(TokenBase):
    def __init__(self, name, display_name, callback, size=(100, 50)):
        super(Button, self).__init__(name, display_name, None, 0)
        self.callback = callback
        self.size = size

    def update_image(self):
        # no need for rect, black background is enough
        # pygame.Rect(self.location * button_size[0], 0, button_size[0], button_size[1])
        self.image = pygame.Surface(self.size)
        self.image.fill(BLACK)
        font = pygame.font.Font(FONT, 15)
        self.image.blit(font.render(self.display_name, True, WHITE, (0, 0)), (20, 5))


class AllButtons(GroupBase):
    def __init__(self):
        super().__init__()

    def draw(self, surface, mouse_pos):
        pass


class ActionToken(TokenBase):
    def __init__(self, name, action, image, location=None):
        super(ActionToken, self).__init__(name, name, pygame.image.load(
            os.path.join(IMAGE_ROOT, IMAGE_ACTION, image)).convert_alpha(), location)
        self.used = False
        self.head = False
        self.action = action
        self.callback = name


class AllActionTokens(GroupBase):
    def __init__(self, dimension):
        super().__init__()
        self.dimension = dimension
        x = dimension.window_height + dimension.action_margin
        self.positions = [(x, i * (dimension.action_size + dimension.action_padding) + dimension.action_margin)
                          for i in range(4)]
        self.all_objects = []
        action = None
        for idx, pair in enumerate(ACTION_TOKEN):
            actions = []
            for p in pair:
                action = ActionToken(**p)
                action.pixel_loc = self.positions[idx]
                action.location = idx
                actions.append(action)
            self.all_objects.append(actions)
            self.objects.append(action)
        self.side = [0] * 4
        self.shuffle()

    def draw(self, surface, mouse_pos):
        for obj in self.objects:
            surface.blit(obj.image, obj.pixel_loc)

    def shuffle(self):
        for i in range(len(self.side)):
            self.side[i] = int(random.random() > 0.5)
            self.objects[i] = self.all_objects[i][self.side[i]]


class Hourglass:
    def __init__(self, name, display_name, image):
        self.name = name
        self.display_name = display_name
        self.image = os.path.join(IMAGE_ROOT, image)