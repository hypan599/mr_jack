import os

images_dir = "images"
detectives = [
    ("kenan", u"江户川柯南", 11, os.path.join(images_dir, "detectives", "detective1.PNG")),
    ("maolixiaowulang", u"毛利小五郎", 7, os.path.join(images_dir, "detectives", "detective2.PNG")),
    ("fubupingci", u"服部平次", 3, os.path.join(images_dir, "detectives", "detective3.PNG")),
]
tiles = [
    ("aliboshi", u"阿笠博士", 1, os.path.join(images_dir, "tiles", "aliboshi10.JPG")),
    ("maolilan", u"毛利　兰", 2, os.path.join(images_dir, "tiles", "maolilan10.JPG")),
    ("guaidaojide", u"怪盗基德", 1, os.path.join(images_dir, "tiles", "guaidaojide10.JPG")),
    ("huiyuanai", u"灰原　哀", 0, os.path.join(images_dir, "tiles", "huiyuanai10.JPG")),
    ("mumushisan", u"目暮十三", 1, os.path.join(images_dir, "tiles", "mumushisan10.JPG")),
    ("chijingxiuyi", u"赤井秀一", 1, os.path.join(images_dir, "tiles", "chijingxiuyi10.JPG")),
    ("beiermode", u"贝尔摩德", 0, os.path.join(images_dir, "tiles", "beiermode10.JPG")),
    ("yuanshanheye", u"远山和叶", 1, os.path.join(images_dir, "tiles", "yuanshanheye10.JPG")),
    ("lingmuyuanzi", u"铃木园子", 1, os.path.join(images_dir, "tiles", "lingmuyuanzi10.JPG")),
]
background_image = os.path.join(images_dir, "begin.jpg")

available_tile_locations = [(i, j) for i in range(3) for j in range(3)]

yellow = 128, 128, 0
grey = 128, 128, 128
white = 255, 255, 255
black = 0, 0, 0