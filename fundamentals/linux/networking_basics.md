# Networking Basics (Linux)

Understanding how Linux handles networking is critical for security analysis, reconnaissance, and troubleshooting.

## 1. Checking Connectivity & Interfaces
- **`ping <IP>`**: Checks basic ICMP connectivity to a target.
- **`ip a`** (or `ifconfig`): Displays available network interfaces and their assigned IP addresses.
- **`ip route`**: Shows the routing table (useful for finding the default gateway).

## 2. Investigating Open Ports & Connections
- **`ss -tulwn`**: The modern replacement for netstat. Shows listening TCP/UDP ports and active connections.
  - `-t` = TCP, `-u` = UDP, `-l` = listening, `-w` = RAW, `-n` = numeric (don't resolve hostnames).
- **`netstat -antp`**: Legacy but still widely used to show all active TCP connections and the processes using them (requires root for process mapping).

## 3. DNS and Routing
- **`nslookup <domain>`** or **`dig <domain>`**: Queries DNS records to resolve domain names to IPs.
- **`traceroute <IP>`**: Maps the path packets take to reach a destination, identifying hops along the way.
