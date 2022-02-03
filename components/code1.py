import PyDynamixel_v2.PyDynamixel_v2 as pd 
import SerialReader.Serial as sr
from time import sleep, time 

import serial 
import pygame 
import math 

# CLASSE PARA AS CORES NO ESTILO RGB - opcional 
class Colors:
    white =  [255, 255, 255]
    lightRed = [ 0xB6, 0x49, 0x3D ]
    black =  [ 20,  20,  20]
    gray  =  [ 75,  75,  75] 
    green =  [  0, 200,   0]
    blue  =  [ 50,  50, 200]
    lightBlue = [0x45, 0x9B, 0xC1]
    red   =  [200,   0,   0]
    orange = [ 255, 127,  40]
    lightGray = [200,190,210]

cor = Colors()

# Variáveis de definição
RAIO_MOTOR1 = 100
RAIO_MOTOR2 = 100
RAIO_MOTORS = 100

POS_MOTOR1 = [125, 125]
POS_MOTOR2 = [125, 350]
POS_MOTORS = [125, 575]

angle_motor1 = 50.0
angle_motor2 = 30.0

WIDTHSURFACE = 750

# função seno que recebe angulos em graus  
f = lambda x : math.sin(math.radians(x))

pointsMotor1 = []
pointsMotor2 = []


# Variaveis para mexer 
tempo = 5
rate = 30

girar = False
meioGiro = False 

BAUDRATE = 115200

angles = 0

# função auxiliar para retangulos 
def _draw_rect(fonte, dim = [0,0], texto="", cor = [0,0,0], enquadro=[5,5]):
	text = fonte.render(texto,2,(0,0,0))
	surface = pygame.Surface((dim[0],dim[1]))
	surface.fill(cor)
	surface.blit(text, (enquadro[0],enquadro[1]))
	end = pygame.Surface((dim[0]+2,dim[1]+2), 0)
	end.fill((0,0,0))
	end.blit(surface, (1,1))
	return end

# função de desenho das estruturas básicas 
def draw_basic():
    pointsMotor1 = []
    pointsMotor2 = []
    for i in range(WIDTHSURFACE):
        pointsMotor1.append( f(angle_motor1+i)*RAIO_MOTOR1 )
        pointsMotor2.append( f(angle_motor2+i)*RAIO_MOTOR2 )
    
    # MOTOR 1
    surfaceMotors = [ [POS_MOTOR1[0], POS_MOTOR1[1]-RAIO_MOTOR1],
                      [WIDTHSURFACE , 2*RAIO_MOTOR1            ] ]
    pygame.draw.rect(screen, cor.black, [[surfaceMotors[0][0]-2, surfaceMotors[0][1]-2],[surfaceMotors[1][0]+4,surfaceMotors[1][1]+4]])
    pygame.draw.rect(screen, cor.lightGray, surfaceMotors)

    for x in range(WIDTHSURFACE):
        pygame.draw.circle(screen, cor.blue, [POS_MOTOR1[0]+x, round(POS_MOTOR1[1]+pointsMotor1[x])], 1 )

    line_motor1 = [  
        POS_MOTOR1[0]+round(RAIO_MOTOR1*math.cos(math.radians(angle_motor1))),
        POS_MOTOR1[1]+round(RAIO_MOTOR1*math.sin(math.radians(angle_motor1))) 
        ]
    pygame.draw.circle(screen, cor.black, POS_MOTOR1, RAIO_MOTOR1+2 )
    pygame.draw.circle(screen, cor.orange, POS_MOTOR1, RAIO_MOTOR1   )
    pygame.draw.line(screen, cor.black, POS_MOTOR1, line_motor1, 3 )
    
    # MOTOR 2
    surfaceMotors = [ [POS_MOTOR2[0], POS_MOTOR2[1]-RAIO_MOTOR2],
                      [WIDTHSURFACE , 2*RAIO_MOTOR2            ] ]
    pygame.draw.rect(screen, cor.black, [[surfaceMotors[0][0]-2, surfaceMotors[0][1]-2],[surfaceMotors[1][0]+4,surfaceMotors[1][1]+4]])
    pygame.draw.rect(screen, cor.lightGray, surfaceMotors)

    for x in range(WIDTHSURFACE):
        pygame.draw.circle(screen, cor.red, [POS_MOTOR2[0]+x, round(POS_MOTOR2[1]+pointsMotor2[x])], 1 )

    line_motor2 = [
        POS_MOTOR2[0]+round(RAIO_MOTOR2*math.cos(math.radians(angle_motor2))),
        POS_MOTOR2[1]+round(RAIO_MOTOR2*math.sin(math.radians(angle_motor2))) 
        ]   
    pygame.draw.circle(screen, cor.black, POS_MOTOR2, RAIO_MOTOR2+2 )
    pygame.draw.circle(screen, cor.orange, POS_MOTOR2, RAIO_MOTOR2 )
    pygame.draw.line(screen, cor.black, POS_MOTOR2, line_motor2, 3 )

    # MOTORS
    surfaceMotors = [ [POS_MOTORS[0], POS_MOTORS[1]-RAIO_MOTORS],
                      [WIDTHSURFACE , 2*RAIO_MOTORS            ] ]
    pygame.draw.rect(screen, cor.black, [[surfaceMotors[0][0]-2, surfaceMotors[0][1]-2],[surfaceMotors[1][0]+4,surfaceMotors[1][1]+4]])
    pygame.draw.rect(screen, cor.lightGray, surfaceMotors)

    for x in range(WIDTHSURFACE):
        pygame.draw.circle(screen, cor.blue, [POS_MOTORS[0]+x, round(POS_MOTORS[1]+pointsMotor1[x])], 1 )
        pygame.draw.circle(screen, cor.red, [POS_MOTORS[0]+x, round(POS_MOTORS[1]+pointsMotor2[x])], 1 )

    line_motor1 = [
        POS_MOTORS[0]+round(RAIO_MOTORS*math.cos(math.radians(angle_motor2))),
        POS_MOTORS[1]+round(RAIO_MOTORS*math.sin(math.radians(angle_motor2))) 
        ]   
    line_motor2 = [
        POS_MOTORS[0]+round(RAIO_MOTORS*math.cos(math.radians(angle_motor1))),
        POS_MOTORS[1]+round(RAIO_MOTORS*math.sin(math.radians(angle_motor1))) 
        ]   

    pygame.draw.circle(screen, cor.black, POS_MOTORS, RAIO_MOTORS+2 )
    pygame.draw.circle(screen, cor.lightRed, POS_MOTORS, RAIO_MOTORS )
    pygame.draw.line(screen, cor.black, POS_MOTORS, line_motor1, 3 )
    pygame.draw.line(screen, cor.black, POS_MOTORS, line_motor2, 3 )

# função de escrita dos textos 
def draw_texts():
    textFont = pygame.font.SysFont(systemFont, 40)
    textSurface = pygame.Surface([400, 650])
    textSurface.fill(cor.black)
    screen.blit(textSurface, (screen_W-450,25) )
    textSurface = pygame.Surface([400-4, 650-4])
    textSurface.fill(cor.lightGray)

    idMotor1 = _draw_rect(textFont, [300,50], "ID motor1:   " + str(ids[0]), cor.lightGray)
    idMotor2 = _draw_rect(textFont, [300,50], "ID motor2:   " + str(ids[1]), cor.lightGray)
    
    textSurface.blit(idMotor1, [50,25])
    textSurface.blit(idMotor2, [50,100])  

    textMotor1 = _draw_rect(textFont, [300, 40], "Angulo do motor 1", cor.lightGray)
    AnguloMotor1 = _draw_rect(textFont, [300,40], str(int(angle_motor1)), cor.lightGray, [125,10])

    textMotor2 = _draw_rect(textFont, [300, 40], "Angulo do motor 2", cor.lightGray)
    AnguloMotor2 = _draw_rect(textFont, [300,40], str(int(angle_motor2)), cor.lightGray, [125,10])

    textOffset = _draw_rect(textFont, [300, 40], "Offset", cor.lightGray, [100,5])
    offset     = _draw_rect(textFont, [300,40], str(offsetValue), cor.lightGray, [125,10])

    textSurface.blit( textMotor1,   [50,210])
    textSurface.blit( AnguloMotor1, [50,250] )

    textSurface.blit( textMotor2,   [50,310])
    textSurface.blit( AnguloMotor2, [50,350])

    textSurface.blit( textOffset,   [50,410])
    textSurface.blit( offset,       [50,450])

    textFont15 = pygame.font.SysFont(systemFont, 15)
    instructions0 = _draw_rect(textFont15, [400, 30], "P para o girar dos motores", cor.lightGray)
    instructions1 = _draw_rect(textFont15, [400, 30], "W e S aumentam e diminuem a velocidade angular", cor.lightGray)
    instructions2 = _draw_rect(textFont15, [400, 30], "I e U aumentam e diminuem o angulo do motor 1", cor.lightGray)
    instructions3 = _draw_rect(textFont15, [400, 30], "J e K aumentam e diminuem o angulo do motor 2", cor.lightGray)

    textSurface.blit( instructions0,   [-2,530])
    textSurface.blit( instructions1,   [-2,560])
    textSurface.blit( instructions2,   [-2,590])
    textSurface.blit( instructions3,   [-2,620])

    screen.blit(textSurface, (screen_W-448,27) )
    

# definição das portas seriais conectadas ao RS845
while True:    
    print('Detectando portas Seriais....\n')
    comports = sr.serialPorts()
    for i, com in enumerate(comports):
        print(i, com, end='\t')
    
    if comports != []:
        ind = input("\nEscolha a porta Serial onde esta conectado o Conversor RS845: ")
    else: 
        print("Nenhuma porta serial detectada ! \nPressione enter para atualizar")
        input()

    try:
        ind = int(ind)
        comport = serial.Serial(comports[ind], baudrate= BAUDRATE)
        comport.close()
        comport = comports[ind]
        break
    except:
        print("Comport inválida, tente outra!")
        comport = 0

serial = pd.DxlComm(port=comport, baudrate=BAUDRATE)

# Definição dos IDS
ids = [1, 28]

# Define os ids dos motores usados
while True:
    print("Ids dos dynamixels cadastrados %s \n" %ids)
    resp = input("Dar entrada a ids diferentes? [S] [N] ")
    if resp.upper() == 'S':
        ids = list( map( int, input("De entrada aos 2 ids do atuador: ").split() ) )
        if type(ids) == list:
            break 
    elif resp.upper() == 'N':
        break
    else: 
        print("Usar s ou S para Sim e n ou N para Não!")

# Criação das juntas 
joint28 = pd.Joint(ids[0])
joint01 = pd.Joint(ids[1])

# Attach das juntas
serial.attach_joints([joint28, joint01])
serial.enable_torques()

# definição dos Offsets 
offsetValue = 0.0

# inicio do pygame 
pygame.init()

pygame.font.init()
systemFont = pygame.font.get_default_font()

screenVideo = pygame.display.Info()
screen_W = screenVideo.current_w
screen_H = screenVideo.current_h

screen = pygame.display.set_mode([screen_W, screen_H])

pygame.display.set_caption("Teste NSEA - Taura")
# Escolher um icone para por aqui 
#pygame.display.set_icon()

# Clock 
clk = pygame.time.Clock()

timeRate   = time()

while True: 

    screen.fill(cor.gray)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            
            # USAR AS TECLAS AQUI
            if event.key == pygame.K_w:
                tempo = tempo + 0.50
            if event.key == pygame.K_s:
                tempo = tempo - 0.50  if tempo - 0.5 > 0 else 0.0

            if event.key == pygame.K_p:
                girar = True if girar is False else False 
            if event.key == pygame.K_i:
                angle_motor1 = angle_motor1 + 1
            if event.key == pygame.K_u:
                angle_motor1 = angle_motor1 - 1
            if event.key == pygame.K_k:
                angle_motor2 = angle_motor2 + 1
            if event.key == pygame.K_j:
                angle_motor2 = angle_motor2 - 1
        
        if event.type == pygame.QUIT:
            pygame.quit()
        
        if pygame.mouse.get_pressed()[0]:
            coords = pygame.mouse.get_pos()

    draw_basic()
    draw_texts()

    if girar:
        attAng = 360 / (tempo*rate) if tempo > 0 else 0 
        if time() - timeRate > 1/60:
            timeRate = time()
            angle_motor1 = angle_motor1 + attAng if angle_motor1 + attAng < 360.0 else 0.0 
            angle_motor2 = angle_motor2 + attAng if angle_motor2 + attAng < 360.0 else 0.0

    # definição dos Offsets 
    offsetValue = round( abs( angle_motor2 - angle_motor1 ) )
    offsetValue = offsetValue if offsetValue < 180.0 else 360.0 - offsetValue

    serial.send_angles({ids[0] : angle_motor1, ids[1] : angle_motor2})
    angles = serial.get_angles()

    pygame.display.update()

    # Display update rate (Hz)
    clk.tick(rate)