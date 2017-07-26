import re, sys
from Instance import *
from settings import *

class Module:
    def __init__(self, line):
        self.name = line.split(" ")[1]
        self.module_line = line.split(" ")[1:]
        self.instances = {}
        self.inputs = []
        self.outputs = []

    def get_pins_of_line(self,line,str):
        index = line.find(str)
        return line[index+len(str):].replace(" ","").replace(";","").split(",")

    def add_input(self,line):
        self.inputs.extend( self.get_pins_of_line(line, "input") )

    def add_output(self,line):
        self.outputs.extend( self.get_pins_of_line(line, "output") )

    def add_inout(self,line):
        self.inouts.append( self.get_pins_of_line(line, "inout") )

    def add_instance(self,line):
        remove_space = line.strip(" ")
        module_end_index = remove_space.find(" ")
        my_module_name = remove_space[:module_end_index]
        remaining_line = remove_space[module_end_index:].replace(" ","")
        inst_end_index = remaining_line.find("(",module_end_index+1)
        inst_name = remaining_line[:inst_end_index]
        #print "add_instance: inst=", inst_name, "module=",my_module_name , ",parent module=",self.name
        self.instances[inst_name] = Instance( self, inst_name, my_module_name, remaining_line[inst_end_index+1:].replace(";","").replace(" ","").replace("\t","")[:-1])
        
        # at this moment, an instance is not flattened
        #module_by_instance_name[inst_name] = self

    def input_count(self):
        return len(self.inputs)

    def output_count(self):
        return len(self.outputs)

    def report_name(self):
        print "name=", self.name

    def report_inputs(self):
        for i in self.inputs:
            print i

    def report_outputs(self):
        for i in self.outputs:
            print i

    def report_inouts(self):
        n=0
        for i in self.inouts:
            print n, i
            n += 1

    def report_instances(self):
        n=0
        print "#instances =", len(self.instances)
        for i in self.instances:
            print n, i.report()
            n += 1

    def find_instance(self, instance_name, this_module=""):
        inst = None
        inst_index = instance_name.find(".")
        if inst_index >=0:
            this_instance_name = instance_name[:inst_index]
        else:
            this_instance_name = instance_name

        if this_module=="":
            this_module = settings.current_design

        if this_module.instances.has_key(this_instance_name):
            #print " ", this_instance_name, "found in ", this_module.name
            inst = this_module.instances[ this_instance_name ]

            if inst_index >= 0:
                next_instance_name = instance_name[inst_index+1:]
                #print "next_instance_name = ", next_instance_name , " in ", inst.module_name

                next_module = settings.my_design.find_module_by_name( inst.module_name )
                if next_module != "":
                    #print "call find_instance(). inst=", next_instance_name, ",module=", inst.module_name
                    inst = next_module.find_instance( next_instance_name, next_module )
                #else:
                    #print "No such module: ", inst.module_name
        else:
            print instance_name, "not found"
            
        return inst

    def is_input(self, pinname):
        ans = False
        for i in self.inputs:
            if i == pinname:
                ans = True
                break

        return ans
        
    def is_output(self, pinname):
        ans = False
        for i in self.outputs:
            if i == pinname:
                ans = True
                break

        return ans
        
