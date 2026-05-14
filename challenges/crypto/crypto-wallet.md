# Crypto Wallet – BIP32 Key Recovery

## Vulnerability Analysis
This challenge demonstrated the risk of using **Non-Hardened Key Derivation** in Hierarchical Deterministic (HD) wallets. If a child private key is leaked and the parent’s extended public key is known, the parent's private key can be mathematically recovered.

## The Recovery Process
1. **Mapping the Path**: Analyzed the derivation path to confirm it used non-hardened indices.
2. **Mathematical Reconstruction**: Using the Root Extended Public Key and a leaked Child Private Key, I applied the formula `k_parent = (k_child - I_L) mod n` to crawl back up the tree.
3. **Target Derivation**: Once the common ancestor private key was recovered, I derived the target private key for the specific path `m/44/0/0/0/402` normally.
