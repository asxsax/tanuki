#!/usr/bin/python3

# Simple packet analyzer.

# TODO: Packet Analyzer
#       > Capture and dump packets real-time
#       > Implement filters [ports, IP, Content]

import textwrap
from scapy.all import *

HEX_MAX_WIDTH = 40
STR_MAX_WIDTH = 20

def callback_function(packet):
    if Raw in packet and packet[Raw].load:
        src = packet[Ether].src
        dst = packet[Ether].dst
        print(f"\n{src} --> {dst}\n")
        print(textwrap.fill(packet[Raw].load.decode('iso-8859-1'), STR_MAX_WIDTH), "\n")
        print(textwrap.fill(packet[Raw].load.hex(), HEX_MAX_WIDTH), "\n")

inc_packets = AsyncSniffer(count=5, prn=callback_function)
inc_packets.start()
inc_packets.join()

pcap = inc_packets.results
