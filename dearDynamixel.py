from utils.PyDynamixel_v2.PyDynamixel_v2 import *
from utils.SerialReader import comportList

from Atuador import Atuador

from dearpygui.dearpygui import * 

from views.inicio import * 
from views.controle import *
from views.sensores import *
from views.parametros import *


'''
    CONTROLE   -> 2_0
    SENSORES   -> 3_0
    PARAMETROS -> 4_0
'''

windows = {
            "Inicio"    : [  ],
            "Controle"  : [  ],
            "Sensores"  : [  ],
            "Parametros": [  ],
            'Sair'      : [  ],
            }
window_opened = ''

def add_image_loaded( img_path ):
    w, h, c, d = load_image( img_path )
    with texture_registry() as reg_id : 
        return add_static_texture( w, h, d, parent = reg_id )

def change_menu(sender, app_data, user_data ):
    global window_opened 
    window_opened = user_data 
    # CLOSE ALL WINDOWS 
    for k in windows.keys():
        for i in windows[k]:
            hide_item(i)
    # OPEN THE RIGHT TAB WINDOW 
    to_open = windows[user_data]
    for i in to_open:
        show_item(i)

# Main Window 
with window( label = 'Main Window', id = 1_0, autosize = True ) as main_window:
    with menu_bar(label = "MenuBar"):
        add_menu_item( label="Inicio"    , callback = change_menu, user_data = "Inicio"     )
        add_menu_item( label="Controle"  , callback = change_menu, user_data = "Controle"   )
        add_menu_item( label="Sensores"  , callback = change_menu, user_data = "Sensores"   )
        add_menu_item( label="Parametros", callback = change_menu, user_data = "Parametros" )
        add_menu_item( label="Sair"      , callback = change_menu, user_data = 'Sair'       )

# Themes configuration
with theme( default_theme = True ) as theme_id:
    add_theme_color( mvThemeCol_Button       , (52, 140, 215), category = mvThemeCat_Core )
    add_theme_style( mvStyleVar_FrameRounding,        5      , category = mvThemeCat_Core )
    # um azul bem bonito -> 52, 140, 215 


setup_viewport()
set_viewport_min_height( height = 700                       ) 
set_viewport_min_width ( width  = 800                       ) 
set_viewport_title     ( title  = 'Controle Atuador - NSEA' )
maximize_viewport() 

set_primary_window    ( main_window, True    )

init_inicio(windows, change_menu)
plots = init_controle(windows, change_menu)

count = 0 
import math 

change_menu(None, None, 'Controle' )
while is_dearpygui_running():
    w, h = get_item_width( 1_0 ), get_item_height( 1_0 )
    render_dearpygui_frame() 

    if get_frame_count()%2 == 0:
        count += 1 
        for plot in plots:
            plot.append( [count, 10*math.sin(math.radians(2*count))] )
    
    if   window_opened == "Inicio"    : render_inicio () 
    elif window_opened == "Controle"  : render_controle( plots ) 
    elif window_opened == "Sensores"  : render_inicio()
    elif window_opened == "Parametros": render_inicio()     
    elif window_opened == "Sair"      : render_inicio()  
