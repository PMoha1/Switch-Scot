# Switch-Scot ⚡

> **High-Performance Cross-Platform Network Resilience & Stress Testing Engine**  
> Designed for Linux (Arch, Kali, Debian, Ubuntu) and Android (Termux with Root).

---

## 📌 Overview

**Switch-Scot** is a lightweight, zero-dependency network stress testing framework engineered to assess network infrastructure resilience, firewall capacity, and gateway load tolerance under controlled laboratory environments.

### 🌟 Key Features
- **Cross-Platform Adaptability:** Compatible across Linux distributions and mobile environments (Termux).
- **Stealth & Identity Obfuscation:**
  - Automated MAC address rotation.
  - OS Fingerprint obfuscation via dynamic TTL randomization.
  - Device hostname spoofing.
  - ARP cache flushing.
- **Ultra-Lightweight Core:** Optimized for maximum throughput with minimal CPU/RAM overhead.
- **Automated Target Discovery:** Automatic gateway and route detection with manual override capabilities.

---

## 🚀 Quick Start

### Prerequisites
Ensure core network utilities are available on your system:
- `hping3`
- `macchanger`
- `iproute2` (ip tool)

### Installation

#### Arch Linux:
```bash
sudo pacman -S hping macchanger iproute2
```

#### Debian / Kali / Ubuntu:
```bash
sudo apt update && sudo apt install -y hping3 macchanger iproute2
```

#### Android (Termux with Root):
```bash
pkg install -y root-repo
pkg install -y tsu hping3 macchanger iproute2
```

---

## 💻 Usage

### Running on Linux:
```bash
sudo python3 scot_termux.py
```

### Running on Termux:
```bash
tsu
python3 scot_termux.py
```

---

## ⚠️ Disclaimer

This tool is strictly developed for educational purposes, authorized security assessments, and network resilience testing. Usage against unauthorized targets without explicit prior consent is strictly prohibited. The author assumes no liability for misuse.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
