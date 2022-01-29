from heapq import heappush
import dearpygui.dearpygui as dpg 

def resize_connect( ):
    new_w, new_h = dpg.get_item_width( 'mainWindow'), dpg.get_item_height( 'mainWindow' )    
    
    dpg.configure_item( 41_0, width = new_w//2, height = new_h//2  )

def init_connect( window ):
    with dpg.window( tag = 41_0, width = -1, height = -1, no_resize = True ) as CONN_WINDOW:
        window['Conexão'].append( CONN_WINDOW ) 
        dpg.add_text( tag = 41_1, default_value = 'Aqui faremos a configuração das portas seriais e conexão ')

    resize_connect() 


def render_connect():
    pass 