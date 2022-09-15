#!/bin/bash

ip netns add ns1
ip netns add ns2

ip link add dev veth1 type veth peer name veth2
ip link set dev veth1 netns ns1
ip link set dev veth2 netns ns2

ip netns exec ns1 ip addr add 10.10.10.1/30 dev veth1
ip netns exec ns2 ip addr add 10.10.10.2/30 dev veth2

ip netns exec ns1 ip link set dev veth1 up
ip netns exec ns2 ip link set dev veth2 up

ip netns exec ns1 ip addr
ip netns exec ns2 ip addr

ip netns exec ns2 ip route add 10.10.20.0/24 via 10.10.10.1

python -c "import socket as s; sock = s.socket(s.AF_UNIX); sock.bind('/tmp/proj.sock')"
ls -l /tmp/ | grep socket

#mkfifo pipe_toserver
#mkfifo pipe_fromserver
#ls -l | grep pipe
