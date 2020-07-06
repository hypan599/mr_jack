# -*- coding:utf-8 -*-
import sys
import pygame
import random
from types import MethodType
from operator import xor
from image import *

log_file = "log.txt"
# direction : u, r, d, l = 0, 1, 2, 3
# suspect: True, False = 1, 0
# oldtodo: select all detectives 时候的两个侦探挨着的问题

f = open(log_file, "w")


class Map:
    def __init__(self, name, chinese_name, hourglass_num):
        global person_list
        self.name = name
        self.hourglass_num = hourglass_num
        self.chinese_name = chinese_name
        self.direction = random.randint(0, 3)
        self.suspect = 1
        self.seen = 0
        self.state = str(self.suspect) + str(self.direction)
        self.pos = (0, 0)
        self.image = image_dict[self.name][self.name + self.state]
        person_list.append(self)
        suspect_people.append(self)

    def __str__(self):
        return self.chinese_name

    def rotate(self, direc=0):
        if direc:
            self.direction = direc
        else:
            self.direction = (self.direction + 1) % 4
        self.state = str(self.suspect) + str(self.direction)
        self.image = image_dict[self.name][self.name + self.state]

    def set_direction(self, direc):
        self.direction = direc
        self.state = str(self.suspect) + str(self.direction)
        self.image = image_dict[self.name][self.name + self.state]

    def set_suspect(self, susp):
        self.suspect = susp
        self.state = str(self.suspect) + str(self.direction)
        self.image = image_dict[self.name][self.name + self.state]

    def get_location(self):
        return 100 + 240 * self.pos[0], 100 + 240 * self.pos[1]


class Detective:
    def __init__(self, name, chinese_name, pos):
        self.name = name
        self.chinese_name = chinese_name
        self.location = pos
        self.image = detective_images[self.name]
        detective_list.append(self)

    def get_location(self, bias=0):
        positions_for_detective = [(170, 0), (410, 0), (650, 0), (820, 170), (820, 410), (820, 650), (650, 820),
                                   (410, 820),
                                   (170, 820), (0, 650), (0, 410), (0, 170)]
        pos_dict = dict(zip(list(range(12)), positions_for_detective))
        return pos_dict[(self.location + bias) % 12]

    def can_reach(self, loc, l=2):
        if loc < self.location:
            loc += 12
        if 0 < loc - self.location < l + 1:
            return True
        else:
            return False

    def go_back(self):
        if self.name == "kenan":
            self.location = 11
        elif self.name == "maolixiaowulang":
            self.location = 7
        else:
            self.location = 3


class Button:
    def __init__(self, name, prompt, pos):
        self.name = name
        self.prompt = prompt
        self.pos = pos
        self.area = pos[0], pos[1], 100, 50
        button_list.append(self)


class ActionCards:
    def __init__(self, name, pos):
        self.name = name
        self.used = False
        self.face = "f"
        self.pos = pos
        actioncard_list.append(self)

    def get_image(self):
        if self.face == "f":
            return action_card_images[self.name[-1] + "f"]
        else:
            return action_card_images[self.name[-1] + "b"]

    def get_location(self):
        return self.pos

    def throw(self):
        self.face = "f" if random.randint(0, 1) == 1 else "b"
        self.used = False

    def turn_over(self):
        if self.face == "b":
            self.face = "f"
            self.used = False
        else:
            self.face = "b"
            self.used = False


def draw_board():
    pygame.draw.rect(screen, black, (0, 0, 1560, 920))

    if winner:
        screen.blit(font.render(u"杰克" if winner == "j" else u"侦探" + u"胜利！抓住了：" + jack.chinese_name,
                                True, white, (0, 0)), (1080, 50))
    elif game_start:
        screen.blit(begin, (0, 0))
        for p in person_list:
            screen.blit(p.image, p.get_location())
        for d in detective_list:
            screen.blit(d.image, d.get_location())
        for c in actioncard_list:
            screen.blit(c.get_image(), c.get_location())
            if c.used:
                screen.blit(action_used, c.get_location())

        # draw_prompt
        def draw_flags(person, num, height):
            screen.blit(font.render(u"杰克标记" if person == "j" else u"侦探标记", True, white, (0, 0)), (1080, height))
            for i in range(num):
                screen.blit(hourglass, (1210 + i * 60, height))

        if not show_jack:
            if turn_over:
                screen.blit(font.render(u"第%d回合结束" % turn, True, white, (0, 0)), (1080, 50))
            else:
                turn_prompt = u"现在是第%d回合，第%s轮，%s行动" % (turn, play_count + 1, u"杰克" if not player else u"侦探")
                screen.blit(font.render(turn_prompt, True, white, (0, 0)), (1080, 50))
        else:
            screen.blit(font.render(u"真凶是：" + jack.chinese_name, True, white, (0, 0)), (1080, 50))
        draw_flags("j", jack_flags, 100)
        draw_flags("d", detec_flags, 160)
        jack_status = {0: u"未知", 1: u"隐藏。杰克标记+1", 2: u"可见。侦探标记+1"}
        screen.blit(font.render(u"杰克状态：" + jack_status[jack_state], True, white, (0, 0)), (1080, 220))

        def show_prompt():
            if game_processing:
                screen.blit(font.render(u"选择行动牌以行动", True, white, (0, 0)), (1080, 300))
                screen.blit(font.render(u"杰克玩家可以随时按下j以查看真凶", True, white, (0, 0)), (1080, 350))
            if acting:
                if select_detective:
                    screen.blit(font.render(u"选择行动1步或两步", True, white, (0, 0)), (1080, 300))
                if original and not select_detective and selected_detective:
                    screen.blit(font.render(u"按下确认以继续，或者按取消重来", True, white, (0, 0)), (1080, 350))
                if rotate_map and not selected_map:
                    screen.blit(font.render(u"选择一个人物以旋转", True, white, (0, 0)), (1080, 300))
                if rotate_map and selected_map:
                    screen.blit(font.render(u"多次点击以旋转不同角度", True, white, (0, 0)), (1080, 300))
                    screen.blit(font.render(u"按下确认以继续，或者按取消重来", True, white, (0, 0)), (1080, 350))
                if exchange_map and not exchange_selected_a:
                    screen.blit(font.render(u"选择一个人", True, white, (0, 0)), (1080, 300))
                if exchange_selected_a and not exchanged:
                    screen.blit(font.render(u"选择另一个人", True, white, (0, 0)), (1080, 300))
                if exchanged:
                    screen.blit(font.render(u"按下确认以继续，或者按取消重来", True, white, (0, 0)), (1080, 300))
                if select_all_detective:
                    screen.blit(font.render(u"选择任意侦探以令所有人归位", True, white, (0, 0)), (1080, 300))
                    screen.blit(font.render(u"或者选择空地使一个人前进一格", True, white, (0, 0)), (1080, 350))
                if select_all_done:
                    screen.blit(font.render(u"按下确认以继续，或者按取消重来", True, white, (0, 0)), (1080, 300))
                if innocent:
                    screen.blit(font.render(u"排除了" + str(innocent) + u"。按确定继续", True, white, (0, 0)), (1080, 300))
                    if not player:
                        screen.blit(font.render(u"杰克获得%d个沙漏" % innocent.hourglass_num, True, white, (0, 0)),
                                    (1080, 350))
            if turn_over:
                screen.blit(font.render(u"回合%d结束" % turn, True, white, (0, 0)), (1080, 350))

        show_prompt()

        if acting:
            if select_detective:
                screen.blit(detective_available, selected_detective.get_location(1))
                screen.blit(detective_available, selected_detective.get_location(2))

            if selected_map:  # tiles selected images
                screen.blit(map_used, selected_map.get_location())
            if exchange_selected_a and not exchanged:  # exchange highlight images
                screen.blit(map_used, exchange_selected_a.get_location())
            if select_all_detective:
                for d in detective_list:
                    screen.blit(detective_available, d.get_location())
                    screen.blit(detective_available, d.get_location(1))

        # live witness
        for i, p in enumerate(person_list):
            screen.blit(
                    pygame.font.Font("msyh.ttf", 20).render(p.chinese_name + (u"  ：可见" if p.seen else u"  :不可见"), True,
                                                            white, (0, 0)), (1080, 500 + i * 30))

    elif debugging:  # saved for debug
        print("hh")
        # test_draw(p)
    else:
        screen.blit(font.render(u"按开始以开始游戏", True, white, (0, 0)), (1080, 300))

    # draw_buttons
    for b in button_list:
        prompt_area = b.pos[0] + 20, b.pos[1] + 5
        pygame.draw.rect(screen, grey, b.area)
        screen.blit(font.render(b.prompt, True, white, (0, 0)), prompt_area)

    # draw_mouse_highlight
    mouse = pygame.mouse.get_pos()
    mouse_place, obj = where_mouse(mouse)
    if not acting:
        if mouse_place == "button":  # soecial case for different phrase
            screen.blit(button_mouse_on, obj.pos)
        if mouse_place == "action" and game_processing and not obj.used:
            screen.blit(action_mouse_on, obj.pos)
    else:  # acting
        if mouse_place == "button":  # soecial case for different phrase
            screen.blit(button_mouse_on, obj.pos)
        if select_detective and mouse_place == "detectives" and selected_detective.can_reach(obj):
            screen.blit(detective_mouse_on, selected_detective.get_location(obj - selected_detective.location))
        if rotate_map and mouse_place == "tiles" and not selected_map:
            screen.blit(map_mouse_on, obj.get_location())
        elif rotate_map and mouse_place == "tiles" and selected_map and obj == selected_map:
            screen.blit(map_mouse_on, obj.get_location())
        if exchange_map and mouse_place == "tiles" and not exchanged:
            if exchange_selected_a and not obj == exchange_selected_a:
                screen.blit(map_mouse_on, obj.get_location())
            elif not exchange_selected_a:
                screen.blit(map_mouse_on, obj.get_location())
        if select_all_detective and mouse_place == "detectives":
            for d in detective_list:
                if obj == d.location:
                    screen.blit(detective_mouse_on, d.get_location())
                elif obj - d.location == 1 or obj - d.location == -11:
                    screen.blit(detective_mouse_on, d.get_location(1))


def where_mouse(mouse):
    if mouse[0] > 1060:  # in right button side
        if mouse[1] < 50:
            button_num = (mouse[0] - 1060) // 100
            return "button", button_list[button_num]
        else:
            return "prompt_area", 0
    elif mouse[0] > 920:  # in actioncard area
        if mouse[1] < 400:
            return "action", actioncard_list[mouse[1] // 100]
        else:
            return "invalid", 0
    else:  # board area
        if mouse[0] < 100:
            if 170 < mouse[1] < 270:
                return "detectives", 11
            elif 410 < mouse[1] < 510:
                return "detectives", 10
            elif 650 < mouse[1] < 750:
                return "detectives", 9
            else:
                return "invalid", 0
        elif mouse[0] > 820:
            if 170 < mouse[1] < 270:
                return "detectives", 3
            elif 410 < mouse[1] < 510:
                return "detectives", 4
            elif 650 < mouse[1] < 750:
                return "detectives", 5
            else:
                return "invalid", 0
        elif mouse[1] < 100:
            if 170 < mouse[0] < 270:
                return "detectives", 0
            elif 410 < mouse[0] < 510:
                return "detectives", 1
            elif 650 < mouse[0] < 750:
                return "detectives", 2
            else:
                return "invalid", 0
        elif mouse[1] > 820:
            if 170 < mouse[0] < 270:
                return "detectives", 8
            elif 410 < mouse[0] < 510:
                return "detectives", 7
            elif 650 < mouse[0] < 750:
                return "detectives", 6
            else:
                return "invalid", 0
        else:  # tiles area
            x = (mouse[0] - 100) // 240
            y = (mouse[1] - 100) // 240
            for p in person_list:
                if p.pos == (x, y):
                    return "tiles", p
            return "invalid", 0


# def test_draw(p):
#     states = [str(1) + str(i) for i in range(4)]
#     locs = [(i, j) for i in range(3) for j in range(3)]
#     locs.pop()
#     for s, l in zip(states, locs):
#         # print(p.name+s)
#         screen.blit(image_dict[p.name][p.name + s], map_loc2pos(l))


def update_action(t):
    if not t:
        for c in actioncard_list:
            c.turn_over()
            c.used = False
    else:
        for c in actioncard_list:
            c.throw()
            c.used = False


def play_once():
    global play_count, player, turn, game_processing, turn_over
    play_count += 1
    if play_count % 2 == 1:
        player = not player
    if play_count == 4:
        turn_over = True
        game_processing = False
        update_witness()


def update_witness():
    def get_person_from_id(i):
        x = i // 3
        y = i % 3
        for p in person_list:
            if p.pos == (x, y):
                return p
        return None

    for p in person_list:
        p.seen = 0
    global jack_state
    wit_dict = {
        0:  (0, 1, 2, -2),
        1:  (3, 4, 5, -2),
        2:  (6, 7, 8, -2),
        3:  (6, 3, 0, -3),
        4:  (7, 4, 1, -3),
        5:  (8, 5, 2, -3),
        6:  (8, 7, 6, 0),
        7:  (5, 4, 3, 0),
        8:  (2, 1, 0, 0),
        9:  (2, 5, 8, -1),
        10: (1, 4, 7, -1),
        11: (0, 3, 6, -1)
    }
    for d in detective_list:
        vision = wit_dict[d.location][0:3]
        direction = wit_dict[d.location][3]
        for i in vision:
            if get_person_from_id(i):
                if get_person_from_id(i).direction + direction == 0:
                    break
                elif abs(get_person_from_id(i).direction + direction) == 2:
                    get_person_from_id(i).seen = 1
                    break
                get_person_from_id(i).seen = 1
    jack_state = 2 if jack.seen else 1


def update_seen():
    global jack_flags, detec_flags
    if jack.seen:
        detec_flags += 1
    else:
        jack_flags += 1
    for p in person_list:
        if p == jack:
            continue
        if p.seen != jack.seen and p.suspect == 1:
            p.set_suspect(0)
            suspect_people.remove(p)


def start_game():
    def shuffle():
        global person_list
        locations = [(i, j) for i in range(3) for j in range(3)]
        random.shuffle(person_list)
        for player, location in zip(person_list, locations):
            player.set_suspect(1)
            player.pos = location
            player.set_direction(random.randint(0, 3))
        person_list[0].set_direction(1)
        person_list[6].set_direction(3)
        person_list[5].set_direction(0)
        global actioncard_list
        for c in actioncard_list:
            c.throw()

    global turn, play_count, player, jack, jack_flags, detec_flags, jack, card_using, jack_state, \
        show_jack, original, game_processing, jack_win, detective_win
    turn = 1
    play_count = 0
    player = 1
    jack_flags = 0
    detec_flags = 0
    jack = None
    card_using = None
    jack_state = 0  # 0: unknown, 1: unseen 2: seen
    show_jack = False
    original = None
    winner = None
    for d in detective_list:
        d.go_back()

    global suspect_people, innocent_people, unexcluded_people
    shuffle()
    jack = random.choice(person_list)
    for p in person_list:
        if p not in suspect_people:
            suspect_people.append(p)
        if p not in unexcluded_people:
            unexcluded_people.append(p)
    suspect_people.remove(jack)
    unexcluded_people.remove(jack)
    # update_innocent(jack, "jack")  # oldtodo: update:innocent
    turn = 1
    play_count = 0
    game_processing = True


innocent_people = []
suspect_people = []
unexcluded_people = []
person_list = []
innocent = None
aliboshi = Map("aliboshi", u"阿笠博士", 1)
maolilan = Map("maolilan", u"毛利　兰", 2)
guaidaojide = Map("guaidaojide", u"怪盗基德", 1)
huiyuanai = Map("huiyuanai", u"灰原　哀", 0)
mumushisan = Map("mumushisan", u"目暮十三", 1)
chijingxiuyi = Map("chijingxiuyi", u"赤井秀一", 1)
beiermode = Map("beiermode", u"贝尔摩德", 0)
yuanshanheye = Map("yuanshanheye", u"远山和叶", 1)
lingmuyuanzi = Map("lingmuyuanzi", u"铃木园子", 1)

detective_list = []
kenan =             Detective("kenan", u"江户川柯南", 11)
maolixiaowulang =   Detective("maolixiaowulang", u"毛利小五郎", 7)
fubupingci =        Detective("fubupingci", u"服部平次", 3)

button_list = []
start = Button("start", u"开始", (1060, 0))
cancel = Button("cancel", u"取消", (1160, 0))
over = Button("over", u"结束", (1260, 0))
quit_game = Button("quit", u"退出", (1360, 0))
ok = Button("ok", u"确认", (1460, 0))


def use_card_c1(self, face):
    global rotate_map, exchange_map, card_using
    if face == "f":
        rotate_map = True
        card_using = "1f"
    else:
        exchange_map = True
        card_using = "1b"


def use_card_c2(self, face):
    global card_using
    if face == "b":
        global select_detective, selected_detective
        select_detective = True
        selected_detective = detective_list[0]
        card_using = "2b"
    else:
        card_using = "2f"
        global jack_flags, detec_flags, innocent, original, unexcluded_people, suspect_people
        innocent = random.choice(unexcluded_people)
        unexcluded_people.remove(innocent)
        if innocent in suspect_people:
            suspect_people.remove(innocent)
        if not player:
            jack_flags += innocent.hourglass_num
        original = 1
        # oldtodo: check one innocent


def use_card_c3(self, face):
    global card_using
    if face == "f":
        global rotate_map
        rotate_map = True
        card_using = "3f"
    else:
        global select_all_detective
        select_all_detective = True
        card_using = "3b"


def use_card_c4(self, face):  # f: fubupingci, b : maolixiaowulang
    global select_detective, selected_detective, card_using
    select_detective = True
    selected_detective = detective_list[1] if face == "b" else detective_list[2]
    card_using = "4" + face


actioncard_list = []
c1 = ActionCards("card1", (940, 0))
c2 = ActionCards("card2", (940, 100))
c3 = ActionCards("card3", (940, 200))
c4 = ActionCards("card4", (940, 300))
c1.use_card = MethodType(use_card_c1, c1)
c2.use_card = MethodType(use_card_c2, c2)
c3.use_card = MethodType(use_card_c3, c3)
c4.use_card = MethodType(use_card_c4, c4)

# global flags
winner = None
jack_win = False
detective_win = False
turn = 1
play_count = 0
player = 1
jack_flags = 0
detec_flags = 0
jack = None
card_using = None
jack_state = 0  # 0: unknown, 1: unseen 2: seen
show_jack = False
original = None

turn_over = False
acting = False
game_processing = False
game_start = False
debugging = False

select_detective = False
select_all_detective = False
select_all_done = False
selected_detective = None

rotate_map = False
selected_map = None
exchange_map = False
exchange_selected_a = None
exchange_selected_b = None
exchanged = False

# events
CANCEL = pygame.USEREVENT + 2  # restart event, used for restart
DEBUGGER = pygame.USEREVENT + 3  # debugger event, not used in game
START = pygame.USEREVENT + 1  # game start event
OVER = pygame.USEREVENT + 4  # undo event
OK = pygame.USEREVENT + 5  # OK in acting
JACKWIN = pygame.USEREVENT + 6
DETECTIVEWIN = pygame.USEREVENT + 7

mouse_event_dict = {
    "start":  pygame.event.Event(START),
    "cancel": pygame.event.Event(CANCEL),
    "quit":   pygame.event.Event(pygame.QUIT),
    "over":   pygame.event.Event(OVER),
    "ok":     pygame.event.Event(OK)
}

while True:
    draw_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == JACKWIN:
            game_processing = False
            game_start = False
            winner = "j"
        elif event.type == DETECTIVEWIN:
            game_processing = False
            game_start = False
            winner = "d"
        elif event.type == CANCEL:
            if original:
                if selected_detective:
                    selected_detective.location = original
                    select_detective = True
                    original = None
                if rotate_map:
                    selected_map.rotate(original - 1)
                    selected_map = None
                    original = None
                if exchanged:
                    exchange_selected_a.pos = original[0]
                    exchange_selected_b.pos = original[1]
                    original = None
                    exchange_selected_a = None
                    exchanged = False
                if select_all_done:
                    if all_back:
                        detective_list[0].location = original[0]
                        detective_list[1].location = original[1]
                        detective_list[2].location = original[2]
                        original = None
                        select_all_detective = True
                        select_all_done = False
                    elif one_forward:
                        one_forward.location = original
                        original = None
                        select_all_detective = True
                        select_all_done = False
            update_witness()
        elif event.type == OK:
            if turn_over:
                player = not player
                turn += 1
                play_count = 0
                update_action(turn % 2)
                if turn == 9:
                    pass
                turn_over = False
                game_processing = True
                update_seen()
                # winning
                if jack_flags >= 6:
                    jack_win = True
                if len(suspect_people) == 0:
                    detective_win = True
                if jack_win and not detective_win:
                    pygame.event.post(pygame.event.Event(JACKWIN))
                elif detective_win and not jack_win:
                    pygame.event.post(pygame.event.Event(DETECTIVEWIN))
                elif detective_win and jack_win:
                    pass  # oldtodo: success_together
                jack_win = False
                detective_win = False
            if original:
                if selected_detective:
                    f.write("move" + selected_detective.name + "done1" + '\n')
                    actioncard_list[int(card_using[0]) - 1].used = True
                    select_detective = False
                    selected_detective = None
                    acting = False
                    game_processing = True
                    original = None
                    # f.write("move" + selected_detective.name + "done2" + '\n')
                if rotate_map:
                    actioncard_list[int(card_using[0]) - 1].used = True
                    rotate_map = False
                    selected_map = None
                    acting = False
                    game_processing = True
                    original = None
                if exchanged:
                    actioncard_list[int(card_using[0]) - 1].used = True
                    exchange_map = False
                    acting = False
                    original = None
                    game_processing = True
                    exchanged = False
                    exchange_selected_a = None
                    exchange_selected_b = None
                if select_all_done:
                    actioncard_list[int(card_using[0]) - 1].used = True
                    one_forward = False
                    all_back = False
                    select_all_detective = False
                    select_all_done = False
                    acting = False
                    original = None
                    game_processing = True
                if innocent:
                    original = None
                    innocent.set_suspect(0)
                    innocent = None
                    actioncard_list[int(card_using[0]) - 1].used = True
                    acting = False
                    game_processing = True
                card_using = None
                play_once()
            update_witness()
        # elif event.type == DEBUGGER:
        #     game_processing = False
        #     debugging = True
        elif event.type == START:
            game_start = True
            start_game()
            # debugging = False
        elif event.type == pygame.KEYDOWN:  # for key board control
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.key == pygame.K_r:
                pygame.event.post(pygame.event.Event(CANCEL))
            if event.key == pygame.K_s:
                pygame.event.post(pygame.event.Event(START))
            # if event.key == pygame.K_d:
            #     pygame.event.post(pygame.event.Event(DEBUGGER))
            if event.key == pygame.K_j:
                show_jack = not show_jack
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            mouse_place, obj = where_mouse(mouse)
            # before game start, only start , quit button works
            if mouse_place == "button" and obj.name in ("start", "quit") and not acting:
                pygame.event.post(mouse_event_dict[obj.name])
            if game_processing:  # main game running, only start, restart, quit works
                if mouse_place == "button" and obj == 3:
                    pygame.event.post(mouse_event_dict[obj.name])
                elif mouse_place == "action" and not obj.used:
                    acting = True
                    obj.use_card(obj.face)
                    game_processing = False
            elif acting or turn_over:
                # two buttons
                if mouse_place == "button" and obj.name in ("ok", "cancel"):  # only ok and cancel available
                    pygame.event.post(mouse_event_dict[obj.name])

                # three detectives
                if select_detective:
                    if mouse_place == "detectives" and selected_detective.can_reach(obj):
                        original = selected_detective.location
                        selected_detective.location = obj
                        select_detective = False
                if rotate_map and mouse_place == "tiles":
                    if not selected_map:
                        selected_map = obj
                        original = obj.direction + 1
                        obj.rotate()
                    elif selected_map and obj == selected_map:
                        obj.rotate()
                if exchange_map and mouse_place == "tiles":
                    if not exchange_selected_a:
                        exchange_selected_a = obj
                        original = obj.pos
                    else:
                        exchange_selected_b = obj
                        original = (exchange_selected_a.pos, exchange_selected_b.pos)
                        temp = exchange_selected_a.pos
                        exchange_selected_a.pos = exchange_selected_b.pos
                        exchange_selected_b.pos = temp
                        exchanged = True
                if select_all_detective and mouse_place == "detectives":
                    all_back = False
                    one_forward = False
                    for d in detective_list:
                        if obj == d.location:
                            all_back = True
                            break
                        elif obj - d.location == 1 or obj - d.location == -11:
                            original = d.location
                            one_forward = d
                            break
                    if all_back:
                        original = (detective_list[0].location, detective_list[1].location, detective_list[2].location)
                        detective_list[0].go_back()
                        detective_list[1].go_back()
                        detective_list[2].go_back()
                        select_all_done = True
                        select_all_detective = False
                    if one_forward:
                        one_forward.location = obj
                        select_all_done = True
                        select_all_detective = False
                update_witness()
            f.write(mouse_place + str(obj.name if not isinstance(obj, int) else obj) + "\n")
    pygame.display.update()
f.close()
