# CyberOS - Frequently Asked Questions (FAQ)

## General Questions

### Q: What is CyberOS?
A: CyberOS is a minimal, lightweight Linux operating system designed for educational purposes, embedded systems, and virtualization environments. It's built on proven open-source technologies (Linux kernel, GRUB2, BusyBox) with a focus on security, performance, and simplicity.

### Q: Why should I use CyberOS?
A: CyberOS is ideal if you:
- Want to learn about OS internals
- Need a lightweight, fast-booting system
- Are studying Linux administration
- Need a minimal base for embedded projects
- Want to understand each component

### Q: How is CyberOS different from other Linux distributions?
A: CyberOS is:
- **Minimal**: ~150MB vs. 2-5GB for mainstream distros
- **Fast**: <10 second boot vs. 30-60 seconds
- **Educational**: Well-documented internals
- **Modular**: Easy to customize
- **Single-focused**: Not trying to be everything to everyone

### Q: Is CyberOS production-ready?
A: Currently (v0.1.0), CyberOS is in **Alpha** and suitable for:
- Learning and experimentation
- Development and testing
- Educational projects

Not recommended for production use until v1.0.0 stable release (August 2025).

---

## Installation & Setup

### Q: What are the minimum system requirements?
A:
- CPU: 64-bit x86 processor
- RAM: 256 MB minimum (1GB recommended)
- Storage: 512MB minimum (5GB recommended)
- Hypervisor: VirtualBox, KVM, or equivalent

### Q: Can I install CyberOS on real hardware?
A: Yes, CyberOS can be installed on real hardware with:
- x86-64 architecture
- BIOS or UEFI firmware
- USB boot capability

However, v0.1.0 is optimized for virtual machines. Real hardware support will be improved in future releases.

### Q: Which virtualization platforms are supported?
A:
**Fully Supported**:
- VirtualBox 6.0+
- KVM/QEMU
- Proxmox VE

**Partially Supported**:
- VMware Workstation/Player
- Hyper-V

### Q: How do I build CyberOS from source?
A:
```bash
git clone https://github.com/XL-Elite/CyberOS.git
cd CyberOS
./scripts/build.sh
```
See [BUILD.md](../docs/BUILD.md) for detailed instructions.

### Q: Where is the ISO download?
A: Download from [GitHub Releases](https://github.com/XL-Elite/CyberOS/releases)

### Q: What's the default password?
A: Default credentials (for v0.1.0):
- Username: `root`
- Password: `cyberos`

**IMPORTANT**: Change these immediately after first login.

---

## Usage & Operations

### Q: What shell does CyberOS use?
A: BusyBox `ash` (compatible POSIX shell). It's lightweight and suitable for scripting.

### Q: How do I configure the network?
A:
```bash
# Edit network configuration
nano /etc/network/interfaces

# Add interface configuration, e.g.:
auto eth0
iface eth0 inet dhcp

# Apply changes
/etc/init.d/networking restart

# Or use ip command
ip address add 192.168.1.10/24 dev eth0
ip route add default via 192.168.1.1
```

### Q: How do I shut down CyberOS?
A:
```bash
shutdown -h now    # Halt immediately
shutdown -r now    # Reboot immediately
poweroff           # Power off
reboot             # Reboot
```

### Q: How do I check system information?
A:
```bash
uname -a                    # Kernel info
cat /proc/cpuinfo          # CPU information
free -m                    # Memory usage
df -h                      # Disk usage
ps aux                     # Running processes
```

### Q: Can I install additional packages?
A: In v0.1.0, package management is minimal. v0.2.0 will introduce a proper package manager.

For now, you can:
- Build from source
- Use cross-compilation toolchain
- Manual installation of binaries

---

## System Administration

### Q: How do I change the hostname?
A:
```bash
# Edit hostname file
echo "newhostname" > /etc/hostname

# Apply immediately
hostname newhostname
```

### Q: How do I manage services?
A:
```bash
# Start a service
/etc/init.d/servicename start

# Stop a service
/etc/init.d/servicename stop

# Restart a service
/etc/init.d/servicename restart

# Check service status
/etc/init.d/servicename status

# Enable at boot
update-rc.d servicename defaults

# Disable at boot
update-rc.d servicename disable
```

### Q: How do I view system logs?
A:
```bash
# View system log
cat /var/log/syslog

# View kernel messages
dmesg

# Use tail for real-time
tail -f /var/log/syslog
```

### Q: How do I access SSH (remote login)?
A: SSH is not included in v0.1.0. It will be added in v0.4.0 (Services Release).

For now, use console access or serial connection.

### Q: How do I resize the filesystem?
A:
```bash
# For ext4 on growing disk
resize2fs /dev/sda1

# For LVM (if applicable)
lvresize -L +5G /dev/vg/lv_root
resize2fs /dev/vg/lv_root
```

---

## Troubleshooting

### Q: Boot hangs at GRUB menu
A: 
- Press Enter to continue
- Check timeout setting in `/boot/grub/grub.cfg`
- Verify ISO integrity if freshly downloaded

### Q: "No space left on device"
A:
```bash
df -h                      # Check disk usage
du -sh /*                  # Find large directories
apt-get clean              # Clean package cache
```

### Q: Network not working
A:
```bash
# Check interface status
ip link show

# Manual IP assignment
ip address add 192.168.1.X/24 dev eth0
ip route add default via 192.168.1.1

# Test connectivity
ping 8.8.8.8
```

### Q: SSH connections fail
A: SSH not available in v0.1.0. Use console or VNC instead.

### Q: Guest Additions not working (VirtualBox)
A:
```bash
# First, install if not already done:
apt-get update
apt-get install virtualbox-guest-x11

# Rebuild if needed:
/opt/VBoxGuestAdditions-*/init/vboxadd setup
```

### Q: Low resolution (640x480)
A:
- **VirtualBox**: Install Guest Additions (see above)
- **KVM**: Use `-vga std` parameter

### Q: System very slow
A:
1. Add more CPU cores (VM Settings)
2. Allocate more RAM
3. Check for runaway processes: `ps aux | sort -k3 -rn`
4. Check disk I/O: `iostat 1`

---

## Development & Building

### Q: How do I contribute?
A: See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Q: Can I modify the kernel?
A: Yes! The kernel source is in `/workspaces/CyberOS/kernel/`.

```bash
# Rebuild kernel
./scripts/build_kernel.sh

# Create new ISO
./scripts/create_iso.sh
```

### Q: How can I add new packages?
A: In v0.1.0: Manual compilation
In v0.2.0+: Package manager integration

### Q: Where can I find documentation?
A:
- Main README: [README.md](../README.md)
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- Installation: [INSTALLATION.md](INSTALLATION.md)
- Build Process: [BUILD.md](BUILD.md) (coming soon)

### Q: How do I report bugs?
A: 
1. Check [GitHub Issues](https://github.com/XL-Elite/CyberOS/issues)
2. Provide detailed reproduction steps
3. Include system information
4. Attach logs if relevant

---

## Licensing & Legal

### Q: What's the license?
A: CyberOS uses multiple licenses:
- Kernel: GPL v2
- Bootloader: Apache 2.0
- Utilities: MIT
- Documentation: CC BY-SA 4.0

See [LICENSE](../LICENSE) for details.

### Q: Can I modify and distribute CyberOS?
A: Yes, per the individual component licenses. Please:
- Acknowledge the original project
- Provide source code access
- Follow license terms

### Q: Can I use CyberOS commercially?
A: Yes, with appropriate licensing compliance:
- Ensure GPL v2 compliance for kernel modifications
- Respect other component licenses
- Consult LICENSE file

---

## Contributing & Community

### Q: How do I get involved?
A:
1. Join discussions: [GitHub Discussions](https://github.com/XL-Elite/CyberOS/discussions)
2. Report issues: [GitHub Issues](https://github.com/XL-Elite/CyberOS/issues)
3. Submit code: Follow [CONTRIBUTING.md](../CONTRIBUTING.md)

### Q: Where can I ask questions?
A:
- **Discussions**: GitHub Discussions (recommended)
- **Issues**: GitHub Issues (for bugs)
- **Email**: support@cyberos.dev

### Q: How often are releases?
A:
- v0.1.0: February 2025
- v0.2.0: March 2025
- Monthly release cycle until v1.0.0 (August 2025)
- Then standard release cycles

---

## Features & Roadmap

### Q: When will [feature X] be available?
A: Check [ROADMAP.md](../ROADMAP.md) for planned features and timelines.

### Q: Why no GUI in v0.1.0?
A: To minimize installation size and boot time. GUI planned for v0.3.0 (April 2025).

### Q: Will CyberOS support containers?
A: Yes, Docker/container support planned for v0.5.0 (June 2025).

### Q: Can I use this for server deployments?
A: v0.1.0 is not recommended for production. v1.0.0 (August 2025) will be suitable for lightweight server use.

---

## Performance & Optimization

### Q: How can I optimize boot time?
A:
```bash
# Use bootchart to profile:
# (Not available in v0.1.0)

# Remove unnecessary services:
update-rc.d servicename disable
```

### Q: What's a typical boot time?
A: ~5-10 seconds from power-on to login prompt on modern hardware.

### Q: Can I run desktop applications?
A: v0.1.0 is CLI only (no X11/GUI). GUI support coming in v0.3.0.

---

## Getting Help

### Q: Where's the documentation?
A:
- [Main Documentation](../docs/)
- [README](../README.md)
- [Installation Guide](INSTALLATION.md)
- [Architecture](ARCHITECTURE.md)

### Q: How do I report security issues?
A: Email security@cyberos.dev with details.

### Q: Where's the issue tracker?
A: [GitHub Issues](https://github.com/XL-Elite/CyberOS/issues)

---

## Still Have Questions?

- Check the [Main README](../README.md)
- Browse [GitHub Issues](https://github.com/XL-Elite/CyberOS/issues)
- Join [GitHub Discussions](https://github.com/XL-Elite/CyberOS/discussions)
- Email: support@cyberos.dev

---

**Last Updated**: February 16, 2025
**Version**: 0.1.0-alpha FAQ
