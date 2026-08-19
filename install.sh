#!/bin/bash

# Switch-Scot Installer ⚡
# Auto-detects Linux distribution or Termux and installs required tools.

echo "====================================================="
echo " ⚡ Switch-Scot Automated Dependency Installer [AR/EN]"
echo " ⚡ سكربت التثبيت التلقائي لمحرك Switch-Scot"
echo "====================================================="

if [ -n "$PREFIX" ] && [ -d "$PREFIX" ] && echo "$PREFIX" | grep -q "com.termux"; then
    echo "[+] Detected Environment: Android (Termux) / تم اكتشاف بيئة تيرمكس"
    pkg update -y
    pkg install -y root-repo
    pkg install -y tsu hping3 macchanger iproute2 python
    BIN_DIR="$PREFIX/bin"
elif command -v pacman >/dev/null 2>&1; then
    echo "[+] Detected Environment: Arch Linux / تم اكتشاف آرش لينكس"
    sudo pacman -Sy --noconfirm hping macchanger iproute2 python
    BIN_DIR="/usr/local/bin"
elif command -v apt-get >/dev/null 2>&1; then
    echo "[+] Detected Environment: Debian / Ubuntu / Kali Linux / تم اكتشاف كالي/دبيان"
    sudo apt-get update -y
    sudo apt-get install -y hping3 macchanger iproute2 python3
    BIN_DIR="/usr/local/bin"
elif command -v dnf >/dev/null 2>&1; then
    echo "[+] Detected Environment: Fedora / RHEL / تم اكتشاف فيدورا"
    sudo dnf install -y hping3 macchanger iproute python3
    BIN_DIR="/usr/local/bin"
else
    echo "[!] Unrecognized package manager. Please manually install: hping3, macchanger, iproute2, python3"
    BIN_DIR="/usr/local/bin"
fi

chmod +x switch_scot.py monitor.py

# Create global system command
if [ -d "$BIN_DIR" ]; then
    echo "[+] Installing 'switch-scot' to $BIN_DIR..."
    if [ -n "$PREFIX" ]; then
        ln -sf "$(pwd)/switch_scot.py" "$BIN_DIR/switch-scot"
        ln -sf "$(pwd)/monitor.py" "$BIN_DIR/switch-scot-monitor"
    else
        sudo ln -sf "$(pwd)/switch_scot.py" "$BIN_DIR/switch-scot"
        sudo ln -sf "$(pwd)/monitor.py" "$BIN_DIR/switch-scot-monitor"
    fi
fi

echo "====================================================="
echo "[+] Installation complete! / تم اكتمال التثبيت بنجاح!"
echo "[+] You can now run the tool globally using:"
echo "    sudo switch-scot"
echo "====================================================="
