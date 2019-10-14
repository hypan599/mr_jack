# -*- coding:utf-8 -*-
import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1560, 920), 0, 32)
font = pygame.font.Font("msyh.ttf", 30)

# color
yellow = 128, 128, 0
grey = 128, 128, 128
white = 255, 255, 255
black = 0, 0, 0


root_path = "images" + os.sep
hourglass = pygame.image.load(root_path + "hourglass.PNG").convert_alpha()
begin = pygame.image.load(root_path + "begin.jpg").convert()
button_mouse_on = pygame.image.load(root_path + "button_mouse_on.PNG").convert_alpha()



map_path = root_path + "tiles" + os.sep
image_dict = {'guaidaojide': {},
              'maolilan': {},
              'huiyuanai': {},
              'aliboshi': {},
              'mumushisan': {},
              'chijingxiuyi': {},
              'beiermode': {},
              'yuanshanheye': {},
              'lingmuyuanzi': {}
              }
states = [str(j) + str(i) for j in range(2) for i in range(4)]  # ['00', '01', '02', '03', '10', '11', '12', '13']
for name, d in image_dict.items():
    for state in states:
        file = map_path + name + state + ".JPG"
        d[name + state] = pygame.image.load(file).convert()
map_mouse_on = pygame.image.load(map_path + "map_mouse_on.PNG").convert_alpha()
map_used = pygame.image.load(map_path + "map_used.PNG").convert_alpha()

detective_path = root_path + "detectives" + os.sep
detective_images = {"kenan": pygame.image.load("images/detectives/detective2.PNG").convert_alpha(),
                    "maolixiaowulang": pygame.image.load("images/detectives/detective3.PNG").convert_alpha(),
                    "fubupingci": pygame.image.load("images/detectives/detective1.PNG").convert_alpha()
                    }
detective_mouse_on = pygame.image.load(detective_path + "detective_mouse_on.PNG").convert_alpha()
detective_available = pygame.image.load(detective_path + "detective_available.PNG").convert_alpha()

action_card_path = root_path + "actions" + os.sep
action_card_images = {
    "1f": pygame.image.load("images/actions/1f.PNG").convert_alpha(),
    "1b": pygame.image.load("images/actions/1b.PNG").convert_alpha(),
    "2f": pygame.image.load("images/actions/2f.PNG").convert_alpha(),
    "2b": pygame.image.load("images/actions/2b.PNG").convert_alpha(),
    "3f": pygame.image.load("images/actions/3f.PNG").convert_alpha(),
    "3b": pygame.image.load("images/actions/3b.PNG").convert_alpha(),
    "4f": pygame.image.load("images/actions/4f.PNG").convert_alpha(),
    "4b": pygame.image.load("images/actions/4b.PNG").convert_alpha()
}
action_mouse_on = pygame.image.load(action_card_path + "action_mouse_on.PNG").convert_alpha()
action_used = pygame.image.load(action_card_path + "action_used.PNG").convert_alpha()

