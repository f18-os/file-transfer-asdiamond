#! /usr/bin/env python3

import socket
import os
import sys

from framedecho import framedSock as fs
from lib import params

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)


def main():
    paramMap = params.parseParams(switchesVarDefaults)
    debug, listenPort = paramMap['debug'], paramMap['listenPort']
    if paramMap['usage']:
        params.usage()

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # listener socket
    bindAddr = ("127.0.0.1", listenPort)
    lsock.bind(bindAddr)
    lsock.listen(5)
    print("listening on:", bindAddr)
    while True:
        sock, addr = lsock.accept()

        if not os.fork():
            print(f'child handling connection from {addr}')
            while True:
                # the first thing sent should be the filename
                filename = fs.framedReceive(sock, debug).decode('utf-8')
                print(f"filename:{filename}")
                # next thing is put or get
                action = fs.framedReceive(sock, debug).decode('utf-8')

                if action == 'put':  # now just write file
                    writer = open(filename + '-SERVER', 'w')
                    writer.write(fs.framedReceive(sock, debug).decode('utf-8'))
                    sys.exit(0)  # everything is fine
                elif action == 'get':  # give them the file
                    file = open(filename).read()
                    fs.framedSend(sock, file.encode('utf-8'))
                    sys.exit(0)


if __name__ == '__main__':
    main()
