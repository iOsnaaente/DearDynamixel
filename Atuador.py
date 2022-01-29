import utils.PyDynamixel_v2.PyDynamixel_v2 as pd 
import utils.SerialReader.Serial as sr 

from serial import Serial 

class Atuador: 

    ID_motor_1 = 0  # Motor esquerda
    ID_motor_2 = 1  # Motor do imã 

    angle_motor_1 = 200.0 
    angle_motor_2 = 200.0

    offset = 0 

    JointL = 0
    JointR = 0 
    
    comport_arduino = 0 
    comport_dynamixels = 0 

    BAUDRATE = 0


    def __init__(self, ID1, ID2, BAUDRATE = 1000000, search_for_serial = True, COMArduino = "", COMRs485 = "" ):
        # Criação do atuador 
        self.BAUDRATE = BAUDRATE
        self.ID_motor_1 = ID1 
        self.ID_motor_2 = ID2 
        if search_for_serial:
            self.search_comports()
        else:
            self.comport_arduino = Serial(COMArduino, BAUDRATE)
            self.comport_dynamixels = pd.DxlComm(port=COMRs485, baudrate= self.BAUDRATE)
        
        self.JointL = pd.Joint(self.ID_motor_1)
        self.JointR = pd.Joint(self.ID_motor_2)

        self.comport_dynamixels.attach_joints([self.JointL, self.JointR])
        self.comport_dynamixels.enable_torques()

        self.offset = self.get_offset()
    

    # salva os dados obtidos 
    def save_data(self, data, dest = ''):
        if dest == '' : 
            dest = 'data.txt'
        with open(dest, 'a') as f:
            f.write(data + '\n')


    # Calcula o offset  
    def get_offset(self):       
        offset = round( abs( self.angle_motor_1 - self.angle_motor_2 ) )
        offset = offset if offset < 180.0 else 360.0 - offset
        self.offset = offset 


    def send_angles(self, angle1, angle2):
        # Enviando os angulos 
        self.comport_dynamixels.send_angles({self.ID_motor_1 : angle1, self.ID_motor_2 : angle2})
        self.angle_motor_1 = angle1
        self.angle_motor_2 = angle2 
        self.offset = self.get_offset()


    def get_real_axis(self):
        # lendo dados do sensor 
        angle = self.comport_arduino.readline().decode()
        angle = angle.split(',')
        self.axis_real = angle[0]
        self.status_sensor = angle[1]
        return self.axis_real
    

    def get_relative_axis(self):
        # Pegando os angulso dos dynamixels e do sensor
        angles = self.comport_dynamixels.get_angles()
        aux = 0 
        for i in angles.values():
            aux = aux + i 
            angles = aux/2
        self.axis_motor = angles
        return self.axis_motor
    

    def set_IDs(self, ID1 = 0 , ID2 = 0):
        if ID1 == 0 and ID2 == 0 :
            print("\nDefinição de ID manual:")
            # Define os ids dos motores usados
            while True:
                print("\nIds dos dynamixels cadastrados %s \n" %ids)
                resp = input("Dar entrada a ids diferentes? [S] [N] ")
                if resp.upper() == 'S':
                    ids = list( map( int, input("De entrada aos 2 ids do atuador: ").split() ) )
                    if type(ids) == list:
                        break 
                elif resp.upper() == 'N':
                    break
                else: 
                    print("Usar s ou S para Sim e n ou N para Não!")
        else : 
            self.ID_motor_1 = ID1 
            self.ID_motor_2 = ID2 


    def search_comports(self, devices = ['Arduino', 'RS485']):
        # definição das portas seriais conectadas ao Arduino
        for device in devices:
            while True:    
                print('Detectando portas Seriais....\n')
                comports = sr.serialPorts()
                for i, com in enumerate(comports):
                    print(i, com, end='\t')
                
                if comports != []:
                    print("\nEscolha a porta Serial onde esta conectado o %s : " %device)
                    ind = input()
                else: 
                    print("Nenhuma porta serial detectada ! \nPressione enter para atualizar")
                    input()

                try:
                    ind = int(ind)
                    comport = Serial(comports[ind], baudrate= self.BAUDRATE)
                    comport.close()
                    comport = comports[ind]
                    break
                except:
                    print("Comport inválida, tente outra!")
                    comport = 0

            if device == "Arduino":
                self.comport_arduino = Serial(comport, baudrate= self.BAUDRATE)
            
            elif device == "RS485":
                self.comport_dynamixels = pd.DxlComm(port=comport, baudrate= self.BAUDRATE)
