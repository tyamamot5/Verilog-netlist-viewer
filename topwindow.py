#
# $Id: topwindow.py,v 1.1 2017/06/14 03:01:53 tyamamot Exp $
#

import re, sys

from Tkinter import *
#from readNetlist import *
from canvas import *
import Instance
from Module import *
from Design import *
#from predefine_module import *
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
        # Create menubar
        menubar = Menu(master)
        
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.say_hi)
        filemenu.add_command(label="Open", command=self.say_hi)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        master.config(menu=menubar)

        # Create Canvas
        self.canvas =  DrawCanvas(master)

        # Create command entry
        #self.inst_nameentry = NameEntry(master)

    #def set_nameentry(self, name):
    #    self.inst_nameentry.set_name(name)


    
#my_settings = settings()
settings.my_design = Design()
settings.my_design.read_verilog("sample.vg")
#my_settings.get_current_design()
#my_settings.set_current_design( my_design.set_current_module( "cpu" ) )
settings.current_design = settings.my_design.set_current_module( "cpu" )

root = Tk()
app = CanvasWindow(master=root)
#app.set_nameentry("u_counter.u_ff0")
#app.display_instance("u_counter")
app.mainloop()
root.destroy()
