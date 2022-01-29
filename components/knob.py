import dearpygui.dearpygui as dpg 
import math

cos = lambda deg : math.cos( math.radians( deg ) )
sin = lambda deg : math.sin( math.radians( deg ) )
tan = lambda deg : math.tan( math.radians( deg ) )

class Knob:
    colors = {
        'r' : [ 200,   0,   0,   200],
        'g' : [   0, 200,   0,   200],
        'b' : [   0,   0, 200,   200],
        'R' : [ 255,   0,   0,   255],
        'G' : [   0, 255,   0,   255],
        'B' : [   0,   0, 255,   255]
    }
    markers = {
        'o' : 10,
        '-' : 0,
        '^' : 3,
        '+' : 4,
        '#' : 5,
    }

    def __init__(self, 
                parent: dpg.window,
                degrees: float, 
                pos: list = [0,0],
                window_title: str = 'None',
                offset_x: int = 0, 
                offset_y: int = 0,
                thickness_circle : int = 1,
                thickness_arrow : int = 1,
                color_circle : str = 'b',
                color_arrow : str = 'B',
                size_arrow : int = 1,
                theme_default : bool = True
                ) -> None:

        self.parent = parent
        if window_title != 'None':
            dpg.configure_item( self.parent, label = window_title, no_move=True, no_close=True, no_resize=True )    
        else: 
            dpg.configure_item( self.parent, no_title_bar= True, no_move=True, no_close=True, no_resize=True )    
        
        self.offset_x, self.offset_y = offset_x, offset_y
        self.pos = pos

        self.width = dpg.get_item_width(self.parent)  
        self.height = dpg.get_item_height(self.parent)

        if self.height < self.width:
            self.radius = self.height/2 - 10
            self.center = [ (self.width-2*self.offset_x-self.pos[0]) + self.pos[0]+self.offset_x, 
                            (self.height-2*self.offset_y-self.pos[1]) + self.pos[1]+self.height-self.offset_y] 
        else: 
            self.radius = ((self.width-self.pos[0]-2*self.offset_x)/2) 
            self.center = [ self.width/2, self.pos[1]+self.offset_y+self.radius] 
            
        self.degree = degrees 

        self.theme_default = theme_default

        self.color_circle = self.colors[color_circle] if color_circle in self.colors.keys() else 'b'
        self.color_arrow = self.colors[color_arrow] if color_arrow in self.colors.keys() else 'B'
        self.thickness_circle = thickness_circle
        self.thickness_arrow = thickness_arrow
        self.size_arrow = size_arrow

        print( self.height, self.center, self.radius)

        self.point_arrow_pos = [ self.center[0] + self.radius*cos(self.degree),
                                 self.center[1] - self.radius*sin(self.degree) ]

        self.circle_id = dpg.generate_uuid()
        dpg.draw_circle( parent=self.parent, id = self.circle_id, center= self.center, radius=self.radius, color=self.color_circle, thickness=self.thickness_circle )
        
        self.arrow_id = dpg.generate_uuid() 
        dpg.draw_arrow(parent=self.parent, p1=self.point_arrow_pos, p2=self.center, color=self.color_arrow, thickness=self.thickness_arrow, size=self.size_arrow )

