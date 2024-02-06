import time
import random
from window import Window
from point import Point
from cell import Cell
from maze import Maze


def main():
    win = Window(800, 600)
    # square = Cell(50, 50, 100, 100, win)
    # square.draw()
    # u = Cell(150, 50, 200, 100, win, True, True, False)
    # u.draw()
    # square.draw_move(u)
    maze = Maze(150, 50, 10, 10, 50, 50, win)
    maze.solve()

    win.wait_for_close()

main()