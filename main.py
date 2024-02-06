import time
import random
from window import Window
from point import Point



class Line:
    def __init__(self, p1, p2):
        self.__p1 = p1
        self.__p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.__p1.x, self.__p1.y, self.__p2.x, self.__p2.y, fill=fill_color, width=2)
        canvas.pack()

class Cell:
    def __init__(self, x1, y1, x2, y2, window=None, left=True, right=True, top=True, bottom=True):
        self.has_left_wall = left
        self.has_right_wall = right
        self.has_top_wall = top
        self.has_bottom_wall = bottom
        self.__x1 = x1  #left point
        self.__y1 = y1  #top point
        self.__x2 = x2  #right point
        self.__y2 = y2  #bottom point
        self.__win = window
        self.visited = False
    
    def draw(self, color="black"):

        if self.has_left_wall:
            self.__win.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)), color)
        else:
            self.__win.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)), "white")
        
        if self.has_right_wall:
            self.__win.draw_line(Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)), color)
        else:
            self.__win.draw_line(Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)), "white")
        
        if self.has_top_wall:
            self.__win.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)), color)
        else:
            self.__win.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)), "white")
        
        if self.has_bottom_wall:
            self.__win.draw_line(Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)), color)
        else:
            self.__win.draw_line(Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)), "white")

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"
        center_x = ((self.__x2 - self.__x1) // 2) + self.__x1
        center_y = ((self.__y2 - self.__y1) // 2) + self.__y1
        center_x_to_cell = ((to_cell.__x2 - to_cell.__x1) // 2) + to_cell.__x1
        center_y_to_cell = ((to_cell.__y2 - to_cell.__y1) // 2) + to_cell.__y1
        self.__win.draw_line(Line(Point(center_x, center_y), Point(center_x_to_cell, center_y_to_cell)), color)

class Maze:
    def __init__ (
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        if seed is not None:
            self.seed = random.seed(seed)

        self.cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self.num_cols):
            list_of_cells = []
            for j in range(self.num_rows):
                list_of_cells.append(self._draw_cell(i, j))
            self.cells.append(list_of_cells)


    def _draw_cell(self, i, j, cell=None):
        
        if cell == None:
            x1 = self.x1 + i * self.cell_size_x
            y1 = self.y1 + j * self.cell_size_y
            x2 = x1 + self.cell_size_x
            y2 = y1 + self.cell_size_y
            cell = Cell(x1, y1, x2, y2, self.win)
        
        if self.win != None:
            cell.draw()
            self._animate()
        return cell
    
    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    
    def _break_entrance_and_exit(self):
        # Entrance will always be at the top-left cell
        self.cells[0][0].has_top_wall = False
        self._draw_cell(0, 0, self.cells[0][0])
        # Exit will always be at the bottom-right cell
        self.cells[-1][-1].has_bottom_wall = False
        self._draw_cell(-1, -1, self.cells[-1][-1])

    def _break_walls_r(self, i, j):
        self.cells[i][j].visited = True
        while True:
            to_visit = self._get_neighbor_to_visit(i, j)

            if len(to_visit) == 0:
                self._draw_cell(0, 0, self.cells[i][j])
                return
            
            next_ij = random.choice(to_visit) # next_ij[0] = i and next_ij[1] = j
            next_cell = self.cells[next_ij[0]][next_ij[1]]

            if next_ij[0] == i - 1: #UP to the current
                self.cells[i][j].has_top_wall = False
                next_cell.has_bottom_wall = False
            elif next_ij[0] == i + 1: #DOWN
                self.cells[i][j].has_bottom_wall = False
                next_cell.has_top_wall = False
            elif next_ij[1] == j - 1: #LEFT
                self.cells[i][j].has_left_wall = False
                next_cell.has_right_wall = False
            elif next_ij[1] == j + 1: #RIGHT
                self.cells[i][j].has_right_wall = False
                next_cell.has_left_wall = False
            
            self._break_walls_r(next_ij[0], next_ij[1])
            
    def _get_neighbor_to_visit(self, i, j):
            neighbor = []
            if i - 1 > 0 and not self.cells[i-1][j].visited:
                neighbor.append((i-1, j)) #UP
            if i + 1 < len(self.cells) and not self.cells[i+1][j].visited:
                neighbor.append((i+1, j)) #DOWN
            if j - 1 > 0 and not self.cells[i][j-1].visited:
                neighbor.append((i, j-1)) #LEFT
            if j + 1 < len(self.cells[i]) and not self.cells[i][j+1].visited:
                neighbor.append((i, j+1)) #RIGHT
            return neighbor
    
    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.cells[i][j].visited = False
        

def main():
    win = Window(800, 600)
    # square = Cell(50, 50, 100, 100, win)
    # square.draw()
    # u = Cell(150, 50, 200, 100, win, True, True, False)
    # u.draw()
    # square.draw_move(u)
    maze = Maze(150, 50, 10, 10, 50, 50, win)

    win.wait_for_close()

main()