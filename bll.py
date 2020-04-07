from model import Location
from model import Direction

import random
import copy


class GameCoreController:
    def __init__(self):
        self.__map = [
            [0] * 4,
            [0] * 4,
            [0] * 4,
            [0] * 4,
        ]
        # 作为中间空间，达到置换工作台作用
        self.__list_merge = []
        self.__list_empty_location = []
        self.is_change = False

    @property
    def map(self):
        return self.__map

    @property
    def is_change(self):
        return self.__is_change

    @is_change.setter
    def is_change(self, value):
        self.__is_change = value

    def __zero_to_end(self):
        for i in range(len(self.__list_merge) - 1, -1, -1):
            if self.__list_merge[i] == 0:
                del self.__list_merge[i]
                self.__list_merge.append(0)

    def __merge(self):
        self.__zero_to_end()
        for i in range(len(self.__list_merge) - 1):
            if self.__list_merge[i] == self.__list_merge[i + 1]:
                self.__list_merge[i] += self.__list_merge[i + 1]
                self.__list_merge[i + 1] = 0
        self.__zero_to_end()

    def __move_left(self):
        for r in range(len(self.__map)):
            self.__list_merge = self.__map[r]
            self.__merge()
            self.__map[r][:] = self.__list_merge

    def __move_right(self):
        for r in range(len(self.__map)):
            self.__list_merge = self.__map[r][::-1]
            self.__merge()
            self.__map[r][::-1] = self.__list_merge

    def __move_up(self):
        for c in range(4):
            self.__list_merge.clear()
            for r in range(4):
                self.__list_merge.append(self.__map[r][c])
            self.__merge()
            for r in range(4):
                self.__map[r][c] = self.__list_merge[r]

    def __move_down(self):
        for c in range(4):
            self.__list_merge.clear()
            for r in range(3, -1, -1):
                self.__list_merge.append(self.map[r][c])
            self.__merge()
            for r in range(3, -1, -1):
                self.map[r][c] = self.__list_merge[3 - r]

    def __calculate_empty_location(self):
        self.__list_empty_location.clear()
        for r in range(4):
            for c in range(4):
                if self.__map[r][c] == 0:
                    loc = Location(r, c)
                    self.__list_empty_location.append(loc)

    def generate_new_number(self):
        self.__calculate_empty_location()
        if len(self.__list_empty_location) == 0:
            return
        loc = random.choice(self.__list_empty_location)
        self.map[loc.r_index][loc.c_index] = 4 if random.randint(1, 10) == 1 else 2
        self.__list_empty_location.remove(loc)

    def move(self, dir):
        original_map = copy.deepcopy(self.__map)
        if dir == Direction.up:
            self.__move_up()
        elif dir == Direction.down:
            self.__move_down()
        elif dir == Direction.left:
            self.__move_left()
        elif dir == Direction.right:
            self.__move_right()
        self.is_change = original_map != self.__map

    def is_game_over(self):
        if len(self.__list_empty_location) > 0:
            return False
        for r in range(4):
            for c in range(3):
                if self.__map[r][c] == self.__map[r][c + 1] or self.__map[c][r] == self.__map[c + 1][r]:
                    return False
        return True
