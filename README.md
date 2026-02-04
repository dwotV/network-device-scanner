# Network Device Scanner

Network Device Scanner is a **Python-based network monitoring and control tool** that discovers devices connected to a local network, identifies their vendors using MAC addresses, detects unknown devices, and allows managing trusted and blocked devices through a **web interface**.

The project is focused on **defensive security** and hands-on learning of networking fundamentals.

---

## Features

- Local network discovery
- Device scanning using **ARP (Scapy)**
- Detection of active devices with:
  - IP address
  - MAC address
  - Vendor (OUI lookup)
- **Web-based interface**
- Local **SQLite database** for persistent storage of devices
- Whitelist management:
  - Add known devices
  - Edit device descriptions
  - Remove devices from the whitelist
- Unknown device detection
- **Device blocking functionality**
- Modular architecture, easy to extend

---

## How It Works

1. The tool detects the active network interface
2. The local IP and netmask are obtained
3. The network range is calculated
4. An ARP scan is performed to discover devices
5. Each device’s vendor is identified via MAC address
6. Devices are compared against a local database, where their status is determined (known, unknown, or blocked) and their information is persistently stored
7. Devices can be:
   - Added to the whitelist
   - Edited (custom description)
   - Removed from the whitelist
   - Blocked from the network

---

## Web Interface

The project includes a **web dashboard** that allows:

- Viewing all detected devices
- Clearly identifying unknown devices
- Managing trusted devices through a whitelist
- Editing device descriptions for better identification
- Blocking unwanted or unauthorized devices from the network

---

## Requirements

- Python 3.14+
- Root privileges (required for ARP scanning and blocking actions)
- flask>=3.1.2
- flask-sqlalchemy>=3.1.1
- mac-vendor-lookup>=0.1.15
- scapy>=2.7.0

### Dependencies

```bash
pip install scapy flask flask-sqlalchemy mac-vendor-lookup
```

---

## Usage

Start the application with:

```bash
sudo python app.py
```

Then access the web interface in your browser:

```bash
http://localhost:5000
```

---
