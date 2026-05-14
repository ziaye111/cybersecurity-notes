# Ethereum Smart Contract Exploitation

## Overview
This series of challenges focused on identifying and exploiting critical vulnerabilities in smart contracts deployed on a private Ethereum testnet using EveCoin. The goal was to drain the contract balances below 10^19 wei.

## Vulnerabilities Detected & Solved
* **NotAWallet (Broken Access Control)**: The contract relied on `tx.origin` for authorization instead of `msg.sender`. I bypassed this by using an intermediary "Attack" contract to phishing-trigger the withdrawal while maintaining the correct `tx.origin` context.
* **BadParity (Uninitialized Proxy)**: This vulnerability mirrored the historic Parity multi-sig incident. The underlying logic library was left uninitialized, allowing me to claim ownership of the library and subsequently withdraw all funds from the wallet.
* **DAO Down (Re-entrancy)**: A classic re-entrancy flaw where the contract sent funds before updating the internal state. I deployed a malicious contract with a `receive()` fallback to recursively call the `withdraw()` function, draining the entire balance in a single transaction sequence.
* **FailDice (Insecure Randomness)**: The contract’s "random" roll was derived from predictable block-level data like `block.timestamp` and `block.number`. I developed a script to pre-calculate the winning roll locally and only placed bets when a win was guaranteed.

## Technical Methodology
* **Environment**: Interacted with the Geth client via `web3.py` and the Geth JavaScript console.
* **Inspection**: Used `debug.traceTransaction` to analyze EVM execution steps and verify state changes in real-time.
