# -*- coding: utf-8 -*-
"""

"""
#Import Libraries:
import serial
import struct

arduinoSerial = serial.Serial('/dev/ttyUSB1', 9600)
Y = [0.0, 0.0]
Ec = [0.0, 0.0, 0.0]
#ser.write(b'5') #Prefixo b necessario se estiver utilizando Python 3.X

while True:

    while ser.in_waiting == 0:
        pass # Enquanto não tiver resposta disponível não faz nada

    # Leitura do valor enviado pelo controlador
    Ec[2] = Ec[1]
    Ec[1] = Ec[0]
    Ec[0] = arduinoSerial.readline()

    # Calcula o valor da planta

    Y[1] = Y[0]
    Y[0]= 0.0

    # Retorna o valor para o controlador
    data = arduinoSerial.write(struct.pack('f', Y[0]))