#
# $Id: canvas.py,v 1.2 2017/08/11 06:06:48 tyamamot Exp $
#

import re, sys, time

from Tkinter import *
from Module import *
from settings import *

class DrawCanvas:
    def __init__(self, root):
        framemid = Frame(root)
        framemid["relief"] = "flat"
        framemid.pack(fill="both", expand="yes")

        self.canvas = Canvas(framemid)
        canvas = self.canvas
        self.canvas["scrollregion"] = "-2500 0 2500 2500"
        self.canvas["width"] = "500"
        self.canvas["height"] = "400"
        self.canvas["xscrollcommand"] = "scroll_row set"
        self.canvas["yscrollcommand"] = "scroll_col set -relief sunken"
        self.canvas["borderwidth"] = "2"
        self.canvas["confine"] = "false"

        self.canvas.tag_bind(settings.tag_instance_box, '<ButtonPress-1>'  , self.start_move_instance)
        self.canvas.tag_bind(settings.tag_instance_box, '<B1-Motion>'      , self.moving_instance)
        self.canvas.tag_bind(settings.tag_instance_box, '<ButtonRelease-1>', self.end_move_instance)

        # $c bind cellbox <B1-Motion>		    "ds dragMoveIns %x %y"
        # $c bind cellbox <ButtonRelease-1>	    "ds moveIns %x %y"

        # $c bind cellbox <Enter>		    "ds insAnyEnter"
        # $c bind cellbox <Leave>		    "ds insAnyLeave"
        # $c bind cellbox <Double-Button-1>	    "ds toggleAbbrName"
        # $c bind cellbox <Shift-1>		    "ds markObject ins" 
        # $c bind cellbox <ButtonPress-3>	    "ds popup_on_cell %X %Y" 
        # $c bind cellbox <ButtonRelease-3>	    "ds popdown_on_cell" 

        self.canvas.tag_bind(settings.tag_input,  '<1>', self.add_instance_input)
        self.canvas.tag_bind(settings.tag_output, '<1>', self.add_instance_output)

        # $c bind inpin <Any-Enter>		    "ds portAnyEnter"
        # $c bind inpin <Any-Leave>		    "ds portAnyLeave"
        # $c bind inpin <1>			    "ds addInsIn"
        # $c bind inpin <Shift-1>		    "ds markObject port" 
        # $c bind inpin <ButtonPress-3>	    "ds popup_on_pin %X %Y"
        # $c bind inpin <ButtonRelease-3>	    "ds popdown_on_pin"

        # $c bind outpin <Any-Enter>		    "ds portAnyEnter" 
        # $c bind outpin <Any-Leave>		    "ds portAnyLeave"
        # $c bind outpin <1>			    "ds addInsOut" 
        # $c bind outpin <Shift-1>		    "ds markObject port" 
        # $c bind outpin <ButtonPress-3>	    "ds popup_on_pin %X %Y"
        # $c bind outpin <ButtonRelease-3>	    "ds popdown_on_pin"

        # $C bind cellname <1>		    "ds startDrag %x %y"
        # $c bind cellname <B1-Motion>	    "ds itemDrag %x %y"
        # $c bind cellname <Enter>		    "ds insAnyEnter"
        # $c bind cellname <Leave>		    "ds insAnyLeave"
        # $c bind cellname <Double-Button-1>	    "ds toggleAbbrName"

        # $c bind pinname <ButtonPress-1>	"ds startMovePortName %x %y"
        # $c bind pinname <B1-Motion>		"ds dragPortName %x %y"
        # $c bind pinname <ButtonRelease-1>	"ds endMovePortName %x %y"
        # $c bind pinname <Enter>		"ds insAnyEnter"
        # $c bind pinname <Leave>		"ds insAnyLeave"
        # $c bind pinname <Double-Button-1>	"ds toggleAbbrName"
        # $c bind pinname <ButtonPress-3>	"ds popup_on_cell %X %Y" 
        # $c bind pinname <ButtonRelease-3>	"ds popdown_on_cell" 

        # $c bind bundlepin <ButtonPress-3>	    "ds popup_on_bundlepin %X %Y" 
        # $c bind bundlepin <ButtonRelease-3>	    "ds popdown_on_bundlepin" 
        # $c bind bundlepin <Enter>		    "ds portAnyEnter"
        # $c bind bundlepin <Leave>		    "ds portAnyLeave"
        # $c bind bundlepin <Double-Button-1>	    "ds toggleAbbrName"

        # $c bind libname <1>		      "ds startDrag %x %y"
        # $c bind libname <B1-Motion>       "ds itemDrag %x %y"
        # $c bind libname <Enter>	      "ds insAnyEnter"
        # $c bind libname <Leave>	      "ds insAnyLeave"
        # $c bind libname <Double-Button-1> "ds toggleAbbrName"

        # $c bind idname <1>			"ds startDrag %x %y"
        # $c bind idname <B1-Motion>		"ds itemDrag %x %y"
        # $c bind idname <Enter>		"ds insAnyEnter"
        # $c bind idname <Leave>		"ds insAnyLeave"
        # $c bind idname <Double-Button-1>	"ds toggleAbbrName"

        # $c bind line   <Any-Enter>	     "ds netEnter"
        # $c bind line   <Any-Leave>	     "ds netLeave"
        # $c bind line   <1>		     "ds lineHighLight"
        # $c bind line   <ButtonPress-1>   "ds setMoveMaker %x %y"
        # $c bind line   <B1-Motion>       "ds moveLine %x %y"
        # $c bind line   <ButtonRelease-1> "ds endMoveLine %x %y"
        # $c bind line   <ButtonPress-3>   "ds popup_on_line %X %Y"

        # bind $c <1>			      "Comment_Add $c %x %y $w"
        # $c bind comment <1>		      "Comment_Button1 $c %x %y"
        # $c bind comment <B1-Motion>	      "ds itemDrag %x %y"

        # bind $c <Control-ButtonPress-1>   "ds startMarkBox %x %y"
        # bind $c <Control-B1-Motion>       "ds dragMarkBox %x %y"
        # bind $c <B1-Motion>               "ds clearMarkBox"
        # bind $c <Control-ButtonRelease-1> "ds endMarkBox %x %y"
        # bind $c <ButtonRelease-1>         "ds clearMarkBox"

        
        scroll_col = Scrollbar(framemid)
        scroll_col["relief"] = "sunken"
        scroll_col["command"] =  "canvas yview"

        scroll_row = Scrollbar(framemid)
        scroll_row["orient"] = "horiz"
        scroll_row["relief"] =  "sunken"
        scroll_row["command"] =  "canvas xview"

        scroll_col.pack(side="right", fill="y")
        scroll_row.pack(side="bottom", fill="x")
        self.canvas.pack(expand="yes", fill="both")

        #
        # Create name entry under canvas
        #
        self.name = StringVar()
        self.name.set("u_counter.u_ff0")
        
        fr = Frame(root)
        #fr.pack(anchor="w", fill="x")
        fr.pack()

        # label = Label(fr)
        # label["text"] = "Cmd"
        # label["relief"] = "groove"
        # label["bd"] = "2"

        entry = Entry(fr)
        entry["relief"] = "sunken"
        entry["width"] = "50"
        entry["bd"] = "2"
        entry["textvariable"] = self.name
        entry["exportselection"] = "yes"
        entry.bind("<Return>", self.return_nameentry)
        #label.pack(padx="1m", pady="1m", fill="x", side="left")
        entry.pack(padx="1m", pady="1m", fill="x", side="left", expand=1)

    def return_nameentry(self, event):
        self.display_instance(self.name.get())

    def display_instance(self, full_instance_name):
        inst = settings.current_design.find_instance(full_instance_name)

        if inst == None:
            return

        id = self.canvas.find_withtag(full_instance_name)
        if len(id) != 0:
            self.forcus(id)
            return
            
        # Display instance box
        width        = settings.box_width
        input_count  = inst.input_count()
        output_count = inst.output_count()

        if input_count == 0 and output_count == 0:
            print "No such module: ", inst.module_name
            return

        if input_count > output_count:
            height = settings.pin_y_pitch * (input_count+1)
        else:
            height = settings.pin_y_pitch * (output_count+1)

        x = settings.first_inst_x
        y = settings.first_inst_y
        x, y = self.find_open_space_to_display(x, y, height+settings.pin_y_pitch, width+2*settings.pin_x_length)

        inst_box_id = inst.display_box(self.canvas, x, y, height, width, full_instance_name)
        inst.display_instance_name(self.canvas, x, y)
        inst.display_module_name(self.canvas, x, y)
        inst.display_pins(self.canvas, x, y, width, inst_box_id ) # drawAllpin 

    def find_open_space_to_display(self, sx, sy, height, width):
        # canvas.find overlapping x y x1 y1
        while 1:
            n=0

            for i in self.canvas.find_overlapping(sx, sy, sx+width, sy+height):
                n += 1

            if n==0:
                break
            else:
                sy += height

        return sx, sy
    
    def get_instance_tag(self):
        inst_id = self.canvas.find_withtag("current")
        tags = self.canvas.gettags(inst_id)
        instance_id = filter(lambda x: settings.instance_tag_prefix in x, tags)
        return instance_id[0]

    def start_move_instance(self, event):
        id = self.get_instance_tag()
        settings.move_x = self.canvas.canvasx(event.x)
        settings.move_y = self.canvas.canvasy(event.y)
        settings.start_x = settings.move_x
        settings.start_y = settings.move_y

    def move_instance(self, event):
        if settings.start_x == -1:
            return

        x  = self.canvas.canvasx(event.x)
        y  = self.canvas.canvasy(event.y)
        cx = x - settings.move_x
        cy = y - settings.move_y
        id = self.get_instance_tag()
        self.canvas.move( id, cx, cy)
        settings.move_x = x
        settings.move_y = y

    def moving_instance(self, event):
        self.move_instance(event)

    def end_move_instance(self, event):
        self.move_instance(event)
        settings.start_x = -1

    def add_instance_input(self, event):
        settings.adding_instance == 1
        id = self.canvas.find_withtag("current")
        tags = self.canvas.gettags(id)
        print "add_instance_input:", tags

    def add_instance_output(self, event):
        id = self.canvas.find_withtag("current")
        tags = self.canvas.gettags(id)
        full_instance_name = self.canvas.gettags(tags[2])[2]
        full_parent_instance_name = full_instance_name[:full_instance_name.rfind(".")+1]
        instance_tag = filter(lambda x: settings.instance_tag_prefix in x, tags)[0]
        pin_tag = filter(lambda x: settings.pin_tag_prefix in x, tags)[0]
        instance = settings.my_design.get_instance_by_tag(instance_tag)
        fanout = instance.get_connections(pin_tag)

        for i in range(0,len(fanout)/2):
            #print i, fanout[i+1], fanout[i+2]
            instance = fanout[i+1]
            pin_name = fanout[i+2]
            #print "display_instance=",full_parent_instance_name+instance.name
            pin2_tag = self.display_instance(full_parent_instance_name+instance.name)
            self.add_nets(pin_tag, pin2_tag)

    def forcus(self,id):
        color = self.canvas.itemconfig(id, "fill")[4]
        self.canvas.itemconfig(id, fill=settings.forcus_color)
        #print self.canvas.find_tags(id)
        #time.sleep(10)
        self.canvas.itemconfig(id, fill=color)

    def add_nets(self, pin1_tag, pin2_tag):
        print "add_nets"
