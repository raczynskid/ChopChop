from ctypes import windll, Structure, c_long, byref
import time


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

class Mouse:
    def __init__(self):
        self.pt = POINT()

    def query_mouse_position(self):
        windll.user32.GetCursorPos(byref(self.pt))
        return self.pt.x, self.pt.y

    def query_left_click(self):
        state = windll.user32.GetKeyState(0x01)
        if state > 1:
            return True
        return False

    def query_right_click(self):
        state = windll.user32.GetKeyState(0x02)
        if state > 1:
            return True
        return False