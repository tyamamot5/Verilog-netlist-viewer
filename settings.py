class settings(object):
    # variables for design
    current_design       = None
    my_design            = None

    instance_tag_count   = 0
    instance_tag_prefix  = "Ins"
    pin_tag_prefix       = "."

    # variables to draw an instance
    first_inst_x         = 100
    first_inst_y         = 100
    box_width            = 38
    shadow_offset        = 2
    pin_x_length         = 8
    pin_y_pitch          = 21
    pin_y_width          = 3
    inst_name_y_offset   = -8
    module_name_y_offset = 8
    forcus_color         = "orange"


    # variables for instance movemnet
    tag_instance_box         = "instbox"
    start_move_x             = -1
    move_x                   = 0
    move_y                   = 0    
    tag_input                = "input"
    tag_output               = "output"
    tag_pin_input            = tag_input
    adding_instance          = 0
    #pin_name_input_x_offset = 5

    def set_current_design(self, module):
        self.current_design = module
        
    def get_current_design(self):
        return self.current_design

    def set_my_design(self, design):
        self.my_design = design

        

