import global_var
class screen_settings():
    def __init__(self):
        super(screen_settings,self).__init__()
        self.screen_width=global_var.get_value('screen_width')
        self.screen_height=global_var.get_value('screen_height')
        self.stage_left=global_var.get_value('stage_left')
        self.stage_width=global_var.get_value('stage_width')
        self.stage_height=global_var.get_value('stage_height')
        self.stage_vSlit=global_var.get_value('stage_vSlit')
        self.amplified_times=global_var.get_value('amplified_times')