# CryptoCommit – Elliptic Curve Commitment Exploit

## Vulnerability Analysis
The core issue was that the commitment was **linear** and used **related generators**. Because of this, the commitment effectively depended on a simple linear equation between the value and the blinding factor.

## Exploitation Steps
1. **Token Issuance**: Requested a valid e-cash token for a specific value using `get_ecash`.
2. **Forging the Commitment**: Leveraged the linear relationship to modify the value while adjusting the blinding factor accordingly.
3. **Redemption**: Reused the same commitment and signature, but with the modified value and blinding factor. The server accepted the forged token because the mathematical verification still held true.

## Key Learnings
* **Linearity is a Flaw**: Demonstrated why commitments must be non-linear to prevent unauthorized value modification.
* **Implementation Challenges**: Navigated difficulties with big vs. little endian formats to ensure the server accepted the signatures.
