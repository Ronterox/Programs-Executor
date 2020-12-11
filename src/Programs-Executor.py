import tkinter as tk
from tkinter import filedialog, ttk
import os
import webbrowser

APP_TITLE = "PROGRAMS EXECUTOR"


class ProgramExecutor:
    applications = []
    urls = []

    def __init__(self):
        self.applications = []
        self.root = tk.Tk()
        self.root.wm_title(APP_TITLE)
        self.root.configure(bg="#00BFA5")
        self.root.wm_maxsize(500, 400)

        titleStyle = ttk.Style()
        titleStyle.configure('TLabel', font=('calibri', 15, 'bold'), anchor='center', foreground='white',
                             borderwidth='1', padding=10, margin=15, width=50, background='#26A69A')

        ttk.Label(self.root, text='Welcome To Programs Executor!', style='TLabel').pack()

        tk.Canvas(self.root, height=400, width=500, bg='#00695C').pack()

        self.frame_apps = ttk.Frame(self.root)
        self.frame_apps.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.15)

        self.frame_buttons = ttk.Frame(self.root, style='TFrame')
        self.frame_buttons.place(relwidth=0.8, relheight=0.1, relx=0.1, rely=0.85)

        buttonStyle = ttk.Style()
        buttonStyle.configure('TButton', font=('calibri', 10, 'bold'),
                              borderwidth='1', padding=5, margin=15, width=50, background='#26A69A')

        actionButtonStyle = ttk.Style()
        actionButtonStyle.configure('Action.TButton', font=('calibri', 10, 'bold'),
                                    borderwidth='1', padding=5, margin=15, width=20)

        frameStyle = ttk.Style()
        frameStyle.configure('TFrame', font=('Arial', 10, 'bold'), borderwidth='1', padding=5, margin=15,
                             background='#00BFA5')

        ttk.Button(self.frame_buttons, text='Open a File', command=self.addApp,
                   style='Action.TButton').pack(side="left")

        ttk.Button(self.frame_buttons, text='Run Applications', command=self.runApps,
                   style='Action.TButton').pack(side="right")

        ttk.Button(self.frame_buttons, text='Load URL', command=self.popupUrl,
                   style='Action.TButton').pack(side="left")

    def popupUrl(self):
        window = PopupWindow(self.root)
        self.root.wait_window(window.top)
        self.addUrl(window.getValue())
        self.updateLabels()

    def runUrls(self):
        for url in self.urls:
            webbrowser.open(url)

    def addUrl(self, url):
        if url:
            self.urls.append(url.strip())

    def saveApps(self):
        with open('saved_apps.txt', 'w') as file:
            for app in self.applications:
                file.write(app + '\n')

    def saveUrls(self):
        with open('saved_urls.txt', 'w') as file:
            for url in self.urls:
                file.write(url + '\n')

    def addApp(self):
        filename = filedialog.askopenfilename(initialdir='/', title='Select an Executable!',
                                              filetypes=(('Executables', '*.exe'), ('All Files', '*')))
        if filename:
            self.applications.append(filename)
            print(filename)
            self.updateLabels()

    def updateLabels(self):
        for widget in self.frame_apps.winfo_children():
            widget.destroy()

        def my_popup(e):
            contextmenu.tk_popup(e.x_root, e.y_root)

        def deleteLabel(appName):
            self.applications = [application for application in self.applications
                                 if os.path.basename(application).strip().lower() != appName.strip().lower()]
            self.updateLabels()

        for app in self.applications:
            label = ttk.Label(self.frame_apps, text=os.path.basename(app).upper(), style='TButton')
            contextmenu = tk.Menu(label, tearoff=False)
            contextmenu.add_command(label='Delete', command=lambda: deleteLabel(label['text']))
            contextmenu.add_separator()
            contextmenu.add_command(label='Exit', command=self.root.quit)

            label.bind('<Button-3>', my_popup)
            label.pack()

        for url in self.urls:
            label = ttk.Label(self.frame_apps, text=os.path.basename(url).upper(), style='TButton')
            contextmenu = tk.Menu(label, tearoff=False)
            contextmenu.add_command(label='Delete', command=lambda: deleteLabel(label['text']))
            contextmenu.add_separator()
            contextmenu.add_command(label='Exit', command=self.root.quit)

            label.bind('<Button-3>', my_popup)
            label.pack()

    def runApps(self):
        for app in self.applications:
            os.startfile(app.replace("\n", ""))
        self.runUrls()

    def start(self):
        if os.path.isfile('saved_apps.txt'):
            with open('saved_apps.txt', 'r') as savedFile:
                self.applications = [line for line in savedFile if line.strip()]
        if os.path.isfile('saved_urls.txt'):
            with open('saved_urls.txt', 'r') as savedFile:
                self.urls = [line for line in savedFile if line.strip()]

        self.updateLabels()
        self.root.mainloop()

        self.saveApps()
        self.saveUrls()


class PopupWindow(object):
    value = None

    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        top.wm_maxsize(500, 100)
        top.title('Load URL - ' + APP_TITLE)
        tk.Label(top, text='Write an URL', padx=15, pady=15).pack()
        self.entry = tk.Entry(top, width=80)
        self.entry.pack()
        tk.Button(top, text='Add', command=self.cleanup).pack()

    def cleanup(self):
        self.value = self.entry.get()
        self.top.destroy()

    def getValue(self):
        return self.value


program_executor = ProgramExecutor()
program_executor.start()
