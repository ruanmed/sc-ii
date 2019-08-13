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
parser.add_argument('--graph', default='stem', help='kind of graph to show, overposition, stem or lines.')

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

Yseries1 = []
ECseries1 = []
Tseries1 = []
k1 = 0
Y1 = [0.0, 0.0, 0.0, 0.0]
Ec1 = [0.0, 0.0, 0.0, 0.0]
Er1 = 0

#ser.write(b'5') #Prefixo b necessario se estiver utilizando Python 3.X
def plot_graph(graph = 'stem'):
	fig = plt.figure(1)
	# plt.title("Response")
	if args.graph == 'overposition':
		ax1 = fig.subplots()

		color = 'tab:red'
		ax1.set_xlabel('Time (s)')
		ax1.set_ylabel('Intensity', color=color)
		line1 = ax1.plot(Tseries, Yseries, label='System response, k=1000', color=color)
		ax1.tick_params(axis='y', labelcolor=color)

		ax2 = ax1.twinx() 

		color = 'tab:blue'
		ax2.set_xlabel('Time (s)')
		ax2.set_ylabel('Intensity', color=color)
		line2 = ax2.plot(Tseries, ECseries, label='Controller effort, k=1000', color=color)
		ax2.tick_params(axis='y', labelcolor=color)

		plt.title('System response and Controller effort')
		plt.grid(True)

		# Adicionando os rótulos, legenda das linhas
		lines = line1+line2
		labels = [l.get_label() for l in lines]
		ax1.legend(lines, labels, loc='upper center')
		
	else:
		plt.subplot(121)
		if args.graph == 'stem':
			plt.stem(Tseries,Yseries,label='k=1000', linefmt='C0--', markerfmt='C0.')
			plt.stem(Tseries1,Yseries1,label='k=2459.85', linefmt='C1--', markerfmt='C1.')
		else:
			plt.plot(Tseries,Yseries,label='k=1000')
			plt.plot(Tseries1,Yseries1,label='k=2459.85')
		plt.legend(loc='best')
		plt.title('System response')
		plt.ylabel('Intensity')
		plt.xlabel('Time (s)')
		plt.grid(True)

		plt.subplot(122)
		if args.graph == 'stem':
			plt.stem(Tseries,ECseries,label='k=1000', linefmt='C0--', markerfmt='C0.')
			plt.stem(Tseries1,ECseries1,label='k=2459.85', linefmt='C1--', markerfmt='C1.')
		else:
			plt.plot(Tseries,ECseries,label='k=1000')
			plt.plot(Tseries1,ECseries1,label='k=2459.85')
		plt.legend(loc='best')
		plt.title('Controller effort')
		plt.ylabel('Intensity')
		plt.xlabel('Time (s)')
		plt.grid(True)

try: 
	while k*samplingTime<2:
		while arduinoSerial.in_waiting == 0:
			pass # Enquanto não tiver resposta disponível não faz nada

		# Leitura do valor enviado pelo controlador
		input_read = str(arduinoSerial.readline().decode()).split(' ')
		print(input_read)
		Ec[3] = Ec[2]
		Ec[2] = Ec[1]
		Ec[1] = Ec[0]
		Ec[0] = float(input_read[0])

		Ec1[3] = Ec1[2]
		Ec1[2] = Ec1[1]
		Ec1[1] = Ec1[0]
		Ec1[0] = float(input_read[1])

		# Calcula o valor da planta
		Y[3] = Y[2]
		Y[2] = Y[1]
		Y[1] = Y[0]
		Y1[3] = Y1[2]
		Y1[2] = Y1[1]
		Y1[1] = Y1[0]

		#Y[0]= Ec[0] * 5.386e-06  + Ec[1]*1.616e-05 + Ec[2]* 1.616e-05 + Ec[3]*5.386e-06 + Y[1]* 2.469 - Y[2]*2.006 + Y[3]*0.5364
		# Y[0] = 7.926e-07*Ec[0] + 2.378e-06*Ec[1] + 2.378e-06*Ec[2] + 7.926e-07*Ec[3] + 2.712*Y[1] -2.444*Y[2] +0.732*Y[3]		
		Y[0] = 0.0000007926*Ec[0] + 0.000002378*Ec[1] + 0.000002378*Ec[2] + 0.0000007926*Ec[3] + 2.712*Y[1] -2.444*Y[2] +0.732*Y[3]
		Y1[0] = 0.0000007926*Ec1[0] + 0.000002378*Ec1[1] + 0.000002378*Ec1[2] + 0.0000007926*Ec1[3] + 2.712*Y1[1] -2.444*Y1[2] +0.732*Y1[3]

		Yseries.append(Y[0])
		ECseries.append(Ec[0])
		Tseries.append(k*samplingTime)
		Yseries1.append(Y1[0])
		ECseries1.append(Ec1[0])
		Tseries1.append(k1*samplingTime)
		drawnow.drawnow(plot_graph)
		plt.pause(0.000001)
		k = k+1
		k1 = k1+1
		# Retorna o valor para o controlador
		#data = arduinoSerial.write(struct.pack('f', Y[0]))
		if args.input == 'step':
			Er = 100- Y[0] #Degrau unitario
			Er1 = 100- Y1[0]
		elif args.input == 'ramp':
			Er = k*samplingTime - Y[0] #Rampa unitaria
			Er1 = k1*samplingTime - Y1[0]
		elif args.input == 'ramp_offset':
			Er = k*samplingTime+0.25 - Y[0] #Rampa unitaria superimposta de degrau compensador de erro de velocidade
			Er1 = k1*samplingTime+0.25 - Y1[0]
		elif args.input == 'cossine':
			Er = math.cos(4*k*samplingTime) - Y[0] #Cosseno(2*w) unitário
			Er1 = math.cos(4*k1*samplingTime) - Y1[0]

		# Formato de saída é uma string "##.## ##.##\n"	
		output = str(str(float(Er)) + ' ' + str(float(Er1)) + '\n')
		arduinoSerial.write(output.encode())
		# print(output)
		#print(Ec[0],Y[0]) # para fins de debug

except KeyboardInterrupt:
	arduinoSerial.close()

drawnow.drawnow(plot_graph)
plt.show()