import cryptography

# List of cipher suites to check
cipher_suites = [
    ('AES-256-GCM', 'aes', 256, 'gcm'),
    ('AES-256-CBC', 'aes', 256, 'cbc'),
    ('BLOWFISH-SHA256', 'bf', 256, 'sha256'),
    ('DES-CBC3-SHA', 'des', 3, 'cbc'),
    ('RC4-MD5', 'rc4', None, 'md5'),
]

# Function to check encryption type
def check_encryption_type(cipher_suite):
    suite = cryptography.x509.load_pem_x509_certificate(
        open(cipher_suite[0], 'rb').read(), default_backend()
    )

    algorithm = suite['signature'].algorithm
    if algorithm != 'sha256':
        print(f"{cipher_suite[1]} is not compatible with SHA-256")
        return False

    encryption_algorithm = suite.get_extension_for_oid('encryption')
    if not encryption_algorithm:
        print(f"{cipher_suite[1]} does not support encryption")
        return False

    if encryption_algorithm.value != 'des-ede3':
        print(f"{cipher_suite[1]} is not compatible with DES-EDE3 encryption")
        return False

    return True

# Iterate through the list of cipher suites and check each one
for suite in cipher_suites:
    if check_encryption_type(suite):
        print(f"{suite[0]} is a valid encryption type")
    else:
        print(f"{suite[0]} is not a valid encryption type")
