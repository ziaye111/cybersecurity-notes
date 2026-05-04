import socket
import json
import re

HOST = "0.0.0.0"
PORT = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print("[+] Listening on UDP 1234")

while True:
    data, addr = sock.recvfrom(4096)
    text = data.decode(errors="ignore")
    print("[+] Received from", addr, text)

    try:
        msg = json.loads(text)
        challenge = msg.get("challenge", "")

        m = re.search(r"(\d+)\s*\*\s*(\d+)", challenge)
        if not m:
            print("[-] Could not parse challenge")
            continue

        answer = int(m.group(1)) * int(m.group(2))
        msg["response"] = answer

        reply = json.dumps(msg).encode()
        sock.sendto(reply, addr)

        print("[+] Sent:", reply.decode())

    except Exception as e:
        print("[-] Error:", e)
