class settings(object):
    # variables for design
    current_design       = None
    my_design            = None

    instance_tag_count   = 0

    # variables to draw an instance
    first_inst_x         = 100
    first_inst_y         = 100
    box_width            = 38
    shadow_offset        = 2
    inst_name_y_offset   = -8
    module_name_y_offset = 8
    instance_tag_prefix  = "Ins"
    forcus_color         = "orange"

    # variables to draw an instance
    pin_x_length         = 8
    pin_y_pitch          = 21
    pin_y_width          = 3
    pin_y_offset         = pin_y_pitch/2
    pin_tag_prefix       = "."

    open_space_grid      = box_width + pin_x_length*2 + box_width

    # variables for instance movemnet
    tag_instance_box         = "instbox"
    start_move_x             = -1
    move_x                   = 0
    move_y                   = 0    
    tag_input                = "input"
    tag_output               = "output"
    tag_pin_input            = tag_input
    tag_pin_output           = tag_output
    adding_instance          = 0
    #pin_name_input_x_offset = 5

    # for lines
    line_color     = "gray"
    line_width     = 1
    line_x_channel = 4
    net_tag_prefix = "net"
     
    def set_current_design(self, module):
        self.current_design = module
        
    def get_current_design(self):
        return self.current_design

    def set_my_design(self, design):
        self.my_design = design

        

