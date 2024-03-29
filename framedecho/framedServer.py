#! /usr/bin/env python3

# sys.path.append("../lib")       # for params
import sys, re, socket
from lib import params
from framedecho import framedSock as fs

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50000),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

progname = "echoserver"
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

while True:
    payload = fs.framedReceive(sock, debug)
    if debug: print("rec'd: ", payload)
    if not payload:
        break
    print(f'payload:{payload}')
    payload += b"!"  # make emphatic!
    fs.framedSend(sock, payload, debug)
