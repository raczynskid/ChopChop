import tkinter
from PIL import Image, ImageTk
from utils.shot import Shot
from utils.clipboard_handle import ClipboardHandle


class App:
    """
    on creation instantiate new Shot object
    create fullscreen canvas with Shot as background
    on left click start drawing selection
    on release create toplevel menu with options
    after option is selected destroy window
    """

    def __init__(self):
        self.root = self.configure_root()
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()
        self.canvas = self.configure_canvas()
        self.rect = None
        self.shot = None

    def configure_root(self):
        """configure fullscreen root"""
        root = tkinter.Tk()
        root.overrideredirect(1)
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        root.geometry(f"{w}x{h}+0+0")
        root.focus_set()
        root.bind("<Escape>", self.clear)
        return root

    def configure_canvas(self):
        """configure new canvas"""
        canvas = tkinter.Canvas(self.root, width=self.w, height=self.h)
        canvas.pack()
        canvas.configure(cursor='cross')
        canvas.configure(background='black')
        canvas.bind("<ButtonPress-1>", self.on_button_press)
        canvas.bind("<B1-Motion>", self.on_move_press)
        canvas.bind("<ButtonRelease-1>", self.on_button_release)
        return canvas

    def crop_shot(self):
        """display pillow image in root"""
        self.shot = Shot()
        self.original_shot = Shot()
        image = ImageTk.PhotoImage(self.shot.img)
        self.canvas.create_image(self.w / 2, self.h / 2, image=image)
        self.root.mainloop()

    def on_button_press(self, event):
        """call event on left mouse button press"""
        # save mouse drag start position
        self.shot = self.original_shot
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(0, 0, 1, 1, outline='red', width=3)

    def on_move_press(self, event):
        """call event on mouse drag"""
        # update current mouse position
        self.cur_x, self.cur_y = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.cur_x, self.cur_y)

    def on_button_release(self, event):
        """call event on left button release"""

        # crop and save screenshot
        capture_coordinates = self.canvas.coords(self.rect)
        self.shot.crop(capture_coordinates)
        self.shot.save()
        self.show_action_menu(capture_coordinates[2:])

    def show_action_menu(self, coords):
        """display context menu after cropping the screenshot"""
        cw = ContextMenu(coords, self.shot)
        cw.show()
        self.clear()

    def clear(self):
        # destroy root window
        self.root.withdraw()
        self.root.quit()
        self.root.destroy()


#

class ContextMenu:
    """display context menu for currently selected screenshot"""

    def __init__(self, coords, shot):
        self.x, self.y = coords
        self.root = self.configure_root()
        self.add_buttons()
        self.shot = shot

    def configure_root(self):
        root = tkinter.Toplevel()
        root.overrideredirect(1)
        root.geometry(f"+{int(self.x) + 10}+{int(self.y) + 10}")
        root.columnconfigure(0, weight=1)
        root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        root.focus_set()
        return root

    def add_buttons(self):
        clipboard = HoverButton(self.root, text="clipboard", command=self.to_clipboard)
        mail = HoverButton(self.root, text="email", command=lambda: print("mail pressed"))
        teams = HoverButton(self.root, text="teams", command=lambda: print("teams pressed"))
        upload = HoverButton(self.root, text="upload", command=lambda: print("upload pressed"))
        clipboard.grid(column=0, row=0, sticky="NSEW")
        mail.grid(column=0, row=1, sticky="NSEW")
        teams.grid(column=0, row=2, sticky="NSEW")
        upload.grid(column=0, row=3, sticky="NSEW")

    def to_clipboard(self):
        myimg = ClipboardHandle.convert_image(self.shot)
        ClipboardHandle.image_to_clipboard(myimg)
        self.clear()

    def show(self):
        self.root.mainloop()

    def clear(self):
        self.root.withdraw()
        self.root.quit()
        self.root.destroy()


class HoverButton(tkinter.Button):
    def __init__(self, master, **kw):
        tkinter.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = 'tan1'

    def on_leave(self, e):
        self['background'] = self.defaultBackground
