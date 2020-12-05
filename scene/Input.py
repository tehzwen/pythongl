

class Input():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.delta_x = 0
        self.delta_y = 0
        self.handle_right_click_press = lambda: None
        self.handle_left_click_press = lambda: None
        self.handle_mouse_zoom_in = lambda: None
        self.handle_mouse_zoom_out = lambda: None
        self.mouse_right_down = False
        self.mouse_left_down = False

    def get_position(self):
        return (self.x, self.y)

    def set_x(self, x):
        self.delta_x = self.x - x
        self.x = x

    def set_y(self,y):
        self.delta_y = self.y - y
        self.y = y
