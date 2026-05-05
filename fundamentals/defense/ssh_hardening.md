# SSH Hardening: Securing Remote Access

SSH is the front door to most Linux servers. If it's not locked down, it's the first thing an attacker will brute-force.

## 1. Disable Root Login
Logging in directly as `root` is a huge risk. You should always log in as a standard user and use `sudo`.
- **Action**: Set `PermitRootLogin no` in `/etc/ssh/sshd_config`.

## 2. Use Key-Based Authentication
Passwords can be guessed or brute-forced. SSH keys are mathematically impossible to guess.
- **Action**: Set `PasswordAuthentication no`.
- **Tip**: Ensure your private key has a passphrase for "Encryption at Rest."

## 3. Change the Default Port
Changing port 22 to something random (like 2222) won't stop a determined hacker, but it will stop 99% of automated bot scans.
- **Action**: Change `Port 22` to `Port <YourChoice>`.

## 4. Limit Access with AllowUsers
Only specific people should be allowed to SSH in.
- **Action**: Add `AllowUsers ziaye111` to the config file to block everyone else.
