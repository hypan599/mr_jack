import os

# Font and Color
FONT = "msyh.ttf"
YELLOW = 128, 128, 0
GREY = 128, 128, 128
WHITE = 255, 255, 255
BLACK = 0, 0, 0

# todo: need some math here
# mac screen is 1440 * 900, windows is much higher
# small, medium(current), high
# but we need to recalculate all other dimensions, don't hard code anything!
DIMENSIONS = {
    "SMALL": {},
    "MEDIUM": {
        "WindowHeight": 920,
        "WindowWidth": 1560,
        "TileSize": 240,
        "TilePadding": 0,
        "ActionSize": 100,
        "ActionPadding": 0,
        "ActionMargin": 10,
        "ButtonHeight": 50,
    },
    "LARGE": {
        "WindowHeight": 920,
        "WindowWeight": 1560,
        "TileSize": 240,
        "TilePadding": 0,
        "ActionToken": 100,
        "ActionPadding": 0,
        "ButtonHeight": 50,
    },
}

IMAGE_ROOT = "images"
BACKGROUND_IMAGE = "begin.jpg"

IMAGE_TILES = "tiles"
TILE_MOUSE_ON = "map_mouse_on.PNG"
TILES = [
    {
        "name": "aliboshi",
        "display_name": u"阿笠博士",
        "head_image": "head_tile1.JPG",
        "tail_image": "tail_tile1.JPG",
        "hourglass_num": 1,
        "wall_blocked": [2],
    },
    {
        "name": "xiaolan",
        "display_name": u"毛利　兰",
        "head_image": "head_tile2.JPG",
        "tail_image": "tail_tile2.JPG",
        "wall_blocked": [2],
        "hourglass_num": 2,
    },
    {
        "name": "jide",
        "display_name": u"怪盗基德",
        "head_image": "head_tile3.JPG",
        "tail_image": "tail_tile3.JPG",
        "wall_blocked": [2],
        "hourglass_num": 1,
    },
    {
        "name": "huiyuanai",
        "display_name": u"灰原　哀",
        "head_image": "head_tile4.JPG",
        "tail_image": "tail_tile4.JPG",
        "wall_blocked": [2],
        "hourglass_num": 2,
    },
    {
        "name": "mumushisan",
        "display_name": u"目暮十三",
        "head_image": "head_tile5.JPG",
        "tail_image": "tail_tile5.JPG",
        "wall_blocked": [2],
        "hourglass_num": 1,
    },
    {
        "name": "chijingxiuyi",
        "display_name": u"赤井秀一",
        "head_image": "head_tile6.JPG",
        "tail_image": "tail_tile6.JPG",
        "wall_blocked": [2],
        "hourglass_num": 1,
    },
    {
        "name": "beiermode",
        "display_name": u"贝尔摩德",
        "head_image": "head_tile7.JPG",
        "tail_image": "tail_tile7.JPG",
        "wall_blocked": [2],
        "hourglass_num": 0,
    },
    {
        "name": "yuanshanheye",
        "display_name": u"远山和叶",
        "head_image": "head_tile8.JPG",
        "tail_image": "tail_tile8.JPG",
        "wall_blocked": [2],
        "hourglass_num": 1,
    },
    {
        "name": "lingmuyuanzi",
        "display_name": u"铃木园子",
        "head_image": "head_tile9.JPG",
        "tail_image": "tail_tile9.JPG",
        "wall_blocked": [2],
        "hourglass_num": 1,
    }
]

IMAGE_DETECTIVES = "detectives"

DETECTIVE_MOUSE_ON = "detective_mouse_on.PNG"
DETECTIVES = [
    {
        "name": "kenan",
        "display_name": u"江户川柯南",
        "image": "detective1.PNG",
        "start_position": 11,
    },
    {
        "name": "xiaowulang",
        "display_name": u"毛利小五郎",
        "image": "detective2.PNG",
        "start_position": 7,
    },
    {
        "name": "pingci",
        "display_name": u"服部平次",
        "image": "detective3.PNG",
        "start_position": 3,
    }
]

HOURGALSS = {
    "name": "Hourglass",
    "display_name": "HOURGLASS",
    "image": "hourglass.PNG",
}

IMAGE_ACTION = "actions"
ACTION_MOUSE_ON = "action_mouse_on.PNG"
ACTION_TOKEN = [
    [
        {
            "name": "move3",
            "action": "MOVE3",
            "image": "head_action4.PNG",
        },
        {
            "name": "move2",
            "action": "MOVE2",
            "image": "tail_action4.PNG",
        },
    ],
    [
        {
            "name": "rotate",
            "action": "ROTATE",
            "image": "head_action3.PNG",
        },
        {
            "name": "joker",
            "action": "JOKER",
            "image": "tail_action3.PNG",
        },
    ],
    [
        {
            "name": "alibi",
            "action": "ALIBI",
            "image": "head_action2.PNG",
        },
        {
            "name": "move1",
            "action": "MOVE1",
            "image": "tail_action2.PNG",
        },
    ],
    [
        {
            "name": "rotate",
            "action": "ROTATE",
            "image": "head_action1.PNG",
        },
        {
            "name": "exchange",
            "action": "EXCHANGE",
            "image": "tail_action1.PNG",
        },
    ]
]

# todo: buttons needs some work
BUTTONS = [
    {
        "name": "",
        "display_name": "",
        "Callback": "",
    }
]
buttons = [
    ("start", "START", "start_game"),
    ("confirm", "CONFIRM", "confirm"),
    ("cancel", "CANCEL", "cancel"),
    ("reveal", "REVEAL", "reveal"),

    ("checkpoint", "SAVE", "checkpoint"),
]
