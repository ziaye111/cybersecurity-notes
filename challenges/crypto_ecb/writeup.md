# AES-ECB Byte-at-a-Time Recovery

## Challenge Goal
The objective was to exploit a remote service running an AES oracle in Electronic Codebook (ECB) mode. The goal was to recover a secret `SECRET_SUFFIX` appended to any user-provided plaintext before encryption.

## Methodology

### 1. Connection & Reconnaissance
The first step involved establishing a persistent TCP connection to the oracle.
- **Target**: `<lab-host>:4242`
- **Tooling**: A custom Python class `OracleConn` was developed to handle the socket communication, drain menu text, and isolate the hexadecimal ciphertext responses.

### 2. Vulnerability Discovery (ECB Mode)
Before launching the attack, the encryption parameters were confirmed:
- **Block Size Detection**: By incrementally increasing the input length, the ciphertext jumped in size once a new block was triggered. This jump was 16 bytes, confirming an **AES block size of 16**.
- **Mode Confirmation**: By sending a repeated 32-byte pattern of identical characters, the resulting ciphertext showed identical blocks, proving that **ECB mode** was being used without a unique Initialization Vector (IV) per block.

### 3. Byte-at-a-Time Exploitation
A "byte-at-a-time" attack was implemented in `local_ecb_recover.py`. The logic followed these steps:
1. **Alignment**: Send a prefix of `block_size - 1` bytes (15 "A"s) so that the first byte of the secret is shifted into the last position of the first block.
2. **Brute-Force Dictionary**: Pre-compute all 256 possible blocks by encrypting the prefix + every possible character.
3. **Matching**: Compare the actual ciphertext block against the dictionary to identify the secret byte.
4. **Iteration**: Shift the prefix again and use the previously recovered bytes to find the next character, repeating until the full secret is leaked.

## Results
The script successfully automated the recovery process, bypassing PKCS#7 padding to reveal the flag:
**`[redacted challenge flag]`**
