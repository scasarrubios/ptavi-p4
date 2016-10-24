#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa servidor SIP
"""

import socketserver
import sys
import time
import json


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    clients = {}
    no_file = False

    def caducity_check(self, line):
        """
        Compara la fecha de caducidad de los clientes del diccionario,
        y si han caducado los añade a la lista caduced para borrarlos
        """
        caduced = []
        for client in self.clients:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
            if now >= self.clients[client][1] and line[4] != 0:
                caduced.append(client)
        for client in caduced:
            del self.clients[client]

    def register2json(self):
        """
        Imprime el diccionario de clientes en un fichero json
        """
        if self.no_file:
            fichero = open('registered.json', 'w')
        else:
            fichero = open('registered.json', 'r+')
        json.dump(self.clients, fichero, indent='\t')

    def json2register(self):
        """
        Comprueba si hay un fichero de json y si lo hay importa los clientes,
        si no cambia el valor de no_file a True
        """
        try:
            with open('registered.json') as data_file:
                self.clients = json.load(data_file)
            print('primera:', self.clients)
        except:
            self.no_file = True
            print(self.no_file)

    def handle(self):
        self.json2register()
        self.wfile.write(b" ")
        line = self.rfile.read().decode('utf-8').split()
        self.caducity_check(line)
        if line[0] == 'REGISTER':
            data = []
            data.append(self.client_address[0])
            self.clients[line[1][4:]] = data
            if line[3] == 'Expires:' and line[4] == '0':
                del self.clients[line[1][4:]]
            elif line[3] == 'Expires:' and line[4] != '0':
                caduc_time = time.gmtime(time.time()+int(line[4]))
                data.append(time.strftime('%Y-%m-%d %H:%M:%S', caduc_time))
                self.clients[line[1][4:]] = data
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            self.register2json()
        print(self.clients)

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', int(sys.argv[1])), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\nFinalizado servidor")
