import os

images_dir = "images"
detectives = [
    ("kenan", u"江户川柯南", 11, os.path.join(images_dir, "detectives", "detective1.PNG")),
    ("maolixiaowulang", u"毛利小五郎", 7, os.path.join(images_dir, "detectives", "detective2.PNG")),
    ("fubupingci", u"服部平次", 3, os.path.join(images_dir, "detectives", "detective3.PNG")),
]
tiles = [
    ("aliboshi", u"阿笠博士", 1, [os.path.join(images_dir, "tiles", i + "tile1.JPG") for i in ["tail_", "head_"]]),
    ("maolilan", u"毛利　兰", 2, [os.path.join(images_dir, "tiles", i + "tile2.JPG") for i in ["tail_", "head_"]]),
    ("guaidaojide", u"怪盗基德", 1, [os.path.join(images_dir, "tiles", i + "tile3.JPG") for i in ["tail_", "head_"]]),
    ("huiyuanai", u"灰原　哀", 0, [os.path.join(images_dir, "tiles", i + "tile4.JPG") for i in ["tail_", "head_"]]),
    ("mumushisan", u"目暮十三", 1, [os.path.join(images_dir, "tiles", i + "tile5.JPG") for i in ["tail_", "head_"]]),
    ("chijingxiuyi", u"赤井秀一", 1, [os.path.join(images_dir, "tiles", i + "tile6.JPG") for i in ["tail_", "head_"]]),
    ("beiermode", u"贝尔摩德", 0, [os.path.join(images_dir, "tiles", i + "tile7.JPG") for i in ["tail_", "head_"]]),
    ("yuanshanheye", u"远山和叶", 1, [os.path.join(images_dir, "tiles", i + "tile8.JPG") for i in ["tail_", "head_"]]),
    ("lingmuyuanzi", u"铃木园子", 1, [os.path.join(images_dir, "tiles", i + "tile9.JPG") for i in ["tail_", "head_"]]),
]

buttons = [
    ("start", "START", "start_game"),
    ("confirm", "CONFIRM", "confirm"),
    ("cancel", "CANCEL", "cancel"),
    ("reveal", "REVEAL", "reveal"),

    ("checkpoint", "SAVE", "checkpoint"),
]
actions = [
    ("rotate", "ROTATE", 0,     os.path.join(images_dir, "actions", "head_action1.PNG")),
    ("exchange", "EXCHANGE", 0, os.path.join(images_dir, "actions", "tail_action1.PNG")),
    ("alibi", "ALIBI", 1,       os.path.join(images_dir, "actions", "head_action2.PNG")),
    ("move1", "MOVE1", 1,       os.path.join(images_dir, "actions", "tail_action2.PNG")),
    ("rotate", "ROTATE", 2,     os.path.join(images_dir, "actions", "head_action3.PNG")),
    ("joker", "JOKER", 2,       os.path.join(images_dir, "actions", "tail_action3.PNG")),
    ("move3", "MOVE3", 3,       os.path.join(images_dir, "actions", "head_action4.PNG")),
    ("move2", "MOVE2", 3,       os.path.join(images_dir, "actions", "tail_action4.PNG")),
]
background_image = os.path.join(images_dir, "begin.jpg")

available_tile_locations = [(i, j) for i in range(3) for j in range(3)]
font = "msyh.ttf"
yellow = 128, 128, 0
grey = 128, 128, 128
white = 255, 255, 255
black = 0, 0, 0
