from tkinter import Tk
from tkinter import *
from parts import *
from PIL import Image, ImageTk
from functools import partial

app = Tk(screenName='Inventor Helper', baseName='Inventor Helper', className='Inventor Helper')
app.title("Inventor Helper")
app.geometry("960x1080")

menu = Menu(app)
app.config(menu=menu)
file_menu = Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open Parts", command=open_parts)
file_menu.add_command(label="Close Parts", command=close_parts)
file_menu.add_command(label="Exit", command=app.quit)
parts, thumbnails = get_parts()
i = 0 
j = 0
part_cards = []

for part, thumbnail in zip(parts, thumbnails):
    part_name = part.split('\\')[-1]  # Get the file name only
    part_name = part_name.replace('.ipt', '')  # Remove the file extension

    pw = PanedWindow(orient='vertical', bg='lightblue')
    msg = Message(app, text=f"{part_name}", width=500)

    img = Image.open(thumbnail)
    tk_img = ImageTk.PhotoImage(img)
    img_label = Label(pw, image=tk_img, anchor='w')
    img_label.image = tk_img  # Keep a reference to avoid garbage collection
    btn = Button(pw, text="Close Part", command=partial(close_part, part_name))
    
    pw.add(msg)
    pw.add(img_label)
    pw.add(btn)
    pw.grid(row=j, column=i, padx=10, pady=10)
    if i == 1:
        i = 0
        j += 1
    else:
        i += 1
    part_cards.append(pw)
orig_num_parts = get_num_parts_open()

while True:
    current_num_parts = get_num_parts_open()
    pw_msg = PanedWindow(orient='vertical', bg='lightblue')
    no_parts_msg = Message(pw_msg, text="No parts open. Please open parts from the File menu.", width=500)
    if current_num_parts == 0:
        pw_msg.add(no_parts_msg)
        pw_msg.grid(row=0, column=0, padx=10, pady=10)
    if current_num_parts != orig_num_parts:
        parts, thumbnails = get_parts()
        orig_num_parts = current_num_parts
        print(f"Updated parts: {len(parts)}")
        for part_card in part_cards:
            part_card.destroy()
        # Remove the "no parts" message if it exists
        for widget in app.grid_slaves():
            if isinstance(widget, PanedWindow):
                children = widget.winfo_children()
                if any(isinstance(child, Message) and "No parts open" in str(child.cget("text")) for child in children):
                    widget.destroy()
        i = 0 
        j = 0
        part_cards = []

        for part, thumbnail in zip(parts, thumbnails):
            part = part.split('\\')[-1]  # Get the part name only
            part = part.replace('.ipt', '')  # Remove the file extension
            pw = PanedWindow(orient='vertical', bg='lightblue')
            msg = Message(app, text=part, width=500)

            img = Image.open(thumbnail)
            tk_img = ImageTk.PhotoImage(img)
            img_label = Label(pw, image=tk_img, anchor='w')
            img_label.image = tk_img  # Keep a reference to avoid garbage collection

            btn = Button(pw, text="Close Part", command=partial(close_part, part))
            pw.add(msg)
            pw.add(img_label)
            pw.add(btn)
            
            pw.grid(row=j, column=i, padx=10, pady=10)
            if i == 1:
                i = 0
                j += 1
            else:
                i += 1
            part_cards.append(pw)
    app.update()