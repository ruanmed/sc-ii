# -*- coding: utf-8 -*-
"""

"""
#Import Libraries:
import serial 
import struct
import matplotlib.pyplot as plt
import math
import drawnow

# Comand line argument parser
import argparse

# Arguments configuration
parser = argparse.ArgumentParser()
parser.add_argument('--port', default='/dev/ttyACM0', help='serial port to communicate.')
parser.add_argument('--baud', default=250000, help='baudrate in the serial port to communicate.')
parser.add_argument('--input', default='step', help='input to the control system')
parser.add_argument('--graph', default='stem', help='kind of graph to show')

args = parser.parse_args()

arduinoSerial = serial.Serial(args.port, args.baud)
# arduinoSerial = serial.Serial('COM5', 250000)

Yseries = []
ECseries = []
Tseries = []
k = 0
samplingTime = 0.019455
Y = [0.0, 0.0, 0.0, 0.0]
Ec = [0.0, 0.0, 0.0, 0.0]
Er = 0
#ser.write(b'5') #Prefixo b necessario se estiver utilizando Python 3.X
def plot_graph(graph = 'stem'):
	fig = plt.figure(1)
	plt.title("Response")
	if args.graph == 'overposition':
		ax = fig.subplots()

		line1, = ax.plot(Tseries, Yseries, label='System response')
		line2, = ax.plot(Tseries, Yseries, label='Controller effort')
		plt.title('System response and Controller effort')
		plt.ylabel('Intensity')
		plt.xlabel('Time (s)')
		plt.grid(True)
	else:
		plt.subplot(121)
		if args.graph == 'stem':
			plt.stem(Tseries,Yseries)
		else:
			plt.plot(Tseries,Yseries)
		plt.title('System response')
		plt.ylabel('Intensity')
		plt.xlabel('Time (s)')
		plt.grid(True)

		plt.subplot(122)
		if args.graph == 'stem':
			plt.stem(Tseries,ECseries)
		else:
			plt.plot(Tseries,ECseries)
		plt.title('Controller effort')
		plt.ylabel('Intensity')
		plt.xlabel('Time (s)')
		plt.grid(True)

try: 
	while k*samplingTime<2:
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
		drawnow.drawnow(plot_graph)
		plt.pause(0.000001)
		k = k+1
		# Retorna o valor para o controlador
		#data = arduinoSerial.write(struct.pack('f', Y[0]))
		if args.input == 'step':
			Er = 100- Y[0] #Degrau unitario
		elif args.input == 'ramp':
			Er = k*samplingTime - Y[0] #Rampa unitaria
		elif args.input == 'ramp_offset':
			Er = k*samplingTime+0.25 - Y[0] #Rampa unitaria superimposta de degrau compensador de erro de velocidade
		elif args.input == 'cossine':
			Er = math.cos(4*k*samplingTime) - Y[0] #Cosseno(2*w) unitário
		arduinoSerial.write(str(str(float(Er))+'\n').encode())
		#print(Ec[0],Y[0]) # para fins de debug

except KeyboardInterrupt:
	arduinoSerial.close()

plot_graph()
plt.show()