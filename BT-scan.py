import bluetooth

def find_bluetooth_devices():
    print("[*] Scanning for Bluetooth devices...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_oui=False)
    
    print(f"[*] Found {len(nearby_devices)} devices.")
    
    for addr, name in nearby_devices:
        print(f"[*] Device: {name} ({addr})")
    
    return nearby_devices

def main():
    print("[*] Starting Bluetooth scanner...")
    devices = find_bluetooth_devices()
    if not devices:
        print("[!] No Bluetooth devices found.")
    print("[*] Bluetooth scan complete.")

if __name__ == "__main__":
    main()
