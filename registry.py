import dearpygui.dearpygui as dpg 
import random 
import math 

with dpg.value_registry( tag = 110_00 ) as dpg_registry: 
    # IDS DOS MOTORES 
    ID_M1         = dpg.add_int_value( tag = 110_01, default_value = 1 )
    ID_M2         = dpg.add_int_value( tag = 110_02, default_value = 2 )

    # VALORES DOS ANGULOS ( DEGREES)
    DEG_M1        = dpg.add_float_value( tag = 110_03, default_value = 100 )
    DEG_M2        = dpg.add_float_value( tag = 110_04, default_value = 100 )
    OFFSET        = dpg.add_float_value( tag = 110_05, default_value = 0   )

    AMPLITUDE_TRI  = dpg.add_float_value( tag = 110_100_11, default_value = 11 )
    FREQUENCIA_TRI = dpg.add_float_value( tag = 110_100_12, default_value = 12 ) 
    AMPLITUDE_SEN  = dpg.add_float_value( tag = 110_100_21, default_value = 21 )
    FREQUENCIA_SEN = dpg.add_float_value( tag = 110_100_22, default_value = 22 ) 
    AMPLITUDE_SQR  = dpg.add_float_value( tag = 110_100_31, default_value = 31 )
    FREQUENCIA_SQR = dpg.add_float_value( tag = 110_100_32, default_value = 32 ) 

    SAVE_NUM_T     = dpg.add_float_value( tag = 110_100_4 , default_value = 10    )
    SAVE_INIT      = dpg.add_bool_value ( tag = 110_100_5 , default_value = False )
    SAVED_T        = dpg.add_float_value( tag = 110_100_6 , default_value = 0    )

    # VALORES DE PONTOS PARA PLOTS 
    LEN_DOMINIO   = dpg.add_int_value       ( tag = 110_06, default_value = 250 )
    DOMINIO_PLOT  = dpg.add_float_vect_value( tag = 110_07, default_value = [ i for i in range(dpg.get_value(LEN_DOMINIO))]   )
    POINTS_MOTOR1 = dpg.add_float_vect_value( tag = 110_08, default_value = [math.sin(math.radians(10*i))*180 +180 for i in range(dpg.get_value(LEN_DOMINIO))]        )
    POINTS_MOTOR2 = dpg.add_float_vect_value( tag = 110_09, default_value = [ 360*math.exp((-5/360)*i) for i in range(dpg.get_value(LEN_DOMINIO))] ) 
    POINTS_OFFSET = dpg.add_float_vect_value( tag = 110_10, default_value = [ abs(dpg.get_value(POINTS_MOTOR1)[i] - dpg.get_value(POINTS_MOTOR2)[i]) for i in range(dpg.get_value(LEN_DOMINIO))] )
    POINTS_SENSOR = dpg.add_float_vect_value( tag = 110_11, default_value = [ 0 for i in range(dpg.get_value(LEN_DOMINIO))] ) 
    PERIODOS_PLOT = dpg.add_float_value     ( tag = 110_12, default_value = 10 )
    POINTS_PERIOD = dpg.add_int_value( tag = 110_13, default_value = 1000 )
    
    CONVOLUCAO = dpg.add_bool_value( tag = 110_99_01, default_value = False )
    WAVE_TRI   = dpg.add_bool_value( tag = 110_99_02, default_value = False ) 
    WAVE_SEN   = dpg.add_bool_value( tag = 110_99_03, default_value = True ) 
    WAVE_SQR   = dpg.add_bool_value( tag = 110_99_04, default_value = False )

    LAST_WAVE_CLICKED = dpg.add_string_value( tag = 110_99_05, default_value = 'sen' )

    # PORTAS SERIAIS DOS DISPOSITIVOS 
    COMP_ARDUINO = dpg.add_string_value( default_value = 'COM1', tag = 110_12 ) 
    COMP_MOTORS  = dpg.add_string_value( default_value = 'COM1', tag = 110_13 )

    CONNECTION_WINDOW =  dpg.add_bool_value( default_value = False, tag = 110_14 )
    STATE_MOTORS = 0

