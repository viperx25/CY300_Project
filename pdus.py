# pdus.py
#
# This file outlines Protocol
# data units to make them easier
# to work with.


import socket
import struct


class EthernetPDU:

    raw_data = None
    source_addr = 0
    source_addr_text = ''
    dest_addr = 0
    dest_addr_text = ''
    protocol_type = 0
    data = None

    def __init__(self, raw_data=None):
        if raw_data:
            self.deencapsulate(raw_data=raw_data)

    def get_mac_addr(self, addr):
        lst = list(addr.hex())
        return ':'.join([lst[i]+lst[i+1] for i in range(0,len(lst),2)])

    def deencapsulate(self, raw_data=None):
        self.raw_data = raw_data if raw_data is not None else self.raw_data
        self.dest_addr, self.source_addr, self.protocol_type = struct.unpack('! 6s 6s H', self.raw_data[:14])
        self.dest_addr_text = self.get_mac_addr(self.dest_addr)
        self.source_addr_text = self.get_mac_addr(self.source_addr)
        self.protocol_type = socket.htons(self.protocol_type)
        self.data = self.raw_data[14:]
        return self.dest_addr_text, self.source_addr_text, self.protocol_type, self.data
