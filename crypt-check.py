import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import algorithms, modes

# List of cipher suites to check
# Format: (Name, Algorithm Class, Key Size (bits) or None, Mode Class or Hash Class)
cipher_suites = [
    ('AES-256-GCM', algorithms.AES, 256, modes.GCM),
    ('AES-256-CBC', algorithms.AES, 256, modes.CBC),
    ('BLOWFISH-SHA256', algorithms.Blowfish, None, hashes.SHA256),
    ('DES-CBC3-SHA', algorithms.TripleDES, None, modes.CBC),
    ('RC4-MD5', algorithms.ARC4, None, hashes.MD5),
]

def check_encryption_compatibility(cipher_suite):
    name, algorithm_cls, key_size, mode_or_hash_cls = cipher_suite

    print(f"Checking compatibility for {name}...")

    # Key size check
    if key_size:
        # Check if algorithm class has key_sizes attribute
        # Most symmetric algorithms in cryptography have .key_sizes
        if hasattr(algorithm_cls, 'key_sizes'):
            # key_sizes can be a set, list or range
            if key_size not in algorithm_cls.key_sizes:
                print(f"  [!] {name}: Key size {key_size} not supported by {algorithm_cls.__name__}. Supported sizes: {list(algorithm_cls.key_sizes)}")
                return False
        else:
            # Fallback or different algorithm type
            print(f"  [?] {name}: Could not verify key size support for {algorithm_cls.__name__} (no key_sizes attribute).")

    # Mode/Hash check
    if isinstance(mode_or_hash_cls, type):
        if issubclass(mode_or_hash_cls, modes.Mode):
             # Just check if it is a valid mode class
             # We avoid instantiating modes here as they often require IVs/nonces which we don't have
             print(f"  [*] {name}: Uses mode {mode_or_hash_cls.__name__}.")
        elif issubclass(mode_or_hash_cls, hashes.HashAlgorithm):
             print(f"  [*] {name}: Uses hash {mode_or_hash_cls.__name__}.")
        else:
             print(f"  [!] {name}: Unknown mode/hash type {mode_or_hash_cls}.")
             return False

    print(f"  [+] {name} appears compatible.")
    return True

# Iterate through the list of cipher suites and check each one
if __name__ == "__main__":
    print(f"Using cryptography version: {cryptography.__version__}")
    for suite in cipher_suites:
        check_encryption_compatibility(suite)
