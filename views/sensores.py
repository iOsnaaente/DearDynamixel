import dearpygui.dearpygui as dpg
from dynamixels_functions import * 
from registry import * 
from themes import * 
import math 

f = 2
w = 2*math.pi * f 

angleM1 = 0.0 
angleM2 = 0.0 
velAngM1 = 100* 2*math.pi * f  
velAngM2 = 100* 2*math.pi * f 

count = 0 

OFFSET_MOVIMENT = 1
STATE_MOTORS = True 

M1_ID = 0 
M2_ID = 0 

def resize_sensores( ):
    new_w, new_h = dpg.get_item_width( 'mainWindow'), dpg.get_item_height( 'mainWindow' )     
    dpg.configure_item( 21_0, width = new_w*0.65   , height = new_h*0.25  , pos = [10, 25]            )
    dpg.configure_item( 22_0, width = new_w*0.65   , height = new_h*0.25  , pos = [10, new_h*0.25+30] )
    dpg.configure_item( 23_0, width = new_w*0.65   , height = new_h*0.5-40, pos = [10, new_h*0.5+35]  )
    dpg.configure_item( 24_0, width = new_w*0.35-20, height = new_h-30    , pos = [new_w*0.65+15,25]  )
    dpg.configure_item( 24_4, width = new_w*0.9    , height = new_h*0.30                              )

def render_sensores():
    pass 


def init_sensores(windows: dict ):
    pass 