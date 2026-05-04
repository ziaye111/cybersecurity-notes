# Linux File System & Permissions

Security heavily relies on access control. Understanding the Linux file system hierarchy and permissions is step zero for privilege escalation and system hardening.

## 1. Critical Directories
- **`/etc`**: Contains core system configuration files (e.g., `/etc/passwd`, `/etc/shadow`).
- **`/var/log`**: Contains system and application logs (crucial for incident response).
- **`/tmp`**: Temporary files. Often world-writable, making it a common drop zone for exploits.
- **`/home`** and **`/root`**: User directories where SSH keys (`.ssh/`) and history files (`.bash_history`) are stored.

## 2. Managing Permissions
Linux uses Read (4), Write (2), and Execute (1) permissions for the Owner, Group, and Others.
- **`chmod 755 <file>`**: Grants rwx to owner, rx to group, rx to others.
- **`chmod 600 <file>`**: Grants rw to owner only (essential for private SSH keys).
- **`chown user:group <file>`**: Changes the owner and group of a file.

## 3. Finding Things (Recon)
- **`find / -name "flag.txt" 2>/dev/null`**: Searches the entire file system for a file named flag.txt, hiding permission denied errors.
- **`grep -rnw '/path/' -e 'password'`**: Recursively searches inside files for the string "password".
