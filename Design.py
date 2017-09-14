from Module import *

class Design:
    current_design_name = ""
    
    # list of "class Module", arg is "
    module_array = []

    # type is "class Module", arg is "module name" (str)
    module_by_module_name = {}

    # type is "class Instance", arg is "instance name" (str)
    instance_by_name = {}

    # type is "class Hinstance", arg is "hierarchy instance name" (str)
    hinstance_by_name = {}

    # type is "class Instance", arg is an instance tag as "I*"
    instance_by_tag = {}

    predefine_module_list = [ ["FF",     "input CK, D;", "output Q;"], \
                              ["BUF",    "input A;",     "output X;"], \
                              ["input",  "input ;",      "output ;"], \
                              ["output", "input ;",      "output ;"] \
    ]

    def __init__(self):
        self.add_library_modules( self.predefine_module_list )
        self.external_input_pin = Pin("","","input")
        self.external_output_pin = Pin("","","output")

    #------------------
    #    For Module
    #------------------
    
    def add_module(self, module):
        #if self.module_by_module_name.has_key(module_name):
        if self.module_by_module_name.has_key(module.name):
            print "Module", module.name, "alreday exists"
        else:
            self.module_array.append( module )
            self.module_by_module_name[ module.name ] = module
        
    def add_modules(self, new_module_list):
        for new_module in new_module_list:
            this_module = Module("module "+new_module[0])
            self.module_array.append( this_module )
            this_module.add_inputs( new_module[1] )
            this_module.add_outputs( new_module[2] )
            self.add_module( this_module )

    def add_library_modules(self, new_module_list):
        for new_module in new_module_list:
            this_module = Module("module "+new_module[0])
            self.module_array.append( this_module )
            this_module.add_library_inputs( new_module[1] )
            this_module.add_library_outputs( new_module[2] )
            self.add_module( this_module )
            
    def set_current_module(self, name ):
        self.current_design_name = name
        self.current_design = self.module_by_module_name[ name ]
        return self.current_design

    def find_module_by_name(self, module_name):
        #if settings.my_design.module_by_module_name.has_key(module_name):
        #    module = settings.my_design.module_by_module_name[ module_name ]
        #print "find_module_by_name: ", module_name
        if self.module_by_module_name.has_key(module_name):
            module = self.module_by_module_name[ module_name ]
        else:
            module = None

        return module

    def print_module_list(self):
        for i in self.module_by_module_name:
            print i

    #------------------
    #    For Instance
    #------------------

    def add_instance_tag(self, instance):
        tag = settings.instance_tag_prefix+str(settings.instance_tag_count)
        self.instance_by_tag[tag] = instance
        settings.instance_tag_count += 1

        return tag

    def get_instance_by_tag(self, tag):
        if self.instance_by_tag.has_key(tag):
            instance = self.instance_by_tag[tag]
        else:
            instance = None

        return instance

    def get_instance_by_tags(self, tags):
        instance_tag = filter(lambda x: settings.instance_tag_prefix in x, tags)[0]
        #print "instance_tag=", instance_tag
        #instance = settings.my_design.get_instance_by_tag(instance_tag)

        return self.instance_by_tag[ instance_tag ]

    
    #--------------------
    #    For Hinstance
    #--------------------

    def add_hinstance(self, hinstance):
        if self.hinstance_by_name.has_key(hinstance.name):
            print "Hinstance", hinstance.name, "alreday exists"
        else:
            self.hinstance_by_name[ hinstance.name ] = hinstance

    def get_hinstance_by_name(self, name):
        if self.hinstance_by_name.has_key(name):
            hinstance = self.hinstance_by_name[ name ]
        else:
            print "get_hinstance_by_name(): No such Hinstance", name
            hinstance = None

        return hinstance

    def get_parent_hinstance_name(self, name):
        return name[:name.rfind(".")+1]

    #--------------------
    #    nets
    #--------------------

    def get_net_tag_id(self, id):
        return settings.net_tag_prefix+str(id)

    #--------------------
    #    To read netlist
    #--------------------

    def read_verilog(self, file):
        fp = open(file,"r")

        line_buffer = ""

        for line in fp:
            line = line[:-1]
        
            if re.search( r'^//', line):
                skip
            else:
                noncomment = re.search( r'^(.*)//', line)

                if noncomment:
                    line_buffer += noncomment.match(1)
                else:
                    line_buffer += line

            if re.search(r';', line):
                if re.search(r'^[\ \t]*module[ ]', line_buffer):
                    #print "add module", line_buffer
                    name = line_buffer.split(" ")[1]
                    this_module = Module(line_buffer)
                    self.add_module( this_module )
    	        elif re.search(r'^[\ \t]*input[ ]', line_buffer):
                    this_module.add_inputs(line_buffer)
	        elif re.search( r'^[\ \t]*output[ ]', line_buffer):
                    this_module.add_outputs(line_buffer)
	        elif re.search( r'^[\ \t]*wire[ ]', line_buffer):
	            print "wire"
         	else:
                    this_module.add_instance(line_buffer)

	        line_buffer = ""
            elif re.search( r'^[\ \t]*endmodule',  line_buffer):
	        #self.add_module( this_module )
	        line_buffer = ""
                pass

        fp.close()


