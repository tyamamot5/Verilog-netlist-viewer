import re, sys
from Module   import *
from settings import *

class Instance:
    # the type is "class module", arg is "instance name"
    #module_by_instance_name = {}

    def __init__(self, parent_module, instance_name, module_name, pin_list):
        self.parent_module = parent_module
        self.module_name   = module_name
        # This instance name is not hierarchy instance name
        self.name          = instance_name
        self.height        = 0
        self.width         = settings.box_width

        # list of ".P0(NET0),.P1(NET1),..."
        self.pin_list              = pin_list
        self.in_module_connections = {}  # arg=net_name
        #self.flat_connections      = None
        self.module                = None
        self.tag                   = None
        #self.module_by_instance_name[instance_name] = self.module

    def is_external_pin(self):
        return False

    def is_external_input(self):
        return False

    def is_external_output(self):
        return False

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

       # print "get_connections(): net_name=", net_name

        if net_name != None:
            if net_name == "":
                print "get_connections(): No connection: pin=", pin_name
            elif self.in_module_connections.has_key(net_name):
                #connections = self.in_module_connections[net_name]
                #print connections
                pass
            else:
                #connections.append(net_name)
                #print "parent=", self.parent_module.name
                for i in self.parent_module.instances:
                    #print i, self.parent_module.instances[i].pin_list

                    if self.name == i:
                        continue
                        
                    for j in self.parent_module.instances[i].pin_list.split(","):
                        # machobj = ".PIN" "netname"
                        matchobj = r.match(j)
                        #print "get_connection(): matchobj=", matchobj.group(1), matchobj.group(2)
                        if matchobj.group(2) == net_name:
                            #connections.append(self.parent_module.instances[i])
                            connections.append( [self.parent_module.instances[i], self.parent_module.instances[i].get_pin_by_name(matchobj.group(1)[1:])] )


                if self.parent_module.inputs.has_key(net_name):
                    pin = self.parent_module.inputs[net_name] 
                    #connections.append(pin)
                    connections.append( [pin, pin] )
                          
                if self.parent_module.outputs.has_key(net_name):
                    pin = self.parent_module.outputs[net_name]
                    #connections.append(pin)
                    connections.append( [pin, pin])

                #print connections
                self.in_module_connections[net_name] = connections

        print "get_connections(): connections=", connections

        return connections

    def set_module(self):
        self.module = settings.my_design.find_module_by_name( self.module_name )        

        if self.module == None:
            print "set_module(): module not find. module=", module

        return self.module

    def input_count(self):
        module = self.set_module()
        if module == None:
            count = 0
        else:
            count = module.input_count()

        return count

    def output_count(self):
        module = self.set_module()
        if module == None:
            count = 0
        else:
            count = module.output_count()

        return count

    def get_module(self):
        if self.module == None:
            self.module = settings.my_design.module_by_module_name[self.module_name]

        return self.module

    #def get_module(self):
    #    if self.module == None:
    #        self.module = settings.my_design.module_by_module_name[ self.module_name ]
    #
    #    return self.module

    #///////////////////////////
    #   methods for pins
    #///////////////////////////

    def get_input(self,ith):
        module = self.get_module()
        return module.get_input(ith)

    def get_output(self,ith):
        module = self.get_module()
        return module.get_output(ith)

    def get_pin_by_name(self,pin_name):
        self.set_module()
        print "get_pin_by_name(): module=", pin_name, self.module, self.module.inputs, self.module.outputs
        if self.module.inputs.has_key(pin_name):
            return self.module.inputs[pin_name]

        if self.module.outputs.has_key(pin_name):
            return self.module.outputs[pin_name]
            
        return None

    def get_pin_type(self, pinname):
        self.get_module()
        if self.module.is_input(pinname):
            pintype = "In"
        elif self.module.is_output(pinname):
            pintype = "Out"
        else: # Unknown
            pintype = "In"

        return pintype

    def get_height(self):
        if self.height == 0:
            input_count  = self.input_count()
            output_count = self.output_count()

            if input_count > output_count:
                self.height = settings.pin_y_pitch * (input_count+1)
            else:
                self.height = settings.pin_y_pitch * (output_count+1)

        return self.height

