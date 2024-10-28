# WiFiDeauthNuke

![WiFiDeauthNuke](https://img.shields.io/badge/version-1.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)

WiFiDeauthNuke is a Python-based tool that allows you to scan nearby Wi-Fi networks, detect connected clients, and perform a deauthentication (deauth) attack on a specific device connected to a Wi-Fi network. This tool is designed for network administrators and cybersecurity professionals to assess the security of Wi-Fi networks by testing their vulnerability to deauthentication attacks.

> **Warning**: This tool should only be used for educational purposes and on networks you own or have permission to test. Unauthorized use of deauthentication attacks is illegal and can result in severe consequences.

---

## Features
- **Scan Nearby Wi-Fi Networks**: Detects and lists nearby Wi-Fi networks in monitor mode.
- **Client Detection**: Identifies devices (clients) connected to a specific network.
- **Deauthentication Attack**: Sends deauthentication packets to disconnect a device from a Wi-Fi network.
- **User-Friendly Interface**: Easy-to-navigate CLI with colored output for enhanced readability.
- **Monitor Mode Management**: Automatically enables and disables monitor mode on the detected Wi-Fi interface.

## Demo
### WiFiDeauthNuke Banner

██╗    ██╗██╗███████╗██╗    ██╗██████╗ ███████╗ █████╗ ███████╗██╗   ██╗██╗  ██╗███████╗
██║    ██║██║██╔════╝██║    ██║██╔══██╗██╔════╝██╔══██╗██╔════╝██║   ██║██║  ██║██╔════╝
██║ █╗ ██║██║█████╗  ██║ █╗ ██║██║  ██║█████╗  ███████║███████╗██║   ██║███████║█████╗  
██║███╗██║██║██╔══╝  ██║███╗██║██║  ██║██╔══╝  ██╔══██║╚════██║██║   ██║██╔══██║██╔══╝  
╚███╔███╔╝██║███████╗╚███╔███╔╝██████╔╝███████╗██║  ██║███████║╚██████╔╝██║  ██║███████╗
 ╚══╝╚══╝ ╚═╝╚══════╝ ╚══╝╚══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝

WiFiDeauthNuke v1.0 - Created by github.com/fatherofphysics


## Requirements
- **Operating System**: Linux-based OS with support for `airmon-ng`
- **Python**: Python 3.x
- **Dependencies**: Ensure you have the following tools installed:
  - `airmon-ng`
  - `airodump-ng`
  - `aireplay-ng`
  
Install these tools with:
```bash
sudo apt update
sudo apt install aircrack-ng

