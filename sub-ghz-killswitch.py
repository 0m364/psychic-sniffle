import time
import numpy as np
from rtlsdr import RtlSdr
from scapy.all import *
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Mock GPS location (replace with actual GPS module integration)
BASE_LOCATION = (40.7128, -74.0060)  # Example: New York City coordinates

# Frequency scanning parameters
FREQ_START = 300e6  # 300 MHz
FREQ_END = 1e9      # 1 GHz
FREQ_STEP = 2e5     # 200 kHz steps
DETECTED_DEVICES = []

def scan_frequency():
    """Scan sub-GHz frequencies for active devices."""
    sdr = RtlSdr()
    sdr.sample_rate = 2.048e6
    sdr.center_freq = FREQ_START
    sdr.gain = 'auto'

    print("Scanning frequencies...")
    for freq in np.arange(FREQ_START, FREQ_END, FREQ_STEP):
        sdr.center_freq = freq
        samples = sdr.read_samples(256 * 1024)
        power = np.mean(np.abs(samples)**2)
        if power > 1e-6:  # Threshold for device detection
            DETECTED_DEVICES.append((freq, power))
            print(f"Device detected at {freq/1e6:.2f} MHz with power {power:.6f}")

    sdr.close()

def locate_devices():
    """Mock device location triangulation."""
    print("Triangulating device locations...")
    locations = []
    for device in DETECTED_DEVICES:
        freq, power = device
        # Mock triangulation: Offset from base location
        location = (
            BASE_LOCATION[0] + np.random.uniform(-0.01, 0.01),
            BASE_LOCATION[1] + np.random.uniform(-0.01, 0.01)
        )
        locations.append((freq, location))
        print(f"Device at {freq/1e6:.2f} MHz located at {location}")
    return locations

def map_devices(locations):
    """Map detected devices."""
    print("Mapping devices...")
    plt.figure(figsize=(8, 6))
    for freq, loc in locations:
        plt.scatter(loc[1], loc[0], label=f"{freq/1e6:.2f} MHz")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Detected Sub-GHz Devices")
    plt.legend()
    plt.grid()
    plt.show()

def shutoff_device(freq):
    """Simulate shutoff command to a device."""
    print(f"Sending shutdown command to device at {freq/1e6:.2f} MHz...")
    # Simulated shutdown command (requires hardware for actual shutdown)
    time.sleep(1)
    print(f"Device at {freq/1e6:.2f} MHz successfully shut off.")

if __name__ == "__main__":
    scan_frequency()
    device_locations = locate_devices()
    map_devices(device_locations)

    # Shutoff example
    if DETECTED_DEVICES:
        for device in DETECTED_DEVICES:
            shutoff_device(device[0])