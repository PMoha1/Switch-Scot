#!/usr/bin/env python3
import time
import os
import sys

def get_stats():
    res = {}
    ifaces = [f for f in os.listdir('/sys/class/net') if f != 'lo']
    for iface in ifaces:
        try:
            with open(f'/sys/class/net/{iface}/statistics/tx_packets') as f:
                tx_p = int(f.read().strip())
            with open(f'/sys/class/net/{iface}/statistics/tx_bytes') as f:
                tx_b = int(f.read().strip())
            res[iface] = (tx_p, tx_b)
        except Exception:
            pass
    return res

print("\033[2J\033[H", end="")
print("=" * 60)
print(" ⚡ LIVE NETWORK THROUGHPUT MONITOR (PPS & SPEED)")
print("=" * 60)

try:
    while True:
        s1 = get_stats()
        time.sleep(1)
        s2 = get_stats()
        
        sys.stdout.write("\033[H\033[2K")
        print("=" * 60)
        print(" ⚡ LIVE NETWORK THROUGHPUT MONITOR (PPS & SPEED)")
        print("=" * 60)
        print(f"{'Interface':<16} | {'Packets/sec (PPS)':<18} | {'Speed (Mbps)':<12}")
        print("-" * 60)
        
        tot_pps = 0
        tot_mbps = 0.0
        
        for iface, (p1, b1) in s1.items():
            if iface in s2:
                p2, b2 = s2[iface]
                pps = p2 - p1
                mbps = (b2 - b1) * 8 / 1_000_000
                tot_pps += pps
                tot_mbps += mbps
                if pps > 0 or iface.startswith('wl'):
                    print(f"{iface:<16} | {pps:>18,} | {mbps:>10.2f} Mbps")
        
        print("-" * 60)
        print(f"{'TOTAL COMBINED':<16} | {tot_pps:>18,} | {tot_mbps:>10.2f} Mbps")
        print("=" * 60)
        print(" Press Ctrl+C to exit.")
        sys.stdout.flush()
except KeyboardInterrupt:
    print("\n[+] Monitor stopped.")
