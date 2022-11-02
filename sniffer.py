#!/usr/bin/python

import socket
import struct
import ipaddress
import os
import socket

# https://www.uv.mx/personal/angelperez/files/2018/10/sniffers_texto.pdf

def get_mac_addr(addr):
    lst = list(addr.hex())
    return ':'.join([lst[i]+lst[i+1] for i in range(0,len(lst),2)])


def get_ipv4_addr(addr):
    return str(ipaddress.IPv4Address(addr))

def ethernet_head(raw_data):
    dest, src, prototype = struct.unpack('! 6s 6s H', raw_data[:14])
    dest_mac = get_mac_addr(dest)
    src_mac = get_mac_addr(src)
    proto = socket.htons(prototype)
    data = raw_data[14:]
    return dest_mac, src_mac, proto, data


def ipv4_head(raw_data):
    version_header_length = raw_data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
    data = raw_data[header_length:]
    return version, header_length, ttl, proto, src, target, data


def tcp_head(raw_data):
    (src_port, dest_port, sequence, ack, orf) = struct.unpack(
            '! H H L L H', raw_data[:14]) # orf = offset reserved flags
    offset = (orf >> 12) * 4
    flag_urg = (orf & 12) >> 5
    flag_ack = (orf & 16) >> 4
    flag_psh = (orf & 8) >> 3
    flag_rst = (orf & 4) >> 2
    flag_syn = (orf & 2) >> 1
    flag_fin = orf & 1
    data = raw_data[offset:]
    return src_port, dest_port, sequence, ack, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data


def main():
    #n = os.fork()

    if 1: #n > 0:
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        while True:
            raw_data, addr = s.recvfrom(65535)
            eth = ethernet_head(raw_data)
            print('\nEthernet Frame:')
            print(f'Destination: {eth[0]}, Source: {eth[1]}, Protocol: {eth[2]}')
    
            if eth[2] == 8: # if this is an ipv4 packet
                ipv4 = ipv4_head(eth[3])
                print('\t - IPv4 Packet:')
                print(f'\t\t - Version: {ipv4[0]}, Header Length: {ipv4[1]}, TTL: {ipv4[2]}')
                print(f'\t\t - Protocol: {ipv4[3]}, Source: {get_ipv4_addr(ipv4[4])}, Target: {get_ipv4_addr(ipv4[5])}')
    
                if ipv4[3] == 6:
                    tcp = tcp_head(ipv4[6])
                    print('\t - TCP Segment:')
                    print(f'\t\t - Source Port: {tcp[0]}, Destination Port: {tcp[1]}')
                    print(f'\t\t - Sequence: {tcp[2]}, Acknowledgment: {tcp[3]},')
                    print(f'\t\t - Flags:')
                    print(f'\t\t\t URG: {tcp[4]}, ACK: {tcp[5]}, PSH: {tcp[6]}')
                    print(f'\t\t\t RST: {tcp[7]}, SYN: {tcp[8]}, FIN: {tcp[9]}')
                    if len(tcp[10]) > 0:
                        if tcp[0] == 8000 or tcp[1] == 8000:
                            print('\t\t - HTTP Data:')
                            print(tcp[10])
                    s = socket.socket(socket.AF_UNIX, socket.SOCK_RAW)
                    s.sendto(raw_data, "/tmp/testsocket")

    else:
        print('you are the parent')
main()
