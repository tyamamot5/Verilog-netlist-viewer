#
# $Id: topwindow.py,v 1.3 2017/08/27 00:40:41 tyamamot Exp $
#

import re, sys

from Tkinter import *
from canvas import *
import Instance
from Module import *
from Design import *
from settings import *


class CanvasWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create(master)
        self.inst_nameentry = ""

    def say_hi(self):
        print "hi there, everyone!"

    def create(self,master):
        menubar = Menu(master)
        
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.say_hi)
        filemenu.add_command(label="Open", command=self.say_hi)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        master.config(menu=menubar)

        # Create Canvas
        self.canvas =  MyCanvas(master)
        self.canvas.set_design(settings.my_design)

    
settings.my_design = Design()
settings.my_design.read_verilog("sample.vg")
settings.current_design = settings.my_design.set_current_module( "cpu" )

root = Tk()
app = CanvasWindow(master=root)
app.mainloop()
root.destroy()
