# 🕵️ Network Sniffer Pro

[![GitHub Repo](https://img.shields.io/badge/GitHub-Network--Sniffer--Pro-blue?logo=github)](https://github.com/ssneon1/Network-Sniffer-Pro)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

A professional-grade, standalone Windows application for real-time network traffic capture and security analysis — built with Python.

---

## 🚀 Key Features

- **💎 Premium Native UI** — Sleek dark-mode interface built with CustomTkinter for a native Windows feel.
- **🌐 Real-time Web Dashboard** — Monitor traffic from any browser at `http://localhost:5000` using Flask-SocketIO.
- **🔐 Credential Detection** — Automatically flags plaintext passwords, usernames, and tokens in unencrypted HTTP traffic.
- **🎯 Precision Targeting** — Filter traffic by specific domain names or IP addresses to reduce noise.
- **📊 Deep Packet Inspection** — View full protocol stacks, TCP flags, ICMP types, raw payloads, and hex data.
- **📦 One-Click Installer** — Easy deployment with an automated setup script that handles Npcap installation.

---

## 📖 Documentation

For more detailed information, please refer to the following guides:

- [🏗️ Architecture](ARCHITECTURE.md) — How the system is built and how data flows.
- [🛠️ Developer Setup](CONTRIBUTING.md#developer-setup) — Getting your environment ready for development.
- [⚠️ Troubleshooting](TROUBLESHOOTING.md) — Solutions for common issues and installation errors.
- [🔌 API Reference](API.md) — SocketIO events and internal data structures.
- [🤝 Contributing](CONTRIBUTING.md) — How to help improve Network Sniffer Pro.

---

## ⚡ Installation (For End Users)

### Prerequisites:
- **Windows OS**
- **Npcap SDK** (Included in the installer package)

### What's in the shared folder:
```
dist/
├── main.exe              ← the application
├── npcap-installer.exe   ← Npcap (required for packet capture)
└── setup.bat             ← run this to install
```

### Steps:
1. **Right-click `setup.bat`** → **Run as Administrator**
2. The script will automatically:
   - Install Npcap if not already installed
   - Copy the app to `Program Files`
   - Create a **Desktop shortcut**
3. Launch from your Desktop — done!

---

## 🛠️ Quick Start (Developers)

```powershell
# Prerequisites: Install Npcap from npcap.com

# Install dependencies
pip install -r requirements.txt

# Run directly
python main.py

# Build the EXE
.\.venv\Scripts\python.exe -m PyInstaller main.spec --noconfirm
```

---

## 🏗️ Architecture Overview

| Layer          | Technology                          |
|----------------|-------------------------------------|
| Native UI      | `CustomTkinter` + `tkinter`         |
| Web Dashboard  | `Flask` + `Flask-SocketIO`          |
| Packet Capture | `Scapy`                             |
| Deployment     | `PyInstaller` + `Inno Setup`        |

---

## ⚠️ Disclaimer

This tool is for **educational and authorized security testing only**. Unauthorized interception of network traffic is illegal. Use responsibly.
