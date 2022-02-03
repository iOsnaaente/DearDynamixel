from xml.etree.ElementInclude import default_loader
import dearpygui.dearpygui as dpg 
import components.PyDynamixel_v2.PyDynamixel_v2 as pd 
import serial 

from dynamixels_functions import * 
from registry import *

def resize_connect( ):
    new_w, new_h = dpg.get_item_width( 'mainWindow'), dpg.get_item_height( 'mainWindow' )    
    dpg.configure_item( 41_0, width = new_w/1.5, height = new_h/2, pos = [new_w/4, new_h/4] )

def init_connect( window ):
    with dpg.window( tag = 41_0, label = 'Configurações de portas seriais', width = dpg.get_item_width('mainWindow')/1.5, height = -1, no_resize = True, pos = [dpg.get_item_width('mainWindow')/4, 50] ) as CONN_WINDOW:
        window['Conexão'].append( CONN_WINDOW ) 
        dpg.add_checkbox( tag = 41_01, label = 'Usar Arduino para quisição de dados AS5043', source = USE_ARDUINO )

        with dpg.group( horizontal = True ):
            with dpg.group():
                with dpg.child_window             ( tag = 41_11_00, width = 240, height = 150, border = False  ):
                    with dpg.table                ( header_row = False ):
                        dpg.add_table_column      ( )
                        dpg.add_table_column      ( )

                        with dpg.table_row        ( tag = 41_11_01 ):
                            with dpg.table_cell   ( tag = 41_11_02 ):
                                dpg.add_text      ( tag = 41_11_03 , default_value = 'COMP Dynamixel:')
                            with dpg.table_cell   ( tag = 41_11_04 ):
                                pass 
                        with dpg.table_row        (tag = 41_12_01 ):
                            with dpg.table_cell   (tag = 41_12_02 ):
                                dpg.add_text      (tag = 41_12_03 , default_value = 'Comport: ')
                            with dpg.table_cell   (tag = 41_12_04 ):
                                dpg.add_combo     (tag = 41_12_05 , default_value = 'COM10', items = COMPORT_LIST, width = -1 )
                        with dpg.table_row        ( tag = 41_13_01 ):
                            with dpg.table_cell   ( tag = 41_13_02 ):
                                dpg.add_text      ( tag = 41_13_03 , default_value = 'Baudrate: ')
                            with dpg.table_cell   ( tag = 41_13_04 ):
                                dpg.add_combo     ( tag = 41_13_05 , default_value = '9600', items = BAUDRATE_LIST, width = -1 )
                    dpg.add_button( tag = 41_14_01, width = -1, label = 'CONNECT'  , callback = try_connect )
                    dpg.add_button( tag = 41_14_02, width = -1, label = 'CONNECTED', show = False )

                with dpg.child_window( tag = 41_21_00, width = 240, height = 150, border = False  ):
                    with dpg.table( header_row = False ):
                        dpg.add_table_column()
                        dpg.add_table_column()
                        with dpg.table_row        ( tag = 41_21_01 ):
                            with dpg.table_cell   ( tag = 41_21_02 ):
                                dpg.add_text      ( tag = 41_21_03 , default_value = 'COMP Arduino:')
                            with dpg.table_cell   ( tag = 41_21_04 ):
                                pass 
                        with dpg.table_row        (tag = 41_22_01 ):
                            with dpg.table_cell   (tag = 41_22_02 ):
                                dpg.add_text      (tag = 41_22_03 , default_value = 'Comport: ')
                            with dpg.table_cell   (tag = 41_22_04 ):
                                dpg.add_combo     (tag = 41_22_05 , default_value = 'COM10', items = COMPORT_LIST, width = -1 )
                        with dpg.table_row        ( tag = 41_23_01 ):
                            with dpg.table_cell   ( tag = 41_23_02 ):
                                dpg.add_text      ( tag = 41_23_03 , default_value = 'Baudrate: ')
                            with dpg.table_cell   ( tag = 41_23_04 ):
                                dpg.add_combo     ( tag = 41_23_05 , default_value = '115200', items = BAUDRATE_LIST, width = -1 )
                    dpg.add_button( tag = 41_24_01, width = -1, label = 'CONNECT'  , callback = try_connect )
                    dpg.add_button( tag = 41_24_02, width = -1, label = 'CONNECTED', show = False )
                
            dpg.configure_item(41_21_00, show = False )
            with dpg.child_window( tag = 41_30, width = 300, height = 305  ):
                with dpg.group( horizontal = True ):
                    dpg.add_text( 'Portas seriais disponíveis:') 
                    dpg.add_button( tag = 41_31_01, label = 'Atualizar Comports', width = -1, callback = atualize_comports )                    
                dpg.add_spacer( height = 10 )
                dpg.add_text( tag = 41_31_02, default_value = '' )

    resize_connect() 


def render_connect():
    pass