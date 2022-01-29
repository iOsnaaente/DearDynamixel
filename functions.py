import dearpygui.dearpygui    as dpg
from datetime import datetime as dt 

import sys 
import os

PATH = os.path.dirname(__file__)
sys.path.insert( 0, PATH )

def add_image_loaded( img_path ):
    w, h, c, d = dpg.load_image( img_path )
    with dpg.texture_registry() as reg_id : 
        return dpg.add_static_texture( w, h, d, parent = reg_id )

