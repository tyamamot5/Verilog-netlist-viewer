import re, sys
from Module import *
from settings import *

class Instance:
    # the type is "class module", arg is "instance name"
    #module_by_instance_name = {}

    def __init__(self, parent_module, instance_name, module_name, pin_list):
        self.parent_module = parent_module
        self.module_name   = module_name
        self.name = instance_name

        # list of ".P0(NET0),.P1(NET1),..."
        self.pin_list = pin_list
        self.in_module_connections = {}  # arg=net_name
        self.flat_connections = None
        self.module = None
        self.tag = None
        #self.module_by_instance_name[instance_name] = self.module

    def report(self):
        print "module=", self.module.name, " inst=", self.name, " pin_list=", self.pin_list

    def get_tag(self):
        if self.tag == None:
            self.tag = settings.my_design.add_instance_tag(self)
            settings.instance_tag_count += 1

        return self.tag

    def get_connections(self, pin_name):
        net_name = None
        connections = []

        r = re.compile(r'(\.\w+)\((\w+)\)')

        for i in self.pin_list.split(","):
            matchobj = r.match(i)
            if matchobj:
                #print "pin=", matchobj.group(1), matchobj.group(2), " type=", self.get_pin_type(matchobj.group(1))
                if matchobj.group(1) == pin_name:
                    net_name = matchobj.group(2)
                    #print "next pin=", matchobj.group(1), "net_name=", net_name
                    break

        if net_name != None:
            if net_name == "":
                print "No connection: pin=", pin_name
            elif self.in_module_connections.has_key(net_name):
                connections = self.in_module_connections[net_name]
                #print connections
            else:
                connections.append(net_name)
                #print "parent=", self.parent_module.name
                for i in self.parent_module.instances:
                    #print i, self.parent_module.instances[i].pin_list

                    if self.name == i:
                        continue
                        
                    for j in self.parent_module.instances[i].pin_list.split(","):
                        matchobj = r.match(j)
                        #print matchobj.group(1), matchobj.group(2)
                        if matchobj.group(2) == net_name:
                            #connections.append(i)  -- Instance name
                            connections.append(self.parent_module.instances[i])
                            connections.append(matchobj.group(1))

                #print connections
                self.in_module_connections[net_name] = connections

        return connections

    def input_count(self):
        module = settings.my_design.find_module_by_name( self.module_name )
        if module == "":
            count = 0
        else:
            count = module.input_count()

        return count

    def output_count(self):
        module = settings.my_design.find_module_by_name( self.module_name )
        if module == "":
            count = 0
        else:
            count = module.output_count()

        return count

    def get_module(self):
        return settings.my_design.module_by_module_name[self.module_name]

    def get_inputs(self):
        module = self.get_module()
        return module.inputs

    def get_outputs(self):
        module = self.get_module()
        return module.outputs

    def display_box(self, canvas, x, y, height, width, full_instance_name):
        offset = settings.shadow_offset
        shadow = canvas.create_rectangle(x+offset, y+offset, x+width+offset, y+height+offset, fill="gray", tags=settings.tag_instance_box)
        inst_box = canvas.create_rectangle(x, y, x+width, y+height, fill="gray", outline="gray", activefill="orange", tags=settings.tag_instance_box)
        canvas.addtag_withtag(self.get_tag(), inst_box)
        canvas.addtag_withtag(full_instance_name, inst_box)
        canvas.addtag_withtag(self.get_tag(), shadow)

        return inst_box

    def display_instance_name(self, canvas, x, y):
        id = canvas.create_text(x+settings.box_width/2, y+settings.inst_name_y_offset, text=self.name)
        canvas.addtag_withtag(self.get_tag(), id)
        

    def display_module_name(self, canvas, x, y):
        id = canvas.create_text(x+settings.box_width/2, y+settings.module_name_y_offset, text=self.module_name)
        canvas.addtag_withtag(self.get_tag(), id)


    #///////////////////////////
    #   methods for pins
    #///////////////////////////
        
    def display_pin(self, canvas, x0, x1, y, tag_in_or_out, tag_pin, inst_box_id):
        id = canvas.create_line(x0, y, x1, y, width=settings.pin_y_width, fill="gray", activefill="orange")
        if tag_in_or_out == settings.tag_pin_input:
            pin_name_anchor="w"
        else:
            pin_name_anchor="e"
        canvas.addtag_withtag(tag_in_or_out, id)
        canvas.addtag_withtag(self.get_tag(), id)
        canvas.addtag_withtag(inst_box_id, id)
        canvas.addtag_withtag(settings.pin_tag_prefix+str(tag_pin), id)
            
        id = canvas.create_text(x0, y, text=tag_pin, anchor=pin_name_anchor)
        canvas.addtag_withtag(self.get_tag(), id)
        #print "pin tag=", tag_in_or_out, self.get_tag(), tag_pin

    def display_pins(self, canvas, x, y, width, inst_box_id):
        x0 = x + width
        x1 = x0 + settings.pin_x_length
        y0 = y + settings.pin_y_pitch

        for i in range(0, self.output_count()):
            outputs = self.get_outputs()
            self.display_pin(canvas, x0, x1, y0, settings.tag_output, outputs[i], inst_box_id)
            y0 += settings.pin_y_pitch

        x0 = x
        x1 = x0 - settings.pin_x_length
        y0 = y + settings.pin_y_pitch

        for i in range(0, self.input_count()):
            #print i, "in", x0, x1, y0
            inputs = self.get_inputs()
            self.display_pin(canvas, x0, x1, y0, settings.tag_input, inputs[i], inst_box_id)
            y0 += settings.pin_y_pitch

    #def get_fanout(self, pin):
        #print "get_fanout:", self.pin_list, "pin=", pin
        #self.get_connections(pin)

    def get_module(self):
        if self.module == None:
            self.module = settings.my_design.module_by_module_name[ self.module_name ]

        return self.module

    def get_pin_type(self, pinname):
        self.get_module()
        if self.module.is_input(pinname):
            pintype = "In"
        elif self.module.is_output(pinname):
            pintype = "Out"
        else: # Unknown
            pintype = "In"

        return pintype
