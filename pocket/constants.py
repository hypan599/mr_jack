import os

# todo: move this to street class
available_tile_locations = [(i, j) for i in range(3) for j in range(3)]

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
        "Window": (1560, 920),
        "BoardArea": (1060, 920),
        "StreetTile": (1060, 920),
        "ActionToken": (1060, 920),
        "Detective": (1060, 920),
        "Prompt": (1060, 920),
        "Button": (100, 50),
    },
    "LARGE": {},
}

IMAGE_ROOT = "images"
BACKGROUND_IMAGE = "begin.jpg"

IMAGE_TILES = "tiles"
TILE_MOUSE_ON = "map_mouse_on.PNG"
TILES = [
    {
        "Name": "aliboshi",
        "DisplayName": u"阿笠博士",
        "HeadImage": "head_tile1.JPG",
        "TailImage": "tail_tile1.JPG",
        "Hourglass": 1,
    },
    {
        "Name": "xiaolan",
        "DisplayName": u"毛利　兰",
        "HeadImage": "head_tile2.JPG",
        "TailImage": "tail_tile2.JPG",
        "Hourglass": 2,
    },
    {
        "Name": "jide",
        "DisplayName": u"怪盗基德",
        "HeadImage": "head_tile3.JPG",
        "TailImage": "tail_tile3.JPG",
        "Hourglass": 1,
    },
    {
        "Name": "huiyuanai",
        "DisplayName": u"灰原　哀",
        "HeadImage": "head_tile4.JPG",
        "TailImage": "tail_tile4.JPG",
        "Hourglass": 2,
    },
    {
        "Name": "mumushisan",
        "DisplayName": u"目暮十三",
        "HeadImage": "head_tile5.JPG",
        "TailImage": "tail_tile5.JPG",
        "Hourglass": 1,
    },
    {
        "Name": "chijingxiuyi",
        "DisplayName": u"赤井秀一",
        "HeadImage": "head_tile6.JPG",
        "TailImage": "tail_tile6.JPG",
        "Hourglass": 1,
    },
    {
        "Name": "beiermode",
        "DisplayName": u"贝尔摩德",
        "HeadImage": "head_tile7.JPG",
        "TailImage": "tail_tile7.JPG",
        "Hourglass": 0,
    },
    {
        "Name": "yuanshanheye",
        "DisplayName": u"远山和叶",
        "HeadImage": "head_tile8.JPG",
        "TailImage": "tail_tile8.JPG",
        "Hourglass": 1,
    },
    {
        "Name": "lingmuyuanzi",
        "DisplayName": u"铃木园子",
        "HeadImage": "head_tile9.JPG",
        "TailImage": "tail_tile9.JPG",
        "Hourglass": 1,
    }
]

IMAGE_DETECTIVES = "detectives"
DETECTIVE_MOUSE_ON = "detective_mouse_on.PNG"
DETECTIVES = [
    {
        "Name": "kenan",
        "DisplayName": u"江户川柯南",
        "Image": "detective1.PNG",
        "StartPosition": 11,
    },
    {
        "Name": "xiaowulang",
        "DisplayName": u"毛利小五郎",
        "Image": "detective2.PNG",
        "StartPosition": 7,
    },
    {
        "Name": "pingci",
        "DisplayName": u"服部平次",
        "Image": "detective3.PNG",
        "StartPosition": 3,
    }
]

HOURGALSS = {
    "Name": "Hourglass",
    "DisplayName": "HOURGLASS",
    "Image": "hourglass.PNG",
}

IMAGE_ACTION = "actions"
ACTION_MOUSE_ON = "action_mouse_on.PNG"
ACTION_TOKEN = [
    [
        {
            "Name": "move3",
            "Action": "MOVE3",
            "Image": "head_action4.PNG",
        },
        {
            "Name": "move2",
            "Action": "MOVE2",
            "Image": "tail_action4.PNG",
        },
    ],
    [
        {
            "Name": "rotate",
            "Action": "ROTATE",
            "Image": "head_action3.PNG",
        },
        {
            "Name": "joker",
            "Action": "JOKER",
            "Image": "tail_action3.PNG",
        },
    ],
    [
        {
            "Name": "alibi",
            "Action": "ALIBI",
            "Image": "head_action2.PNG",
        },
        {
            "Name": "move1",
            "Action": "MOVE1",
            "Image": "tail_action2.PNG",
        },
    ],
    [
        {
            "Name": "rotate",
            "Action": "ROTATE",
            "Image": "head_action1.PNG",
        },
        {
            "Name": "exchange",
            "Action": "EXCHANGE",
            "Image": "tail_action1.PNG",
        },
    ]
]


# todo: buttons needs some work
BUTTONS = [
    {
        "Name": "",
        "DisplayName": "",
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
