import math
import random
import sweeperlib
import datetime

graphics = {
    "window": None,
    "background": None,
    "bg_color": None,
    "batch": None,
    "sprites": [],
    "images": {}
}

handlers = {
    "timeouts": [],
}

state = {
    "field": [],
    "mines": 0,
    "time_started": 0,
    "time_ended": 0,
    "time_played": 0,
}

points_to_check = []
seen = set()

def create_play_area(width: int, height: int):
    field = []
    for row in range(width):
        field.append([])
        for col in range(height):
            field[-1].append(" ")

    state["field"] = field

    available = []
    for x in range(width):
        for y in range(height):
            available.append((x, y))


def place_mines(mines):
    """
    Places N mines to a field in random tiles.
    """
    height = len(state["field"])
    width = len(state["field"][0])

    available_tiles = []
    for x in range(width):
        for y in range(height):
            available_tiles.append((x, y))

    placed_mines = 0

    while placed_mines < mines:
        # pop random element from available tile list
        list_length = len(available_tiles)
        random_coordinate = available_tiles.pop((random.randint(0, list_length - 1)))
        random_x = random_coordinate[0]
        random_y = random_coordinate[1]
        if state["field"][random_y][random_x] != "x":
            state["field"][random_y][random_x] = "x"
            placed_mines += 1
        else:
            # else just get a new pair of coordinates from the list
            # technically this block is never run
            print("else triggered")
            continue


def count_mines(x, y):
    """
    Counts the mines surrounding one tile and returns the result.
    """
    mines = 0
    # top row
    if state["field"][y][x] == "x":
        return "x"
    if check_square_for_mine(y - 1, x + 1):
        mines += 1
    if check_square_for_mine(y, x + 1):
        mines += 1
    if check_square_for_mine(y + 1, x + 1):
        mines += 1
    # middle row
    if check_square_for_mine(y - 1, x):
        mines += 1
    #if check_square_for_mine(y, x):
     #   mines += 1
    if check_square_for_mine(y + 1, x):
        mines += 1
    # bottom row
    if check_square_for_mine(y - 1, x - 1):
        mines += 1
    if check_square_for_mine(y, x - 1):
        mines += 1
    if check_square_for_mine(y + 1, x - 1):
        mines += 1

    # state["field"][y][x] = mines
    return mines


def check_square_for_mine(y, x):
    if is_valid(x, y):
        try:
            #print(f"checked {x, y}")
            #print(state["field"][y][x])
            if state["field"][y][x] == "x":
                return True
        except IndexError:
            return False


def is_valid(x, y):
    width = len(state["field"][1])
    height = len(state["field"])
    if y > height or y < 0:  # if y +- 1 is over height or negative
        return False
    if x > width or x < 0:  # if x +- 1 is over width or negative
        return False
    if width >= x >= 0 and height >= y >= 0:  # test for if selection is on the state["field"]
        return True



def floodfill(x, y):
    """
    Marks previously unknown connected areas as safe, starting from the given
    x, y coordinates.
    """

    points_to_check.append((x, y))
    seen.add((x, y))

    def floodfill_revealer(y, x):
        if is_valid(x, y):
            seen.add((x, y))
            try:
                state["field"][y][x] = count_mines(x, y)
                print(state["field"][y][x])
                if state["field"][y][x] == "0":
                    print("true")
                if state["field"][y][x] == "0" or state["field"][y][x] == " ":
                    print("test")
                    if (x, y) not in seen:
                        points_to_check.append((x, y))
                    else:
                        return
            except IndexError:
                return

    while points_to_check:  # while list has elements, its bool is true
        print("points_to_check:" + str(points_to_check))
        x, y = points_to_check.pop()
        state["field"][y][x] = count_mines(x, y)
        print("points seen: " + str(seen))
        # right column
        floodfill_revealer(y - 1, x + 1)
        floodfill_revealer(y, x + 1)
        floodfill_revealer(y + 1, x + 1)
        # middle column, skipping centerpoint
        floodfill_revealer(y - 1, x)
        #floodfill_revealer(y, x)
        floodfill_revealer(y + 1, x)
        # left column
        floodfill_revealer(y - 1, x - 1)
        floodfill_revealer(y, x - 1)
        floodfill_revealer(y + 1, x - 1)


def set_mine_flag(x, y):
    # set flag
    if state["field"][y][x] == " ":
        state["field"][y][x] = "f"
    # remove flag
    elif state["field"][y][x] == "f":
        state["field"][y][x] = " "


def click_detection(x, y, mouse_button):
    clicked_square_x = math.trunc(x / 40)
    clicked_square_y = math.trunc(y / 40)
    print(f"square clicked is {clicked_square_x}, {clicked_square_y}")
    if mouse_button == sweeperlib.MOUSE_LEFT:
        if state["field"][clicked_square_y][clicked_square_x] == "x":
            game_lost()
        if state["field"][clicked_square_y][clicked_square_x] == " ":
            floodfill(clicked_square_x, clicked_square_y)
        check_win_condition()
    if mouse_button == sweeperlib.MOUSE_RIGHT:
        set_mine_flag(clicked_square_x, clicked_square_y)
        check_win_condition()
    if mouse_button == sweeperlib.MOUSE_MIDDLE:
        print(count_mines(clicked_square_x, clicked_square_y))
        check_win_condition()


def check_win_condition():
    unopened_tiles = 0
    for list in state["field"]:
        for i in list:
            if i == " ":
                unopened_tiles += 1
    #print("unopened tiles " + str(unopened_tiles))
    if unopened_tiles == 0:
        game_won()


def game_lost():
    print("clicked on a mine and you lost the game.")
    calculate_time_difference()
    print(f"time played was: " + str(state["time_played"]))
    sweeperlib.close()


def game_won():
    print(f"Game won in: " + str(state["time_played"]) + " seconds")
    calculate_time_difference()
    print(f"time played was: " + str(state["time_played"]))
    sweeperlib.close()


def calculate_time_difference():
    end_date = datetime.datetime.now()
    time_diff = end_date - state["time_started"]
    state["time_ended"] = end_date
    state["time_played"] = time_diff


def save_statistics():
    pass

def read_statistics():
    pass

