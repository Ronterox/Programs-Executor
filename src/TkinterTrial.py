import tkinter as tk
from tkinter import filedialog
import os

applications = []


def saveApps():
    with open('saved_apps.txt', 'w') as file:
        for app in applications:
            file.write(app + '\n')


def addApp():
    filename = filedialog.askopenfilename(initialdir='/', title='Select an Executable!',
                                          filetypes=(('Executables', '*.exe'), ('All Files', '*')))
    if filename:
        applications.append(filename)
        print(filename)
        updateLabels()


def updateLabels():
    for widget in frame.winfo_children():
        widget.destroy()
    for app in applications:
        label = tk.Label(frame, text=app)
        label.pack()


def runApps():
    for app in applications:
        os.startfile(app)


# Application Layout
root = tk.Tk()

canvas = tk.Canvas(root, height=500, width=500, bg='#00695C')
canvas.pack()

frame = tk.Frame(root, bg='#A7FFEB')
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

openAppButton = tk.Button(root, text='Open a File', padx=10, pady=5, fg='black', bg='#A7FFEB', command=addApp)
openAppButton.pack()

runAppsButton = tk.Button(root, text='Run Applications', padx=10, pady=5, fg='black', bg='#A7FFEB', command=runApps)
runAppsButton.pack()

if os.path.isfile('saved_apps.txt'):  # before showing the GUI we check for a saved file
    with open('saved_apps.txt', 'r') as savedFile:
        applications = [line for line in savedFile if line.strip()]
        updateLabels()

root.mainloop()

saveApps()
