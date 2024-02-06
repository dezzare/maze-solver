from point import Point
from tkinter import Tk, BOTH, Canvas

class Line:
    def __init__(self, p1, p2):
        self.start = p1
        self.end = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_color, width=2)
        canvas.pack(fill=BOTH, expand=True)