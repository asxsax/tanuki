#!/usr/bin/python3

# > Plot IPs on geo-map for observation

import json
import requests
import matplotlib.pyplot as plt
from scapy.all import *
from shapely.geometry import Point
import geopandas as gpd

HEX_MAX_WIDTH = 40
STR_MAX_WIDTH = 20

unique_ip = set()

def collect_ip(packet):
    ip_src = packet[IP].src
    ip_dst = packet[IP].dst
    unique_ip.update([ip_src, ip_dst])

def geo_location(ip):
    response = requests.get(f"http://ipinfo.io/{ip}/json")
    if response.status_code == 200:
        return response.json()
    else:
        return None

packets = AsyncSniffer(count=1000, prn=collect_ip, filter="ip")
packets.start()
packets.join()
pcap = packets.results

geos = {ip: geo_location(ip) for ip in unique_ip}

geo_locations={}
for ip, data in geos.items():
    if 'loc' in data:
        geo_locations[ip] = data['loc']
print (f"Longs&Lats: {geo_locations}")

points = [Point(float(loc.split(',')[1]), float(loc.split(',')[0])) for loc in geo_locations.values()]

df = gpd.GeoDataFrame(geometry=points)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

fig, ax = plt.subplots(figsize=(10, 7))
base = world.plot(ax=ax, color='lightblue', edgecolor='gray')
df.plot(ax=base, marker='x', color='red', markersize=25)

plt.axis('off')
plt.show()
