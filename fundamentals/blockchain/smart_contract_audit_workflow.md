# Smart Contract Auditing & Verification Checklist

A structured approach to reviewing Ethereum Virtual Machine (EVM) bytecodes and Solidity logic.

## 1. Initial Static Analysis
- **Visibility Checks**: Ensure functions intended to be internal are not exposed publicly (mitigating vulnerabilities similar to uninitialized proxy or library exploits).
- **Origin Contexts**: Flag any instance of `tx.origin` used in place of `msg.sender` for access control, as it leaves the contract open to phishing-induced state changes.

## 2. Dynamic Execution & Node Emulation
When interacting with custom or localized chains (such as Clique Proof-of-Authority environments via `web3.py`), standard execution behaviors can shift:
- **Gas Estimation Traps**: Failed transactions simulate as execution reverts during `estimate_gas`. A failing simulation typically signals a logic or balance failure rather than an infrastructure bug.
- **Middleware Integration**: Proof-of-Authority chains require injecting specific layer-0 middleware (like `geth_poa_middleware`) into the web3 instance to correctly process extra-data block headers.

## 3. Transaction Trace Auditing
- **Low-Level Analysis**: Utilizing `debug.traceTransaction` allows the auditor to step through EVM opcodes directly to witness state changes, memory allocation, and exact depth execution during recursive calls (Re-entrancy).
