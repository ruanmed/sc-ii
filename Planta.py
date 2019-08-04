# -*- coding: utf-8 -*-
"""

"""
#Import Libraries:
import serial 
import struct
import matplotlib.pyplot as plt
import math

#arduinoSerial = serial.Serial('/dev/ttyACM0', 9600)
arduinoSerial = serial.Serial('COM5', 250000)

Yseries = []
ECseries = []
Tseries = []
k = 0
samplingTime = 0.019455
Y = [0.0, 0.0, 0.0, 0.0]
Ec = [0.0, 0.0, 0.0, 0.0]
Er = 0
#ser.write(b'5') #Prefixo b necessario se estiver utilizando Python 3.X

while k*samplingTime<10:
	while arduinoSerial.in_waiting == 0:
		pass # Enquanto não tiver resposta disponível não faz nada

	# Leitura do valor enviado pelo controlador
	Ec[3] = Ec[2]
	Ec[2] = Ec[1]
	Ec[1] = Ec[0]
	Ec[0] = float(arduinoSerial.readline())

	# Calcula o valor da planta
	Y[3] = Y[2]
	Y[2] = Y[1]
	Y[1] = Y[0]
	#Y[0]= Ec[0] * 5.386e-06  + Ec[1]*1.616e-05 + Ec[2]* 1.616e-05 + Ec[3]*5.386e-06 + Y[1]* 2.469 - Y[2]*2.006 + Y[3]*0.5364
	# Y[0] = 7.926e-07*Ec[0] + 2.378e-06*Ec[1] + 2.378e-06*Ec[2] + 7.926e-07*Ec[3] + 2.712*Y[1] -2.444*Y[2] +0.732*Y[3]
	Y[0] = 0.0000007926*Ec[0] + 0.000002378*Ec[1] + 0.000002378*Ec[2] + 0.0000007926*Ec[3] + 2.712*Y[1] -2.444*Y[2] +0.732*Y[3]
	Yseries.append(Y[0])
	ECseries.append(Ec[0])
	Tseries.append(k*samplingTime)
	k = k+1
	# Retorna o valor para o controlador
	#data = arduinoSerial.write(struct.pack('f', Y[0]))
	Er = 100- Y[0] #Degrau unitario 
	#Er = k*samplingTime - Y[0] #Rampa unitaria
	#Er = k*samplingTime+0.25 - Y[0] #Rampa unitaria superimposta de degrau compensador de erro de velocidade
	#Er = math.cos(4*k*samplingTime) - Y[0] #Cosseno(2*w) unitário
	arduinoSerial.write(str(str(float(Er))+'\n').encode())
	#print(Ec[0],Y[0]) # para fins de debug

plt.figure(1)
plt.plot(Tseries,Yseries)
plt.title('system response')
plt.ylabel('Intensity')
plt.xlabel('time - s')
plt.grid(True)

plt.figure(2)
plt.plot(Tseries,ECseries)
plt.title('controller effort')
plt.ylabel('Intensity')
plt.xlabel('time - s')
plt.grid(True)

plt.show()