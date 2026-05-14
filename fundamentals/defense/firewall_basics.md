# Firewall Management (UFW)

A firewall is the first line of defense. In Linux, Uncomplicated Firewall (UFW) is the standard for managing iptables without the complexity.

## 1. The "Default Deny" Strategy
The most secure way to run a server is to block everything by default and only open what is strictly necessary.
- **Command**: `ufw default deny incoming`
- **Command**: `ufw default allow outgoing`

## 2. Opening Essential Services
- **SSH**: `ufw allow 22/tcp` (or your custom port).
- **Web**: `ufw allow 80/tcp` and `ufw allow 443/tcp`.

## 3. Limiting Brute Force
UFW has a built-in rate limiter that is great for stopping automated attacks on SSH.
- **Command**: `ufw limit ssh`
*(This denies connections from an IP address that has attempted to initiate 6 or more connections in the last 30 seconds).*

## 4. Checking Status
- **Command**: `ufw status numbered`
- **Command**: `ufw enable`
