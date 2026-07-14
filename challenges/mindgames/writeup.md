# Mindgames Challenge Write-up

## Context

Mindgames was an authorized binary-exploitation lab built around a remote guessing game. The challenge helped me connect several ideas that I had previously studied separately: predictable pseudo-random numbers, information leaks, return-oriented programming, control-flow protections, and glibc file structures.

Sensitive challenge values are intentionally omitted.

## Stage 1 — From predictable randomness to code execution

### Understanding the random-number generator

The game appeared to seed its pseudo-random number generator with the current time. The welcome message included a server timestamp, so I converted that value into candidate Unix timestamps and tested nearby seeds.

I compared both the generated high-score name and score instead of trusting a single value. Once the correct seed was identified, the game's future values became predictable.

### Building an information leak

The function responsible for setting the high-score name accepted far more data than its destination could safely hold. The overflow reached a pointer inside the high-score structure.

I partially overwrote that pointer so that displaying the high score read from a Global Offset Table entry. Leaking the runtime address of a libc function allowed me to calculate the libc base despite address-space randomization.

### Redirecting control flow

A cyclic-pattern test showed that the saved instruction pointer was reached after 280 bytes. With the libc base known, I constructed a small return-oriented programming chain that placed the address of `/bin/sh` in the first argument register and called `system()`.

An additional `ret` gadget was needed to maintain the stack alignment expected by the x86-64 calling convention. The final payload produced a shell in the lab environment, after which the grading command confirmed Stage 1.

## Stage 2 — Working around shadow-stack protection

Stage 2 enabled Control-flow Enforcement Technology, including shadow-stack protection. A normal overwritten return address no longer worked because the processor compared it with the protected copy.

That changed the problem: instead of returning through a ROP chain, I needed a path that redirected execution without a mismatched return.

### Leaking libc and PIE addresses

The same overflow reached data stored in the `.bss` section. Controlled partial pointer overwrites exposed entries associated with libc and the position-independent executable. These leaks provided the bases needed to reason about runtime addresses.

### File-stream-oriented programming

The program's `stdout` pointer was close enough to the overflowing buffer to become a useful target. I built a fake glibc `_IO_FILE` structure in controlled memory and redirected `stdout` to it.

The fake structure was arranged so that a later output operation followed controlled wide-data and vtable pointers and eventually reached `system()`. This avoided a conventional corrupted return and therefore did not directly conflict with the shadow stack.

The final layout required careful attention to structure offsets, internal consistency checks, payload length, and stack-independent control flow. Triggering the next normal output operation produced a shell and allowed the lab grader to confirm Stage 2.

## What I learned

- Time-seeded pseudo-random values are predictable when the seed space is small.
- An address leak can turn an unreliable exploit into one that accounts for ASLR and PIE.
- A mitigation usually blocks a technique, not every possible route to the same goal.
- File-stream exploitation depends on precise knowledge of the target glibc version and internal layout.
- Reliable exploitation comes from validating each primitive separately: prediction, leak, base calculation, overwrite, and trigger.

## Scope and ethics

This work was completed in an authorized course environment. Real flags, tokens, and credentials are not included in this repository.
