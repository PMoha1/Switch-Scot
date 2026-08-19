#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Switch-Scot Monitor ⚡
Real-Time Live Network Throughput & PPS Monitor [AR/EN]
"""

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

title = "⚡ شاشة المراقبة اللحظية لتدفق الحزم والسرعة (Switch-Scot Monitor)"
header_iface = "الكرت (Interface)"
header_pps = "حزمة/ثانية (PPS)"
header_mbps = "السرعة (Mbps)"
total_label = "المجموع الإجمالي"
exit_hint = "اضغط Ctrl+C للإغلاق والخروج. (Press Ctrl+C to exit)"

print("\033[2J\033[H", end="")
print("=" * 65)
print(f" {title}")
print("=" * 65)

try:
    while True:
        s1 = get_stats()
        time.sleep(1)
        s2 = get_stats()
        
        sys.stdout.write("\033[H\033[2K")
        print("=" * 65)
        print(f" {title}")
        print("=" * 65)
        print(f"{header_iface:<24} | {header_pps:<24} | {header_mbps:<14}")
        print("-" * 65)
        
        tot_pps = 0
        tot_mbps = 0.0
        
        for iface, (p1, b1) in s1.items():
            if iface in s2:
                p2, b2 = s2[iface]
                pps = p2 - p1
                mbps = (b2 - b1) * 8 / 1_000_000
                tot_pps += pps
                tot_mbps += mbps
                if pps > 0 or iface.startswith('wl') or iface.startswith('en'):
                    print(f"{iface:<24} | {pps:>24,} | {mbps:>12.2f} Mbps")
        
        print("-" * 65)
        print(f"{total_label:<24} | {tot_pps:>24,} | {tot_mbps:>12.2f} Mbps")
        print("=" * 65)
        print(f" {exit_hint}")
        sys.stdout.flush()
except KeyboardInterrupt:
    print("\n[+] تم إيقاف شاشة المراقبة.")
