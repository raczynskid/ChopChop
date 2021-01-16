from io import BytesIO
import win32clipboard
from PIL import Image
from utils.screenshot_handler import ScreenShot


class ClipboardHandle:
    @staticmethod
    def image_to_clipboard(data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    @staticmethod
    def convert_image(shot):
        output = BytesIO()
        shot.img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        return data
