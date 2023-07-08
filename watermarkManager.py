import tkinter as tk
from tkinter import *
from tkinter import ttk, font
import tkinter.filedialog as filehandler
from PIL import ImageTk, Image, ImageFont, ImageDraw
import pathlib
import os


def clear_text(e):
    widget = e.widget
    widget.delete(first=0, last=END)


class watermarkManager:
    def __init__(self, frame):
        self.draw = None
        self.frm = frame
        self.file = None
        self.PIL_copy = None
        self.PIL_image = None
        self.selected_img = None
        self.text = tk.StringVar()
        self.file_save_path = tk.StringVar()
        self.width, self.height = 0, 0
        self.tune_x, self.tune_y = 0, 0
        self.watermark_button_state = "disabled"
        self.label = ttk.Label(self.frm, image="")
        self.entry = ttk.Entry(self.frm, textvariable=self.text)
        self.font = ImageFont.truetype(font="Conquest.ttf", size=50)
        self.filetypes = [("JPG", "*.jpg"), ("JPEG", "*.jpeg"), ("PNG", "*.png")]

    def file_selector(self):
        self.PIL_image = ""
        self.file = pathlib.Path(filehandler.askopenfilename(filetypes=self.filetypes, title="Choose Image"))

    def file_type_validator(self):
        try:
            self.selected_img = Image.open(fp=self.file)
        except PermissionError:
            self.watermark_button_state = "disabled"
        else:
            self.watermark_button_state = "normal"

    def img_size_processor(self):
        self.width, self.height = self.selected_img.width, self.selected_img.height
        if self.height > self.width:
            self.PIL_image = self.selected_img.resize((450, 550))
            self.tune_x, self.tune_y = 150, 500
        elif self.width > self.height:
            self.PIL_image = self.selected_img.resize((650, 450))
            self.tune_x, self.tune_y = 250, 400
        else:
            self.PIL_image = self.selected_img.resize((550, 550))
            self.tune_x, self.tune_y = 300, 500
        self.selected_img.close()
        self.PIL_copy = self.PIL_image.copy()
        self.show_image()

    def add_watermark(self):
        self.entry.destroy()
        self.entry = ttk.Entry(self.frm,
                               font=font.Font(family="Times", size=20),
                               textvariable=self.text,
                               justify="center")
        self.entry.grid(column=0, row=2, columnspan=4)
        self.entry.bind(sequence="<Return>", func=self.on_return)
        self.entry.grid(column=0, row=2, columnspan=4, ipadx=100)
        self.entry.insert(index=0, string="<Enter> your watermark text.")
        self.entry.lift()

    def on_return(self, event):
        self.entry.destroy()
        self.PIL_image = self.PIL_copy.copy()
        watermark_location = (event.x+self.tune_x, event.y+self.tune_y)
        self.draw = ImageDraw.Draw(im=self.PIL_image)
        self.draw.text(xy=watermark_location, fill=(0, 0, 0), text=self.text.get().lower(), font=self.font, anchor="mm")
        self.show_image()

    def add_logo(self):
        self.file_selector()
        with Image.open(fp=self.file) as selected_logo:
            logo = selected_logo.resize((50, 50))
            self.PIL_image = self.PIL_copy.copy()
            self.PIL_image.paste(im=logo, box=(200, 500))
        self.show_image()

    def show_image(self):
        self.label.destroy()
        photo_image = ImageTk.PhotoImage(image=self.PIL_image)
        self.label = ttk.Label(self.frm, image=photo_image)
        self.label.image = photo_image
        self.label.grid(column=0, row=2, columnspan=4)

    def save_image(self):
        self.entry.destroy()
        self.entry = ttk.Entry(self.frm,
                               font=font.Font(family="Times", size=20),
                               textvariable=self.file_save_path,
                               justify="center")
        self.entry.insert(index=0, string="<Enter> your image as filename.extension")
        self.entry.bind(sequence="<ButtonPress>", func=clear_text)
        self.entry.grid(column=0, row=2, columnspan=4, ipadx=100)
        self.entry.bind(sequence="<Return>", func=self.on_save)
        self.entry.lift()

    def on_save(self, event):
        event.widget.destroy()
        self.label.destroy()
        image_export = self.PIL_image
        image_export.resize((self.width, self.height))
        path = './watermark-image'
        if not os.path.exists(path):
            os.mkdir(path)
        current_script_dir = str(os.path.dirname(os.path.abspath(__file__)))
        file_path = current_script_dir+"\\watermark-image\\"+self.file_save_path.get()
        image_export.save(file_path)
