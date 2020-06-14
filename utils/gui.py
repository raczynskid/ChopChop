import tkinter
import copy
from PIL import Image, ImageTk
from utils.shot import Shot
from utils.clipboard_handle import ClipboardHandle
from tkinter import filedialog


def cleanup(f):
    """cleanup decorator to destroy context menu after function call"""

    def wrap(self, *args):
        f(self, *args)
        self.action = True
        self.root.withdraw()
        self.root.quit()
        if isinstance(self.root, tkinter.Toplevel):
            self.root.destroy()

    return wrap


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
        self.original_shot = None

    def configure_root(self):
        """configure fullscreen root"""
        root = tkinter.Tk()

        # general root settings
        root.overrideredirect(1)
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        root.geometry(f"{w}x{h}+0+0")
        root.focus_set()

        # set events
        root.bind("<Escape>", lambda e: cleanup(e))
        return root

    def configure_canvas(self):
        """configure new canvas"""

        # general canvas settings
        canvas = tkinter.Canvas(self.root, width=self.w, height=self.h)
        canvas.pack()
        canvas.configure(cursor='cross')
        canvas.configure(background='black')

        # set events
        canvas.bind("<ButtonPress-1>", self.on_button_press)
        canvas.bind("<B1-Motion>", self.on_move_press)
        canvas.bind("<ButtonRelease-1>", self.on_button_release)
        return canvas

    def crop_shot(self):
        """display pillow image in root"""
        self.original_shot = Shot()
        self.shot = copy.deepcopy(self.original_shot)
        image = ImageTk.PhotoImage(self.shot.img)
        self.canvas.create_image(self.w / 2, self.h / 2, image=image)
        self.root.mainloop()

    def on_button_press(self, event):
        """call event on left mouse button press"""

        # save mouse drag start position

        self.shot = copy.deepcopy(self.original_shot)
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

    @cleanup
    def show_action_menu(self, coords):
        """display context menu after cropping the screenshot"""
        cw = ContextMenu(coords, self.shot)
        cw.show()


class ContextMenu:
    """display context menu for currently selected screenshot"""

    def __init__(self, coords, shot):
        self.x, self.y = coords
        self.root = self.configure_root()
        self.add_buttons()
        self.shot = shot
        self.action = False

    def configure_root(self):
        root = tkinter.Toplevel()
        root.overrideredirect(1)

        # offset menu location to NW if too close to SE border
        screen_offset_x, screen_offset_y = 10, 10
        if (abs(root.winfo_screenwidth() - self.x) < 100) or (abs(root.winfo_screenheight() - self.y) < 100):
            screen_offset_x, screen_offset_y = -100, -300
        root.geometry(f"+{int(self.x) + screen_offset_x}+{int(self.y) + screen_offset_y}")
        root.columnconfigure(0, weight=1)
        root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        root.focus_set()
        return root

    def add_buttons(self):
        clipboard = HoverButton(self.root, text="clipboard", command=self.to_clipboard)
        mail = HoverButton(self.root, text="email", command=lambda: print("mail pressed"), state=tkinter.DISABLED)
        teams = HoverButton(self.root, text="teams", command=lambda: print("teams pressed"), state=tkinter.DISABLED)
        upload = HoverButton(self.root, text="upload", command=lambda: print("upload pressed"), state=tkinter.DISABLED)
        save_as = HoverButton(self.root, text="save as...", command=self.save_as)
        clipboard.grid(column=0, row=0, sticky="NSEW")
        save_as.grid(column=0, row=1, sticky="NSEW")
        mail.grid(column=0, row=2, sticky="NSEW")
        teams.grid(column=0, row=3, sticky="NSEW")
        upload.grid(column=0, row=4, sticky="NSEW")

    @cleanup
    def to_clipboard(self):
        myimg = ClipboardHandle.convert_image(self.shot)
        ClipboardHandle.image_to_clipboard(myimg)

    @cleanup
    def save_as(self):
        directory = filedialog.asksaveasfilename(initialdir="/<file_name>",
                                                 title="Save as...",
                                                 filetypes=(("png files", "*.png"),
                                                            ("jpeg files", "*.jpg"),
                                                            ("all files", "*.*")),
                                                 defaultextension='')
        self.shot.save_as(directory)

    def show(self):
        self.root.mainloop()

    def clear(self):
        self.root.quit()
        self.root.destroy()


class HoverButton(tkinter.Button):
    def __init__(self, master, **kw):
        tkinter.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        if self['state'] == tkinter.DISABLED:
            self['background'] = 'gray'
        else:
            self.bind("<Enter>", self.on_enter)
            self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = 'tan1'

    def on_leave(self, e):
        self['background'] = self.defaultBackground
