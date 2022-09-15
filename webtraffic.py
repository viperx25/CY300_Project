#!/usr/bin/python
'''
webtraffic.py

This file contains classes pertaining to web traffic generation.
'''

class NetworkTools():

    @staticmethod
    def get_addresses(net_addr: str, cidr: int):
        net_addr = ''.join([format(int(x), '08b') for x in net_addr.split('.')])
        mask = bin(int(''.join(['1' if i<cidr else '0' for i in range(0,32)]), 2))[2:]
        #print(net_addr)
        #print(mask)
        #bnet = int(net_addr, 2)
        #bmask = int(mask, 2)
        #print(format(bnet & (~bmask), '032b'))
        bad_addr = False if int(net_addr, 2) & ~int(mask, 2) == 0 else True
        if bad_addr:
            print('Bad address and/or mask!')
            return None
        num = ~int(mask, 2) & 0xFFFFFFFF
        num_addrs = 2**(32-cidr) - 2
        
        addresses = []
        for i in range(1, num_addrs+1):
            addr = list(format(int(net_addr, 2) + i, '032b'))
            addr_s = [addr[i:i+8] for i in range(0, 32, 8)]
            addresses.append('.'.join([str(int(''.join(a),2)) for a in addr_s]))

        return addresses


class TrafficEmulator():

    net_addr = '0.0.0.0'
    net_mask = 32
    net_addresses = []

    def __init__(self, net_addr: str, mask: int):
        self.net_addr = net_addr
        self.net_mask = net_mask
        self.addresses = NetworkTools.get_addresses(net_addr, mask)
        print(self.addresses)

addr = input('enter network address: ')
mask = int(input('enter subnet mask: /'))
te = TrafficEmulator(addr, mask)
