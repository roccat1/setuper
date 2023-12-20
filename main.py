import json, os, sys
import tkinter as tk
from tkinter import filedialog, messagebox


output = '''
# -*- coding: utf-8 -*-
#executable created by Roc Rodríguez Arumí (https://github.com/roccat1)
import json, os

savedDir = @!*_*!@savedDir@!*_*!@

#function to write a file
def writeFile(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

def loadDir(path, data):
    #loads the directory structure of the given path
    for root, dirs, files in data:
        root=root[1:]
        #create directories
        for dir in dirs:
            os.makedirs(os.path.join(path, root, dir), exist_ok=True)
        #create files
        for file in files:
            writeFile(os.path.join(path, root, file[0]), file[1])

def main():
    os.makedirs(@!*_*!@dirName@!*_*!@, exist_ok=True)
    loadDir(os.path.join(@!*_*!@dirName@!*_*!@), savedDir)

if __name__ == '__main__':
    main() 
    print('done')
'''

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#function to read a file
def readFile(filename):
    with open(filename, 'rb') as f:
        data = f.read()    
    return data

#function to write a file
def writeFile(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)


#function to read a json file
def readJson(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

#function to write a json file
def writeJson(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def saveDir(path):
    #saves the directory structure of the given path
    result = []
    #cycle through the directory [path dir, dirs inside, [name files inside, content],...]
    for root, dirs, files in os.walk(path):
        filesResult = []
        #save files
        for file in files:
            filesResult.append([file, readFile(os.path.join(root, file))])
        result.append([root.replace(path, ''), dirs, filesResult])

    return result

def loadDir(path, data):
    #loads the directory structure of the given path
    for root, dirs, files in data:
        root=root[1:]
        #create directories
        for dir in dirs:
            os.makedirs(os.path.join(path, root, dir), exist_ok=True)
        #create files
        for file in files:
            writeFile(os.path.join(path, root, file[0]), file[1])

def browseFolders():
    global filename
    filename = filedialog.askdirectory()
    canvas.itemconfig(textMod, text="Folder Opened: "+os.path.basename(filename))

def setupIt():
    global filename, output

    print('setting up...')

    try:
        filename
    except NameError:
        print('no folder selected')
        canvas.itemconfig(textMod, text="No folder selected")
        return

    dirName= os.path.basename(filename)
    output=output.replace("@!*_*!@dirName@!*_*!@", '"'+dirName+'"')

    savedDir = saveDir(os.path.join(filename))
    output=output.replace("@!*_*!@savedDir@!*_*!@", str(savedDir))

    with open(os.path.join('setup.py'), 'w') as f: f.write(output.encode('UTF-8').decode('UTF-8'))

    print(str(os.path.basename(filename)), 'has been set up')
    canvas.itemconfig(textMod, text=str(os.path.basename(filename))+" has been set up")
    messagebox.showinfo("Done!", str(os.path.basename(filename))+" has been set up")

def main():
    global canvas, textMod

    window = tk.Tk()

    window.geometry("640x480")
    window.configure(bg = "#C8EABC")


    canvas = tk.Canvas(
        window,
        bg = "#C8EABC",
        height = 480,
        width = 640,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        131.0,
        104.0,
        469.0,
        fill="#C8EABC",
        outline="")

    canvas.create_rectangle(
        0.0,
        0.0,
        640.0,
        118.0,
        fill="#B5E4FF",
        outline="")

    canvas.create_text(
        167.0,
        13.0,
        anchor="nw",
        text="Welcome to Setuper",
        fill="#000000",
        font=("Inter", 32 * -1)
    )

    textMod = canvas.create_text(
        10.0,
        66.0,
        anchor="nw",
        text="Choose Folder",
        fill="#000000",
        font=("Inter", 30 * -1)
    )

    button_image_1 = tk.PhotoImage(
        file=resource_path("assets\\frame0\\browseFolder.png"))
    button_1 = tk.Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=browseFolders,
        relief="flat"
    )
    button_1.place(
        x=21.0,
        y=140.0,
        width=598.0,
        height=80.0
    )

    button_image_2 = tk.PhotoImage(
        file=resource_path("assets\\frame0\\run.png"))
    button_2 = tk.Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=setupIt,
        relief="flat"
    )
    button_2.place(
        x=21.0,
        y=249.0,
        width=599.0,
        height=80.0
    )

    button_image_3 = tk.PhotoImage(
        file=resource_path("assets\\frame0\\exit.png"))
    button_3 = tk.Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=exit,
        relief="flat"
    )
    button_3.place(
        x=21.0,
        y=367.0,
        width=599.0,
        height=80.0
    )
    window.resizable(False, False)
    window.mainloop()


if __name__ == '__main__':
    main()