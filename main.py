#image = nombre,ruta,lenguajeP,status,fecha,intentos,tipo,dificultad

import os
import tkinter as tk
from tkinter import ttk
from tkinter import Checkbutton, IntVar
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Style
from functools import partial
import threading
from PIL import ImageTk, Image
import shutil

background_color = "#95b589"
opt_bar_color = "#6e7f68"
h1_color = "#90908c"
conts_btn_color = "#616d5c"
prob_btn_color = "#4682a7"
AC_color = "#61d649"
WA_color = "#ea2626"
TLI_color = "#eadb26"
window_width = 1000
window_height = 500
contests_path = "contests/"
icons_path = "icons/"
class VerticalScrolledFrame(tk.Frame):
    def __init__(self, parent,color, *args ,**kw):
        tk.Frame.__init__(self, parent, *args, **kw)
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL,width=20)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.TRUE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set,height = 500,bg = color)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)
        def _configure_interior(event):
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)
        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
        interior.bind_all('<MouseWheel>', lambda event:     vscrollbar.yview("scroll",event.delta,"units"))
class Main(object):
    def __init__(self,master):
        self.master = master
        self.initial_settings()
        self.optiones_bar()
        self.constest_list()
        self.problems_list()
        self.master.mainloop()
    def __get_contests(self):
        return os.listdir(contests_path)
    def initial_settings(self):
        self.master.title("Alpha 6")
        self.master.resizable(False,False)
        self.master.geometry("1000x500")
        self.master.config(bg=background_color)
    def optiones_bar(self):
        opt_bar = tk.Frame(self.master)
        opt_bar.config(width=window_width,height=40,bg=opt_bar_color)
        opt_bar.pack(fill = "y")
        opt_bar.pack_propagate(False)
        btn1 = tk.Button(opt_bar,text="Add new contest",font=("Arial",18),bg=opt_bar_color,bd = 3,relief=tk.GROOVE,command = self.new_contest)
        btn2 = tk.Button(opt_bar,text="Add new problem",font=("Arial",18),bg=opt_bar_color,bd = 3,relief=tk.GROOVE)
        btn3 = tk.Button(opt_bar,text="Push on Github",font=("Arial",18),bg=opt_bar_color,bd = 3,relief=tk.GROOVE)
        btn4 = tk.Button(opt_bar,text="Statistics",font=("Arial",18),bg=opt_bar_color,bd = 3,relief=tk.GROOVE)
        btn5 = tk.Button(opt_bar,text="Settings",font=("Arial",18),bg=opt_bar_color,bd = 3,relief=tk.GROOVE)
        btn6 = tk.Button(opt_bar,text="Information",font=("Arial",18),bg=opt_bar_color,bd = 3,relief=tk.GROOVE)
        btn1.pack(side = tk.LEFT)
        btn2.pack(side = tk.LEFT)
        btn3.pack(side = tk.LEFT)
        btn4.pack(side = tk.LEFT)
        btn5.pack(side = tk.LEFT)
        btn6.pack(side = tk.LEFT)
    def constest_list(self):
        conts_list = tk.Frame(self.master)
        conts_list.config(width=window_width/3,height=30,bg=opt_bar_color)
        conts_list.pack(side = tk.LEFT,fill="y")
        conts_list.pack_propagate(False)
        h1 = tk.Frame(conts_list)
        h1.config(width=window_width/3,height=40,bg=h1_color)
        h1.pack(side = tk.TOP)
        h1.pack_propagate(False)
        label1 = tk.Label(h1,text="Contests",font=("Arial",18),bg=h1_color,bd = 3)
        label1.pack()
        self.contest_scframe = VerticalScrolledFrame(conts_list,color = opt_bar_color)
        self.contest_scframe.pack()
        img = Image.open("icons/"+"delate.png")
        img = img.resize((45,45), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        for contest in self.__get_contests():
            index = tk.Frame(self.contest_scframe.interior,width = int(window_width/3),height = 2,bg = background_color)
            index.pack(side = tk.TOP)
            delate = tk.Button(index,image = photo,bg = opt_bar_color,command = partial(self.delate_contest,contest))
            delate.pack(side = tk.LEFT)
            delate.image = photo
            index = tk.Button(index,text = str(contest),font=("Arial",12),relief = tk.RAISED,width = 50,height = 2,bg = conts_btn_color,command = partial(self.show_problems,contest))
            index.pack(side = tk.LEFT)
    def delate_contest(self,contest):
            if(messagebox.askokcancel("Delate contest","Would you like to delete the contest "+contest+"?")):
                shutil.rmtree(os.path.join(contests_path,contest))
                img = Image.open("icons/"+"delate.png")
                img = img.resize((45,45), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)
                for widget in self.contest_scframe.interior.winfo_children():
                        widget.destroy()
                for contest in self.__get_contests():
                    index = tk.Frame(self.contest_scframe.interior,width = int(window_width/3),height = 2,bg = background_color)
                    index.pack(side = tk.TOP)
                    delate = tk.Button(index,image = photo,bg = opt_bar_color,command = partial(self.delate_contest,contest))
                    delate.pack(side = tk.LEFT)
                    delate.image = photo
                    index = tk.Button(index,text = str(contest),font=("Arial",12),relief = tk.RAISED,width = 50,height = 2,bg = conts_btn_color,command = partial(self.show_problems,contest))
                    index.pack(side = tk.LEFT)
    def problems_list(self):
        conts_list = tk.Frame(self.master)
        conts_list.config(width=2*window_width/3,height=30,bg=background_color)
        conts_list.pack(side = tk.LEFT,fill="y")
        conts_list.pack_propagate(False)
        h1 = tk.Frame(conts_list)
        h1.config(width=2*window_width/3,height=40,bg=h1_color)
        h1.pack(side = tk.TOP)
        h1.pack_propagate(False)
        self.problems_label = tk.Label(h1,text="Problems("+str(self.__get_contests()[0])+")",font=("Arial",18),bg=h1_color,bd = 3)
        self.problems_label.pack()
        scframe = VerticalScrolledFrame(conts_list,color = background_color)
        scframe.pack()
        img = Image.open("icons/"+"delate.png")
        img = img.resize((25,25), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        for contest in range(100):
            index = tk.Frame(scframe.interior,width = int(2*window_width/3),height = 2,bg = background_color)
            index.pack(side = tk.TOP)
            delate = tk.Button(index,image = photo,bg = opt_bar_color)
            delate.image = photo
            label1 = tk.Label(index,width = 18,text="Not solved",font=("Arial",10))
            btn1 = tk.Button(index,width = 35,text="hola.cpp",font=("Arial",11),bg = prob_btn_color)
            btn2 = tk.Button(index,width = 5,text="AC",font=("Arial",11),bg = AC_color)
            btn3 = tk.Button(index,width = 5,text="WA",font=("Arial",11),bg = WA_color)
            btn4 = tk.Button(index,width = 5,text="TLI",font=("Arial",11),bg = TLI_color)
            delate.pack(side = tk.LEFT)
            btn1.pack(side = tk.LEFT)
            btn2.pack(side = tk.LEFT)
            btn3.pack(side = tk.LEFT)
            btn4.pack(side = tk.LEFT)
            label1.pack(side = tk.LEFT)
    def show_problems(self,contest):
        self.problems_label["text"] = "Problems("+contest+")"
    def new_contest(self):
        window = tk.Toplevel(self.master)
        window.pack_propagate(False)
        window.config(width="350", height="150",bg=background_color)
        header = tk.Frame(window)
        window.title("Results")
        header.config(width="350",height="50",bg=background_color)
        header.pack(fill="y")
        header.pack_propagate(False)
        title = tk.Label(header,width="350",text="Add new contest",font=("Arial",25),bg=h1_color)
        label1 = tk.Label(window,text="Name : ",font=("Arial",15),bg=background_color)
        entry1 = tk.Entry(window,font=("Arial",15))
        btn1 = tk.Button(window,width = 100,text="Add contest",font=("Arial",15),bg = AC_color,command = lambda: self.accion_add_contest(window,entry1.get()))
        title.pack()
        btn1.pack(side = tk.BOTTOM)
        label1.pack(side = tk.LEFT,padx = 15)
        entry1.pack(side = tk.LEFT)
    def accion_add_contest(self,window,new_contest):
        if(not(new_contest in self.__get_contests())):
            os.mkdir(os.path.join(contests_path,new_contest))
            for widget in self.contest_scframe.interior.winfo_children():
                    widget.destroy()
            img = Image.open("icons/"+"delate.png")
            img = img.resize((45,45), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            for contest in self.__get_contests():
                index = tk.Frame(self.contest_scframe.interior,width = int(window_width/3),height = 2,bg = background_color)
                index.pack(side = tk.TOP)
                delate = tk.Button(index,image = photo,bg = opt_bar_color,command = partial(self.delate_contest,contest))
                delate.pack(side = tk.LEFT)
                delate.image = photo
                index = tk.Button(index,text = str(contest),font=("Arial",12),relief = tk.RAISED,width = 50,height = 2,bg = conts_btn_color,command = partial(self.show_problems,contest))
                index.pack(side = tk.LEFT)
            window.destroy()
            window.update()
root = tk.Tk()
my_gui = Main(root)
