#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver
import sys
import time


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    clients = {}
    def caducity_check(self, line):
        caduced = []
        for client in self.clients:
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
            if now >= self.clients[client][1] and line[4] != 0:
                caduced.append(client)
        for client in caduced:
            del self.clients[client]
            
    def to_json(self, fich_name):
        data = []
        fichero = open(register.json, 'w')
        for line in self.tags_list:
            for tag in line:
                data[tag] = json.dumps(line[tag])
        json.dump(data, fichero)
                
    def handle(self):
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
        else:
            print("El cliente", self.client_address, "nos manda:", ' '.join(line))
        print(self.clients)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time())))

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', int(sys.argv[1])), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\nFinalizado servidor")
