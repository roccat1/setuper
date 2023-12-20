import json, os
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
    label_file_explorer.configure(text="Folder Opened: "+filename)

def setupIt():
    global filename, output

    print('setting up...')

    try:
        filename
    except NameError:
        print('no folder selected')
        label_file_explorer.configure(text="no folder selected")
        return

    dirName= os.path.basename(filename)
    output=output.replace("@!*_*!@dirName@!*_*!@", '"'+dirName+'"')

    savedDir = saveDir(os.path.join(filename))
    output=output.replace("@!*_*!@savedDir@!*_*!@", str(savedDir))

    with open(os.path.join('setup.py'), 'w') as f: f.write(output.encode('UTF-8').decode('UTF-8'))

    print(str(os.path.basename(filename)), 'has been set up')
    label_file_explorer.configure(text=str(os.path.basename(filename))+" has been set up")
    messagebox.showinfo(str(os.path.basename(filename))+" has been set up")

def main():
    global label_file_explorer

    window = tk.Tk()
    window.title('setuper')
    window.geometry("700x300")
    window.config(background = "white")

    label_file_explorer = tk.Label(window, 
							text = "choose the folder to be converted to an executable",
							width = 100, height = 4, 
							fg = "blue")

    button_explore = tk.Button(window, 
						text = "Browse Folder",
						command = browseFolders) 
    
    button_run = tk.Button(window, 
						text = "Run program",
						command = setupIt) 
    
    button_exit = tk.Button(window, 
					text = "Exit",
					command = exit) 

    label_file_explorer.grid(column = 1, row = 1)

    button_explore.grid(column = 1, row = 2)

    button_run.grid(column = 1, row = 3)

    button_exit.grid(column = 1,row = 4)

    # Let the window wait for any events
    window.mainloop()

if __name__ == '__main__':
    main()