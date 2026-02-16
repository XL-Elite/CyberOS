# CyberOS Root Filesystem

This directory contains the root filesystem template and configuration for CyberOS.

## Overview

The root filesystem (rootfs) is the complete directory hierarchy that forms the runtime system, excluding the kernel.

## Directory Structure

```
rootfs/
├── bin/              # User binaries (symlink to /usr/bin)
├── sbin/             # System binaries (symlink to /usr/sbin)
├── lib/              # C library and basic libraries
├── usr/              # User programs and data
│   ├── bin/          # User programs
│   ├── sbin/         # System programs
│   ├── lib/          # Libraries
│   └── share/        # Shared data
├── etc/              # Configuration files
│   ├── inittab       # Init configuration
│   ├── fstab         # Mount table
│   ├── hosts         # Hostname resolution
│   ├── hostname      # System hostname
│   ├── network/      # Network configuration
│   └── init.d/       # Service scripts
├── var/              # Variable data
│   ├── log/          # Log files
│   ├── run/          # Runtime files
│   └── tmp/          # Temporary files
├── home/             # User home directories
├── root/             # Root home directory
├── tmp/              # Temporary files
├── proc/             # Process information (virtual)
├── sys/              # System information (virtual)
├── dev/              # Device files
├── boot/             # Boot files
└── mnt/              # Mount points
```

## Size

- **Base RootFS**: ~50-100 MB (uncompressed)
- **Compressed**: ~20-40 MB with gzip
- **In RAM**: ~64 MB when booted (idle)

## Components

### BusyBox
Provides 100+ Unix utilities in a single ~800KB binary:
- Shell (ash)
- File utilities (cp, mv, rm, etc.)
- Text utilities (grep, sed, awk, etc.)
- System utilities (ps, top, etc.)

### musl libc
Minimal C standard library (~600KB) for program execution.

### System Services
- Init (sysvinit-based)
- logging (syslogd)
- Scheduler (crond - future)
- SSH (v0.4.0+)

## Configuration Files

### /etc/fstab
Filesystem mount table defining what gets mounted at boot:
```
/dev/sda1   /   ext4   defaults,errors=remount-ro    0   1
proc        /proc   proc   defaults                     0   0
sysfs       /sys    sysfs  defaults                     0   0
```

### /etc/inittab
Init system configuration with runlevels:
```
id:3:initdefault:           # Default runlevel 3
si::sysinit:/etc/rc.sysinit # Run at startup
l3:3:wait:/etc/rc.d/rc 3    # Runlevel 3 startup
```

### /etc/hostname
```
cyberos
```

### /etc/network/interfaces
Network configuration:
```
auto eth0
iface eth0 inet dhcp        # Use DHCP for IP
```

## Building RootFS

### Automated Build
```bash
./scripts/build_rootfs.sh
```

### Manual Build

```bash
# Create directory structure
mkdir -p rootfs/{bin,sbin,etc,lib,usr,var,tmp,proc,sys,dev,boot,home,root,mnt}

# Install BusyBox
busybox --install -s rootfs/bin/

# Copy libc
cp /lib64/ld-linux-x86-64.so.2 rootfs/lib/
cp /lib/x86_64-linux-gnu/libc.so.6 rootfs/lib/

# Create essential configuration files
# (see templates in /etc)

# Create device files
mknod rootfs/dev/console c 5 1
mknod rootfs/dev/null c 1 3
```

## Modifying RootFS

### Add Tools
To include additional tools:

1. Add binaries to `bin/` or `usr/bin/`
2. Add libraries to `lib/` or `usr/lib/`
3. Update startup scripts if needed
4. Rebuild ISO: `./scripts/build.sh`

### Change Default Services
Edit `/etc/init.d/rc.sysinit` to modify startup behavior.

### Add Users
```bash
# In running system
adduser newuser
```

## Filesystem Hierarchy Standard (FHS)

CyberOS follows the Linux Filesystem Hierarchy Standard:

| Directory | Purpose |
|-----------|---------|
| `/bin` | Essential command binaries |
| `/sbin` | System command binaries |
| `/etc` | System configuration files |
| `/lib` | Essential libraries |
| `/home` | User home directories |
| `/root` | Root user home |
| `/tmp` | Temporary files (world writable) |
| `/usr` | User programs and data |
| `/var` | Variable data (logs, cache) |
| `/boot` | Boot loader files |
| `/dev` | Device files |
| `/proc` | Process information |
| `/sys` | System kernel interface |

## Permissions

Default permissions are set as follows:

```
/           755     drwxr-xr-x root:root
/root       700     drwx------ root:root
/tmp        1777    drwxrwxrwt root:root
/var/tmp    1777    drwxrwxrwt root:root
/etc        755     drwxr-xr-x root:root
/etc/shadow 640     -rw-r----- root:shadow
```

## Future Enhancements

- **v0.2.0**: Package management system
- **v0.3.0**: GUI libraries and tools
- **v0.4.0**: System service daemons
- **v0.5.0**: Container runtime support

## References

- [Linux FHS](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard)
- [BusyBox](https://busybox.net/)
- [musl libc](https://musl.libc.org/)

---

**Last Updated**: February 16, 2025
