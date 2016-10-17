#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    clients = {}
    def handle(self):
        self.wfile.write(b" ")
        for line in self.rfile:
            if line.decode('utf-8')[0:8] == 'REGISTER':
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                self.clients[line.decode('utf-8')[line.decode('utf-8').find(':')+1:line.decode('utf-8').rfind(' ')]] = self.client_address
            print("El cliente", self.client_address, "nos manda", line.decode('utf-8'))
        print(self.clients)

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', int(sys.argv[1])), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\nFinalizado servidor")
