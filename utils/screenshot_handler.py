from PIL import ImageGrab
from ctypes import windll
import os

# must be ran on import - modify windll behavior to account for screen DPI
user32 = windll.user32
user32.SetProcessDPIAware()


class ScreenShot:
    def __init__(self):
        self.img = None
        self.path = "./TempScreens"
        self.filename = "tmp.png"
        self.prepdir()
        self.grab()

    def grab(self):
        self.img = ImageGrab.grab()

    def save(self):
        self.img.save("/".join([self.path, self.filename]))

    def save_as(self, pth):
        self.img.save(pth)

    def crop(self, box):
        self.img = self.img.crop(box)

    def display(self):
        self.img.show()

    def prepdir(self):
        if not os.path.isdir(self.path):
            os.mkdir(self.path)