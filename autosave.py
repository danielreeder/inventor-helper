import win32com.client as wc
from tkinter import Tk
from tkinter.filedialog import askdirectory
import os
import time

def save_file_as_stl():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    folder = ''
    if os.path.exists("folder.txt"):
        with open("folder.txt", 'r') as f:
            folder = f.readline().strip()
    else:
        folder = askdirectory(initialdir=os.path.expanduser("~\\Desktop")) # show an "Open" dialog box and return the path to the selected file
        with open("folder.txt", 'w') as f:
            f.write(folder)

    try:
        wc.GetActiveObject("Inventor.Application")
    except:
        print("Inventor is not currently open.")
        return
    
    inventor = wc.Dispatch("Inventor.Application")
    file_name = ''

    try:
        file_name = inventor.ActiveDocument.FullDocumentName.split('\\')[-1]
    except:
        print("There is no document open.")
        return

    file_name = file_name.split('.')[0]

    output = folder + "/" + file_name + ".stl"
    print(output)
    inventor.ActiveDocument.SaveAs(output, 15100)

    print(f"Document saved as {file_name}.stl to {folder}.")
    time.sleep(1)

save_file_as_stl()

