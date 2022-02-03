import math
#------------------- Import from PyDimitri ---------------------
import sys
import numpy as np
from PyDimitri import Joint, DxlComm
import time 

port = DxlComm('/dev/ttyUSB0', 1)
#----------------------- Set foot ---------------------------------
idmotors1 = [21,23]
setAngle1 = [6.22,0.83]
joints1 = [Joint(mid1) for mid1 in idmotors1]
port.attachJoints(joints1)

i = 0

for j in joints1:
	j.enableTorque()
for j in joints1:
    j.setGoalAngle(setAngle1[i])
    print(setAngle1[i])
    i += 1
port.sendGoalAngles()
#--------------------- Set joelho -------------------------------
idmotors = [13,15,17,19]
setAngle = [4.32,5.11,1.24,5.37]
joints = [Joint(mid) for mid in idmotors]

port.attachJoints(joints)
i = 0
# for j in joints:
# 	j.enableTorque()
for j in joints:
    j.setGoalAngle(setAngle[i])
    print(setAngle[i])
    i += 1
port.sendGoalAngles()
#------------------------------------------------------------------

time.sleep(3)

#------------------ Set Sensor ---------------------------------
motor_id = int(104)
j1 = Joint(motor_id)
#------------------ Define port --------------------------------
port.attachJoint(j1)



# Use first 30 or so measures to calibrate the center value
print("Calibrating...")
values = []
for i in range(300):
	values.append(j1.receiveSEA())
j1.setCenterValue(np.mean(values))
print('primeiro valor: ', j1.receiveSEA())
aux = j1.receiveSEA()