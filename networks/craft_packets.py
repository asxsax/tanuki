#!/usr/bin/python3

# Work in Progress

# TODO: Craft packets
#       Either > Simple DoS recon tool
#       Or     > Phrack implementation

from scapy.all import *

# Packet structure
ip      = IP(dst="192.168.40.239")
type    = ICMP()
payload = Raw(load="Hello world!")

# Craft packet
packet = ip / type / payload

reply = sr1(packet)
print(reply.show())