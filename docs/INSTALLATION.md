# CyberOS Installation Guide

## Table of Contents

1. [Pre-Installation](#pre-installation)
2. [Download](#download)
3. [VirtualBox Installation](#virtualbox-installation)
4. [KVM/QEMU Installation](#kvmqemu-installation)
5. [Initial Setup](#initial-setup)
6. [Post-Installation](#post-installation)
7. [Troubleshooting](#troubleshooting)

---

## Pre-Installation

### System Requirements

#### Minimum
- **CPU**: 64-bit x86 processor
- **RAM**: 256 MB
- **Storage**: 512 MB free space
- **Boot**: BIOS/Legacy boot support

#### Recommended
- **CPU**: 64-bit x86 processor
- **RAM**: 1 GB
- **Storage**: 5-10 GB SSD space
- **Network**: Ethernet or WiFi adapter

### Supported Hypervisors

✅ **Fully Supported**
- VirtualBox 6.0, 6.1, 7.0+
- KVM/QEMU (Linux hosts)
- Proxmox VE 7.0+

⚠️ **Partially Tested**
- VMware Workstation/Player
- Hyper-V (basic functionality)

### Prerequisites

1. **Virtualization Software**: Install VirtualBox or KVM
2. **ISO Image**: Download CyberOS installation media
3. **Storage**: Prepare disk space for VM

---

## Download

### Getting the ISO

```bash
# Option 1: Download from GitHub Releases
wget https://github.com/XL-Elite/CyberOS/releases/download/v0.1.0/cyberos-0.1.0-alpha.iso

# Option 2: Build from source
git clone https://github.com/XL-Elite/CyberOS.git
cd CyberOS
./scripts/build.sh
# ISO will be in ./iso/cyberos.iso
```

### Verify Integrity

```bash
# Download checksum file
wget https://github.com/XL-Elite/CyberOS/releases/download/v0.1.0/cyberos-0.1.0-alpha.iso.sha256

# Verify
sha256sum -c cyberos-0.1.0-alpha.iso.sha256
```

---

## VirtualBox Installation

### Step 1: Create Virtual Machine

1. Open VirtualBox
2. Click "New" or press Ctrl+N
3. Configure VM:
   ```
   Name: CyberOS
   Machine Folder: [Your preferred location]
   Type: Linux
   Version: Linux 2.6 / 3.x / 4.x (64-bit)
   ```
4. Click "Next"

### Step 2: Allocate Resources

1. **Memory**: Set to 1024 MB (minimum 256 MB)
2. Click "Next"
3. **Virtual Hard Disk**:
   - Select "Create a virtual hard disk now"
   - Type: VDI (VirtualBox Disk Image)
   - Storage: Dynamically allocated
   - Size: 5 GB minimum
4. Click "Create"

### Step 3: Configure Settings

1. Right-click VM → "Settings"
2. **System**:
   - Processor: Assign 2 vCPUs
   - Enable PAE/NX
   - Disable 3D Acceleration
3. **Storage**:
   - Click empty IDE controller
   - Select CyberOS ISO
4. **Network**:
   - Adapter 1: Bridged or NAT
4. Click "OK"

### Step 4: Boot and Install

1. Double-click the CyberOS VM
2. Machine boots from ISO
3. Follow installation wizard:
   ```
   Welcome Screen
   ↓ Press Enter to continue
   
   Keyboard Layout
   ↓ Select your layout
   
   Hostname
   ↓ Enter: cyberos
   
   Network Configuration
   ↓ Choose: Auto (DHCP) or Manual
   
   Disk Partitioning
   ↓ Select: Automatic (Whole Disk)
   
   User Account
   ↓ Username: admin
   ↓ Password: [create password]
   
   Confirm and Install
   ↓ Press Enter to start installation
   ```
4. Wait for installation to complete
5. Machine automatically reboots
6. Login with your credentials

### Step 5: Post-Install

1. **Install Guest Additions** (optional but recommended):
   ```bash
   su - root
   apt-get update
   apt-get install virtualbox-guest-x11
   reboot
   ```

2. **Enable Shared Clipboard** (optional):
   - Right-click VM → Devices → Shared Clipboard → Bidirectional

---

## KVM/QEMU Installation

### Step 1: Prepare Environment

```bash
# Install KVM/QEMU
sudo apt-get install qemu-system-x86 libvirt-daemon virt-manager

# Verify installation
kvm --version
virsh list
```

### Step 2: Create VM

```bash
# Create VM disk
qemu-img create -f qcow2 ~/cyberos.qcow2 5G

# Launch VM with QEMU directly
qemu-system-x86_64 \
  -m 1024 \
  -smp 2 \
  -hda ~/cyberos.qcow2 \
  -cdrom ~/cyberos-0.1.0-alpha.iso \
  -boot d \
  -net nic,model=rtl8139 \
  -net user,hostfwd=tcp::2222-:22 \
  -enable-kvm

# Or use virt-manager for GUI
virt-manager
```

### Step 3: Follow Installation

- Same steps as VirtualBox (see above)

### Step 4: Boot from Disk

After installation:
```bash
qemu-system-x86_64 \
  -m 1024 \
  -smp 2 \
  -hda ~/cyberos.qcow2 \
  -net nic,model=rtl8139 \
  -net user,hostfwd=tcp::2222-:22 \
  -enable-kvm
```

---

## Initial Setup

### First Boot Tasks

1. **Update System**
   ```bash
   apt-get update
   apt-get upgrade
   ```

2. **Configure Network** (if not automatic)
   ```bash
   # Edit network config
   nano /etc/network/interfaces
   
   # Add or modify:
   auto eth0
   iface eth0 inet dhcp
   
   # Restart networking
   /etc/init.d/networking restart
   ```

3. **Set Timezone**
   ```bash
   timedatectl set-timezone [Zone/Region]
   # e.g., timedatectl set-timezone America/New_York
   ```

4. **Change Root Password** (recommended)
   ```bash
   passwd root
   ```

### Enable SSH (Optional)

```bash
# SSH is NOT installed by default
# Install OpenSSH (available in v0.4.0+)
# Or use console access

# Test network connectivity
ping 8.8.8.8
ping google.com
```

---

## Post-Installation

### Recommended Optimizations

1. **Reduce Boot Time**
   ```bash
   # Remove unnecessary services
   update-rc.d service_name disable
   ```

2. **Optimize Disk Space**
   ```bash
   # Clean package cache
   apt-get clean
   apt-get autoclean
   ```

3. **Enable Guest Tools**
   ```bash
   # For VirtualBox ONLY
   su - root
   # Insert Guest Additions CD
   mount /media/cdrom
   ./autorun.sh
   ```

### Snapshot (Recommended)

Create a VM snapshot before making changes:

**VirtualBox**:
- Machine → Take Snapshot
- Name: "Base Installation"

**KVM/QEMU**:
```bash
qemu-img snapshot -c base_snapshot ~/cyberos.qcow2
```

---

## Troubleshooting

### Boot Issues

#### Problem: "Cannot boot from ISO"
**Solution**:
1. Shut down VM
2. Settings → Storage
3. Ensure ISO is in IDE/SATA controller
4. Reboot

#### Problem: "Boot timeout"
**Solution**:
1. Extended timeout - this is normal on first boot
2. Check BIOS settings - enable legacy boot if needed
3. Ensure sufficient RAM allocated

### Network Issues

#### Problem: "No internet connection"
**Solution**:
```bash
# Check network interface
ip link show

# Check IP assignment
ip addr show

# Request DHCP lease
dhclient eth0

# Check routing
ip route show

# Manual IP assignment
ifconfig eth0 192.168.1.X netmask 255.255.255.0
route add default gw 192.168.1.1
```

### Display Issues

#### Problem: "Low resolution (640x480)"
**Solution**:
1. VirtualBox: Guest Additions required (see above)
2. KVM: QEMU uses VESA driver - add:
   ```
   -vga std
   ```

### Disk Issues

#### Problem: "Disk full"
**Solution**:
```bash
# Check disk usage
df -h

# Find large files
du -sh /* | sort -rh

# Clean cache
apt-get clean
```

### VM Performance

#### Problem: "Slow performance"
**Solution**:
1. Allocate more CPU cores (Settings → Processor)
2. Allocate more RAM (Settings → Memory)
3. Ensure enable-kvm is used for KVM
4. Check host system resources

---

## Getting Help

### Documentation

- [Main README](../README.md)
- [Architecture Guide](ARCHITECTURE.md)
- [User Manual](USER_MANUAL.md)
- [FAQ](FAQ.md)

### Support

- **Issues**: [GitHub Issues](https://github.com/XL-Elite/CyberOS/issues)
- **Discussions**: [GitHub Discussions](https://github.com/XL-Elite/CyberOS/discussions)
- **Email**: support@cyberos.dev

---

## Next Steps

After successful installation:

1. Read [USER_MANUAL.md](USER_MANUAL.md)
2. Explore system commands and utilities
3. Review [ARCHITECTURE.md](ARCHITECTURE.md)
4. Join community discussions
5. Report issues or suggest improvements

---

**Last Updated**: February 16, 2025
**Version**: 0.1.0-alpha
