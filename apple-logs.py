import subprocess
import re
import time
import sys

def capture_ios_logs(output_file):
    print(f"[*] Capturing iOS logs to {output_file}...")
    cmd = ['idevicesyslog']

    try:
        with open(output_file, 'w') as f:
            process = subprocess.Popen(cmd, stdout=f)
            try:
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("\n[*] Stopping log capture...")
                process.terminate()
                process.wait()
                print("[*] Log capture stopped.")
    except Exception as e:
        print(f"[!] Error capturing logs: {e}")

def parse_nfc_logs(log_file):
    nfc_entries = []
    nfc_regex = re.compile(r'.*CoreNFC.*')  # Simplified regex for NFC entries
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                if nfc_regex.match(line):
                    nfc_entries.append(line.strip())
    except FileNotFoundError:
        print(f"[!] Log file {log_file} not found.")
        return []
    
    return nfc_entries

def main():
    log_file = "ios_syslog.txt"
    print("[*] Start capturing logs...")
    print("[*] Press Ctrl+C to stop capturing.")
    
    capture_ios_logs(log_file)

    print("[*] Parsing NFC logs...")
    nfc_logs = parse_nfc_logs(log_file)
    
    if not nfc_logs:
        print("[!] No NFC logs found.")
    else:
        print("[*] Found NFC logs:")
        for entry in nfc_logs:
            print(entry)

if __name__ == "__main__":
    main()
