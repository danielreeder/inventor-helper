import win32com.client as wc
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
import time

def close_part(part_name):
    inventor = wc.Dispatch("Inventor.Application")
    part_name = part_name + '.ipt'  # Ensure the part name is in lowercase and has the correct extension

    for doc in inventor.Documents:
        part_name_doc = doc.FullFileName.split('\\')[-1]
        print(part_name_doc)
        if part_name_doc.lower() == part_name.lower():
            doc.Close(False)
            print(f"Closed {part_name}.")
            return
    print(f"Part {part_name} is not currently open.")

def open_parts():
    inventor = wc.Dispatch("Inventor.Application")

    folder = askdirectory(initialdir=os.path.expanduser("~\\Desktop\\Inventor Projects"))

    for ipt in os.listdir(folder):
        to_open = folder + '/' + ipt
        inventor.Documents.open(to_open, True)
        print(f"Opened {to_open}.")

def close_parts():
    inventor = wc.Dispatch("Inventor.Application")
    inventor.Documents.CloseAll(False)
    print("Closed all documents.")

def get_parts():
    inventor = wc.Dispatch("Inventor.Application")
    parts = []
    thumbnails = []
    
    for doc in inventor.Documents.VisibleDocuments:
        if not doc.FullFileName.lower().endswith('.ipt'):
            continue
        
        parts.append(doc.FullFileName)

        width = 256
        height = 256

        doc.Activate()

        # Build a unique thumbnail path for each part
        part_name = os.path.splitext(os.path.basename(doc.FullFileName))[0]
        thumbnail_path = os.path.expanduser(f"~\\Desktop\\Inventor Projects\\{part_name}_thumbnail.bmp")
        
        # Save the active view as a bitmap
        inventor.ActiveView.SaveAsBitmap(thumbnail_path, width, height)
        print(f"Thumbnail image saved as {thumbnail_path}")

        thumbnails.append(thumbnail_path)
    return parts, thumbnails

def get_num_parts_open():
    inventor = wc.Dispatch("Inventor.Application")
    count = 0
    for doc in inventor.Documents:
        if doc.FullFileName.lower().endswith('.ipt'):
            count += 1
    return len(inventor.Documents)