# Mindgames - Binary Exploitation (Pwn)

**Category:** Binary Exploitation / Pwn  
**Key Concepts:** RNG Prediction, Buffer Overflow (.bss), Partial Overwrites, ROP, FSOP (House of Apple 2), CET / Hardware Shadow Stack Bypass.

## The Challenge Goal
The objective of "Mindgames" was to exploit two remote Linux binaries running on ports `1336` (Stage 1) and `1337` (Stage 2). The core goal was to gain reliable control of the execution flow, achieve Remote Code Execution (RCE), and execute the `grade` command on the remote server to retrieve the flags.

## The Vulnerabilities
Both binaries featured a guessing game with a custom highscore system. The core vulnerabilities were:
1. **Insecure Randomness:** The server seeded its RNG using the current time (`srand(time(NULL))`), which was leaked in the welcome banner.
2. **Global Buffer Overflow:** The `set_highscore_name()` function used `read(0, buffer, 4096)` to copy user input into a massively undersized buffer located in the `.bss` segment.

---

## Attack Path & Methodology

### Stage 1 (Port 1336) - Defeating ASLR with ROP
*   **RNG Sync:** Parsed the server time from the banner and brute-forced timezone offsets locally to perfectly sync the `libc` random number generator, allowing 100% accurate game predictions.
*   **Information Leak:** Abused the buffer overflow to perform a 1-byte partial overwrite on the `highscore.name` pointer, redirecting it to `printf@got`. Calling the "Show Highscore" function leaked the actual memory address, allowing the calculation of the `libc` base.
*   **Code Execution:** Triggered the overflow a second time to execute a standard Return-Oriented Programming (ROP) chain: `pop rdi; ret` -> `/bin/sh` -> `system()`.

### Stage 2 (Port 1337) - Bypassing CET & Shadow Stack via FSOP
Stage 2 enabled **Control-flow Enforcement Technology (CET)**, meaning a hardware-level Shadow Stack was tracking return addresses. Traditional ROP was impossible.
*   **Dual Leaks:** Used the same 1-byte GOT overwrite technique twice to consecutively leak the `libc` base (via `printf@got`) and the `PIE` base (via `exit@got`).
*   **House of Apple 2 (FSOP):** Because the overflow occurred in the `.bss` segment, I noticed the binary's actual `stdout` pointer was located exactly 192 bytes after the highscore buffer.
*   **Execution:** Forged a perfectly shifted 496-byte `_IO_FILE` structure within the buffer. The payload naturally overwrote the `stdout` pointer. When the program attempted to call `printf()`, it traversed my faked vtables and executed `system("  sh;")`, completely bypassing the Shadow Stack.

## Deliverables Included
*   `writeup.md`: In-depth, step-by-step personal writeup.
*   `exploit1.py`: Automated exploit script for Stage 1.
*   `exploit2.py`: Automated exploit script for Stage 2 (House of Apple 2).
*   `flags.txt`: The final retrieved flags.
