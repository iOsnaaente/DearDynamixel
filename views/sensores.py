from string import hexdigits
from tkinter import HORIZONTAL
from tokenize import group
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

  
def change_offset_moviment(sender, data, user):
    global OFFSET_MOVIMENT
    OFFSET_MOVIMENT = data 

def motor_state(sender, data, user):    
    global STATE_MOTORS 
    STATE_MOTORS = not STATE_MOTORS 
    if STATE_MOTORS: 
        with dpg.theme() as ACTIVE_MOTORS:
            dpg.add_theme_color( dpg.mvThemeCol_Button, [22, 200, 50, 200] )
            dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, [44, 240, 70, 200] )
        dpg.set_item_theme(sender, ACTIVE_MOTORS)
        dpg.configure_item( sender, label='LIGADO')
    else: 
        with dpg.theme() as DEACTIVE_MOTORS:
            dpg.add_theme_color( dpg.mvThemeCol_Button, [200, 20, 50, 200]  )  
            dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, [240, 40, 70, 200] )
        dpg.set_item_theme(sender, DEACTIVE_MOTORS)
        dpg.configure_item( sender, label='DESLIGADO')

def init_sensores(windows: dict ):
    with dpg.window( tag = 21_0, width = -1, height = -1, no_move = True, no_close = True, no_title_bar = True, no_resize = True ) as WinPltM1:
        windows['Sensores'].append(WinPltM1)
        with dpg.plot( tag = 21_1, label = 'Posição do motor M1', height = -1, width = -1, anti_aliased = True ): 
            dpg.add_plot_legend( )
            with dpg.plot_axis( dpg.mvXAxis, label = 'time [s]', time = True, no_tick_labels = True ):
                dpg.set_axis_limits( axis = dpg.last_item(), ymin = 0, ymax =10 )
            with dpg.plot_axis(dpg.mvYAxis, label = 'Angulo [º]' ):
                dpg.set_axis_limits( axis = dpg.last_item(), ymin = -5, ymax = 375 )
                dpg.add_line_series( [0,1,2,3,4,5,6,7,8,9], [10,23,35,46,56,78,85,91,150], tag = 21_2, label = 'Posição M1' )


    with dpg.window( tag = 22_0, width = -1 , height = -1, no_move = True, no_close = True, no_title_bar = True, no_resize = True ) as WinPltM2:
        windows['Sensores'].append(WinPltM2)
        with dpg.plot( tag = 22_1, label = 'Posição do motor M2', height = -1, width = -1, anti_aliased = True ): 
            dpg.add_plot_legend( )
            with dpg.plot_axis( dpg.mvXAxis, label = 'time [s]', time = True, no_tick_labels = True ):
                dpg.set_axis_limits( axis = dpg.last_item(), ymin = 0, ymax = 10 )
            with dpg.plot_axis(dpg.mvYAxis, label = 'Angulo [º]' ):
                dpg.set_axis_limits( axis = dpg.last_item(), ymin = -5, ymax = 375 )
                dpg.add_line_series( [0,1,2,3,4,5,6,7,8,9], [10,23,35,46,56,78,85,91,150], tag = 22_2, label = 'Posição M2' )
            
 
    with dpg.window( tag = 23_0, width = -1 , height = -1, no_move = True, no_close = True, no_title_bar = True, no_resize = True ) as WinPltMx:
        windows['Sensores'].append(WinPltMx)
        with dpg.plot( tag = 23_1, label = 'Ofsset dos motores', height = -1, width = -1, anti_aliased = True ): 
            dpg.add_plot_legend( )
            with dpg.plot_axis( dpg.mvXAxis, label = 'time [s]', time = True, no_tick_labels = True ):
                dpg.set_axis_limits( axis = dpg.last_item(), ymin = 0, ymax = 10 )
            with dpg.plot_axis(dpg.mvYAxis, label = 'Angulo [º]' ):
                dpg.set_axis_limits( axis = dpg.last_item(), ymin  = -5, ymax = 375 )
                dpg.add_line_series( [], [], tag = 23_21, label = 'Posição M1', source = 21_2 )
                dpg.add_line_series( [], [], tag = 23_22, label = 'Posição M2', source = 22_2 )
                dpg.add_line_series( [], [], tag = 23_23, label = 'Offset'     )
     
    with dpg.window( tag = 24_0, width= -10.35-20, height = -1, no_move = True, no_close = True, no_title_bar = True, no_resize = True ) as Comandos: 
        windows['Sensores'].append(Comandos)
        dpg.add_text("ID dos motores")
        with dpg.child_window( tag = 24_1, autosize_x = True, height = 60):
            with dpg.group( horizontal = True ):
                dpg.add_text('ID motor 1:')
                dpg.add_input_int( tag = 24_11, default_value = 1, source = ID_M1 ,user_data = 'm1', callback = change_id )
            with dpg.group( horizontal = True ):    
                dpg.add_text('ID motor 2:')
                dpg.add_input_int( tag = 24_12, default_value = 2, source = ID_M2 ,user_data = 'm2', callback = change_id )
        
        dpg.add_spacer(width = 3)
        dpg.add_text('Angulo dos motores')
        with dpg.child_window( tag = 24_2, autosize_x = True, height = 60):
            with dpg.group( horizontal = True ):    
                dpg.add_text('Angulo M1:')
                dpg.add_drag_float( tag = 24_21, enabled=True, source = DEG_M1 )  
            with dpg.group( horizontal = True ):    
                dpg.add_text('Angulo M2:')
                dpg.add_drag_float( tag = 24_22, enabled=True, source = DEG_M2 )
        
        dpg.add_spacer(width=3)
        dpg.add_text('Offset')
        with dpg.child_window( tag = 24_3, autosize_x = True, height = 40 ):
            with dpg.group( horizontal = True ):    
                dpg.add_text('Offset:')
                dpg.add_input_float( tag = 24_31, step = 0.1, max_value = 120, min_value = 0, source = OFFSET, callback = change_offset_moviment )

        dpg.add_spacer(width=3)
        dpg.add_text("Controle manual dos motores")
        with dpg.child_window( tag = 24_4, autosize_x = True, height = 275 ):
            with dpg.table( ):
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.table_cell( ):    
                        dpg.add_button ( tag = 24_4_11, label = '+M1 -M2', height = 50, width = -1, user_data = '+m1-m2', callback = change_motor_angle)
                    with dpg.table_cell( ):
                        dpg.add_button ( tag = 24_4_12, label = '+M1',     height = 50, width = -1, user_data = '+m1'   , callback = change_motor_angle)
                    with dpg.table_cell( ):
                        dpg.add_button ( tag = 24_4_13, label = '+M1 +M2', height = 50, width = -1, user_data = '+m1+m2', callback = change_motor_angle)
                with dpg.table_row(): 
                    with dpg.table_cell( ):
                        dpg.add_button ( tag = 24_4_21, label = '-M2' , height = 50, width = -1, user_data = '-m2' , callback=change_motor_angle)
                    with dpg.table_cell( ):
                        dpg.add_button ( tag = 24_4_22, label = 'STOP', height = 50, width = -1, user_data = 'stop', callback = motor_state )
                    with dpg.table_cell( ):
                        dpg.add_button ( tag = 24_4_23, label = '+M2' , height = 50, width = -1, user_data ='+m2'  , callback=change_motor_angle)
                with dpg.table_row( ):
                    with dpg.table_cell( ):
                        dpg.add_button ( tag = 24_4_31, label = '-M1 -M2', height = 50, width = -1, user_data = '-m1-m2', callback = change_motor_angle)
                    with dpg.table_cell( ):    
                        dpg.add_button ( tag = 24_4_32, label = '-M1',     height = 50, width = -1, user_data = '-m1'   , callback = change_motor_angle)
                    with dpg.table_cell( ):
                        dpg.add_button ( tag = 24_4_33, label = '-M1 +M2', height = 50, width = -1, user_data = '-m1+m2', callback = change_motor_angle)
            
            with dpg.group( horizontal = True ):
                dpg.add_text('Escala:')
                dpg.add_input_float( tag = 24_4_4, source = SCALE, callback = change_offset_moviment )     

        dpg.add_spacer( width = 3 )
        dpg.add_text("Informações")
        with dpg.child_window( tag = 24_5, autosize_x = True, autosize_y = True ):
            dpg.add_text("P para o girar dos motores")            
            dpg.add_text("W e S aumentam e diminuem a velocidade angular")
            dpg.add_text("I e U aumentam e diminuem o angulo do motor 1")
            dpg.add_text("J e K aumentam e diminuem o angulo do motor 2")   
            dpg.add_text("MAS AINDA NÃO FOI IMPLEMENTADO, ESPERA AI")            
    

    dpg.bind_item_theme( 21_2 , plot_blue_line  ) 
    dpg.bind_item_theme( 22_2 , plot_green_line ) 
    dpg.bind_item_theme( 23_21, plot_blue_line  ) 
    dpg.bind_item_theme( 23_22, plot_green_line ) 
    dpg.bind_item_theme( 23_23, plot_red_line   ) 
    
