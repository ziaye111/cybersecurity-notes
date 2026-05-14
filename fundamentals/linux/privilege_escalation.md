# Linux Privilege Escalation & Hardening

Gaining access is only the first step. Post-exploitation involves elevating privileges and maintaining access.

## 1. SUID/SGID Executables
Finding binaries that run with root permissions:
- **Command**: `find / -perm -u=s -type f 2>/dev/null`
*(If a misconfigured binary like `vim` or `bash` has SUID set, it allows for instant root shells).*

## 2. Exploiting Writable `/etc/passwd`
If permissions are misconfigured (e.g., `777` on `/etc/passwd`), a new root user can be added manually:
- **Action**: Generate a hash (`openssl passwd -1 password`) and append it to the file.

## 3. Automated Enumeration Tools
In real-world environments, I utilize scripts to find misconfigurations:
- **LinPEAS**: The most comprehensive tool for finding privesc paths.
- **LinEnum**: A lightweight alternative for basic system auditing.

## 4. Cron Job Exploitation
Checking for scheduled tasks running as root that execute writable scripts:
- **Command**: `cat /etc/crontab`
