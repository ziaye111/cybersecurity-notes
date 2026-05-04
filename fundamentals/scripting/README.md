# Scripting & Automation for Security

Security engineering requires efficiency. If you have to do a task more than twice, you should script it.

## 1. Bash (`ping_sweep.sh`)
Bash is native to Linux. It is perfect for stringing together native command-line tools.
- Our `ping_sweep.sh` uses a `for` loop to iterate through IPs 1-254.
- It uses `grep` and `cut` to parse the output and only show us the IPs that responded.
- The `&` at the end of the ping command runs the tasks in the background, making the scan asynchronous and *much* faster.

## 2. Python (`port_scanner.py`)
Python allows for deeper programmatic control. 
- Our `port_scanner.py` uses the `socket` library to attempt TCP handshakes.
- `s.connect_ex()` returns `0` if a connection is established (meaning the port is open and listening).
- We utilize `try/except` blocks to handle errors gracefully, like the user hitting `Ctrl+C` to cancel the scan.
