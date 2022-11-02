#!/usr/bin/python

import socket
import struct
import ipaddress
import os
import socket
from packet import Packet

# https://www.uv.mx/personal/angelperez/files/2018/10/sniffers_texto.pdf

def main():
    #n = os.fork()

    if 1: #n > 0:
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        while True:
            raw_data, addr = s.recvfrom(65535)
            packet = Packet(raw_data)
            print(packet.l2_dest_mac)
    else:
        print('you are the parent')
main()
