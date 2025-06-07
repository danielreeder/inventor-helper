from tkinter import Tk
from tkinter import *
from parts import *
from PIL import Image, ImageTk
from functools import partial

class App():
    def __init__(self):
        self.app = Tk(screenName='Inventor Helper', baseName='Inventor Helper', className='Inventor Helper')
        self.num_parts = get_num_files_open()
        self.part_cards = []
        self.part_cards_container = PanedWindow(self.app, orient='vertical', bg='lightblue')

    def main_loop(self):
        current_num_parts = get_num_files_open()
        pw_msg = PanedWindow(orient='vertical', bg='lightblue')
        no_parts_msg = Message(pw_msg, text="No parts open. Please open parts from the File menu.", width=500)
        if current_num_parts == 0:
            pw_msg.add(no_parts_msg)
            pw_msg.grid(row=0, column=0, padx=10, pady=10)
        if current_num_parts != self.num_parts:
            self.num_parts = current_num_parts
            
            for part_card in self.part_cards:
                part_card.destroy()
            self.part_cards = []

            # Remove the "no parts" message if it exists
            for widget in self.app.grid_slaves():
                if isinstance(widget, PanedWindow):
                    children = widget.winfo_children()
                    if any(isinstance(child, Message) and "No parts open" in str(child.cget("text")) for child in children):
                        widget.destroy()

            self.setup_part_cards()
            print(f"Updated parts: {len(self.part_cards)}")

        self.app.after(100, self.main_loop)  # Check for updates every second

    def run(self):
        wc.Dispatch("Inventor.Application")
        self.setup()
        self.app.after(100, self.main_loop)  # Check for updates every second
        self.app.mainloop()

    def setup(self):
        self.app.title("Inventor Helper")
        self.app.geometry("960x1080")

        file_menu = self.add_menu(self.app, "File")
        file_menu.add_command(label="Open File", command=open_file)
        file_menu.add_command(label="Open Folder", command=open_folder)
        file_menu.add_command(label="Close Files", command=close_files)
        file_menu.add_command(label="Exit", command=self.app.quit)
        self.setup_part_cards()
        self.part_cards_container.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    def add_menu(self, parent, label):
        menu = Menu(parent)
        self.app.config(menu=menu)
        file_menu = Menu(menu)
        menu.add_cascade(label=label, menu=file_menu)
        return file_menu

    def setup_part_cards(self):
        parts, thumbnails = get_open_files()
        i = 0 
        j = 0

        for part, thumbnail in zip(parts, thumbnails):
            part_name = part.split('\\')[-1]  # Get the file name only
            part_name = part_name.split('.')[0]  # Remove the file extension

            pw1 = PanedWindow(orient='vertical', bg='lightblue')
            pw2 = PanedWindow(pw1, orient='horizontal', bg='lightblue')
            pw2_1 = PanedWindow(pw2, orient='vertical', bg='lightblue')

            msg = Message(self.app, text=f"{part_name}", width=500)

            img = Image.open(thumbnail)
            tk_img = ImageTk.PhotoImage(img)
            img_label = Label(pw2, image=tk_img, anchor='w')
            img_label.image = tk_img  # Keep a reference to avoid garbage collection
            btn = Button(pw2_1, text="Close Part", command=partial(close_file, part_name))
            btn.config(width=10, height=2, bg='red', fg='white', font=('Arial', 12, 'bold'))

            pw2_1.add(btn)

            pw2.add(img_label)
            pw2.add(pw2_1)
            
            pw1.add(msg)
            pw1.add(pw2)

            row = j
            col = i
            self.part_cards_container.add(pw1)

            pw1.grid(row=row, column=col, padx=10, pady=10)

            if i == 2:
                i = 0
                j += 1
            else:
                i += 1
            self.part_cards.append(pw1)
        
App().run()