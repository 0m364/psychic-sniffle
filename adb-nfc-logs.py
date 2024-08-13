import os
import subprocess
import re

def pull_logs():
    print("[*] Pulling logs from the Android device...")
    cmd = ['adb', 'logcat', '-d']
    
    try:
        log_output = subprocess.check_output(cmd).decode('utf-8')
        return log_output
    except subprocess.CalledProcessError as e:
        print("[!] Failed to get logs:", e)
        return None

def parse_nfc_logs(log_data):
    nfc_entries = []
    nfc_regex = re.compile(r'.*NfcService.*')  # Simplified regex for NFC entries
    
    for line in log_data.splitlines():
        if nfc_regex.match(line):
            nfc_entries.append(line)
    
    return nfc_entries

def main():
    log_data = pull_logs()
    if not log_data:
        print("[!] No log data found.")
        return
    
    print("[*] Parsing NFC logs...")
    nfc_logs = parse_nfc_logs(log_data)
    
    if not nfc_logs:
        print("[!] No NFC logs found.")
    else:
        print("[*] Found NFC logs:")
        for entry in nfc_logs:
            print(entry)

if __name__ == "__main__":
    main()
