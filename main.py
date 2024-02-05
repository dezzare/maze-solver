from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.__root = Tk()
        self.__root.title("Maze")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canva = Canvas(width=self.width, height=self.height)
        self.__canva.pack()
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



def main():
    win = Window(800, 600)
    win.wait_for_close()

main()