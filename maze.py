from cell import Cell
from point import Point
import random
import time

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
        for row in range(self.num_rows):
            self.cells.append([])
            for col in range(self.num_cols):
                top_left_point = Point(self.x1 + col * self.cell_size_x, self.y1 + row * self.cell_size_y)
                top_right_point = Point(self.x1 + (col + 1) * self.cell_size_x, self.y1 + row * self.cell_size_y)
                bottom_left_point = Point(self.x1 + col * self.cell_size_x, self.y1 + (row + 1) * self.cell_size_y)
                bottom_right_point = Point(self.x1 + (col + 1) * self.cell_size_x, self.y1 + (row + 1) * self.cell_size_y)
                self.cells[row].append(Cell(top_left_point, top_right_point, bottom_left_point, bottom_right_point, False, self.win))
                self._draw_cell(Cell(top_left_point, top_right_point, bottom_left_point, bottom_right_point, False, self.win))


    def _draw_cell(self, cell=None):
        cell.draw()
        self._animate()
    
    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    
    def _break_entrance_and_exit(self):
        # Entrance will always be at the top-left cell
        self.cells[0][0].has_top_wall = False
        self._draw_cell(self.cells[0][0])
        # Exit will always be at the bottom-right cell
        self.cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self.cells[-1][-1])

    def _break_walls_r(self, i, j):
        self.cells[i][j].visited = True
        while True:
            to_visit = self._get_neighbor_to_visit(i, j)

            if len(to_visit) == 0:
                self._draw_cell(self.cells[i][j])
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
            self.cells[i][j].draw()
            next_cell.draw()
            self._break_walls_r(next_ij[0], next_ij[1])
            
    def _get_neighbor_to_visit(self, i, j):
            neighbor = []
            if i > 0 and not self.cells[i-1][j].visited:
                neighbor.append((i-1, j)) #UP
            if i < self.num_rows-1 and not self.cells[i+1][j].visited:
                neighbor.append((i+1, j)) #DOWN
            if j > 0 and not self.cells[i][j-1].visited:
                neighbor.append((i, j-1)) #LEFT
            if j < self.num_cols -1 and not self.cells[i][j+1].visited:
                neighbor.append((i, j+1)) #RIGHT
            return neighbor
    
    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.cells[i][j].visited = False
    
    def solve(self):
        return self._solve_r(0,0)
    
    def _solve_r(self, i, j):
        self._animate()
        self.cells[i][j].visited = True

        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True
        
        neighbours = self._get_neighbor_to_visit(i, j)
        
        for cell in neighbours:
            if not self._has_wall(i, j, cell[0], cell[1]):
                self.cells[i][j].draw_move(self.cells[cell[0]][cell[1]])
                if self._solve_r(cell[0], cell[1]):
                    return True
                self.cells[i][j].draw_move(self.cells[cell[0]][cell[1]], True)
        return False
    
    def _has_wall(self, i, j, i2, j2):
        if i < i2: # down
            return self.cells[i][j].has_bottom_wall
        if i > i2: # up
            return self.cells[i][j].has_top_wall
        if j < j2: # right
            return self.cells[i][j].has_right_wall
        return self.cells[i][j].has_left_wall


