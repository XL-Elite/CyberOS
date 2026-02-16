# CyberOS Release Notes & Version History

## Latest Release

### v0.1.0 - Alpha Release
**Release Date**: February 28, 2025 (Target)  
**Status**: 🔴 In Development

---

## Release History

### v0.1.0 - Alpha (Current Development)

**Codename**: "Genesis"

#### Overview
The inaugural release of CyberOS - a minimal, educational Linux operating system designed for virtualization environments. This alpha release establishes the core architecture and demonstrates proof-of-concept functionality.

#### System Requirements
- **Processor**: 64-bit x86 (Intel/AMD)
- **RAM**: 256MB minimum (1GB recommended)
- **Disk**: 512MB minimum (5GB recommended)
- **Hypervisor**: VirtualBox 6.0+, KVM/QEMU, or equivalent
- **Boot Type**: BIOS/Legacy or UEFI

#### Features Included ✅

**Core System**
- Linux 6.8 LTS kernel (minimal configuration)
- GRUB2 bootloader with menu system
- BusyBox-based root filesystem
- musl libc C library
- sysvinit initialization system

**Utilities & Tools**
- Basic shell (ash/bash)
- Standard Unix utilities
- Network utilities (ping, ifconfig, etc.)
- Text editors (nano, vi)
- File management tools

**Installation**
- Text-based installer
- VirtualBox Guest Additions support
- Basic network configuration
- User account creation

**Development**
- Complete documentation
- Web dashboard (HTML/CSS/JS)
- Build system
- GitHub repository

#### Known Issues 🐛

1. **Boot Time**: Initial boot may take 10-15 seconds in VirtualBox
   - *Workaround*: Normal performance after first boot

2. **Resolution**: Default resolution may be 640x480
   - *Workaround*: Adjust VM display settings manually

3. **Network Configuration**: Must be done manually via CLI
   - *Workaround*: Use `ip` command or edit /etc/network/interfaces

#### Known Limitations ⚠️

- Single-user system (multi-user in v0.2.0)
- No GUI/desktop environment (planned for v0.3.0)
- Limited hardware support (expanding in v0.4.0)
- Minimal package availability (addressed in v0.2.0)
- No SSH by default (added in v0.4.0)
- No container support (planned for v0.5.0)

#### Installation Instructions

1. Download CyberOS v0.1.0 ISO
2. Create new VirtualBox VM:
   - RAM: 1GB
   - Storage: 5GB
   - Network: Bridged or NAT
3. Boot from ISO
4. Follow installation wizard
5. Reboot and login (default: root/cyberos)

#### Upgrade Path

**From other systems**: Clean installation required

**To v0.2.0**: Manual upgrade or clean installation recommended

#### Security Considerations

- Default root password: **MUST BE CHANGED** on first login
- No firewall enabled by default
- SELinux/AppArmor not included (v0.5.0+)
- Keep updated with security patches

#### Performance Metrics

| Metric | Value |
|--------|-------|
| Boot Time | ~5-15 seconds |
| Memory Usage (Idle) | ~64MB |
| Disk Space (Minimal) | ~150MB |
| Installation Time | ~2-3 minutes |

#### Download Links

- **ISO Image**: [cyberos-0.1.0-alpha.iso](https://github.com/XL-Elite/CyberOS/releases/download/v0.1.0/cyberos-0.1.0-alpha.iso)
- **SHA256 Checksum**: [cyberos-0.1.0-alpha.iso.sha256](https://github.com/XL-Elite/CyberOS/releases/download/v0.1.0/cyberos-0.1.0-alpha.iso.sha256)
- **Size**: ~180MB

#### Supported Platforms

✅ **Fully Supported**
- VirtualBox 6.0, 6.1, 7.0+
- KVM/QEMU
- Proxmox VE

⚠️ **Partially Supported**
- VMware Workstation (basic functionality)
- Hyper-V (untested)

#### Installation HowTo

See [docs/INSTALLATION.md](docs/INSTALLATION.md)

#### Frequently Asked Questions

See [docs/FAQ.md](docs/FAQ.md)

---

## Upcoming Releases

### v0.2.0 - Package Manager Edition
**Target**: March 31, 2025  
**Codename**: "Repository"

**Planned Features**:
- CyberPKG package manager
- Package repository system
- 50+ essential packages
- System update mechanism

### v0.3.0 - Desktop Edition
**Target**: April 30, 2025  
**Codename**: "Interface"

**Planned Features**:
- Lightweight GUI environment
- VNC remote access
- File manager and terminal
- Theme customization

### v0.4.0 - Services Edition
**Target**: May 31, 2025  
**Codename**: "Services"

**Planned Features**:
- Service management system
- SSH server
- Firewall
- System monitoring

### v0.5.0 - Enterprise Edition
**Target**: June 30, 2025  
**Codename**: "Enterprise"

**Planned Features**:
- Container support
- Security hardening
- Clustering capabilities
- Advanced monitoring

### v1.0.0 - Stable Release
**Target**: August 31, 2025  
**Codename**: "Stable"

**Support**: Long-term support until August 2028

---

## Support Matrix

| Version | Release Date | End of Support | Status | Download |
|---------|--------------|----------------|--------|----------|
| 0.1.0   | Feb 28, 2025 | May 28, 2025   | 🔴 Alpha | [ISO](https://github.com/XL-Elite/CyberOS/releases) |
| 0.2.0   | Mar 31, 2025 | Jun 30, 2025   | 📋 Planned | TBD |
| 0.3.0   | Apr 30, 2025 | Jul 31, 2025   | 📋 Planned | TBD |
| 0.4.0   | May 31, 2025 | Aug 31, 2025   | 📋 Planned | TBD |
| 0.5.0   | Jun 30, 2025 | Sep 30, 2025   | 📋 Planned | TBD |
| 1.0.0   | Aug 31, 2025 | Aug 31, 2028   | 📋 Planned | TBD |

---

## Changelog

### v0.1.0 (Initial Release)

**Added**:
- Initial project structure
- GRUB2 bootloader configuration
- Linux kernel build configuration
- BusyBox integration
- RootFS hierarchy
- Build system scripts
- Web dashboard (HTML/CSS/JS)
- Comprehensive documentation
- GitHub repository setup

**Fixed**:
- N/A (Initial release)

**Security**:
- Secure boot capability
- Basic file permissions
- User/group system

**Deprecated**:
- N/A (Initial release)

**Known Issues**:
- See Known Issues section above

---

## Migration Guides

### Upgrading from Alpha to Beta (v0.1 → v0.2)

Coming soon with v0.2.0 release.

### Upgrading between Minor Versions

Minor version upgrades will be incremental and backward-compatible.

### Downgrading

Not recommended. Each version offers distinct features.

---

## Troubleshooting Release-Specific Issues

### V0.1.0 Troubleshooting

**Issue**: Won't boot in VirtualBox
- **Solution**: Ensure BIOS boot is selected, not UEFI

**Issue**: Network not connecting
- **Solution**: Manual configuration required - see docs/NETWORK.md

**Issue**: Screen resolution too low
- **Solution**: Adjust VM display settings or install Guest Additions

---

## Community Contributions

Thanks to all contributors in v0.1.0:
- [Contributors to be listed after initial release]

## Feedback & Bug Reports

- **Issues**: [GitHub Issues](https://github.com/XL-Elite/CyberOS/issues)
- **Discussions**: [GitHub Discussions](https://github.com/XL-Elite/CyberOS/discussions)
- **Email**: releases@cyberos.dev

---

## Archive

Previous releases and older versions will be available in the [releases archive](https://github.com/XL-Elite/CyberOS/releases).

---

**Release Manager**: CyberOS Development Team  
**Last Updated**: February 16, 2025  
**Next Review**: February 28, 2025
