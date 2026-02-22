import scapy.all as scapy
import subprocess
import time

def get_mac_address(ip_address):
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    try:
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        return answered_list[0][1].hwsrc if answered_list else None
    except Exception as e:
        print(f"[!] Error getting MAC address for {ip_address}: {e}")
        return None

def detect_arp_spoofing():
    # Get the ARP table
    print("[*] Retrieving ARP table...")
    try:
        arp_output = subprocess.check_output("arp -a", shell=True).decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to get ARP table: {e}")
        return []
    
    lines = arp_output.splitlines()
    
    # Parse ARP table for IP and MAC addresses
    arp_table = {}
    for line in lines:
        if "(" in line and ")" in line:
            # Unix-style output: ? (192.168.1.1) at 00:11:22:33:44:55 ...
            try:
                ip = line.split("(")[1].split(")")[0]
                mac = line.split()[-1]
                # Filter out incomplete entries
                if mac != "<incomplete>":
                     arp_table[ip] = mac
            except IndexError:
                continue
        else:
            # Fallback for other formats or skip
            parts = line.split()
            if len(parts) >= 2:
                # Basic heuristic: if it looks like an IP and MAC
                # This is risky without regex, so we might just skip or log
                pass
    
    # Check for multiple IPs associated with the same MAC address
    mac_addresses = {}
    for ip, mac in arp_table.items():
        if mac not in mac_addresses:
            mac_addresses[mac] = [ip]
        else:
            mac_addresses[mac].append(ip)
    
    spoofed_ips = []
    for mac, ips in mac_addresses.items():
        if len(ips) > 1:
            print(f"[!] Potentially spoofed IPs for MAC {mac}: {', '.join(ips)}")
            spoofed_ips.extend(ips)
    
    if not spoofed_ips:
        print("[*] No ARP spoofing detected.")
    
    return spoofed_ips

def main():
    print("[*] Checking for ARP spoofing...")
    spoofed_ips = detect_arp_spoofing()
    
    if spoofed_ips:
        print(f"[!] Detected ARP spoofing for the following IPs: {', '.join(spoofed_ips)}")
        print("[*] Performing further checks for MITM activity...")
        
        for ip in spoofed_ips:
            actual_mac = get_mac_address(ip)
            if actual_mac:
                print(f"[?] IP {ip} should have MAC address {actual_mac}, but detected spoofing activities.")
            else:
                print(f"[!] Could not retrieve MAC address for {ip}.")
    else:
        print("[*] No MITM activity detected.")

if __name__ == "__main__":
    main()
