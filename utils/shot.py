from PIL import ImageGrab
from ctypes import windll
import os

user32 = windll.user32
user32.SetProcessDPIAware()

class Shot:
    def __init__(self):
        self.img = None
        self.path = "D:/Python/TempScreens"
        self.filename = "tmp.png"
        self.prepdir()
        self.grab()
    def grab(self):
        self.img = ImageGrab.grab()
    def save(self):
        self.img.save("/".join([self.path, self.filename]))
    def crop(self, box):
        self.img = self.img.crop(box)
    def display(self):
        self.img.show()
    def prepdir(self):
        if not os.path.isdir(self.path):
            os.mkdir(self.path)