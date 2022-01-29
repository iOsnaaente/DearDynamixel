import dearpygui.dearpygui as dpg


'''                 Px = (norm_x * dx) + Po_x
Po  ____________________________________
    |__________________________________|
    |__________________________________|    Py = (norm_y * dy) + Po_y
    |__________________________________|
    |__________________________________| Pf = (Po + dx, Po + dy) 

'''

class Ploter:
    
    colors = {
        'r' : [ 255,   0,   0, 200],
        'g' : [   0, 255,   0, 200],
        'b' : [   0,   0, 255, 200],
        'R' : [ 255,   0,   0, 255],
        'G' : [   0, 255,   0, 255],
        'B' : [   0,   0, 255, 255]
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
                data: list, 
                pos: list,
                window_title: str = 'None',
                resolution: int = 100, 
                offset_x: int = 0, 
                offset_y: int = 0,
                thickness_line : int = 1,
                show_line : bool = True,
                color_line : str = 'b',
                color_mark : str = 'B',
                size_mark : int = 1,
                marker : str = 'o',
                theme_default : bool = True,
                drawlist_border : bool = True,
                drawlist_border_color : list = [0,0,0,0],
                drawlist_background : list = [0,0,0,0],
                drawlist_border_round : int = 10,
                ) -> None:

        self.parent = parent
        if window_title != 'None':
            dpg.configure_item( self.parent, label = window_title, no_move=True, no_close=True, no_resize=True )    
        else: 
            dpg.configure_item( self.parent, no_title_bar= True, no_move=True, no_close=True, no_resize=True )    
            
        self.offset_x, self.offset_y = offset_x, offset_y
        self.height = dpg.get_item_height(self.parent)-self.offset_y
        self.width = dpg.get_item_width(self.parent)-self.offset_x 
        self.resolution = resolution
        self.draw_points = [] 
        self.data = data 
        self.pos = pos

        self.drawlist_border_color = drawlist_border_color
        self.drawlist_border_round = drawlist_border_round
        self.drawlist_background = drawlist_background
        self.drawlist_border = drawlist_border
        self.theme_default = theme_default

        self.color_mark = self.colors[color_mark] if color_mark in self.colors.keys() else 'B'
        self.color_line = self.colors[color_line] if color_line in self.colors.keys() else 'b'
        self.marker = self.markers[marker] if marker in self.markers.keys() else 'o'

        self.thickness_line = thickness_line
        self.size_mark = size_mark 
        self.show_line = show_line

        self.markers_ids = [ dpg.generate_uuid() for _ in range(self.resolution) ]
        self.polyline_id = dpg.generate_uuid()

        self._ajust_stack()
        self._normalize_data()

        if not self.theme_default:
            self.set_theme()

        dpg.draw_polyline(parent=self.parent, id=self.polyline_id, points=self.data, closed=False, color=self.color_line, thickness=self.thickness_line)
        if self.marker:
            for ind in range(len(self.data)):
                dpg.draw_circle(  parent=self.parent, id=self.markers_ids[ind], center=self.data[ind], radius= self.size_mark, color=self.color_mark, segments=self.marker)

        dpg.add_resize_handler(self.parent, callback = self.resize )
        self.update()


    def update(self, srt : bool = True ):
        if srt: 
            self.draw_points.sort()
        if self.marker:
            for ind in range(len(self.draw_points)):
                dpg.configure_item( item=self.markers_ids[ind], center=self.draw_points[ind], radius= self.size_mark, color=self.color_mark, segments=self.marker)
        dpg.configure_item(item=self.polyline_id, points=self.draw_points, color=self.color_line, thickness=self.thickness_line)


    def resize(self ):
        self.width, self.height = dpg.get_item_width(self.parent), dpg.get_item_height(self.parent)
        self._normalize_data()
        self.update()


    def move(self, pos : list ): 
        self.pos = pos 
        dpg.configure_item(self.parent, width=self.width, height=self.height, pos=self.pos )
        self._normalize_data() 
        self.update()


    def append(self, new_point ) :
        self.data.append( new_point )
        self._ajust_stack()
        self._normalize_data()
        self.update()


    def set_resolution(self, new_resolution):
        self._get_unique_id(new_resolution)


    def set_theme(self) -> None:
        with dpg.theme() as theme_item:
            dpg.add_theme_style( dpg.mvStyleVar_WindowBorderSize, self.drawlist_border )
            dpg.add_theme_style( dpg.mvStyleVar_WindowRounding  , x = self.drawlist_border_round , y = self.drawlist_border_round  )
            dpg.add_theme_color( dpg.mvThemeCol_WindowBg, self.drawlist_background )
            dpg.add_theme_color( dpg.mvThemeCol_BorderShadow , self.drawlist_border_color ) 
        dpg.set_item_theme(self.parent, theme=theme_item)

    def _get_unique_id(self, new_resolution):
        self.resolution = new_resolution
        self.ids = [ dpg.generate_uuid() for _ in range(new_resolution)]
        for id in self.ids:
            dpg.delete_item( id )


    def _ajust_stack(self, sort : bool = False ): 
        if not self.data:
            self.data = [ [i,1] for i in range(self.resolution)]
        elif len(self.data) > self.resolution:
            self.data = [value for value in self.data[len(self.data)-self.resolution:]]
        else:
            self.data = self.data

        if sort:
            self.data = sorted(self.data)


    def _normalize_data(self):
        norm = lambda max, min, value : (value-min)/(max-min) if max-min != 0 else 0
        x_max, x_min = max(self.data)[0], min(self.data)[0]
        y_max, y_min = max(self.data, key = lambda x : x[1])[1], min(self.data, key = lambda x : x[1])[1]
        self.draw_points = [ 
            [norm(x_max, x_min, x)*(self.width-2*self.offset_x-self.pos[0]) + self.pos[0]+self.offset_x, 
            -norm(y_max, y_min, y)*(self.height-2*self.offset_y-self.pos[1]) + self.pos[1]+self.height-self.offset_y]  for x, y  in self.data[::-1] ]
        
