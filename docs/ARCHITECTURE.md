# CyberOS System Architecture

## Table of Contents

1. [Overview](#overview)
2. [System Components](#system-components)
3. [Boot Process](#boot-process)
4. [Filesystem Hierarchy](#filesystem-hierarchy)
5. [Memory Layout](#memory-layout)
6. [Design Decisions](#design-decisions)
7. [Security Architecture](#security-architecture)

---

## Overview

CyberOS is a minimal Linux-based operating system with a focus on:

- **Minimal Resource Usage**: ~150MB installation size
- **Fast Boot**: Target <5 seconds on modern hardware
- **Security-First Design**: Hardened compilation options
- **Educational Purpose**: Clear, documented components
- **Modularity**: Easy to customize and extend

### Architecture Diagram

```
┌─────────────────────────────────────┐
│        CyberOS Architecture         │
├─────────────────────────────────────┤
│  Applications / User Services       │
├─────────────────────────────────────┤
│  C Library (musl libc)              │
├─────────────────────────────────────┤
│  System Utilities (BusyBox)         │
├─────────────────────────────────────┤
│  System Services (init/systemV)     │
├─────────────────────────────────────┤
│  Linux Kernel (6.x LTS)             │
├─────────────────────────────────────┤
│  GRUB2 Bootloader                   │
├─────────────────────────────────────┤
│  BIOS/Firmware                      │
└─────────────────────────────────────┘
```

---

## System Components

### 1. Bootloader: GRUB2

**Purpose**: Loads and executes the Linux kernel

**Features**:
- Menu-driven boot selection
- Configurable timeout (3 seconds default)
- Support for BIOS and UEFI
- Password protection capability
- Multiple boot options

**Location**: `/boot/grub/`

**Configuration**: `/boot/grub/grub.cfg` (auto-generated)

### 2. Linux Kernel

**Version**: 6.x LTS (Long-Term Support)

**Configuration**: Minimal, optimized for:
- Small image size
- Fast boot time
- Common hardware support
- Security hardening

**Location**: `/boot/vmlinuz-6.x`

**Features Included**:
- x86_64 architecture support
- Common storage drivers (ATA, SATA, SCSI)
- Network drivers (e1000, rtl8139, etc.)
- Ext4 filesystem support
- Basic security features

**Features Disabled** (for size):
- IPv6 (can be enabled)
- Advanced debugging
- Unnecessary modules
- GUI/DRM drivers

### 3. C Library: musl libc

**Purpose**: C standard library for user applications

**Why musl**:
- Smaller than glibc (~600KB vs ~2.5MB)
- Static linking support
- Security focus
- Better portable binary compatibility

**Location**: `/lib/ld-musl-x86_64.so.1`

### 4. System Utilities: BusyBox

**Purpose**: Provides essential Unix utilities in a single binary

**Included Utilities**:
```
Core:  ls, cp, mv, rm, mkdir, chmod, chown
Shell: sh, ash (with basic scripting)
Network: ifconfig, ping, telnet, wget, nc
System: ps, top, kill, reboot, shutdown
Text: cat, less, more, sed, awk, grep
```

**Location**: `/bin/busybox` (symlinked to other services)

**Size**: ~800KB (single binary for 100+ utilities)

### 5. Init System: sysvinit

**Purpose**: Process management and service startup

**Components**:
- PID 1 process (init)
- Runlevel support (0-6)
- Service startup scripts (`/etc/init.d/`)
- Inittab configuration

**Runlevels**:
```
0: Halt
1: Single-user mode
2: Multi-user (text)
3: Multi-user (text) - DEFAULT
4: User-defined
5: Multi-user (GUI) - not included in v0.1.0
6: Reboot
```

---

## Boot Process

### Boot Sequence Timeline

```
1. Firmware POST (Power-On Self-Test) [~1 second]
   ↓
2. BIOS loads GRUB2 MBR/GPT [~0.5 seconds]
   ↓
3. GRUB2 initialization [~1 second]
   ├─ Load stage2 from /boot/grub
   ├─ Display menu (3 second timeout)
   └─ Load selected kernel option
   ↓
4. Kernel initialization [~1-2 seconds]
   ├─ Memory setup
   ├─ CPU initialization
   ├─ Interrupt vector setup
   ├─ Filesystem mount
   └─ Root device preparation
   ↓
5. init execution (PID 1) [~1 second]
   ├─ Read /etc/inittab
   ├─ Execute /etc/rc.d/rc.sysinit
   ├─ Run runlevel scripts
   └─ Execute /etc/rc.d/rc.local
   ↓
6. Runlevel services start [~1-2 seconds]
   ├─ Network setup
   ├─ System logging
   ├─ TTY initialization
   └─ User login ready
   ↓
   BOOT COMPLETE (Total: ~5-10 seconds)
```

### Kernel Parameters

Classic kernel boot parameters:

```
root=/dev/sda1              # Root filesystem
ro                          # Mount read-only initially
quiet                       # Suppress boot messages
console=tty0               # Kernel console
console=ttyS0,115200       # Serial console (if enabled)
```

---

## Filesystem Hierarchy

### Standard Directory Structure

```
/
├── bin/          → /usr/bin (symlink)
├── sbin/         → /usr/sbin (symlink)
├── lib/          → Libraries and libc
├── lib64/        → 64-bit libraries
├── usr/
│   ├── bin/      → User binaries
│   ├── sbin/     → System binaries
│   ├── lib/      → User libraries
│   └── share/    → Shared data
├── etc/          → Configuration files
│   ├── inittab
│   ├── fstab
│   ├── hosts
│   ├── hostname
│   ├── network/
│   │   └── interfaces
│   └── init.d/   → Service scripts
├── boot/         → Bootloader and kernel
│   ├── vmlinuz-6.x
│   ├── initramfs
│   └── grub/
├── home/         → User home directories
├── root/         → Root user home
├── tmp/          → Temporary files
├── var/          → Variable data
│   ├── log/      → Log files
│   └── run/      → Runtime files
├── dev/          → Device files
├── proc/         → Process virtual filesystem
├── sys/          → System virtual filesystem
├── run/          → Runtime data
└── mnt/          → Mount points
```

### Key Configuration Files

| File | Purpose |
|------|---------|
| `/etc/hostname` | System hostname |
| `/etc/hosts` | DNS name resolution |
| `/etc/fstab` | Filesystem mount table |
| `/etc/inittab` | Init system configuration |
| `/etc/network/interfaces` | Network configuration |
| `/root/.bashrc` | Root shell configuration |

---

## Memory Layout

### Virtual Memory Layout (32-bit x86 reference)

```
Kernel Space (3GB - 4GB)
├── Kernel Code
├── Kernel Data
├── Dynamic Memory (kmalloc)
└── Paging Structures

│ 3GB Memory Boundary
├───────────────────┤

User Space (0GB - 3GB)
├── Stack (grows down from ~3GB)
│
├── Heap (grows up)
│
├── .bss (uninitialized data)
├── .data (initialized data)
├── .text (code)
└── ELF Header
```

### Physical Memory Usage (Idle System)

```
Total RAM: 1GB allocated

Kernel:           ~50MB (kernel code + fixed structures)
RootFS:          ~30MB (in RAM buffer)
Services:        ~10MB (init, getty, syslogd)
Free/Cache:     ~910MB available
```

---

## Design Decisions

### 1. Linux Kernel 6.x LTS

**Why**: 
- Long-term support (5+ years)
- Recent security patches
- Good hardware compatibility
- Reduced complexity vs. newer versions

### 2. BusyBox Utilities

**Why**:
- Single 800KB binary vs. tens of MB for individual tools
- Sufficient for minimal system operation
- Compatible with standard Unix scripts
- Easy to customize

### 3. musl libc

**Why**:
- Significantly smaller than glibc
- Static linking support
- Security focus
- Faster compilation times

### 4. sysvinit

**Why**:
- Simpler than systemd (especially for minimal systems)
- Easier to understand and modify
- Lightweight
- Suitable for v0.1 alpha release
- Future: systemd alternative in v0.4+

### 5. Ext4 Filesystem

**Why**:
- Good balance of features and simplicity
- Journaling for data integrity
- Good performance
- Wide compatibility
- Alternative: ext3 for older hardware

---

## Security Architecture

### Kernel Security Features

#### Compiled-in Features
- Stack Smashing Protection (SSP/Canary)
- Address Space Layout Randomization (ASLR)
- Executable Space Protection (DEP/NX)
- Limited PTRACE (debugger restrictions)

#### Configuration Hardening
- Minimal module loading
- SELinux/AppArmor: Disabled (planned v0.5+)
- Firewall: Disabled (users must enable)

### File System Security

#### Default Permissions
```
/       755     drwxr-xr-x      root:root
/root   700     drwx------      root:root
/tmp    1777    drwxrwxrwt      root:root
/etc    755     drwxr-xr-x      root:root
/etc/shadow  640   -rw-r-----      root:shadow
```

### User/Group Security

#### Default Setup
```
root:x:0:0      (UID 0, GID 0)
bin:x:1:1       (System users)
sys:x:2:2

root group 0
bin group 1
sys group 2
```

#### Principle of Least Privilege
- No sudo by default (v0.1.0)
- Minimal default services
- Restrictive default permissions

### Update Security

- GPG signature verification for updates (planned)
- Secure package repository (planned v0.2+)
- Security patch delivery mechanism

---

## Performance Characteristics

### Boot Performance

| Metric | Target | Actual |
|--------|--------|--------|
| BIOS POST | 1-2s | 1-2s |
| Bootloader | 1s | 1s |
| Kernel Init | 2-3s | 2-3s |
| Service Start | 1-2s | 1-2s |
| **Total** | **<10s** | **~5-8s** |

### Runtime Performance

| Resource | Idle | Active |
|----------|------|--------|
| CPU | ~0% | <10% (typical) |
| Memory | 64MB | 128-256MB |
| Disk | - | <50 IOPS (typical) |

---

## Future Architecture Changes (v0.2+)

### Planned
- Package manager integration
- More modular kernel configuration
- Additional device driver support
- Service management improvements

### Considered
- systemd migration (v0.4+)
- Container runtime support (v0.5+)
- Advanced security frameworks (v0.5+)

---

## References

- [Linux Kernel Documentation](https://www.kernel.org/doc/)
- [musl libc](https://musl.libc.org/)
- [BusyBox](https://busybox.net/)
- [GRUB Manual](https://www.gnu.org/software/grub/manual/)

---

**Last Updated**: February 16, 2025
**Version**: 0.1.0-alpha
