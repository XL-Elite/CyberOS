# CyberOS User Manual

## Table of Contents

1. [Basic System Usage](#basic-system-usage)
2. [Commands and Utilities](#commands-and-utilities)
3. [File Management](#file-management)
4. [System Administration](#system-administration)
5. [Networking](#networking)
6. [Tips and Tricks](#tips-and-tricks)

---

## Basic System Usage

### Login and Logout

**Initial Login**:
```bash
# At the login prompt
username: root
password: cyberos (please change this)
```

**Logout**:
```bash
exit
or
logout
or
Ctrl+D
```

### Password Management

**Change your password**:
```bash
passwd               # Change current user password
passwd username      # Change another user's password (root only)
```

### Power Management

```bash
shutdown -h now      # Shutdown immediately
shutdown -r now      # Reboot immediately  
poweroff             # Power off the system
reboot               # Reboot
halt                 # Stop the system
```

---

## Commands and Utilities

### Essential Commands

**Navigation**:
```bash
pwd                  # Print working directory
cd /path/to/dir      # Change directory
cd -                 # Return to previous directory
ls                   # List files
ls -la               # List with details
tree                 # Tree view (if available)
```

**File Operations**:
```bash
cat file.txt         # Display file contents
less file.txt        # View file with pagination
grep "pattern" file  # Search file for pattern
head -n 10 file      # Show first 10 lines
tail -f file         # Follow file (watch in real-time)
wc -l file           # Count lines
diff file1 file2     # Compare files
```

**Directory Operations**:
```bash
mkdir dirname        # Create directory
rmdir dirname        # Remove empty directory
rm -r dirname        # Remove directory recursively
cp file1 file2       # Copy file
mv file1 file2       # Move/rename file
find . -name "*.txt" # Find files by pattern
```

### System Information

```bash
uname -a             # System information
uptime               # System uptime
date                 # Current date/time
whoami               # Current user
id                   # User and group info
df -h                # Disk space usage
du -sh dirname       # Directory size
free -m              # Memory usage
ps aux               # Running processes
top                  # Process monitor
```

---

## File Management

### File Permissions

```bash
# Changing permissions (octal)
chmod 755 file       # rwxr-xr-x
chmod 644 file       # rw-r--r--
chmod 700 file       # rwx------

# Changing ownership
chown user file      # Change owner
chown user:group file # Change user and group
chgrp group file     # Change group

# Symbolic mode
chmod u+x file       # Add execute for user
chmod g-w file       # Remove write from group
chmod o=r file       # Set others to read-only
```

### File Copying and Moving

```bash
# Copy
cp file1 file2       # Copy file
cp -r dir1 dir2      # Copy directory
cp -v file1 file2    # Verbose output

# Move/Rename
mv file1 file2       # Rename file
mv file1 dir/        # Move file to directory
mv -i file1 file2    # Interactive (ask before overwrite)
```

### Searching Files

```bash
find . -name "*.txt"                    # By filename
find . -type f -name "*.log"            # By type and name
find . -size +100M                      # By file size
find . -mtime -7                        # Modified in last 7 days
grep -r "pattern" /path                 # Recursive grep
grep -i "pattern" file                  # Case-insensitive
```

---

## System Administration

### User Management

```bash
# Add user
adduser username
# or
useradd -m -s /bin/ash username

# Remove user
deluser username

# Modify user
usermod -G groupname username           # Add to group
usermod -s /bin/ash username            # Change shell
usermod -aG sudo username               # Add to sudo group (if available)

# Lists
cat /etc/passwd                         # User list
cat /etc/group                          # Group list
cat /etc/shadow                         # Password hashes (root only)
```

### Service Management

```bash
# List services
/etc/init.d/                # View available services

# Service control
/etc/init.d/servicename start   # Start
/etc/init.d/servicename stop    # Stop
/etc/init.d/servicename restart # Restart
/etc/init.d/servicename status  # Status

# Enable at boot
update-rc.d servicename defaults    # Enable
update-rc.d servicename disable     # Disable
```

### System Logs

```bash
# View logs
cat /var/log/syslog             # System log
tail -f /var/log/syslog         # Follow log
dmesg                           # Kernel message buffer
dmesg | tail -20                # Last 20 kernel messages

# Kernel logs
cat /var/log/kern.log           # Kernel log
journalctl (if systemd)         # Journal log
```

### Scheduled Tasks

```bash
# Cron jobs (if installed in future versions)
# crontab -e                   # Edit cron jobs
# crontab -l                   # List cron jobs
# 0 2 * * * /path/to/script   # Run daily at 2am
```

---

## Networking

### Network Information

```bash
ip address show         # Show IP addresses
ip link show            # Show network interfaces
ip route show           # Show routing table
ifconfig (if available) # Network config (deprecated but common)
```

### Network Configuration

```bash
# Static IP assignment
ip address add 192.168.1.10/24 dev eth0
ip route add default via 192.168.1.1
ip route add default via 192.168.1.1 dev eth0

# DHCP (request address from server)
dhclient eth0

# DNS configuration
cat /etc/resolv.conf    # Current DNS
# Add nameserver 8.8.8.8 to /etc/resolv.conf
```

### Network Testing

```bash
ping 8.8.8.8            # Test connectivity (Ctrl+C to stop)
ping -c 4 8.8.8.8       # Send 4 pings
host google.com         # DNS lookup
dig google.com          # DNS info (if installed)
nslookup google.com     # DNS lookup (if installed)

netstat (if available)  # Network statistics
ss (socket statistics)  # Connection info
```

### Remote Connectivity

```bash
# SSH (v0.4.0+)
ssh user@hostname       # Connect to remote
ssh -p 2222 user@host   # Connect on different port
scp user@host:/path . # Copy from remote

# Telnet (simple, unencrypted)
telnet hostname port    # Test connection
nc -zv hostname port    # Netcat connection test
```

---

## Tips and Tricks

### Command Line Shortcuts

```bash
Ctrl+C      Cancel current command
Ctrl+D      End of input / Logout
Ctrl+Z      Suspend process
Ctrl+L      Clear screen (same as 'clear')
Ctrl+A      Move to start of line
Ctrl+E      Move to end of line
Ctrl+R      Search command history
Tab         Autocomplete filename/command
!!          Repeat last command
!ls         Repeat last ls command
```

### Piping and Redirection

```bash
command > file          # Redirect output to file (overwrite)
command >> file         # Append output to file
command < file          # Use file as input
command1 | command2     # Pipe output to next command
command 2> error.log    # Redirect errors
command 2>&1            # Combine stderr with stdout
```

### Working with Archives

```bash
# TAR compression
tar -czf archive.tar.gz files/  # Create gzip tar
tar -xzf archive.tar.gz         # Extract gzip tar
tar -cbf archive.tar.bz2 files/ # Create bzip2 tar
tar -xbf archive.tar.bz2        # Extract bzip2 tar

# Gzip
gzip file               # Compress file
gunzip file.gz          # Decompress
gzip -d file.gz         # Same as above

# ZIP (if installed)
zip archive.zip files/  # Create zip
unzip archive.zip       # Extract zip
```

### Text Processing

```bash
# AWK - Text processing
awk '{print $1}' file           # Print first column
awk -F: '{print $3}' /etc/hosts # Use : as delimiter

# SED - Stream editor
sed 's/old/new/g' file          # Replace all occurrences
sed -i 's/old/new/g' file       # Edit in place
sed '5d' file                   # Delete line 5
sed -n '1,10p' file             # Print lines 1-10

# GREP - Pattern matching
grep -i "pattern" file          # Case-insensitive
grep -v "pattern" file          # Invert match (exclude)
grep -c "pattern" file          # Count matches
grep "^pattern" file            # Match at start of line
```

### Useful Command Combinations

```bash
# Find and remove files
find . -name "*.tmp" -delete

# List files by size
du -sh * | sort -hr

# Process monitoring
ps aux | grep processname

# Find which process uses a port
netstat -tlnp | grep :8080

# System load average
uptime
cat /proc/loadavg

# Memory usage
free -m
cat /proc/meminfo | head -5
```

### Creating and Editing Files

```bash
# Create empty file
touch filename

# Create/Edit with cat (type text, Ctrl+D to save)
cat > filename
text here
Ctrl+D

# View file with line numbers
cat -n filename
less -N filename

# Edit with nano (simple editor)
nano filename
# Ctrl+X to exit, Y to save

# Edit with vi (advanced editor)
vi filename
# Type 'i' to insert, Esc to exit insert mode, ':wq' to save and quit
```

---

## Environment Variables

```bash
# View environment variables
env
printenv

# Set variable (current session)
export VAR_NAME=value

# Use variable
echo $VAR_NAME

# Common variables
$HOME       # Home directory
$USER       # Current user
$PWD        # Current directory
$SHELL      # Current shell
$TERM       # Terminal type
$PATH       # Command search path
```

---

## Shell Functions and Aliases

```bash
# Create alias (temporary)
alias ll='ls -la'
alias ..='cd ..'

# Use alias
ll

# Remove alias
unalias ll

# View all aliases
alias

# Make aliases permanent:
# Add to ~/.ashrc or /root/.ashrc
```

---

## Troubleshooting

### Common Issues

**Out of disk space**:
```bash
df -h               # Check space
du -sh /var         # Find largest directories
rm -rf /tmp/*       # Clean temp
apt-get clean       # Clean package cache (if apt available)
```

**System can't find command**:
```bash
which command       # Find command location
echo $PATH          # Check search path
type command        # Show command type
```

**Need to become root**:
```bash
# Switch to root
su -                # Requires root password
su - username       # Switch to user

# Run single command as root (v0.4.0+ with sudo)
# sudo command
```

---

## Getting Help

**Built-in help**:
```bash
man command         # Show manual page
help command        # Show help (shell builtin)
command --help      # Show help
command -h          # Short help
```

**In CyberOS**:
- Limited man pages available
- Refer to `/usr/share/doc/` if available
- Check online documentation

---

## Next Steps

- Explore the filesystem
- Try different commands
- Set up your network
- Create user accounts
- Review system logs
- Check available services

---

**Last Updated**: February 16, 2025
**Version 0.1.0-alpha
