import tkinter
import copy
import os
from PIL import Image, ImageTk
from utils.shot import Shot
from utils.clipboard_handle import ClipboardHandle
from utils.mail_handle import MailHandler
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
        root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
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
        canvas.bind("<ButtonRelease-3>", self.open_folder)
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
    def open_folder(self, event):
        os.popen(f'explorer "{os.path.abspath(self.shot.path)}"')

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

        # create the root
        root = tkinter.Toplevel()
        root.overrideredirect(1)

        # offset menu location to NW if too close to SE border
        screen_offset_x, screen_offset_y = 10, 10
        if (abs(root.winfo_screenwidth() - self.x) < 100) or (abs(root.winfo_screenheight() - self.y) < 100):
            screen_offset_x, screen_offset_y = -100, -300
        root.geometry(f"+{int(self.x) + screen_offset_x}+{int(self.y) + screen_offset_y}")
        root.columnconfigure(0, weight=1)

        # bind events
        root.bind("<Escape>", lambda e: (e.widget.quit()))
        root.focus_set()
        return root

    def add_buttons(self):
        # create and configure context menu buttons
        clipboard = HoverButton(self.root, text="clipboard", command=self.to_clipboard)
        mail = HoverButton(self.root, text="email", command=self.send_mail)
        teams = HoverButton(self.root, text="teams", command=lambda: print("teams pressed"), state=tkinter.DISABLED)
        upload = HoverButton(self.root, text="upload", command=lambda: print("upload pressed"), state=tkinter.DISABLED)
        save = HoverButton(self.root, text="save", command=self.save_input)
        folder = HoverButton(self.root, text="edit", command=self.edit)

        # grid the buttons
        clipboard.grid(column=0, row=0, sticky="NSEW")
        save.grid(column=0, row=1, sticky="NSEW")
        mail.grid(column=0, row=3, sticky="NSEW")
        teams.grid(column=0, row=4, sticky="NSEW")
        upload.grid(column=0, row=5, sticky="NSEW")
        folder.grid(column=0, row=6, sticky="NSEW")

    @cleanup
    def to_clipboard(self):
        """copy image to clipboard"""
        myimg = ClipboardHandle.convert_image(self.shot)
        ClipboardHandle.image_to_clipboard(myimg)

    @cleanup
    def save_as(self):
        """open save as filedialog and choose save directory"""
        directory = filedialog.asksaveasfilename(initialdir="/<file_name>",
                                                 title="Save as...",
                                                 filetypes=(("png files", "*.png"),
                                                            ("jpeg files", "*.jpg"),
                                                            ("all files", "*.*")),
                                                 defaultextension='')
        if directory != "":
            self.shot.save_as(directory)

    @cleanup
    def save(self, filename):
        """save in default directory but with custom name"""
        self.shot.filename = filename + '.png'
        self.shot.save()

    @cleanup
    def send_mail(self):
        """send mail with screenshot embedded in html body"""
        self.shot.save()
        MailHandler.compose_mail(os.path.abspath("/".join([self.shot.path, self.shot.filename])))

    @cleanup
    def open_folder(self):
        """open folder containing snips"""
        os.popen(f'explorer "{os.path.abspath(self.shot.path)}"')

    @cleanup
    def edit(self):
        """open current snip with paint"""
        os.popen(f'C:\Windows\System32\mspaint.exe {os.path.abspath("/".join([self.shot.path, self.shot.filename]))}')

    def save_input(self):
        """
        show additional options when save button is clicked
        meant to concatenate quick save and save as into less space
        """
        # create a frame
        frame = tkinter.Frame(self.root)
        # inside the frame:
        # create a text field
        txt_field = tkinter.Entry(frame)
        # create ok button to confirm
        ok_btn = HoverButton(frame, text='save', command=lambda: self.save(txt_field.get()))
        # create browse button to open file explorer
        browse_btn = HoverButton(frame, text='...', command=self.save_as)
        # grid the objects into the frame
        txt_field.grid(column=0, row=1, columnspan=2, sticky="W")
        ok_btn.grid(column=2, row=1, sticky="W")
        browse_btn.grid(column=3, row=1, sticky="W")
        # replace save button in context menu with filled frame
        frame.grid(column=0, row=1)
        # focus on entry text field
        txt_field.focus()

    def show(self):
        self.root.mainloop()

    def clear(self):
        self.root.quit()
        self.root.destroy()


class HoverButton(tkinter.Button):
    """Button class with changing colors on hover"""

    def __init__(self, master, **kw):
        tkinter.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = 'tan1'

    def on_leave(self, e):
        self['background'] = self.defaultBackground
