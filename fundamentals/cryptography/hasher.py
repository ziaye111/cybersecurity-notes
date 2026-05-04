#!/usr/bin/env python3

import sys
import hashlib

# Quick and Dirty Password Hasher
# Usage: python3 hasher.py <text_to_hash>

if len(sys.argv) != 2:
    print("Usage: python3 hasher.py <text_to_hash>")
    sys.exit()

# We have to encode the string to bytes before hashing it
plaintext = sys.argv[1].encode('utf-8')

print("-" * 40)
print(f"Target String: {sys.argv[1]}")
print("-" * 40)

# MD5 (Look how short it is. This is why it's easy to crack!)
md5_hash = hashlib.md5(plaintext).hexdigest()
print(f"[+] MD5:     {md5_hash}")

# SHA-1 (A bit better, but still considered broken by today's standards)
sha1_hash = hashlib.sha1(plaintext).hexdigest()
print(f"[+] SHA-1:   {sha1_hash}")

# SHA-256 (The modern standard. Much longer, much harder to crack)
sha256_hash = hashlib.sha256(plaintext).hexdigest()
print(f"[+] SHA-256: {sha256_hash}")

print("-" * 40)
