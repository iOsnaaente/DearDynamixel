from dearpygui.dearpygui import *
import os 

def hover_buttons_IN ( sender, data, user ):
    if   user == "Visualização geral"  :
        configure_item( 1_3_1, default_value = user )
    elif user == "Posição do sol"      :
        configure_item( 1_3_1, default_value = user )
    elif user == "Atuadores"           :
        configure_item( 1_3_1, default_value = user )
    elif user == "Atuação da base"     :
        configure_item( 1_3_1, default_value = user )
    elif user == "Atuação da elevação" :
        configure_item( 1_3_1, default_value = user )
    elif user == "Configurações"       :
        configure_item( 1_3_1, default_value = user )

def render_inicio    ( ):
    w , h = get_item_width( 1_0 ), get_item_height( 1_0 )
    
    configure_item( 1_1 , width = w-15     , height = h*3/10    , pos = [ 10       , 25             ] )
    configure_item( 1_2 , width = w/3      , height = h*6.60/10 , pos = [ 10       , (h//10)*3 + 30 ] )
    configure_item( 1_3 , width = w*2/3-20 , height = h*6.60/10 , pos = [ w//3 + 15, (h//10)*3 + 30 ] )

    w_header , h_header  = get_item_width( 1_1 ), get_item_height( 1_1 )
    w_lateral, h_lateral = get_item_width( 1_2 ), get_item_height( 1_2 )


    v_spacing = h_lateral // 6  # LATERAL 
    configure_item( 1_2_1, width = w//3 - 15, height = v_spacing ) 
    configure_item( 1_2_2, width = w//3 - 15, height = v_spacing ) 
    configure_item( 1_2_3, width = w//3 - 15, height = v_spacing ) 
    configure_item( 1_2_4, width = w//3 - 15, height = v_spacing ) 
    configure_item( 1_2_5, width = w//3 - 15, height = v_spacing )  

def init_inicio      ( windows :dict, callback ): 
    with theme( id = 'no_win_border'):
        add_theme_style( mvStyleVar_WindowBorderSize, 0 , category = mvThemeCat_Core )

    with window( label = 'Header' , id = 1_1, pos = [10, 25], no_move= True, no_close= True, no_title_bar= True, no_resize= True ) as Header_IN:    
        windows['Inicio'].append( Header_IN )
    with window( label = 'Lateral', id = 1_2, no_move= True, no_close= True, no_title_bar= True, no_resize= True ) as Lateral_IN:
        windows['Inicio'].append( Lateral_IN )
        add_spacing( count = 4 )
        add_button(  label ="Inicio"    , id = 1_2_1, arrow  = False, callback = callback, user_data   = "Inicio"    )
        add_button(  label ="Controle"  , id = 1_2_2, arrow  = False, callback = callback, user_data   = "Controle"  )
        add_button(  label ="Sensores"  , id = 1_2_3, arrow  = False, callback = callback, user_data   = "Sensores"  )
        add_button(  label ="Parametros", id = 1_2_4, arrow  = False, callback = callback, user_data   = "Parametros")
        add_button(  label ="Sair"      , id = 1_2_5, arrow  = False, callback = callback, user_data   = "Sair"      )
        
    with window(     label = 'Main'               , id = 1_3  , no_move= True , no_close = True       , no_title_bar= True, no_resize= True) as Main_IN:
        windows['Inicio'].append( Main_IN )
        add_text( 'HOVER SOME ITEM AT THE LEFT SIDE...', id = 1_3_1)
        add_hover_handler( parent = 1_2_1, callback = hover_buttons_IN, user_data = "Inicio"    )
        add_hover_handler( parent = 1_2_2, callback = hover_buttons_IN, user_data = "Controle"  )
        add_hover_handler( parent = 1_2_3, callback = hover_buttons_IN, user_data = "Sensores"  )
        add_hover_handler( parent = 1_2_4, callback = hover_buttons_IN, user_data = "Parametros")
        add_hover_handler( parent = 1_2_5, callback = hover_buttons_IN, user_data = "Sair"      )
        
    set_item_theme(1_1, 'no_win_border')
    set_item_theme(1_2, 'no_win_border')
    set_item_theme(1_3, 'no_win_border')

