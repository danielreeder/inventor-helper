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
        self.inventor = wc.Dispatch("Inventor.Application")
        self.inventor.Visible = True  # Ensure Inventor is visible

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
        file_menu.add_command(label="Open File", command=partial(open_file, inventor=self.inventor))
        file_menu.add_command(label="Open Folder", command=partial(open_folder, inventor=self.inventor))
        file_menu.add_command(label="Close Files", command=partial(close_files, inventor=self.inventor))
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
        parts, thumbnails = get_open_files(self.inventor)
        i = 0 
        j = 0

        for part, thumbnail in zip(parts, thumbnails):
            part_name = part.split('\\')[-1]  # Get the file name only
            part_name = part_name.split('.')[0]  # Remove the file extension

            main_part_card_window = PanedWindow(self.part_cards_container, orient='vertical', bg='lightblue')
            part_card_name_window = PanedWindow(main_part_card_window, orient='horizontal', bg='lightblue')
            part_card_image_window = PanedWindow(main_part_card_window, orient='horizontal', bg='lightblue')
            part_card_button_window = PanedWindow(part_card_image_window, orient='vertical', bg='lightblue')

            msg = Message(part_card_name_window, text=f"{part_name}", width=500)
            part_card_name_window.add(msg)

            img = Image.open(thumbnail)
            tk_img = ImageTk.PhotoImage(img)
            img_label = Label(part_card_image_window, image=tk_img, anchor='w')
            img_label.image = tk_img  # Keep a reference to avoid garbage collection
            part_card_image_window.add(img_label)

            close_part_button = self.create_button("Close Part", 'red', close_file, part_name, self.inventor)
            part_card_button_window.add(close_part_button)

            save_as_stl_button = self.create_button("Save as STL", 'blue', save_file_as_stl, part_name, self.inventor)
            part_card_button_window.add(save_as_stl_button)

            part_card_image_window.add(part_card_button_window)
            main_part_card_window.add(part_card_name_window)
            main_part_card_window.add(part_card_image_window)

            row = j
            col = i
            self.part_cards_container.add(main_part_card_window)

            main_part_card_window.grid(row=row, column=col, padx=10, pady=10)

            if i == 1:
                i = 0
                j += 1
            else:
                i += 1
            self.part_cards.append(main_part_card_window)
    
    def create_button(self, text, color, command, *args):
        btn = Button(self.app, text=text, command=partial(command, *args))
        btn.config(width=12, height=1, bg=color, fg='white', font=('Terminal', 10, 'bold'))
        btn.bind("<Enter>", lambda e: e.widget.config(bg='gray'))
        btn.bind("<Leave>", lambda e: e.widget.config(bg=color))
        return btn
    
App().run()