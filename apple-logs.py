import subprocess
import re

def capture_ios_logs(output_file):
    print("[*] Capturing iOS logs...")
    cmd = ['idevicesyslog']
    with open(output_file, 'w') as f:
        try:
            subprocess.run(cmd, stdout=f)
        except KeyboardInterrupt:
            print("\n[*] Stopped capturing logs.")
        except subprocess.CalledProcessError as e:
            print("[!] Error capturing logs:", e)

def parse_nfc_logs(log_file):
    nfc_entries = []
    nfc_regex = re.compile(r'.*CoreNFC.*')  # Simplified regex for NFC entries
    
    with open(log_file, 'r') as f:
        for line in f:
            if nfc_regex.match(line):
                nfc_entries.append(line)
    
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
