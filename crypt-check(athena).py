import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import algorithms, modes

# List of cipher suites to check
cipher_suites = [
    ('AES-256-GCM', algorithms.AES, 256, modes.GCM),
    ('AES-256-CBC', algorithms.AES, 256, modes.CBC),
    ('BLOWFISH-SHA256', algorithms.Blowfish, None, hashes.SHA256),
    ('DES-CBC3-SHA', algorithms.TripleDES, None, modes.CBC),
    ('RC4-MD5', algorithms.ARC4, None, hashes.MD5),
]

# Function to check encryption compatibility
def check_encryption_compatibility(cipher_suite):
    name, algorithm, key_size, mode_or_hash = cipher_suite
    
    # Algorithm checks
    if key_size:
        if algorithm.key_size is not None and algorithm.key_size != key_size:
            print(f"{name} is not compatible with key size {key_size}")
            return False

    if isinstance(mode_or_hash, type) and issubclass(mode_or_hash, modes.Mode):
        # Mode checks
        try:
            mode_or_hash(None)  # Probes to see if the mode is viable
        except TypeError:
            print(f"{name} does not support the mode {mode_or_hash.__name__}")
            return False
    elif isinstance(mode_or_hash, type) and issubclass(mode_or_hash, hashes.HashAlgorithm):
        # Hash checks
        if algorithm.name != "blowfish":
            if not algorithm.algorithm_matches(mode_or_hash().name):
                print(f"{name} is not compatible with hashing algorithm {mode_or_hash().name}")
                return False

    print(f"{name} is compatible with given parameters")
    return True

# Iterate through the list of cipher suites and check each one
for suite in cipher_suites:
    if check_encryption_compatibility(suite):
        print(f"{suite[0]} is a valid encryption type")
    else:
        print(f"{suite[0]} is not a valid encryption type")
