from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.__root = Tk()
        self.__root.title("Maze")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas = Canvas(width=self.width, height=self.height)
        self.__canvas.pack()
        self.__is_running = False
        
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()

    def close(self):
        self.__is_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x, y):
        #X is horizontal coordinate
        #x=0 is the left of the screen
        self.x = x
        #Y is vertical coordinate
        #y=0 is the top of the screen
        self.y = y

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
    
    def draw(self):
        color = "black"

        if self.has_left_wall:
            self.__win.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)), color)
        
        if self.has_right_wall:
            self.__win.draw_line(Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)), color)
        
        if self.has_top_wall:
            self.__win.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)), color)
        
        if self.has_bottom_wall:
            self.__win.draw_line(Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)), color)



def main():
    win = Window(800, 600)
    square = Cell(50, 50, 100, 100, win)
    square.draw()
    u = Cell(150, 50, 200, 100, win, True, True, False)
    u.draw()

    win.wait_for_close()

main()