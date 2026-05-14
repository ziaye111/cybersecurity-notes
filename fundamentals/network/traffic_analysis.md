# Network Traffic Analysis & Protocol Security

Deep packet inspection is critical for detecting anomalies and understanding how exploits travel across a network.

## 1. The TCP Three-Way Handshake
Understanding the handshake is essential for identifying SYN scans and connection-based attacks.
- **SYN**: Client requests connection.
- **SYN-ACK**: Server acknowledges and requests back.
- **ACK**: Client confirms.
*(In the **FailDice** exploit, understanding these low-level connections was key to managing persistent TCP oracles).*

## 2. Wireshark/Tshark Filters
For efficient analysis, I utilize specialized filters:
- `http.request.method == "POST"`: To find credential sniffing opportunities.
- `tcp.flags.syn == 1 && tcp.flags.ack == 0`: To detect port scanning activity.
- `ip.addr == <target>`: To isolate traffic for a specific host.

## 3. Protocol Weaknesses
- **HTTP vs HTTPS**: The risk of cleartext data transmission.
- **DNS Spoofing**: How attackers redirect traffic by poisoning the local cache.
