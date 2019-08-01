# -*- coding: utf-8 -*-
"""

"""
#Import Libraries:
import serial 
import struct

arduinoSerial = serial.Serial('/dev/ttyUSB0', 9600)
Y = [0.0, 0.0, 0.0, 0.0]
Ec = [0.0, 0.0, 0.0, 0.0]
#ser.write(b'5') #Prefixo b necessario se estiver utilizando Python 3.X

while True:

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
    Y[0]= Ec[0] * 5.386e-06  + Ec[1]*1.616e-05 + Ec[2]* 1.616e-05 + Ec[3]*5.386e-06 + Y[1]* 2.469 - Y[2]*2.006 + Y[3]*0.5364
    

    # Retorna o valor para o controlador
    data = arduinoSerial.write(struct.pack('d', Y[0]))
    print(data)