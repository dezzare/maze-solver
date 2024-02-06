from line import Line
from point import Point

class Cell:
    def __init__(self, x1, y1, x2, y2, win, window=None, left=True, right=True, top=True, bottom=True):
        self.has_left_wall = left
        self.has_right_wall = right
        self.has_top_wall = top
        self.has_bottom_wall = bottom
        
        self.top_left_point = x1  
        self.top_right_point = y1  
        self.bottom_left_point = x2  
        self.bottom_right_point = y2  
        
        self.window = window
        self.visited = False
        self._win = win
    
    def draw(self, color="black"):
        if self.window:
            if self.has_left_wall:
                self.window.draw_line(Line(self.bottom_left_point, self.top_left_point), color)
            else:
                self.window.draw_line(Line(self.bottom_left_point, self.top_left_point), "white")
            if self.has_right_wall:
                self.window.draw_line(Line(self.bottom_right_point, self.top_right_point), color)
            else:
                self.window.draw_line(Line(self.bottom_right_point, self.top_right_point), "white")
            if self.has_top_wall:
                self.window.draw_line(Line(self.top_left_point, self.top_right_point), color)
            else:
                self.window.draw_line(Line(self.top_left_point, self.top_right_point), "white")
            if self.has_bottom_wall:
                self.window.draw_line(Line(self.bottom_left_point, self.bottom_right_point), color)
            else:
                self.window.draw_line(Line(self.bottom_left_point, self.bottom_right_point), "white")

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "grey"
        self.window.draw_line(Line(self.get_center_point(), to_cell.get_middle_point()), color)
    
    def get_center_point(self):
        return Point((self.top_left_point.x + self.top_right_point.x) / 2, (self.top_left_point.y + self.bottom_left_point.y) / 2)

        
