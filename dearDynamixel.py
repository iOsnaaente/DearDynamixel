# INICIO DO CONTEXTO DEARPYGUI 
import dearpygui.dearpygui as dpg 

dpg.create_context()
dpg.create_viewport( title = 'NSEA - Atuador de série elástica', min_width = 800, min_height = 600 )
dpg.setup_dearpygui()

from time import sleep 
from os import path  
PATH = path.dirname( __file__ ) 

# IMPORTAÇÕES 
from utils.PyDynamixel_v2.PyDynamixel_v2 import Joint 
from views.controle import *  
from registry       import * 
from themes         import * 


windows = {
            "Inicio"  : [  ],
            "Controle": [  ],
            "Sensores": [  ],
            "Conexão" : [  ],
            'Sair'    : [  ],
            }
window_opened = ''


# CALLBACKS
def change_menu(sender, app_data, user_data ):
    global window_opened 
    window_opened = user_data 
    # CLOSE ALL WINDOWS 
    for k in windows.keys():
        for i in windows[k]:
            dpg.hide_item(i)
    # OPEN THE RIGHT TAB WINDOW 
    to_open = windows[user_data]
    for i in to_open:
        dpg.show_item(i)
    resize_main()

def show_hide_window( sender, data, user ):
    if dpg.get_item_configuration(user)['show'] == False: 
        dpg.show_item( user )
    else: 
        dpg.hide_item( user )
            
def closing_dpg( sender, data, user ): 
    with dpg.window( pos = [ dpg.get_item_width('mainWindow')/2.5, dpg.get_item_height('mainWindow')/2.5]): 
        dpg.add_text( 'Obrigado por usar nosso programa\nEle irá encerrar em instantes' )
    sleep(2)
    dpg.stop_dearpygui() 


# MAIN FUNCTIONS
def resize_main( ):
    global window_opened
    #if   window_opened == "Controle"  : resize_inicio()     
    #elif window_opened == "Sensores"  : resize_sensores()   
    #elif window_opened == "Conexão"   : resize_connect()      
    if window_opened == "Controle"     : resize_controle()   

def render_main( ):
    global window_opened
    #if   window_opened == "Inicio"    : render_inicio()    
    #elif window_opened == "Sensores"  : render_sensores()  
    #elif window_opened == "Conexão"   : render_connect()  
    if window_opened == "Controle"     : render_controle()  

def init_main():
    with dpg.window( label = 'Main Window', id = 'mainWindow', autosize = True ) as main_window:
        with dpg.menu_bar(label = "MenuBar"):
            #dpg.add_menu_item( label = "Inicio"   , callback = change_menu     , user_data = "Inicio"   )
            dpg.add_menu_item( label = "Controle" , callback = change_menu     , user_data = "Controle" )
            #dpg.add_menu_item( label = "Sensores" , callback = change_menu     , user_data = "Sensores" )
            #dpg.add_menu_item( label = "Conexão"  , callback = show_hide_window, user_data = 41_0, check = True  )
            dpg.add_menu_item( label = "Sair"     , callback = closing_dpg     , user_data = 'Sair'     )

            '''
                CONTROLE -> 2_0
                SENSORES -> 3_0
                CONEXÃO  -> 4_0
            '''


init_main      ( ) 
init_controle  ( windows )
change_menu    ( None, None, 'Controle' ) 

# CONFIGURATIONS 
dpg.set_primary_window          ( 'mainWindow', True          )
dpg.set_viewport_large_icon     ( PATH + '\\utils\\ico\\large_ico.ico' )
dpg.set_viewport_small_icon     ( PATH + '\\utils\\ico\\small_ico.ico' )
dpg.set_viewport_resize_callback( resize_main                 )
dpg.maximize_viewport           (                             ) 



# Criação do item atuador
#atuador = Atuador(M1_ID, M2_ID, search_for_serial=False )
# Criação das juntas 
#joint28 = pd.Joint(ids[0])
#joint01 = pd.Joint(ids[1])
#
## Attach das juntas
#serial.attach_joints([joint28, joint01])
#serial.enable_torques()
#offsetValue = round( abs( angle_motor2 - angle_motor1 ) )
#offsetValue = offsetValue if offsetValue < 180.0 else 360.0 - offsetValue
#
#serial.send_angles({ids[0] : angle_motor1, ids[1] : angle_motor2})
#angles = serial.get_angles()


# START OF DPG VIEW 
dpg.show_viewport( )

resize_controle()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame() 
    render_main() 
         
