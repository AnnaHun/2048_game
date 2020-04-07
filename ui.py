from bll import GameCoreController
from model import Direction

import os


class GameConsoleView:
    def __init__(self):
        self.__controller = GameCoreController()

    def start(self):
        self.__controller.generate_new_number()
        self.__controller.generate_new_number()
        self.__print_map()

    def __print_map(self):
        os.system("clean")
        for r in range(len(self.__controller.map)):
            for c in range(len(self.__controller.map[r])):
                print(self.__controller.map[r][c], end="\t")
            print()

    def update(self):
        while True:
            self.__move_map()
            if self.__controller.is_change:
                self.__controller.generate_new_number()
                self.__print_map()
                if self.__controller.is_game_over():
                    print("游戏结束")
                    break

    def __move_map(self):
        dir = input("请输入移动方向")
        if dir == "w":
            self.__controller.move(Direction.up)
        elif dir == "s":
            self.__controller.move(Direction.down)
        elif dir == "d":
            self.__controller.move(Direction.right)
        elif dir == "a":
            self.__controller.move(Direction.left)
