# Switch-Scot ⚡

> **Universal High-Performance Network Resilience & Load Testing Engine**  
> Engineered for Linux (Arch, Kali, Debian, Ubuntu, Fedora) and Android (Termux with Root).

---

## 📌 Overview

**Switch-Scot** is a lightweight, zero-dependency network stress testing framework engineered to assess network infrastructure resilience, firewall capacity, and gateway load tolerance under controlled laboratory environments.

### 🌟 Key Features
- **Zero External Python Dependencies:** 100% built on Python standard libraries.
- **Dynamic Platform Adaptation:** Automatically detects Termux (`tsu`) vs standard Linux (`sudo`).
- **Persistent Obfuscation Layer:**
  - Automated MAC address rotation via `macchanger`.
  - OS Fingerprint obfuscation via dynamic TTL randomization.
  - Device hostname spoofing.
  - ARP cache flushing.
- **Multi-Protocol Evaluation Modes:**
  - `tcp-syn`: TCP SYN Connection Load *(Default)*
  - `udp`: UDP Stateless Buffer Stress
  - `icmp`: ICMP Echo Control Plane Latency
  - `tcp-ack`: TCP ACK Stateful Filter Inspection
- **Automated Interface Discovery:** Auto-detects active network route and adapter.

---

## 🚀 Quick Start

### 1. Automated Installation
Run the automated installer script:
```bash
chmod +x install.sh
./install.sh
```

### 2. Manual Installation

#### Arch Linux:
```bash
sudo pacman -S hping macchanger iproute2 python
```

#### Debian / Kali / Ubuntu:
```bash
sudo apt update && sudo apt install -y hping3 macchanger iproute2 python3
```

#### Android (Termux with Root):
```bash
pkg install -y root-repo
pkg install -y tsu hping3 macchanger iproute2 python
```

---

## 💻 Usage

### Basic Execution (Default Target: `10.0.0.1`, Mode: `tcp-syn`, Port: `80`):
```bash
# On Linux
sudo python3 switch_scot.py

# On Termux
tsu
python3 switch_scot.py
```

### Advanced Usage Examples:

```bash
# Target custom IP and port
sudo python3 switch_scot.py -t 192.168.1.1 -p 443

# UDP Stateless Stress Test
sudo python3 switch_scot.py -t 10.0.0.1 -p 53 -m udp

# ICMP Echo Latency Assessment
sudo python3 switch_scot.py -t 10.0.0.1 -m icmp

# Bind to a specific network interface
sudo python3 switch_scot.py -i wlan0 -t 10.0.0.1
```

### CLI Options:
```text
options:
  -h, --help            Show help message and exit
  -t, --target TARGET   Target IP address (Default: 10.0.0.1)
  -p, --port PORT       Target Port (Default: 80)
  -i, --interface IFACE Network interface to bind (Default: Auto-detected)
  -m, --mode MODE       Evaluation Mode: [tcp-syn, udp, icmp, tcp-ack] (Default: tcp-syn)
```

---

## ⚠️ Disclaimer

This tool is strictly developed for educational purposes, authorized security assessments, and network resilience testing. Usage against unauthorized targets without explicit prior consent is strictly prohibited. The author assumes no liability for misuse.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
