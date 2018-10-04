#! /usr/bin/env python3

# Echo client program
import re
import socket
import sys

# framed send and framed receive
from framedecho import framedSock as fs
from lib import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50000"),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)


# tries connecting, otherwise calls exit
def safe_connect(serverHost, serverPort):
    s = None
    for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            print(" error: %s" % msg)
            s = None
            continue
        try:
            print(" attempting to connect to %s" % repr(sa))
            s.connect(sa)
        except socket.error as msg:
            print(" error: %s" % msg)
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)
    return s


def main():
    # progname = "framedClient"
    paramMap = params.parseParams(switchesVarDefaults)
    server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]
    if usage:
        params.usage()

    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    s = safe_connect(serverHost, serverPort)

    print("sending hello world")
    fs.framedSend(s, b"hello world", debug)
    print("received:", fs.framedReceive(s, debug))
    print("sending hello world")
    fs.framedSend(s, b"hello world", debug)
    print("received:", fs.framedReceive(s, debug))


if __name__ == '__main__':
    main()
