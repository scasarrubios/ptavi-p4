#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente SIP que abre un socket a un servidor
"""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    line = ' '.join(sys.argv[3:5])
    expires = sys.argv[5]
    name = sys.argv[4]
    int(expires)
except:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    if sys.argv[3] == 'register':
        line = "REGISTER sip:" + name + " SIP/2.0\r\nExpires: " + expires
    my_socket.send(bytes(line, 'utf-8') + b'\r\n\r\n')
    data = my_socket.recv(1024)
    print("Enviando:", line)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
