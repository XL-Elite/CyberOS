# CyberOS Linux Kernel Configuration

This directory contains Linux kernel source and configuration for CyberOS.

## Overview

- **Version**: Linux 6.x LTS (Long-Term Support)
- **Configuration**: Minimal, optimized for size and performance
- **Architecture**: x86-64 (AMD64)
- **Compression**: bzip2

## Directory Structure

```
kernel/
├── .config          # Kernel configuration file (generated)
├── Makefile         # Kernel build system
├── arch/            # Architecture-specific code
├── drivers/         # Device drivers
├── fs/              # Filesystem code
├── net/             # Networking code
└── kernel/          # Core kernel code
```

## Configuration

### Included Features
- Ext4 filesystem support
- Common NIC drivers (e1000, rtl8139, virtio)
- SSD/SATA support
- USB support (basic)
- IPv4 networking
- TCP/IP stack
- Security features (ASLR, DEP, SSP)

### Excluded Features (for size)
- IPv6 (can be enabled)
- Wireless drivers
- Advanced debugging
- Documentation
- Many optional modules

## Building

### From Source

```bash
# Download kernel sources
cd kernel
wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.8.tar.xz
tar -xf linux-6.8.tar.xz

# Configure kernel
make menuconfig          # Interactive configuration
make oldconfig           # Update existing config

# Compile
make bzImage            # Compressed kernel image
make modules            # Build kernel modules

# Install
sudo make install
sudo make modules_install
```

### Via Build Script

```bash
cd ..
./scripts/build_kernel.sh
```

## Configuration File

The minimal `.config` file is ~50KB. Key sections:

- `CONFIG_X86=y` - x86 architecture
- `CONFIG_EXT4_FS=y` - Ext4 support
- `CONFIG_E1000=m` - Intel network driver
- `CONFIG_SECURITY_SMACK=y` - Security attributes
- `CONFIG_SLUB=y` - Memory allocator

## Image Size

The resulting `vmlinuz` compressed kernel is typically:
- **5-8 MB** in size
- Decompresses to ~15-20 MB in memory

## Kernel Parameters

Available boot parameters (in GRUB):
- `ro` - Read-only mount
- `root=/dev/...` - Root device
- `console=...` - Console output
- `nousb` - Disable USB
- `nomsi` - Disable MSI interrupts

## Customization

To add/modify features:

```bash
# Use menuconfig for interactive
make menuconfig

# Or enable specific options
./scripts/enable_feature.sh feature_name

# Rebuild
make clean
make bzImage
```

## Debugging Kernel

### Boot Parameters
```
debug          # Enable debugging
loglevel=7     # Maximum logging
```

### Live Debugging
```bash
# Enable sysrq-key
echo 1 > /proc/sys/kernel/sysrq

# Show kernel log buffer
dmesg
cat /proc/cmdline      # Boot parameters used
```

## References

- [Linux Kernel Documentation](https://www.kernel.org/doc/)
- [Kernel Newbies](https://kernelnewbies.org/)
- [Linux Kernel Development](https://www.kernel.org/doc/html/latest/process/development-process.html)
- [Kernel Config Options](https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html)

## Version History

- **v0.1.0**: Linux 6.8 LTS baseline
- **v0.2.0**: Additional driver support
- **v0.3.0**: GUI driver support
- **v1.0.0**: Hardware optimization

---

**Last Updated**: February 16, 2025
