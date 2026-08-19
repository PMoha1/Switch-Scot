#!/bin/bash

# Switch-Scot Installer ⚡
# Auto-detects Linux distribution or Termux and installs required tools.

echo "====================================================="
echo " ⚡ Switch-Scot Automated Dependency Installer"
echo "====================================================="

if [ -n "$PREFIX" ] && [ -d "$PREFIX" ] && echo "$PREFIX" | grep -q "com.termux"; then
    echo "[+] Detected Environment: Android (Termux)"
    pkg update -y
    pkg install -y root-repo
    pkg install -y tsu hping3 macchanger iproute2 python
elif command -v pacman >/dev/null 2>&1; then
    echo "[+] Detected Environment: Arch Linux"
    sudo pacman -Sy --noconfirm hping macchanger iproute2 python
elif command -v apt-get >/dev/null 2>&1; then
    echo "[+] Detected Environment: Debian / Ubuntu / Kali Linux"
    sudo apt-get update -y
    sudo apt-get install -y hping3 macchanger iproute2 python3
elif command -v dnf >/dev/null 2>&1; then
    echo "[+] Detected Environment: Fedora / RHEL"
    sudo dnf install -y hping3 macchanger iproute python3
else
    echo "[!] Unrecognized package manager. Please manually install: hping3, macchanger, iproute2, python3"
fi

chmod +x switch_scot.py
echo "====================================================="
echo "[+] Installation complete. Run with: sudo python3 switch_scot.py"
echo "====================================================="
