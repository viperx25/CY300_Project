# packet.py
#
# This file contains the code to process incoming packets.
#
# Peter Toth
# 14OCT2022


import struct
import socket
import ipaddress

# https://www.uv.mx/personal/angelperez/files/2018/10/sniffers_texto.pdf


class TCPSegment:

    def __init__(self, data, src_port=0, dest_port=0, sequence=0, ack=0, offset=0, furg=0, fack=0, fpsh=0, frst=0, fsyn=0, ffin=0):
        if src_port == 0:
            (src_port, dest_port, sequence, ack, orf) = struct.unpack('! H H L L H', data[:14])
            offset = (orf >> 12) * 4
            furg = (orf & 12) >> 5
            fack = (orf & 16) >> 4
            fpsh = (orf & 8) >> 3
            frst = (orf & 4) >> 2
            fsyn = (orf & 2) >> 1
            ffin = orf & 1
            data = data[offset:]
        self.data = data
        self.src_port = src_port
        self.dest_port = dest_port
        self.sequence = sequence
        self.ack = ack
        self.offset = offset
        self.furg = furg
        self.fack = fack
        self.fpsh = fpsh
        self.frst = frst
        self.fsyn = fsyn
        self.ffin = ffin

    def get_raw_data():
        pass


class Packet:

    def __init__(self, raw_data):
        decapsulated_packet = self.ethernet_head(raw_data)
        decapsulated_segment = self.ipv4_head(decapsulated_packet)
        data = self.tcp_head(decapsulated_segment)

    def get_mac_addr(self, addr):
        lst = list(addr.hex())
        return ':'.join([lst[i]+lst[i+1] for i in range(0,len(lst),2)])


    def get_ipv4_addr(self, addr):
        return str(ipaddress.IPv4Address(addr))

    def ethernet_head(self, raw_data):
        dest, src, prototype = struct.unpack('! 6s 6s H', raw_data[:14])
        self.l2_dest_mac = self.get_mac_addr(dest)
        self.l2_src_mac = self.get_mac_addr(src)
        self.l2_proto = socket.htons(prototype)
        data = raw_data[14:]
        return data


    def ipv4_head(self, raw_data):
        self.l3_version_header_length = raw_data[0]
        self.l3_version = self.l3_version_header_length >> 4
        self.l3_header_length = (self.l3_version_header_length & 15) * 4
        self.l3_ttl, self.l3_proto, self.l3_src, self.l3_target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
        data = raw_data[self.l3_header_length:]
        return data


    def tcp_head(self, raw_data):
        (src_port, dest_port, sequence, ack, orf) = struct.unpack(
                '! H H L L H', raw_data[:14]) # orf = offset reserved flags
        self.l4_tcp_offset = (orf >> 12) * 4
        self.l4_tcp_flag_urg = (orf & 12) >> 5
        self.l4_tcp_flag_ack = (orf & 16) >> 4
        self.l4_tcp_flag_psh = (orf & 8) >> 3
        self.l4_tcp_flag_rst = (orf & 4) >> 2
        self.l4_tcp_flag_syn = (orf & 2) >> 1
        self.l4_tcp_flag_fin = orf & 1
        data = raw_data[self.l4_tcp_offset:]
        return data


    def __str__(self):
    
    	s = "Ethernet Frame:"
    	s = f"{s}\nDestination: {self.l2_dest_mac}, Source: {self.l2_dest_src}, Protocol: {self.l2_proto}"
'''
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
'''
