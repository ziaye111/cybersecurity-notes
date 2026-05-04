#!/usr/bin/env python3

import sys
import socket
from datetime import datetime

# Basic Port Scanner
# Usage: python3 port_scanner.py <Target_IP>

if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1])
else:
    print("Invalid amount of arguments.")
    print("Syntax: python3 port_scanner.py <ip>")
    sys.exit()

print("-" * 50)
print(f"Scanning target: {target}")
print(f"Time started: {str(datetime.now())}")
print("-" * 50)

try:
    # Scanning common ports (1 to 1024)
    for port in range(1, 1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1) # Don't hang on dead ports
        result = s.connect_ex((target, port)) # Returns 0 if successful
        if result == 0:
            print(f"Port {port} is OPEN")
        s.close()

except KeyboardInterrupt:
    print("\nExiting program.")
    sys.exit()
except socket.gaierror:
    print("\nHostname could not be resolved.")
    sys.exit()
except socket.error:
    print("\nCould not connect to server.")
    sys.exit()
