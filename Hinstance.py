# $Id$

from Module   import *
from Hpin     import *
from Instance import *
from settings import *


class Hinstance:
    def __init__(self, instance, name, mycanvas):
        self.instance = instance

        # Hierarhcy name
        self.name     = name

        self.mycanvas        = mycanvas
        self.name_id         = None
        self.module_name_id  = None
        self.box_id          = None
        self.inputs          = []
        self.outputs         = []

        mycanvas.design.add_hinstance(self)
        
        if self.instance.is_external_pin() == False:
            for i in self.instance.module.inputs:
                #self.inputs.append( Hpin(i) )
                self.inputs.append( Hpin(self.instance.module.inputs[i]) )

            for i in self.instance.module.outputs:
                #self.outputs.append( Hpin(i) )
                self.outputs.append( Hpin(self.instance.module.outputs[i]) )
        elif self.instance.is_external_output() == True:
                self.inputs.append( Hpin(self.mycanvas.design.external_input_pin) )
        elif self.instance.is_external_input() == True:
                self.outputs.append( Hpin(self.mycanvas.design.external_output_pin) )
                
    def add_box_id(self, box_id):
        if self.box_id != None:
            print "add_box_id(): box_id is overwrited. id=",self.box_id, box_id
        self.box_id   = box_id

    def add_name_id(self, name_id):
        self.name_id = name_id

    def get_xy(self):
        coords = self.mycanvas.canvas.coords(self.box_id)
        return [coords[0], coords[1]]

    def get_module_name(self):
        #print "get_module_name=", self.instance.get_module()
        #return self.instance.module.name
        return self.instance.get_module().name

    def get_name(self):
        return self.name

    def get_width(self):
        return self.instance.width

    def get_height(self):
        return self.instance.height

    def get_output_pin_name(self, ith):
        return self.instance.module.outputs[ith].name

    def get_input_pin_name(self, ith):
        return self.instance.module.inputs[ith].name

    def get_tag(self):
        return self.instance.get_tag()

    def get_instance_box_id(self):
        return self.box_id

    def output_count(self):
        return self.instance.output_count()

    def input_count(self):
        return self.instance.input_count()    

    def add_pin_ids(self, pin_ids):
        self.pin_ids = pin_ids

    #def add_pin_id_in_output(self, ith, id):
    #    return self.outputs[ith].add_id(id)

    #def add_pin_id_in_input(self, ith, id):
    #    return self.inputs[ith].add_id(id)

