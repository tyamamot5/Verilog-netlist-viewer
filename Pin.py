# $Id: Pin.py,v 1.1 2017/08/27 00:40:41 tyamamot Exp $

from Module import *

# Extpin is the special call only for inputs and outputs of class Pin
#class Extpin:
#    def get_name(self):
#        return ""


class Pin:
    def __init__(self, name, module, inout):
        self.name   = name
        self.module = module
        self.inout  = inout
        self.width  = settings.box_width / 2
        self.height = settings.pin_y_pitch * 1.5
        self.external_pin = False
        self.tag    = None

        #if self.inout == "input":
        #    self.inputs = Extpin()
        #    print "Pin.__init__(): module=", name, module.name

        #if self.inout == "output":
        #    self.outputs = Extpin()

    def set_is_external_pin(self):
        self.external_pin = True

    def get_name(self):
        return self.name

    def get_inout_type(self):
        return self.inout

    def get_module(self):
        return self.module

    def is_external_pin(self):
        return self.external_pin

    def is_external_input(self):
        return self.inout == settings.tag_input

    def is_external_output(self):
        return self.inout == settings.tag_output

    def is_input(self):
        return self.inout == settings.tag_input

    def is_output(self):
        return self.inout == settings.tag_output

    #
    # methodes for instance drawing
    #
    def get_height(self):
        return self.height

    def get_tag(self):
        if self.tag == None:
            self.tag = settings.my_design.add_instance_tag(self)
            settings.instance_tag_count += 1

        return self.tag

    #def set_module(self):
    #    self.module = Module()

    #    retrun self.module
