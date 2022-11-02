#!/usr/bin/python

import socket, os

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove("/tmp/testsocket")
except OSError:
    pass
s.bind("/tmp/testsocket")
s.listen(1)
conn, addr = s.accept()
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.send(data)
conn.close()
