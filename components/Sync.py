import PyDynamixel_v2.PyDynamixel_v2 as pd 
import SerialReader.Serial as sr
from time import sleep
from math import pi
import serial 

BAUDRATE = 115200

while True:
    
    comports = sr.serialPorts()
    for i, com in enumerate(comports):
        print(i, com, end='\t')

    ind = input("\nEscolha a porta Serial onde esta conectado o Conversor RS845: ")
    
    try:
        ind = int(ind)
        comport = serial.Serial(comports[ind], baudrate= BAUDRATE)
        comport.close()
        comport = comports[ind]
        break
    except:
        comport = 0

serial = pd.DxlComm(port=comport, baudrate=BAUDRATE)

ids = [1, 28]
# Define os ids dos motores usados
while True:
    resp = input("Dar entrada aos ids? [S] [N] ")
    if resp.upper() == 'S':
        ids = list( map( int, input("De entrada aos ids: ").split() ) )
        if type(ids) == list:
            break 
    elif resp.upper() == 'N':
        break
    else: 
        print("Usar s ou S para Sim e n ou N para Não!")

joint28 = pd.Joint(ids[0])
joint01 = pd.Joint(ids[1])

# Attach das juntas
serial.attach_joints([joint28, joint01])
serial.enable_torques()

count = 0
offset = 1 

while True:
    # Em graus com offset de 10º
    for i in range(1, 360, 10):
        serial.send_angles({ids[0] : i-offset, ids[1] : i})
        sleep(0.1)
        angles = serial.get_angles()

        print(ids, angles)
            
    count = count + 1 
    if count > 5:
        break 