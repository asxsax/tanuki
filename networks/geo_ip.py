#!/usr/bin/python3

# > Plot IPs on geo-map for observation

import requests
import cartopy.crs as crs
import cartopy.features as cfeature
import matplotlib.pyplot as plt
from scapy.all import *

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

def plot_geos(geos):
    plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.Robinsion())

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.add_feature(cfeature.LAND, facecolor='lightgreen')
    ax.add_feature(cfeature.LAKES, facecolor='lightblue')
    ax.add_feature(cfeature.RIVERS)

    for ip, geo in geos.items():
        if geo and 'loc' in geo:
            lat, lon = map(float, geo['loc'].split(','))
            plt.plot(lon, lat, marker='o', color='red', 
                     markersize=5, transform=ccrs.Geodetic())
            plt.text(lon, lat, ip, transform=ccrs.Geodetic())

packets = AsyncSniffer(count=500, prn=collect_ip, filter="ip")
packets.start()
packets.join()
pcap = packets.results

geos = {ip: geo_location(ip) for ip in unique_ip}

plt.title("IP Geolocation")
plt.show()
