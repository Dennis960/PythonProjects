import tkinter as Tkinter


def create_text(text, position, font, font_size, color):
    x, y = position
    label = Tkinter.Label(text=text, font=(font, font_size), fg=color, bg='white', )
    label.master.overrideredirect(True)
    label.master.geometry(f"+{x}+{y}")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")
    label.pack()
    return label
label = create_text('Text to test', (20, 20), 'Calibri', 20, 'black')
create_text('Another text', (200, 20), 'Calibri', 20, 'black')
label.master.mainloop()