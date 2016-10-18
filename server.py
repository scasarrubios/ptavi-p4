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
        line = self.rfile.read().decode('utf-8').split()
        if line[0] == 'REGISTER':
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            self.clients[line[1][4:]] = self.client_address[0]
        else:
            print("El cliente", self.client_address, "nos manda:", ' '.join(line))
        print(self.clients)

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', int(sys.argv[1])), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\nFinalizado servidor")
