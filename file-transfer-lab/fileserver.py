#! /usr/bin/env python3

import socket

from framedecho import framedSock as fs
from lib import params

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50000),
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
    sock, addr = lsock.accept()
    print("connection rec'd from", addr)

    # the first thing sent should be the filename
    # if everything is ok the file will come after
    filename = fs.framedReceive(sock, debug).decode('utf-8')
    print(f"filename:{filename}")

    # now just write file
    writer = open(filename + '-SERVER', 'w')
    writer.write(fs.framedReceive(sock, debug).decode('utf-8'))


if __name__ == '__main__':
    main()
