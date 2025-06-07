import win32com.client as wc
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
import os
import time

def close_file(part_name):
    inventor = wc.Dispatch("Inventor.Application")
    part_name = part_name.split('.')[0]
    for doc in inventor.Documents:
        part_name_doc = doc.FullFileName.split('\\')[-1].split('.')[0]  # Get the part name without extension
        print(part_name_doc, part_name)
        if part_name_doc.lower() == part_name.lower():
            doc.Close(False)
            print(f"Closed {part_name}.")
            return
    print(f"Part {part_name} is not currently open.")

def open_folder():
    inventor = wc.Dispatch("Inventor.Application")

    folder = askdirectory(initialdir=os.path.expanduser("~\\Desktop\\Inventor Projects"))

    for ipt in os.listdir(folder):
        to_open = folder + '/' + ipt
        inventor.Documents.open(to_open, True)
        print(f"Opened {to_open}.")
    
def open_file():
    inventor = wc.Dispatch("Inventor.Application")
    file_path = askopenfilename(initialdir=os.path.expanduser("~\\Desktop\\Inventor Projects"))
    if file_path:
        inventor.Documents.Open(file_path, True)
        print(f"Opened {file_path}.")
    else:
        print("No file selected.")

def close_files():
    inventor = wc.Dispatch("Inventor.Application")
    inventor.Documents.CloseAll(False)
    print("Closed all documents.")

def get_open_files():
    inventor = wc.Dispatch("Inventor.Application")
    open_files = []
    thumbnails = []
    
    for doc in inventor.Documents.VisibleDocuments:
        open_files.append(doc.FullFileName)

        width = 256
        height = 256

        doc.Activate()

        # Build a unique thumbnail path for each part
        file_name = os.path.splitext(os.path.basename(doc.FullFileName))[0]
        thumbnail_path = os.path.expanduser(f"~\\Desktop\\Inventor Projects\\{file_name}_thumbnail.bmp")
        
        # Save the active view as a bitmap
        inventor.ActiveView.SaveAsBitmap(thumbnail_path, width, height)
        print(f"Thumbnail image saved as {thumbnail_path}")

        thumbnails.append(thumbnail_path)
    return open_files, thumbnails

def get_num_files_open():
    inventor = wc.Dispatch("Inventor.Application")
    return len(inventor.Documents.VisibleDocuments)

inventor = wc.Dispatch("Inventor.Application")
print(inventor.Documents.VisibleDocuments.count)