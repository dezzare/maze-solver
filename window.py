from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.root = Tk()
        self.root.title("Maze")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(fill = BOTH, expand = True)
        self.is_running = False
        
    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def close(self):
        self.is_running = False

    def draw_line(self, line, fill_color):
        self.line = line
        self.fill_color = fill_color
        line.draw(self.canvas, self.fill_color)
