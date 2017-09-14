# $Id$

from Module import *
from Pin    import *

class Hpin:
    def __init__(self, pin):
        # Class Pin
        self.pin    = pin

        # An id of the pin rectangle on canvas
        self.id     = None

        # List of net ids connected with the pin on canvas
        self.nets   = []

    def get_id(self):
        return self.id

    def add_id(self, pin_id):
        if self.id != None:
            print "Hpin.add_id(): id is overwrited. id=", self.id, pin_id
        self.id = pin_id

    def add_net_id(self, net_id):
        #print "add_net_id(): net_id=", net_id, self.nets
        if net_id in self.nets:
            pass
        else:
            self.nets.append(net_id)
            #print "add_net_id(): net_id=", net_id

    def remove_net_id(self, net_id):
        #print "remove_net_id(): net_id=", net_id, self.nets        
        self.nets.remove(net_id)
        #print "remove_net_id(): net_id=", net_id, self.nets        

    def get_name(self):
        return self.pin.name

    def is_external_pin(self):
        return self.pin.is_external_pin()
