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




def main():
    win = Window(800, 600)
    point_1 = Point(50, 50)
    point_2 = Point(200, 50)
    line_1 = Line(point_1, point_2)
    win.draw_line(line_1, "black")
    win.wait_for_close()

main()