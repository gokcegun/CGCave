from tkinter import *
from tkinter.filedialog import askdirectory
import os
import glob
import os.path
import time
import threading
from pathlib import Path


class CgCave:
    project_path = "undefined"
    refreshthread = None



    def __init__(self, master):
        favicon = PhotoImage(file="images/favicon.png")
        master.tk.call('wm', 'iconphoto', root._w, favicon)
        master.minsize(width=640, height=640)
        master.maxsize(width=640, height=640)
        master.title("CGCave 3D Help")
        top_frame = Frame(master)
        top_frame.grid(row=0, padx=20, pady=5)
        mid_frame = Frame(master)
        mid_frame.grid(row=1, padx=20, pady=5)
        bottom_frame = Frame(master)
        bottom_frame.grid(row=2, padx=20, pady=5)
        mid_rightframe = Frame(mid_frame)
        mid_rightframe.grid(column=3)

        my_file = Path("lastpath.txt")
        if my_file.is_file():
            last_pathfile = open("lastpath.txt", "r")
            last_pathrec = last_pathfile.read()
        else:
            last_path = open("lastpath.txt", "w")
            last_path.write("c:/")
            last_path.close()
            last_pathfile = open("lastpath.txt", "r")
            last_pathrec = last_pathfile.read()

        self.entry_1 = Entry(top_frame, width=90)
        self.entry_1.grid(row=0)
        self.browseButton = Button(top_frame, text="...", command=self.browsePath)
        self.browseButton.grid(row=0, column=1, padx=5)

        self.refresh_image = PhotoImage(file="images/refreshimage.png")
        self.refresh_button = Button(top_frame, text="Refresh", width=20)
        self.refresh_button.config(image=self.refresh_image)
        self.refresh_button.grid(row=0, column=2)
        self.refresh_button.bind("<Button-1>", self.refreshlists)

        self.quitButton = Button(bottom_frame, text="Quit", command=self.on_closing, width=30)
        self.quitButton.grid(row=0, column=1, padx=30)

        self.debug_button = Button(bottom_frame, text="debug", command=self.debug, width=30)
        self.debug_button.grid(row=0, column=0, padx=30)

        self.render_list = Listbox(mid_frame, width=30)
        self.render_list.grid(row=0, column=1)
        self.render_list.bind('<Double-Button-1>', self.openRender)

        self.model_list = Listbox(mid_frame, width=30)
        self.model_list.grid(row=0, column=2, padx=5)
        self.model_list.bind('<Double-Button-1>', self.openModel)

        self.entry_1.insert(END, last_pathrec)

        CgCave.project_path = last_pathrec

        self.filllistbox("jpg", self.render_list)
        self.filllistbox("max", self.model_list)

        self.autoback_button = Button(mid_rightframe, text="Last AutoBack:", width=31)
        self.autoback_button.grid(row=0)
        self.autoback_button.bind("<Button-1>", self.launchautoback)

        self.refreshlists("launch")

    def timer1(self):
        print("in timer")
        self.refreshthread = threading.Timer(1.0, self.timer1)
        self.refreshthread.start()
        self.refreshlists(self)


    def debug(self):
        print("debug")
        print("a")

    def launchautoback(self, event):
        list_of_files = glob.glob(CgCave.project_path + "/autoback/*.max")
        last_autoback = max(list_of_files, key=os.path.getmtime)
        os.startfile(last_autoback)

    def refreshlists(self, event):
        print("in refresh")
        self.filllistbox("jpg", self.render_list)
        self.filllistbox("max", self.model_list)
        list_of_files = glob.glob(CgCave.project_path + "/autoback/*.max")
        if len(list_of_files) != 0:
            last_autoback = max(list_of_files, key=os.path.getmtime)
            last_abtime = time.ctime(os.path.getmtime(last_autoback))
            self.autoback_button["text"] = "Last AutoBack: " + last_abtime


    def filllistbox(self, file_type, list_box):
        sub_path = {
            "jpg": "/renderoutput",
            "max": "/scenes"}
        list_of_files = glob.glob(CgCave.project_path + sub_path[file_type] + "/*." + file_type)
        if list_box != "none":
            list_box.delete(0, END)
            a = 0
            for files in list_of_files:
                a += 1
                files1 = files.split("/")
                filecount = len(files1)
                list_box.insert(a, files1[filecount - 1])
        return list_of_files

    def browsePath(self):
        CgCave.project_path = askdirectory()

        last_path = open("lastpath.txt", "w")
        last_path.write(CgCave.project_path)
        last_path.close()

        self.filllistbox("jpg", self.render_list)
        self.filllistbox("max", self.model_list)

    def openRender(self, event):
        if CgCave.project_path == "undefined":
            print("select folder")
        else:
            list_of_files = self.filllistbox("jpg", "none")
            if len(list_of_files) != 0:
                chosen_file = self.render_list.curselection()
                selected_file = list_of_files[chosen_file[0]]
                os.startfile(selected_file)
            else:
                print("Choose a file")

    def openModel(self, event):
        if CgCave.project_path == "undefined":
            print("select folder")
        else:
            list_of_files = self.filllistbox("max", "none")
            if len(list_of_files) != 0:
                chosen_file = self.model_list.curselection()
                selected_model = list_of_files[chosen_file[0]]
                os.startfile(selected_model)

    def on_closing(self):
        self.refreshthread.cancel()
        root.destroy()


print("init")
root = Tk()
b = CgCave(root)
b.timer1()
root.protocol("WM_DELETE_WINDOW", b.on_closing)
root = mainloop()
