from tkinter import Tk, font, PanedWindow, Message, Canvas, Frame, Scrollbar, VERTICAL, RIGHT, LEFT, Y, BOTH

root = Tk()

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window to half the width and full height, aligned left
window_width = screen_width // 2
window_height = screen_height
root.geometry(f"{window_width}x{window_height}+0+0")

fonts = font.families()

# Create a canvas and a vertical scrollbar for scrolling
canvas = Canvas(root)
scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

# Create a frame inside the canvas to hold the font messages
frame = Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor='nw')

# Add font messages to the frame
i = 0
font_frame = PanedWindow(frame, orient="horizontal")
font_frame.pack(fill="x", expand=True)
for font_name in fonts:
    try:
        font_used = font.Font(family=font_name)
        message = Message(font_frame, text=font_name, font=font_used, width=300)
        font_frame.add(message)
        i += 1
        if i > 4:
            font_frame = PanedWindow(frame, orient="horizontal")
            font_frame.pack(fill="x", expand=True)
            i = 0
    except:
        pass

# Update scrollregion when all widgets are in place
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))

frame.bind('<Configure>', on_configure)

root.mainloop()
