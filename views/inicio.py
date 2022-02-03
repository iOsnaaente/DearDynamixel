import dearpygui.dearpygui as dpg 
import time 
import sys 
import os

PATH = os.path.dirname(__file__).removesuffix('views')
sys.path.insert( 0, PATH )

def add_image_loaded( img_path ):
    w, h, c, d = dpg.load_image( img_path )
    with dpg.texture_registry() as reg_id : 
        return dpg.add_static_texture( w, h, d, parent = reg_id )

def closing_dpg( sender, data, user ): 
    with dpg.window( pos = [ dpg.get_item_width('mainWindow')/2.5, dpg.get_item_height('mainWindow')/2.5]): 
        dpg.add_text( 'Obrigado por usar nosso programa\nEle irá encerrar em instantes' )
    time.sleep(2)
    dpg.stop_dearpygui() 

def show_hide_window( sender, data, user ):
    if dpg.get_item_configuration(sender)['show'] == False: 
        if data:
            dpg.show_item( user )
        else: 
            dpg.hide_item( user )
       
# REGISTRIES ESPECIFIC 
img_fundo  = add_image_loaded( PATH + '\\public\\fundo.png'              )
img_logo   = add_image_loaded( PATH + '\\public\\distico_UFSM.png'       )
img_inici  = add_image_loaded( PATH + '\\public\\init_img\\img_inici.jpg')
img_contr  = add_image_loaded( PATH + '\\public\\init_img\\img_contr.png')
img_senso  = add_image_loaded( PATH + '\\public\\init_img\\img_senso.png')
img_param  = add_image_loaded( PATH + '\\public\\init_img\\img_param.jpg')
img_sair   = add_image_loaded( PATH + '\\public\\init_img\\img_sair.png' ) 

WinInitHeader  = dpg.window 
WinInitLateral = dpg.window
WinInitMain    = dpg.window

# HANDLER_REGISTERS / THEMES 
def handlers_and_themes_inicio( ): 
    # HANDLER CALLBACK_FUNCTION 
    def hover_buttons ( sender, data, user ):
        if   data == 9_12_1: dpg.configure_item( 9_13_11, texture_tag = img_inici )
        elif data == 9_12_2: dpg.configure_item( 9_13_11, texture_tag = img_contr )
        elif data == 9_12_3: dpg.configure_item( 9_13_11, texture_tag = img_senso )
        elif data == 9_12_4: dpg.configure_item( 9_13_11, texture_tag = img_param )
        elif data == 9_12_5: dpg.configure_item( 9_13_11, texture_tag = img_sair  )

    # HANDLERS 
    with dpg.item_handler_registry( ) as handler_hover:
        dpg.add_item_hover_handler( callback = hover_buttons )
    dpg.bind_item_handler_registry( item = 9_12_1, handler_registry = handler_hover )
    dpg.bind_item_handler_registry( item = 9_12_2, handler_registry = handler_hover )
    dpg.bind_item_handler_registry( item = 9_12_3, handler_registry = handler_hover )
    dpg.bind_item_handler_registry( item = 9_12_4, handler_registry = handler_hover )
    dpg.bind_item_handler_registry( item = 9_12_5, handler_registry = handler_hover )
    
    # THEMES 
    with dpg.theme( tag = 100_02 ) as theme_no_win_border:
        with dpg.theme_component( dpg.mvAll):
            dpg.add_theme_style( dpg.mvStyleVar_WindowBorderSize, 0 , category = dpg.mvThemeCat_Core )
    dpg.bind_item_theme( WinInitHeader , theme_no_win_border)
    dpg.bind_item_theme( WinInitLateral, theme_no_win_border)
    dpg.bind_item_theme( WinInitMain   , theme_no_win_border)

# MAIN FUNCTIONS 
def resize_inicio( ): 
    w , h = dpg.get_item_width('mainWindow'), dpg.get_item_height('mainWindow')
    dpg.configure_item( WinInitHeader  , width = w-15     , height = h*3/10    , pos = [ 10       , 25             ] )
    dpg.configure_item( WinInitLateral , width = w/3      , height = h*6.60/10 , pos = [ 10       , (h//10)*3 + 30 ] )
    dpg.configure_item( WinInitMain    , width = w*2/3-20 , height = h*6.60/10 , pos = [ w//3 + 15, (h//10)*3 + 30 ] )

    w_header , h_header  = dpg.get_item_width( WinInitHeader ), dpg.get_item_height( WinInitHeader )
    dpg.configure_item( 911_1  , width = w_header-16 , height = h_header-16 )  
    dpg.configure_item( 911_11 , pmin  = (-30,-30)   , pmax   = ( w, round( h*3/10)*2 ))
    dpg.configure_item( 911_12 , pmin  = (10,10)     , pmax   = (350,200) )

    v_spacing = dpg.get_item_height( WinInitLateral ) // 6  
    dpg.configure_item( 912_1, width = w//3 - 15, height = v_spacing ) 
    dpg.configure_item( 912_2, width = w//3 - 15, height = v_spacing ) 
    dpg.configure_item( 912_3, width = w//3 - 15, height = v_spacing ) 
    dpg.configure_item( 912_4, width = w//3 - 15, height = v_spacing ) 
    dpg.configure_item( 912_5, width = w//3 - 15, height = v_spacing )  

    dpg.configure_item( 913_1 , width = (w*2/3-20)*0.99 , height = (h*6.60/10)*0.875 )
    dpg.configure_item( 913_11, pmax  = [ (w*2/3-20)*0.99 , (h*6.60/10)*0.8750 ]  )
    dpg.configure_item( 913_12, pos   = [ (w*2/3-20)*0.99//3 , 50 ])

def render_inicio ( ):
    if dpg.get_frame_count() % 10 == 0: 
        resize_inicio()    

def init_inicio ( windows :dict, callback ): 
    global WinInitHeader    
    global WinInitLateral
    global WinInitMain

    with dpg.window( label = 'Header' , tag = dpg.generate_uuid(), pos = [10, 25], no_move= True, no_close= True, no_title_bar= True, no_resize= True ) as WinInitHeader:    
        windows['Inicio'].append( WinInitHeader )  
        with dpg.drawlist( tag = 9_11_1, width = -1, height = - 1 ):      
            dpg.draw_image  ( tag = 9_11_11, label = 'imgFundo', texture_tag = img_fundo, pmin = (0,0), pmax = (1,1) ) 
            dpg.draw_image  ( tag = 9_11_12, label = 'imgLogo' , texture_tag = img_logo , pmin = (0,0), pmax = (1,1) )
            # ADICIONAR O TÍTULO DO ATUADOR E UMA FOTINHO DELE 

    with dpg.window( label = 'Lateral', tag = dpg.generate_uuid(), no_move= True, no_close= True, no_title_bar= True, no_resize= True ) as WinInitLateral: 
        windows['Inicio'].append( WinInitLateral )
        dpg.add_spacer(  width = 4 )
        dpg.add_button(  label = "Inicio"    , tag = 9_12_1, arrow  = False, callback = callback         , user_data   = "Inicio"   )
        dpg.add_button(  label = "Controle"  , tag = 9_12_2, arrow  = False, callback = callback         , user_data   = "Controle" )
        dpg.add_button(  label = "Sensores"  , tag = 9_12_3, arrow  = False, callback = callback         , user_data   = "Sensores" )
        dpg.add_button(  label = "Conexão"   , tag = 9_12_4, arrow  = False, callback = show_hide_window , user_data   = 42_0  )
        dpg.add_button(  label = "Sair"      , tag = 9_12_5, arrow  = False, callback = closing_dpg      , user_data   = "Sair"     )
        
    with dpg.window(  label = 'Main'  , tag = dpg.generate_uuid()  , no_move= True , no_close = True       , no_title_bar= True, no_resize= True) as WinInitMain:
        windows['Inicio'].append( WinInitMain )
        with dpg.drawlist ( tag = 9_13_1, width = 1000, height = 1000 ): 
            dpg.draw_image( tag = 9_13_11, label = 'imgMain', texture_tag = img_inici, pmin = (0,0), pmax = (100,100) ) 
            dpg.draw_text ( tag = 9_13_12, pos = [500/500], text = '', size = 20 )
    
    resize_inicio() 
    handlers_and_themes_inicio()
