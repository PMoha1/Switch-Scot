# Switch-Scot ⚡

> **Universal High-Performance Multi-Interface Network Resilience & Load Testing Engine**  
> Engineered for Linux (Arch, Kali, Debian, Ubuntu, Fedora) and Android (Termux with Root).

---

## 📌 Overview

**Switch-Scot** is a lightweight, zero-dependency network stress testing framework engineered to assess network infrastructure resilience, firewall capacity, and gateway load tolerance under controlled laboratory environments.

### 🌟 Key Features
- **Simultaneous Multi-Interface Engine:** Bind and launch parallel high-throughput traffic across multiple Wi-Fi/Ethernet cards simultaneously (`1,2` or `all`).
- **Interactive Easy-Menu (like Wifite):** Simple numbered prompts with smart auto-detection.
- **Zero External Python Dependencies:** 100% built on Python standard libraries.
- **Dynamic Platform Adaptation:** Automatically detects Termux (`tsu`) vs standard Linux (`sudo`).
- **Carrier & Route Synchronization:** Intelligently verifies link carrier state and route table readiness before launching traffic.
- **Persistent Obfuscation Layer:**
  - Automated MAC address rotation via `macchanger` across all selected adapters.
  - OS Fingerprint obfuscation via dynamic TTL randomization (64–128).
  - Device hostname spoofing.
  - ARP cache flushing.
- **Multi-Protocol Evaluation Modes:**
  - `tcp-syn`: TCP SYN Connection Load *(Default)*
  - `udp`: UDP Stateless Buffer Stress
  - `icmp`: ICMP Echo Control Plane Latency
  - `tcp-ack`: TCP ACK Stateful Filter Inspection

---

## 🚀 Quick Start

### Automated Installation
```bash
git clone https://github.com/PMoha1/Switch-Scot.git
cd Switch-Scot
./install.sh
```

---

## 💻 Usage

### 1. Interactive Mode (Easy Numbered Menu):
Simply run the command with `sudo` and follow the numbers:
```bash
sudo switch-scot
```

```text
  ___         _ _       _          ___ cot ⚡
 / __|_ __ __(_) |_ ___| |_ _____ / __| __ ___ 
 \__ \ V  V /| |  _/ __| ' \_____\__ \ _| '_ \
 |___/\_/\_/ |_|\__\___|_||_|    |___/__| .__/
                                         |_|   
 Universal Multi-Interface Network Resilience Engine v3.0

=================================================================
 🛠️  INTERACTIVE EASY SETUP MENU
=================================================================

[+] Detected Network Interfaces:
  [1] wlp4s0 (Default)
  [2] wlp9s0f4u2
  [3] enp3s0
  [A] ALL Interfaces Simultaneously (Multi-Card Turbo Mode 🚀)

[?] Select Interface(s) [e.g. 1, 1,2, or A for all - default 1]: 1,2
 -> Selected: wlp4s0, wlp9s0f4u2

[?] Enter Target IP [Default: 192.168.8.1]: 
 -> Target IP: 192.168.8.1

[?] Enter Target Port [Default: 80]: 80
 -> Target Port: 80

[+] Evaluation Modes:
  [1] TCP-SYN  - Connection Table Saturation (Default)
  [2] UDP      - Stateless Buffer Stress
  [3] ICMP     - Control Plane Latency
  [4] TCP-ACK  - Stateful Firewall Inspection

[?] Select Mode [1-4, default 1]: 1
 -> Selected Mode: TCP-SYN

[+] MAC Address Randomization Policy:
  [1] Keep Current MAC (Recommended for stable active Wi-Fi)
  [2] Randomize MAC Address (Full Hardware Spoofing)

[?] Select MAC Policy [1-2, default 1]: 1
 -> MAC Policy: Keep Active MAC (Safe Wi-Fi)

-----------------------------------------------------------------
⚡ Press [ENTER] to launch Switch-Scot on all selected interfaces...
```

### 2. Fast CLI Mode:
```bash
# Dual-Card execution simultaneously in one command
sudo switch-scot -i wlp4s0 wlp9s0f4u2 -t 192.168.8.1 -p 80 --no-mac

# Use ALL available interfaces at once
sudo switch-scot -i all -t 192.168.8.1 -p 80 --no-mac

# Real-time PPS Monitor
switch-scot-monitor
```

---

## ⚠️ Disclaimer

This tool is strictly developed for educational purposes, authorized security assessments, and network resilience testing. Usage against unauthorized targets without explicit prior consent is strictly prohibited. The author assumes no liability for misuse.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
