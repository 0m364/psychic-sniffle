import nfc
import sys

def on_connect(tag):
    print(f"[*] Connected to {tag}")
    print(f"[*] Tag type: {tag.type}")
    print(f"[*] Tag ID: {tag.identifier.hex()}")
    
    # Read some data if supported
    try:
        if tag.ndef:
            print("[*] NDEF data:")
            for record in tag.ndef.records:
                print(f"\t{record}")
    except AttributeError:
        print("[*] This tag does not support NDEF.")
    
    return False  # Disconnect immediately after connected

def main():
    clf = nfc.ContactlessFrontend()

    if not clf.open('usb'):
        print("[!] Failed to open NFC reader. Ensure it is connected.")
        sys.exit(1)
    
    print("[*] NFC reader ready. Scan a tag...")
    try:
        clf.connect(rdwr={'on-connect': on_connect})
    except KeyboardInterrupt:
        print("\n[*] Exiting NFC scanner.")
    finally:
        clf.close()

if __name__ == "__main__":
    main()
