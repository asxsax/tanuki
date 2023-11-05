#!/usr/bin/python3

# > Simple packet sniffer.
# Dumps source, destination IPs and MACs.
# Dumps data in packet, if present.

import textwrap
from scapy.all import *

HEX_MAX_WIDTH = 40
STR_MAX_WIDTH = 20

def callback_function(packet):

    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        print(f"\n{ip_src} --> {ip_dst}")

    if Raw in packet and packet[Raw].load:
        eth_src = packet[Ether].src
        eth_dst = packet[Ether].dst
        print(f"{eth_src} --> {eth_dst}\n")
        print(textwrap.fill(packet[Raw].load.decode('iso-8859-1'),
                            STR_MAX_WIDTH), "\n")
        print(textwrap.fill(packet[Raw].load.hex(), HEX_MAX_WIDTH), "\n")

inc_packets = AsyncSniffer(count=5, prn=callback_function)
inc_packets.start()
inc_packets.join()
pcap = inc_packets.results
