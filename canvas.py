#
# $Id: canvas.py,v 1.2 2017/08/11 06:06:48 tyamamot Exp $
#

import re, sys, time

from Tkinter   import *
from Module    import *
from Hinstance import *
from settings  import *

class MyCanvas:
    def __init__(self, root):
        self.root = root
        framemid = Frame(root, relief="flat")
        #framemid["relief"] = "flat"
        framemid.pack(fill="both", expand="yes")

        self.canvas = Canvas(framemid, scrollregion="-2500 0 2500 2500", width=500, height=400, borderwidth=2, confine="false")
        canvas = self.canvas
        #self.canvas["scrollregion"] = "-2500 0 2500 2500"
        #self.canvas["width"] = "500"
        #self.canvas["height"] = "400"
        #self.canvas["borderwidth"] = "2"
        #self.canvas["confine"] = "false"

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

        
        #scroll_col = Scrollbar(framemid)
        #scroll_col["relief"] = "sunken"
        #scroll_col["command"] =  "canvas yview"
        scroll_col = Scrollbar(framemid, relief="sunken", command=self.canvas.yview)

        #scroll_row            = Scrollbar(framemid)
        #scroll_row["orient"]  = "horiz"
        #scroll_row["relief"]  =  "sunken"
        #scroll_row["command"] =  "canvas xview"
        scroll_row            = Scrollbar(framemid, orient="horiz", relief="sunken", command=self.canvas.xview)

        #self.canvas["xscrollcommand"] = scroll_row.set
        #self.canvas["yscrollcommand"] = scroll_col.set # -relief sunken
        self.canvas.config(xscrollcommand=scroll_row.set)
        self.canvas.config(yscrollcommand=scroll_col.set) # -relief sunken

        scroll_col.pack(side="right", fill="y")
        scroll_row.pack(side="bottom", fill="x")
        self.canvas.pack(expand="yes", fill="both")

        #
        # Create name entry under canvas
        #
        self.name = StringVar()
        self.name.set("u_counter.u_ff3")
        
        fr = Frame(root)
        fr.pack(anchor="w", fill="x")
        fr.pack()

        # label = Label(fr)
        # label["text"] = "Cmd"
        # label["relief"] = "groove"
        # label["bd"] = "2"

        entry = Entry(fr, relief="sunken", width=50, bd=2, textvariable=self.name, exportselection="yes")
        #entry["relief"] = "sunken"
        #entry["width"] = "50"
        #entry["bd"] = "2"
        #entry["textvariable"] = self.name
        #entry["exportselection"] = "yes"
        entry.bind("<Return>", self.return_nameentry)
        #label.pack(padx="1m", pady="1m", fill="x", side="left")
        entry.pack(padx="1m", pady="1m", fill="x", side="left", expand=1)

        self.id_dir  = {}
        #self.id_type = []

    def set_design( self, design ):
        self.design = design

    def return_nameentry(self, event):
        #self.add_instance(self.name.get())
        full_instance_name = self.name.get()
        inst = settings.current_design.find_instance(full_instance_name)
        #inst = self.design.find_instance(full_instance_name)

        if inst == None:
            print "No such instance: ", full_instance_name
            return

        hinstance = self.design.get_hinstance_by_name(full_instance_name)
        if hinstance:
            #print "nameentry(): forcus", full_instance_name
            self.forcus(hinstance.box_id)
        else:
            #print "nameentry(): add_instance", full_instance_name
            self.add_instance(full_instance_name)
            
        return


    #///////////////////////////
    #   methods for instances
    #///////////////////////////
    def is_instance(self, full_instance_name):
        id = self.canvas.find_withtag(full_instance_name)
        return len(id) != 0

    def add_instance(self, full_instance_name, *xy):
        #inst = settings.current_design.find_instance(full_instance_name)
        inst = self.design.current_design.find_instance(full_instance_name)

        if inst == None:
            return

        print "add_instance(): inst=", inst, full_instance_name

        inst.get_height()

        x, y = self.find_open_space(inst, xy)

        hinstance   = Hinstance( inst, full_instance_name, self)
        inst_box_id = self.add_instance_box(hinstance, x, y)
        hinstance.add_box_id(inst_box_id)
        self.add_instance_name(hinstance)
        self.add_module_name(hinstance)
        self.add_pins(hinstance)

        self.add_object_by_id(inst_box_id, hinstance)

        #return inst_box_id
        return hinstance 

    def add_instance_box(self, hinstance, x, y):
        offset = settings.shadow_offset
        width  = hinstance.instance.width
        height = hinstance.instance.height

        shadow = self.canvas.create_rectangle(x+offset, y+offset, x+width+offset, y+height+offset, fill="gray", tags=settings.tag_instance_box)
        inst_box = self.canvas.create_rectangle(x, y, x+width, y+height, fill="gray", outline="gray", activefill="orange", tags=settings.tag_instance_box)
        hinstance.box_id = inst_box
        self.canvas.addtag_withtag(hinstance.instance.get_tag(), inst_box)
        self.canvas.addtag_withtag(hinstance.name              , inst_box)
        self.canvas.addtag_withtag(hinstance.instance.get_tag(), shadow)

        return inst_box

    def add_instance_name(self, hinstance):
        xy = hinstance.get_xy()
        id = self.canvas.create_text(xy[0]+settings.box_width/2, xy[1]+settings.inst_name_y_offset, text=hinstance.name)
        hinstance.name_id = id
        self.canvas.addtag_withtag(hinstance.instance.get_tag(), id)

    def add_module_name(self, hinstance):
        xy = hinstance.get_xy()
        id = self.canvas.create_text(xy[0]+settings.box_width/2, xy[1]+settings.module_name_y_offset, text=hinstance.get_module_name())
        hinstance.module_name_id = id
        self.canvas.addtag_withtag(hinstance.instance.get_tag(), id)

    def find_open_space(self, instance, xy):
        if len(xy) == 0:
            x = settings.first_inst_x
            y = settings.first_inst_y
        else:
            x = xy[0][0]
            y = xy[0][1]

        height = instance.get_height() + settings.pin_y_pitch
        width  = instance.width        + 2*settings.pin_x_length

        if len(xy) == 2:
            if xy[1] == "input":
                x -= settings.open_space_grid

            else:
                x += settings.open_space_grid

        while 1:
            n=0

            for i in self.canvas.find_overlapping(x, y, x+width, y+height):
                n += 1

            if n==0:
                break
            else:
                y += height

        return x, y
    
    def get_id_of_current(self):
        #print "get_id_of_current():",self.canvas.find_withtag("current")
        return self.canvas.find_withtag("current")[0]

    def get_instance_tag(self):
        inst_id = self.get_id_of_current()
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
        id_tag = self.get_instance_tag()
        self.canvas.move( id_tag, cx, cy)
        settings.move_x = x
        settings.move_y = y
        self.move_nets()

    def moving_instance(self, event):
        self.move_instance(event)

    def end_move_instance(self, event):
        self.move_instance(event)
        settings.start_x = -1

    def add_instance_input(self, event):
        id = self.get_id_of_current()
        to_hpin = self.get_object_by_id(self.get_id_of_current())
        print "add_instance_input(): id=", id

        # The tags should contrains 
        # 1: "output" or "input"
        # 2: "Ins*" = instance index
        # 3: Instance canvas id
        # 4: Pin name
        # 5: current
        tags = self.canvas.gettags(id)

        print "add_instance_input(): tags=", tags
        full_instance_name        = self.get_hinstance_name_by_id(id)
        hinstance                 = self.design.get_hinstance_by_name( full_instance_name )
        full_parent_instance_name = self.design.get_parent_hinstance_name(full_instance_name)
        instance                  = self.design.get_instance_by_tags(tags)
        to_pin_name               = self.get_pin_name_by_tags(tags)
        fanin                     = instance.get_connections(to_pin_name)

        # fanin[0]   = net name
        # fanin[i+1] = class Instance
        # fanin[i+2] = class Pin

        print "add_instance_input(): #fanin=", len(fanin)

        for i in fanin:
            instance    = i[0]
            from_pin    = i[1]
            print "add_instance_input(): ",i, instance.name, from_pin.name, from_pin.get_inout_type() , from_pin.is_external_pin()
            from_hinstance_name = full_parent_instance_name+instance.name
            from_hinstance      = self.design.get_hinstance_by_name(from_hinstance_name)

            # if the instance is already added in canvas
            if from_hinstance:
                pass
#            elif from_pin.is_external_pin() == False or from_pin.is_external_input() == False:
#                continue

            from_hinstance   = self.add_instance(from_hinstance_name, hinstance.get_xy(), "input")
            print "add_instance_input(): from_instance_id=", from_hinstance.get_instance_box_id()
                
            print "add_instance_input(): from_hinstance.inputs=", from_hinstance.outputs
            for j in from_hinstance.outputs:
                print "add_instance_input(): from_pin.name=", from_pin.get_name(), "j.name=", j.get_name()

                if from_pin.get_name() == j.get_name() or j.is_external_pin() == False:
                    if self.is_connected( to_hpin, j) == False:
                        net_id = self.add_net(j, to_hpin, from_hinstance.instance.get_tag(), hinstance.instance.get_tag())


    def get_tags_by_id(self,id):
        return self.canvas.gettags(id)

    def get_hinstance_name_by_id(self,id):
        tags = self.get_tags_by_id(id)
        return self.canvas.gettags(tags[2])[2]

    def add_instance_output(self, event):
        id = self.get_id_of_current()
        from_hpin = self.get_object_by_id(self.get_id_of_current())
        print "add_instance_output(): id=", id

        # The tags should contrains 
        # 1: "output" or "input"
        # 2: "Ins*" = instance index
        # 3: Instance canvas id
        # 4: Pin name
        # 5: current
        tags = self.canvas.gettags(id)

        print "add_instance_output(): tags=", tags
        full_instance_name        = self.get_hinstance_name_by_id(id)
        hinstance                 = self.design.get_hinstance_by_name( full_instance_name )
        full_parent_instance_name = self.design.get_parent_hinstance_name(full_instance_name)
        instance                  = self.design.get_instance_by_tags(tags)
        from_pin_name             = self.get_pin_name_by_tags(tags)
        fanout                    = instance.get_connections(from_pin_name)

        # fanout[0]   = net name
        # fanout[i+1] = class Instance
        ## fanout[i+2] = pin name
        # fanout[i+2] = class Pin

        print "add_instance_output(): #fanout=", len(fanout)

        for i in fanout:
            #instance    = fanout[i+1]
            #to_pin      = fanout[i+2]
            instance    = i[0]
            to_pin      = i[1]
            print "add_instance_output(): ",i, instance.name, to_pin.name
            to_hinstance_name = full_parent_instance_name+instance.name
            to_hinstance      = self.design.get_hinstance_by_name(to_hinstance_name)

            # if the instance is already added in canvas
            if to_hinstance:
                #to_instance_id = to_hinstance.box_id
                pass
            else:
                #to_instance_id = self.add_instance(to_hinstance_name, hinstance.get_xy(), "output")
                to_hinstance   = self.add_instance(to_hinstance_name, hinstance.get_xy(), "output")
                #to_hinstance   = self.design.get_hinstance_by_name( to_hinstance_name )
                print "add_instance_output(): to_instance_id=",to_hinstance.get_instance_box_id()
                
            print "add_instance_output(): to_hinstance.inputs=", to_hinstance.inputs
            for j in to_hinstance.inputs:
                print "add_instance_output(): to_pin.name=", to_pin.get_name(), "j.name=", j.get_name()

                if to_pin.get_name() == j.get_name() or j.is_external_pin() == False:
                    if self.is_connected( from_hpin, j) == False:
                        net_id = self.add_net(from_hpin, j, hinstance.instance.get_tag(), to_hinstance.instance.get_tag())

    def forcus(self,id):
        color = self.canvas.itemconfig(id, "fill")[4]
        self.canvas.itemconfig(id, fill=settings.forcus_color)
        print "forcus(): forcus_color=", settings.forcus_color
        #time.sleep(10)
        self.root.after(5000, self.change_back_color(id, color))

    def change_back_color(self, id, color):
        print "change_back_color(): color=", color
        self.canvas.itemconfig(id, fill=color)


    #///////////////////////////
    #   methods for pins
    #///////////////////////////

    def get_pin_name_by_tags(self, tags):
        pin_name = filter(lambda x: settings.pin_tag_prefix in x, tags)[0]
        #print "get_pin_name_by_tags: pin_name=", pin_name

        return pin_name

    def add_pin(self, hinstance, pin, nth, tag_in_or_out):
        xy = hinstance.get_xy()
        y  = xy[1] + settings.pin_y_pitch + nth*settings.pin_y_pitch

        if tag_in_or_out != settings.tag_pin_input:
            x0 = xy[0] + hinstance.get_width()
            x1 = x0    + settings.pin_x_length
            #name = hinstance.get_output_pin_name(ith)
            name = pin.get_name()
            pin_name_anchor="e"
        else:
            x0 = xy[0]
            x1 = x0 - settings.pin_x_length
            #name = hinstance.get_input_pin_name(ith)
            name = pin.get_name()
            pin_name_anchor="w"

        id = self.canvas.create_line(x0, y, x1, y, width=settings.pin_y_width, fill="gray", activefill="orange")
        self.canvas.addtag_withtag(tag_in_or_out                     , id)
        self.canvas.addtag_withtag(hinstance.get_tag()               , id)
        self.canvas.addtag_withtag(hinstance.get_instance_box_id()   , id)
        self.canvas.addtag_withtag(settings.pin_tag_prefix+str(name) , id)
        print "add_pin(): id=",id,"tags=", self.get_tags_by_id(id)
            
        if tag_in_or_out == settings.tag_pin_input:
            y  += settings.pin_y_offset

        name_id = self.canvas.create_text(x0, y, text=name, anchor=pin_name_anchor)
        self.canvas.addtag_withtag(hinstance.get_tag(), name_id)

        print "add_pin(): pin=", pin, pin.get_name()
        pin.add_id(id)
        self.add_object_by_id(id, pin)

    def add_object_by_id(self, id, object):
        #print "add_object_by_id(): ", id, object
        self.id_dir[id] = object
        #print "add_object_by_id():", self.id_dir

    def get_object_by_id(self, id):
        if self.id_dir.has_key(int(id)):
            return self.id_dir[int(id)]

        #print "get_object_by_id(): no id=", int(id), self.id_dir[int(id)]
        #print "get_object_by_id(): id_dir=", self.id_dir
        return None

    def add_pins(self, hinstance):
        xy = hinstance.get_xy()
        #x, y, width, inst_box_id 

        #x0 = xy[0] + hinstance.get_width()
        #x1 = x0    + settings.pin_x_length
        #y0 = xy[1] + settings.pin_y_pitch

        #print "#output=",hinstance.output_count()

        #pin_ids = []

        #for i in range(0, hinstance.output_count()):
        nth = 0
        for i in hinstance.outputs:
            #pin_ids.append( self.add_pin(hinstance, i, settings.tag_output) )
            id = self.add_pin(hinstance, i, nth, settings.tag_output)
            #hinstance.add_pin_id_in_output(i, id)
            #i.add_id(id)
            #y0 += settings.pin_y_pitch
            nth += 1

        #x0 = xy[0]
        #x1 = x0 - settings.pin_x_length
        #y0 = xy[1] + settings.pin_y_pitch

        #print "#input=",hinstance.input_count()
        #for i in range(0, hinstance.input_count()):
        nth = 0
        for i in hinstance.inputs:
            #print i, "in", x0, x1, y0
            #pin_ids.append( self.add_pin(hinstance, i, settings.tag_input) )
            id = self.add_pin(hinstance, i, nth, settings.tag_input)
            #hinstance.add_pin_id_in_input(i, id)
            #i.add_id(id)
            #y0 += settings.pin_y_pitch
            nth += 1

        #hinstance.add_pin_ids(pin_ids)

        #return pin_ids

    #///////////////////////////
    #   methods for nets
    #///////////////////////////

    def find_channel(self, from_x, from_y, to_x, to_y):
        print "find_channel(): ", from_x, from_y, to_x, to_y
        from_x = int(from_x)
        from_y = int(from_y)
        to_x   = int(to_x)
        to_y   = int(to_y)
        for i in range(from_x, to_x, settings.line_x_channel):
            print "find_channel(): x=", i
            ids = self.canvas.find_overlapping(i, from_y, i+settings.line_x_channel, to_y)
            print "find_channle(): find_overlapping=", ids

            if len(ids) == 0:
                return i

        return from_x + settings.line_x_channel
        
    def is_connected(self, from_hpin, to_hpin):
        print "is_connected(), from_id=", from_hpin, from_hpin.get_name(), "to_id=", to_hpin, to_hpin.get_name()
        #print "is_connected(), from_id_tag=", self.canvas.gettags(from_id), "to_id_tag=", self.canvas.gettags(to_id)
        #from_pin_matching = [s for s in self.canvas.gettags(from_id) if settings.net_tag_prefix in s]
        #to_pin_matching   = [s for s in self.canvas.gettags(to_id)   if settings.net_tag_prefix in s]
        
        #for i in from_pin_matching:
        #    if any(i in s for s in to_pin_matching):
        #        return True
        print "is_connected(): from_hpin.nets=", from_hpin.nets
        print "is_connected(): to_hpin.nets=", to_hpin.nets

        for i in from_hpin.nets:
            if i in to_hpin.nets:
                print "is_connected(): True"
                return True

        print "is_connected(): False"
        return False

    def add_tag_to_id(self, tag, pin_id):
        tags = self.canvas.gettags(pin_id)
        print "add_tag_to_id(): id=",id,"tags=", tags
        if any(tag in s for s in tags) == False:
            print "add_tag_to_id(): add tag >", tag
            self.canvas.addtag_withtag(tag, pin_id)
        print "add_tag_to_id(): id=", pin_id, "tags=",self.canvas.gettags(id)

    def add_net(self, from_hpin, to_hpin, *tags):
        #print "add_net(): ", from_hpin.get_id(), to_hpin.get_id()
        #print "add_net(): from_pin xy=", self.canvas.coords(from_hpin.get_id())
        #print "add_net(): to_hpin xy =", self.canvas.coords(to_hpin.get_id())

        from_coords = self.canvas.coords(from_hpin.get_id())
        to_coords   = self.canvas.coords(to_hpin.get_id())

        if from_coords[0] > from_coords[2]: 
            from_x = from_coords[0]
        else:
            from_x = from_coords[2]
            
        from_y = from_coords[3]

        if to_coords[0] > to_coords[2]: 
            to_x = to_coords[2]
        else:
            to_x = to_coords[1]

        to_y = to_coords[1]

        x1 = self.find_channel(from_x, from_y, to_x, to_y)
        id = self.canvas.create_line(from_x, from_y, x1, from_y, x1, to_y, to_x, to_y, width=settings.line_width, fill=settings.line_color)

        net_tag_id = self.design.get_net_tag_id(id)
        self.canvas.addtag_withtag(from_hpin.get_id(),id)
        self.canvas.addtag_withtag(to_hpin.get_id()  ,id)
        from_hpin.add_net_id(id)
        to_hpin.add_net_id(id)

        return id
            
    def move_nets(self):
        #print "move_nets(): id=", self.get_id_of_current()
        hinstance = self.get_object_by_id(self.get_id_of_current())

        for i in hinstance.inputs:
            for j in i.nets:
                #print "move_nets(): id=", j, i.pin.name, self.canvas.coords(j), self.canvas.coords(i.id)
                to_pin_x  = self.canvas.coords(i.id)[2]
                to_pin_y  = self.canvas.coords(i.id)[3]
                xy        = self.canvas.coords(j)
                n         = len(xy)
                xy[6]     = to_pin_x
                xy[7]     = to_pin_y
                if xy[5] != xy[7]:
                    xy[5] = xy[7]
                net_tags = self.canvas.gettags(j)
                #print "move_nets(): net_tags=", net_tags
                from_hpin = self.get_object_by_id( net_tags[0] )
                #print "move_nets(): old net tags=", net_tags
                self.canvas.delete(j)
                net_id = self.canvas.create_line(xy[0], xy[1], xy[2], xy[3],xy[4], xy[5], xy[6], xy[7], width=settings.line_width, fill=settings.line_color)
                self.canvas.addtag_withtag( from_hpin.get_id(), net_id)
                self.canvas.addtag_withtag( i.get_id(), net_id)                
                i.remove_net_id(j)
                i.add_net_id(net_id)
                from_hpin.remove_net_id(j)
                from_hpin.add_net_id(net_id)
                #print "move_nets(): from_hpin.net_id=", from_hpin.nets
                #print "move_nets(): to_hpin.net_id=", i.nets

        for i in hinstance.outputs:
            for j in i.nets:
                #print "move_nets(): id=", j, i.pin.name, self.canvas.coords(j), self.canvas.coords(i.id)
                from_pin_x  = self.canvas.coords(i.id)[2]
                from_pin_y  = self.canvas.coords(i.id)[3]
                xy          = self.canvas.coords(j)
                n           = len(xy)
                xy[0]       = from_pin_x
                xy[1]       = from_pin_y
                if xy[1] != xy[3]:
                    xy[3] = xy[1]
                net_tags = self.canvas.gettags(j)
                #print "move_nets(): net_tags=", net_tags
                to_hpin = self.get_object_by_id( net_tags[1] )
                #print "move_nets(): old net tags=", net_tags
                self.canvas.delete(j)
                net_id = self.canvas.create_line(xy[0], xy[1], xy[2], xy[3],xy[4], xy[5], xy[6], xy[7], width=settings.line_width, fill=settings.line_color)
                self.canvas.addtag_withtag( i.get_id(), net_id)                
                self.canvas.addtag_withtag( to_hpin.get_id(), net_id)
                i.remove_net_id(j)
                i.add_net_id(net_id)
                to_hpin.remove_net_id(j)
                to_hpin.add_net_id(net_id)
                #print "move_nets(): from_hpin.net_id=", i.nets
                #print "move_nets(): to_hpin.net_id=", to_hpin.nets
                
