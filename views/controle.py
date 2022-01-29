import dearpygui.dearpygui as dpg

from dynamixels_functions import * 
from registry import * 
from themes import * 

import math 
from decimal import Decimal 

# FUNCTIONS 
def change_wave_form( sender, data, user ):
    data = dpg.get_value( CONVOLUCAO )
    dpg.set_value( LAST_WAVE_CLICKED, user )

    if sender is None: 
        dpg.set_value( WAVE_SEN, False )
        dpg.set_value( WAVE_TRI, False )
        dpg.set_value( WAVE_SQR, False )

    if user == 'tri':
        dpg.set_value( WAVE_TRI, not dpg.get_value(WAVE_TRI) ) 
        if not data:
            dpg.set_value( WAVE_SEN, False ) 
            dpg.set_value( WAVE_SQR, False ) 

    elif user == 'sen':
        dpg.set_value( WAVE_SEN, not dpg.get_value(WAVE_SEN) ) 
        if not data:
            dpg.set_value( WAVE_TRI, False ) 
            dpg.set_value( WAVE_SQR, False ) 

    elif user == 'sqr':
        dpg.set_value( WAVE_SQR, not dpg.get_value(WAVE_SQR) ) 
        if not data:
            dpg.set_value( WAVE_SEN, False ) 
            dpg.set_value( WAVE_TRI, False ) 

    if dpg.get_value( WAVE_SQR ):   dpg.bind_item_theme( 24_3_213, button_green   )
    else:                           dpg.bind_item_theme( 24_3_213, button_default )
    if dpg.get_value( WAVE_TRI ):   dpg.bind_item_theme( 24_3_211, button_green   )
    else:                           dpg.bind_item_theme( 24_3_211, button_default )
    if dpg.get_value( WAVE_SEN ):   dpg.bind_item_theme( 24_3_212, button_green   )
    else:                           dpg.bind_item_theme( 24_3_212, button_default )

    dpg.configure_item(24_3_3, show = dpg.get_value( WAVE_TRI) ) # tri
    dpg.configure_item(24_3_4, show = dpg.get_value( WAVE_SEN) ) # sen 
    dpg.configure_item(24_3_5, show = dpg.get_value( WAVE_SQR) ) # deg 

    soma = sum([ 1 for i in [dpg.get_value( WAVE_TRI), dpg.get_value( WAVE_SEN), dpg.get_value( WAVE_SQR)] if i is True ] )
    dpg.configure_item( 24_3, height = 100 + 50*soma )
  
def save_data_measure( sender, data, user ) :
    dpg.set_value( SAVE_INIT, not dpg.get_value( SAVE_INIT) ) 
    if dpg.get_value( SAVE_INIT ): 
        dpg.configure_item( sender, label = 'Gravando / Parar ') 
        dpg.bind_item_theme( sender, button_red )
        dpg.configure_item( 24_5_3, show = True )
        dpg.configure_item( 24_5, height = 100  )
    else:
        dpg.configure_item( sender, label = 'Gravar') 
        dpg.bind_item_theme( sender, button_default )
        dpg.configure_item( 24_5_3, show = False    )
        dpg.configure_item( 24_5, height = 75       )

SEN_FUNC = lambda dt, po : po + dpg.get_value( AMPLITUDE_SEN )*math.sin( 2*math.pi*math.radians(dpg.get_value(FREQUENCIA_SEN))*dt )
SQR_FUNC = lambda dt, po : po + dpg.get_value( AMPLITUDE_SQR )*( 1 if float(Decimal(dt/( 1/dpg.get_value(FREQUENCIA_SQR)))) < 0.5 else 0 )
TRI_FUNC = lambda dt, po : po + dpg.get_value( AMPLITUDE_TRI )*2*float(Decimal(dt/( 1/dpg.get_value(FREQUENCIA_TRI))))*( 1 if float(Decimal(dt/( 2/dpg.get_value(FREQUENCIA_TRI)))) < 0.5 else -1 )

def change_plot_period( sender, data, user ) : 
    LARGE_T = 0  
    if dpg.get_value(WAVE_TRI): LARGE_T = 1/dpg.get_value( FREQUENCIA_TRI ) if 1/dpg.get_value( FREQUENCIA_TRI ) > LARGE_T else LARGE_T
    if dpg.get_value(WAVE_SEN): LARGE_T = 1/dpg.get_value( FREQUENCIA_SEN ) if 1/dpg.get_value( FREQUENCIA_SEN ) > LARGE_T else LARGE_T
    if dpg.get_value(WAVE_SQR): LARGE_T = 1/dpg.get_value( FREQUENCIA_SQR ) if 1/dpg.get_value( FREQUENCIA_SQR ) > LARGE_T else LARGE_T

    LARGE_T = LARGE_T * data if LARGE_T != 0 else data 
    POINTS_P = dpg.get_value(POINTS_PERIOD) * LARGE_T 
    print( POINTS_P )
    dpg.set_value( LEN_DOMINIO, POINTS_P )
    dpg.set_value( DOMINIO_PLOT, [ i for i in range(dpg.get_value(LEN_DOMINIO))] ) 

    OFFSET_POINTS = [] 
    M1_POINTS     = [] 
    M2_POINTS     = [] 
    for i in  dpg.get_value( DOMINIO_PLOT ): 
        M1_POINTS.append( SEN_FUNC( i, 0 )  )  
        M2_POINTS.append( SEN_FUNC( i, 0 )  )
        OFFSET_POINTS.append( abs(M1_POINTS[-1] - M2_POINTS[-1] ) )
    
    dpg.set_value( POINTS_OFFSET, OFFSET_POINTS  )  
    dpg.set_value( POINTS_MOTOR1, M1_POINTS  )  
    dpg.set_value( POINTS_MOTOR2, M2_POINTS  )  

    dpg.configure_item( 23_21, x = dpg.get_value( DOMINIO_PLOT), y = dpg.get_value(POINTS_MOTOR1) )
    dpg.set_axis_limits( 21_10, ymin = dpg.get_value( DOMINIO_PLOT)[0], ymax = dpg.get_value( DOMINIO_PLOT)[-1] ) 

    dpg.configure_item( 23_22, x = dpg.get_value( DOMINIO_PLOT), y = dpg.get_value(POINTS_MOTOR2) ) 
    dpg.configure_item( 23_23, x = dpg.get_value( DOMINIO_PLOT), y = dpg.get_value(POINTS_OFFSET) ) 
  
# MAIN FUNCTIONS 
def resize_controle( ):
    new_w, new_h = dpg.get_item_width( 'mainWindow'), dpg.get_item_height( 'mainWindow' )     

    dpg.configure_item( 21_0, width = new_w*0.65   , height = new_h*0.25  , pos = [10, 25]            )
    dpg.configure_item( 22_0, width = new_w*0.65   , height = new_h*0.25  , pos = [10, new_h*0.25+30] )
    dpg.configure_item( 23_0, width = new_w*0.65   , height = new_h*0.5-40, pos = [10, new_h*0.5+35]  )
    dpg.configure_item( 24_0, width = new_w*0.35-20, height = new_h-30    , pos = [new_w*0.65+15,25]  )
    
    soma = sum([ 1 for i in [dpg.get_value( WAVE_TRI), dpg.get_value( WAVE_SEN), dpg.get_value( WAVE_SQR)] if i is True ] )
    dpg.configure_item( 24_3, height = 100 + 50*soma )
    #dpg.configure_item( 24_4, width = new_w*0.9    , height = new_h*0.30                              )

def render_controle():
    dtime = dpg.get_delta_time() 

    dpg.get_value( LEN_DOMINIO   )
    dpg.get_value( DOMINIO_PLOT  )
    dpg.get_value( POINTS_MOTOR1 )
    dpg.get_value( POINTS_MOTOR2 )
    dpg.get_value( POINTS_OFFSET )
    dpg.get_value( POINTS_SENSOR )
    dpg.get_value( PERIODOS_PLOT )
    dpg.get_value( CONVOLUCAO    )
    dpg.get_value( WAVE_TRI      )
    dpg.get_value( WAVE_SEN      )
    dpg.get_value( WAVE_SQR      )  

def init_controle(windows: dict ):
    # MOTOR 1
    with dpg.window( tag = 21_0, width = -1, height = -1, no_move = True, no_close = True, no_title_bar = True, no_resize = True ) as WinPltM1:
        windows['Controle'].append(WinPltM1)
        with dpg.plot( tag = 21_1, label = 'Posição do motor M1', height = -1, width = -1, anti_aliased = True ): 
            dpg.add_plot_legend( )
            with dpg.plot_axis( dpg.mvXAxis, label = 'time [s]', no_tick_labels = True, tag = 21_10 ):
                dpg.set_axis_limits( axis = 2110, ymin = 0, ymax = dpg.get_value(LEN_DOMINIO) )
            with dpg.plot_axis(dpg.mvYAxis, label = 'Angulo [º]' ):
                dpg.set_axis_limits( axis = dpg.last_item(), ymin = -5, ymax = 375 )
                dpg.add_line_series( dpg.get_value(DOMINIO_PLOT), dpg.get_value(POINTS_MOTOR1), tag = 21_2, label = 'Posição M1' )

    # MOTOR 2
    with dpg.window( tag = 22_0, width = -1 , height = -1, no_move = True, no_close = True, no_title_bar = True, no_resize = True ) as WinPltM2:
        windows['Controle'].append(WinPltM2)
        with dpg.plot( tag = 22_1, label = 'Posição do motor M2', height = -1, width = -1, anti_aliased = True ): 
            dpg.add_plot_legend( )
            with dpg.plot_axis( dpg.mvXAxis, label = 'time [s]', time = True, no_tick_labels = True ):
                dpg.set_axis_limits( axis = dpg.last_item(), ymin = 0, ymax = dpg.get_value(LEN_DOMINIO) )
            with dpg.plot_axis(dpg.mvYAxis, label = 'Angulo [º]' ):
                dpg.set_axis_limits( axis = dpg.last_item(), ymin = -5, ymax = 375 )
                dpg.add_line_series( dpg.get_value(DOMINIO_PLOT), dpg.get_value(POINTS_MOTOR2), tag = 22_2, label = 'Posição M2' )
            
    # OFFSET MOTORES 
    with dpg.window( tag = 23_0, width = -1 , height = -1, no_move = True, no_close = True, no_title_bar = True, no_resize = True ) as WinPltMx:
        windows['Controle'].append(WinPltMx)
        with dpg.plot( tag = 23_1, label = 'Ofsset dos motores', height = -1, width = -1, anti_aliased = True ): 
            dpg.add_plot_legend( )
            with dpg.plot_axis( dpg.mvXAxis, label = 'time [s]', time = True, no_tick_labels = True ):
                dpg.set_axis_limits( axis = dpg.last_item(), ymin = 0, ymax = dpg.get_value(LEN_DOMINIO) )
            with dpg.plot_axis(dpg.mvYAxis, label = 'Angulo [º]' ):
                dpg.set_axis_limits( dpg.last_item(), ymin = -5, ymax = 375 )
                dpg.add_line_series( tag = 23_21, x = [], y = [], label = 'Posição M1', source = 21_2 )
                dpg.add_line_series( tag = 23_22, x = [], y = [], label = 'Posição M2', source = 22_2 )
                dpg.add_line_series( tag = 23_23, x = dpg.get_value(DOMINIO_PLOT), y = dpg.get_value(POINTS_OFFSET), label = 'Offset'   )
                dpg.add_line_series( tag = 23_24, x = dpg.get_value(DOMINIO_PLOT), y = dpg.get_value(POINTS_SENSOR), label = 'Sensor'   )
     
    # JANELA DE CONTROLE 
    with dpg.window( tag = 24_0, width= -1, height = -1, no_move = True, no_close = True, no_title_bar = True, no_resize = True ) as Comandos: 
        windows['Controle'].append(Comandos)
        
        dpg.add_text("Informações de posição")
        with dpg.child_window( tag = 24_1, autosize_x = True, height = 115 ):
            with dpg.table( tag = 24_10, header_row = False ):
                dpg.add_table_column( )
                dpg.add_table_column( )
                dpg.add_table_column( )
                with dpg.table_row( ) : 
                    with dpg.table_cell():
                        dpg.add_text       ( tag = 24_1_11, default_value = 'Angulo Motor 1: ')
                    with dpg.table_cell():
                        dpg.add_knob_float( tag = 24_1_12, width = -1, source = DEG_M1, max_value = 360 )
                    with dpg.table_cell():
                        dpg.add_input_float( tag = 24_1_13, width = -1, source = DEG_M1 )

                with dpg.table_row( ) : 
                    with dpg.table_cell(): 
                        dpg.add_text       ( tag = 24_1_21, default_value = 'Angulo motor 2: ') 
                    with dpg.table_cell():
                        dpg.add_knob_float( tag = 24_1_22, width = -1, source = DEG_M2, max_value = 360  )
                    with dpg.table_cell():               
                        dpg.add_input_float( tag = 24_1_23, width = -1, source = DEG_M2 )

        dpg.add_text("Offset")
        with dpg.child_window( tag = 24_2, autosize_x = True, height = 40 ):
            with dpg.table( tag = 24_20, header_row = False ): 
                dpg.add_table_column( )
                dpg.add_table_column( )
                with dpg.table_row() : 
                    with dpg.table_cell():
                        dpg.add_text       ( tag = 24_211, default_value = 'Offset: ')
                    with dpg.table_cell(): 
                        dpg.add_input_float( tag = 24_212, width = -1, step = 0.1, max_value = 120, min_value = 0, source = OFFSET )
        
        dpg.add_spacer( width = 3 )
        dpg.add_text("Controle - Formas de onda ")
        with dpg.child_window( tag = 24_3, autosize_x = True, height = 300 ):
            dpg.add_checkbox ( tag = 24_3_1, label = 'Sobreposição de ondas', source = CONVOLUCAO, callback = lambda S, D, U: change_wave_form( None, None, dpg.get_value(LAST_WAVE_CLICKED))  )
            with dpg.tooltip ( parent = 24_3_1 ):
                dpg.add_text ( 'Cuidado com os valores de amplitude passados como parametro, para \nnão danificar o atuador com offsets extremos ( OFFSET > 120º)')
            
            with dpg.table( header_row = False ):
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.table_cell( ):    
                        dpg.add_button ( tag = 24_3_211, label = 'Triangular', height = 50, width = -1, user_data = 'tri', callback = change_wave_form )
                    with dpg.table_cell( ):
                        dpg.add_button ( tag = 24_3_212, label = 'Senoidal'  , height = 50, width = -1, user_data = 'sen', callback = change_wave_form)
                    with dpg.table_cell( ):
                        dpg.add_button ( tag = 24_3_213, label = 'Degrau'    , height = 50, width = -1, user_data = 'sqr', callback = change_wave_form)
                    dpg.bind_item_theme( 24_3_212, button_green   )
            
            with dpg.table( header_row = False ): 
                dpg.add_table_column() 
                dpg.add_table_column()
                with dpg.table_row( show = False, tag = 24_3_3 ): 
                    with dpg.table_cell():
                        dpg.add_text( tag = 24_3_3110, default_value ='Amplitude Triangular' )
                        dpg.add_input_float( tag = 24_3_311, width = -1, source = AMPLITUDE_TRI, max_value = 180, min_value = 0, step = 0.1 )  
                    with dpg.table_cell():
                        dpg.add_text( tag = 24_3_3110, default_value ='Frequência Triangular' )
                        dpg.add_input_float( tag = 24_3_312, width = -1, source = FREQUENCIA_TRI, max_value = 10, min_value = 0, step = 0.1 )  
                
                with dpg.table_row( show = True, tag = 24_3_4 ): 
                    with dpg.table_cell():
                        dpg.add_text( tag = 24_3_4110, default_value = 'Amplitude Senoidal' )
                        dpg.add_input_float( tag = 24_3_411, width = -1, source = AMPLITUDE_SEN, max_value = 180, min_value = 0, step = 0.1 )  
                    with dpg.table_cell():
                        dpg.add_text( tag = 24_3_4110, default_value = 'Frequência Senoidal' )
                        dpg.add_input_float( tag = 24_3_412, width = -1, source = FREQUENCIA_SEN, max_value = 10, min_value = 0, step = 0.1 )  
                
                with dpg.table_row( show = False, tag = 24_3_5 ): 
                    with dpg.table_cell():
                        dpg.add_text( tag = 24_3_5110, default_value ='Amplitude Degrau' )
                        dpg.add_input_float( tag = 24_3_511, width = -1, source = AMPLITUDE_SQR, max_value = 180, min_value = 0, step = 0.1 )  
                    with dpg.table_cell():
                        dpg.add_text( tag = 24_3_5110, default_value ='Frequência Degrau' )
                        dpg.add_input_float( tag = 24_3_512, width = -1, source = FREQUENCIA_SQR, max_value = 10, min_value = 0, step = 0.1 )  
                
        dpg.add_spacer( width = 3 )
        dpg.add_text( "Configurações de plotagem" )
        with dpg.child_window( tag = 24_4, autosize_x = True, height = 75 ):
            with dpg.table( header_row = False ): 
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.table_cell():
                        dpg.add_text  ( tag = 24_4_11, default_value = 'Periodo de plotagem' )
                        dpg.add_input_float( tag = 24_4_21, width = -1, source = PERIODOS_PLOT, callback = change_plot_period ) 

        dpg.add_spacer( width = 3 )
        dpg.add_text("Configurações de backup dos dados")
        with dpg.child_window( tag = 24_5, autosize_x = True, height = 75 ):
            with dpg.table( header_row = False ): 
                dpg.add_table_column() 
                dpg.add_table_column()
                with dpg.table_row( tag = 24_5_1 ): 
                    with dpg.table_cell():
                        dpg.add_text  ( tag = 24_5_11, default_value = 'Número de periodos' )
                        dpg.add_input_float( tag = 24_5_21, width = -1, source = SAVE_NUM_T )  
                    with dpg.table_cell():
                        dpg.add_text  ( tag = 24_5_12, default_value = 'Iniciar gravação dos dados' )
                        dpg.add_button( tag = 24_5_22, label = 'Salvar', width = -1, callback = save_data_measure ) 
            dpg.add_input_float( tag = 24_5_3, width = -1, readonly = True, source = SAVED_T, show = False  )

        dpg.add_spacer( width = 3 )
        dpg.add_text("Informações")
        with dpg.child_window( tag = 24_6, autosize_x = True, height = 150 ):
            dpg.add_text( tag = 24_6_01, default_value = "P para o girar dos motores")            
            dpg.add_text( tag = 24_6_02, default_value = "W e S aumentam e diminuem a velocidade angular")
            dpg.add_text( tag = 24_6_03, default_value = "I e U aumentam e diminuem o angulo do motor 1")
            dpg.add_text( tag = 24_6_04, default_value = "J e K aumentam e diminuem o angulo do motor 2")   
            dpg.add_text( tag = 24_6_05, default_value = "MAS AINDA NÃO FOI IMPLEMENTADO, ESPERA AI")            
    
    dpg.bind_item_theme( 21_2 , plot_blue_line  ) 
    dpg.bind_item_theme( 22_2 , plot_green_line ) 
    dpg.bind_item_theme( 23_21, plot_blue_line  ) 
    dpg.bind_item_theme( 23_22, plot_green_line ) 
    dpg.bind_item_theme( 23_23, plot_red_line   ) 
    dpg.bind_item_theme( 23_24, plot_yellow_line   ) 
    
