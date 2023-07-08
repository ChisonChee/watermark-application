from tkinter import *
from tkinter import ttk
from watermarkManager import watermarkManager

root = Tk(className="Image-Watermark-Processor")
root.configure(bg="black")
root.geometry("1200x750+150-55")
style = ttk.Style()
style.map("TFrame", background="black")
style.configure("TLabel", background="black", foreground="white")
style.map("TButton",
          foreground=[('pressed', 'gold'), ('disabled', 'grey'), ('active', 'green')],
          background=[('pressed', '!disabled', 'gold'), ('disabled', 'grey'), ('active', 'green')])

frm = ttk.Frame(root, padding=50, style="TFrame")
frm.pack(anchor=CENTER)

watermark_manager = watermarkManager(frame=frm)


def button_state():
    watermark_manager.file_selector()
    watermark_manager.file_type_validator()
    watermark_manager.img_size_processor()
    add_watermark_entry['state'] = watermark_manager.watermark_button_state
    add_logo['state'] = watermark_manager.watermark_button_state
    save_file['state'] = watermark_manager.watermark_button_state


app_title = ttk.Label(frm, text="Image Watermarking Application", font=("Courier", 35, "bold"), style="TLabel")
app_title.grid(column=0, row=0, ipady=10, columnspan=4)

file_select_button = ttk.Button(frm, text="Choose The Image",
                                command=button_state,
                                style="TButton")
file_select_button.grid(column=0, row=1, pady=10)

add_watermark_entry = ttk.Button(frm,
                                 text="Add Watermark",
                                 command=watermark_manager.add_watermark,
                                 style="TButton",
                                 state="disabled")
add_watermark_entry.grid(column=1, row=1, pady=10)

add_logo = ttk.Button(frm,
                      text="Add Logo",
                      style="TButton",
                      state="disabled",
                      command=watermark_manager.add_logo)
add_logo.grid(column=2, row=1, pady=10)

save_file = ttk.Button(frm,
                       text="Save File",
                       style="TButton",
                       state="disabled",
                       command=watermark_manager.save_image)
save_file.grid(column=3, row=1, pady=10)

root.mainloop()
