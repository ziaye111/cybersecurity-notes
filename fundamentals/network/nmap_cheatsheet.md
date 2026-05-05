# Nmap Reconnaissance Methodology

Scanning isn't just about finding open ports; it's about doing it efficiently and quietly.

## 1. Basic Scanning Types
- **`nmap -sT <IP>`**: TCP Connect Scan (completes the 3-way handshake). Easy to detect.
- **`nmap -sS <IP>`**: SYN Stealth Scan (half-open). Faster and harder to log.
- **`nmap -sU <IP>`**: UDP Scan. Much slower but necessary for finding DNS, DHCP, or SNMP.

## 2. Aggressive Enumeration
- **`nmap -A <IP>`**: The "Everything" switch. Enables OS detection, version detection, script scanning, and traceroute.
- **`nmap -sV <IP>`**: Probes open ports to determine service/version info (crucial for finding exploits).

## 3. Nmap Scripting Engine (NSE)
Nmap can do more than scan; it can find vulnerabilities.
- **`nmap --script vuln <IP>`**: Runs a library of scripts to check for known vulnerabilities on the target.

## 4. Best Practice Command
For a standard engagement, I use:
`nmap -sC -sV -oN initial_scan.txt <IP>`
*(Scripts, Versions, and save output to a file)*.
