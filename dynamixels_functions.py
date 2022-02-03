from matplotlib.pyplot import show
import components.PyDynamixel_v2.PyDynamixel_v2 as pd
from components.Serial import serialPorts 
import dearpygui.dearpygui as dpg 
import serial 
from registry import * 

def change_id( sender, data, user ): 
    global MOTOR1, MOTOR2
    try:
        # Criação das juntas 
        MOTOR1 = pd.Joint( dpg.get_value(ID_M1) ) 
        MOTOR2 = pd.Joint( dpg.get_value(ID_M2) )
    except:
        print('Por algum motivo na função change id no arquivo dynamixels_functions, deu erro na troca dos ids dos motores dynamixels')

def attach_joints( sender, data, user ): 
    global MOTOR1, MOTOR2
    global DYNA_SERIAL 
    try: 
        # Attach das juntas
        DYNA_SERIAL.attach_joints( [MOTOR1, MOTOR2])
        DYNA_SERIAL.enable_torques() 
    except: 
        print('Por algum motivo na função attach_joints no arquivo dynamixels_functions, deu erro no attach dos motores dynamixels')

def try_connect(sender, data, user ): 
    global DYNA_CONNECTED, ARDU_CONNECTED
    global DYNA_SERIAL, ARDU_SERIAL 

    if DYNA_CONNECTED == True:
        DYNA_SERIAL.release()
        print( 'tentando fechar a comport dynamixel')
    if dpg.get_value( 41_01 ) == False :
        try: 
            dpg.configure_item( 41_14_02, show = True, label = 'Tentando conectar {}'.format(dpg.get_value(41_12_05)))
            DYNA_SERIAL = pd.DxlComm   ( port = dpg.get_value(41_12_05) , baudrate = int ( dpg.get_value( 41_13_05 ) ) )
            dpg.configure_item( 41_14_02, show = True, label = 'Conectado na {}'.format(dpg.get_value(41_12_05) ) )
            DYNA_CONNECTED = True 
        except:
            dpg.configure_item( 41_14_02, show = True, label = 'Impossível conectar {}'.format(dpg.get_value(41_12_05)))
            DYNA_CONNECTED = False
    else:
        dpg.configure_item( 41_14_02, show = True, label = 'Tentando conectar {}'.format(dpg.get_value(41_12_05)))
        dpg.configure_item( 41_24_02, show = True, label = 'Aguardando {} conectar'.format(dpg.get_value(41_12_05)))
        try:
            DYNA_SERIAL = pd.DxlComm   ( port = dpg.get_value(41_12_05) , baudrate = int ( dpg.get_value( 41_13_05 ) ) )
            dpg.configure_item( 41_14_02, show = True, label = 'Conectado na {}'.format(dpg.get_value(41_12_05)))
            DYNA_CONNECTED = True 
        except:
            dpg.configure_item( 41_14_02, show = True, label = 'Impossível conectar {}'.format(dpg.get_value(41_12_05)))
            DYNA_CONNECTED = False
        try: 
            if ARDU_CONNECTED == True:  
                ARDU_SERIAL.close() 
                print('tentanto fechar a comport arduino')
            dpg.configure_item( 41_24_02, show = True, label = 'Tentando conectar {}'.format(dpg.get_value(41_22_05)))
            ARDU_SERIAL = serial.Serial( port = dpg.get_value(41_22_05) , baudrate = int ( dpg.get_value( 41_23_05 ) ) )
            dpg.configure_item( 41_24_02, show = True, label = 'Conectado na {}'.format(dpg.get_value(41_22_05)))
            ARDU_CONNECTED = True 
        except:
            dpg.configure_item( 41_24_02, show = True, label = 'Impossível conectar {}'.format(dpg.get_value(41_22_05)))
            ARDU_CONNECTED = False 

def send_motor_angles(sender, data, user ):
    global DYNA_SERIAL 
    MOTOR1.set_goal_value(dpg.get_value( DEG_M1 ))
    MOTOR2.set_goal_value(dpg.get_value( DEG_M2 ))
       
def get_motor_angles( sender, data, user ): 
    angles = serial.get_angles()

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

def atualize_comports(sender, data, user ):
    global COMPORTS_AVAILABLE  
    dpg.configure_item(41_31_01, label = 'Procurando comports')
    COMPORTS_AVAILABLE = serialPorts(20)
    dpg.configure_item( 41_12_05, items = COMPORTS_AVAILABLE )
    dpg.configure_item( 41_22_05, items = COMPORTS_AVAILABLE )
    dpg.configure_item(41_31_01, label = 'Atualizar Comports')
    if len(COMPORTS_AVAILABLE) != 0 :
        comport_list = '' 
        for i in COMPORTS_AVAILABLE: 
            comport_list += i 
            comport_list += '\n'
        dpg.configure_item(41_31_02, default_value = comport_list )
    else: 
        dpg.configure_item(41_31_02, default_value = 'No serial available' )
        
    dpg.configure_item(41_31_020, show = True, height = len(COMPORTS_AVAILABLE)*25 ) 
    h = dpg.get_item_configuration(41000)['height']
    dpg.configure_item( 41000, height = h+len(COMPORTS_AVAILABLE)*37) 
    dpg.configure_item( 41_31_020, height = len(COMPORTS_AVAILABLE)*35 )

    print(  len(COMPORTS_AVAILABLE)*25 )
    
    
