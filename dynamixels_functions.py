from tkinter import OFF
import dearpygui.dearpygui as dpg 

from registry import * 

def change_id( sender, data, user ): 
    pass 

def change_motor_angle(sender, data, user):
    deg_m1 = dpg.get_value( DEG_M1 )
    deg_m2 = dpg.get_value( DEG_M2 )
    offset = dpg.get_value( OFFSET )

    if   '+m1' in user: deg_m1 += offset/2
    elif '-m1' in user: deg_m1 -= offset/2
    
    if   '+m2' in user: deg_m2 += offset/2
    elif '-m2' in user: deg_m2 -= offset/2

    deg_m1 = deg_m1 - 360 if deg_m1 >= 360 else 360 - abs(deg_m1) if deg_m1 < 0 else deg_m1 
    deg_m2 = deg_m2 - 360 if deg_m2 >= 360 else 360 - abs(deg_m2) if deg_m2 < 0 else deg_m2 

    dpg.set_value( OFFSET, abs(deg_m1 - deg_m2) )
    dpg.set_value( DEG_M1, deg_m1 )
    dpg.set_value( DEG_M2, deg_m2 )

def change_offset_moviment( sender, data, user ): 
    pass 
