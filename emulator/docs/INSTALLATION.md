# CyberOS Emulator Installation Guide

Complete setup instructions for CyberOS Emulator on macOS, Linux, and Windows.

## Table of Contents

- [macOS Installation](#macos-installation)
- [Linux Installation](#linux-installation)
- [Windows Installation](#windows-installation)
- [GUI Setup](#gui-setup)
- [Troubleshooting](#troubleshooting)

---

## macOS Installation

### Prerequisites

- macOS 10.14 or later
- Homebrew package manager
- At least 2 GB free RAM (recommended: 4 GB+)

### Step 1: Install Homebrew

If you don't have Homebrew installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Automatic Installation

Run the automatic setup script:

```bash
cd /path/to/CyberOS/emulator/macos
chmod +x install_dependencies.sh
./install_dependencies.sh
```

This will:
- Install QEMU
- Create VM directory (`~/.cyberos/vms`)
- Create configuration file (`~/.cyberos_vm.conf`)
- Set up launch scripts

### Step 3: Manual Installation (Alternative)

If you prefer to install manually:

```bash
# Install QEMU
brew install qemu

# Verify installation
qemu-system-x86_64 --version

# Create directories
mkdir -p ~/.cyberos/vms

# Make scripts executable
chmod +x emulator/macos/run_cyberos.sh
chmod +x emulator/gui/cyberos_emulator.py
```

### Step 4: Verify Installation

```bash
# Check QEMU installation
which qemu-system-x86_64

# Check Python
python3 --version

# Run diagnostic
./emulator/macos/run_cyberos.sh --check
```

---

## Linux Installation

### Prerequisites

- Ubuntu 20.04 LTS or later (tested on 20.04, 22.04, 24.04)
- Sudo privileges for dependency installation
- At least 2 GB free RAM (recommended: 4 GB+)
- For KVM: Intel VT-x or AMD-V CPU support

### Step 1: Automatic Installation

Run the automatic setup script with sudo:

```bash
cd /path/to/CyberOS/emulator/linux
sudo chmod +x install_dependencies.sh
sudo ./install_dependencies.sh
```

This will:
- Install QEMU and KVM
- Set up KVM access for your user
- Create VM directory (`~/.cyberos/vms`)
- Create configuration file (`~/.cyberos_vm.conf`)
- Install Python 3 and tkinter

### Step 2: Manual Installation (Alternative)

If you prefer to install manually on Ubuntu/Debian:

```bash
# Update package lists
sudo apt-get update

# Install dependencies
sudo apt-get install -y \
    qemu-system-x86 \
    qemu-utils \
    qemu-kvm \
    libvirt-clients \
    python3 \
    python3-tk

# Create directories
mkdir -p ~/.cyberos/vms

# Make scripts executable
chmod +x emulator/linux/run_cyberos.sh
chmod +x emulator/gui/cyberos_emulator.py

# (Optional) Add user to KVM group for KVM without sudo
sudo usermod -a -G kvm $USER
# Log out and log back in for group changes to take effect
```

### Step 3: Verify KVM Support

Check if your CPU supports KVM:

```bash
# Check for KVM device
[ -c /dev/kvm ] && echo "KVM supported" || echo "KVM not supported"

# Check CPU flags
grep -E "vmx|svm" /proc/cpuinfo | head -1
```

If KVM is not available, the emulator will fall back to TCG (slower but still functional).

### Step 4: Verify Installation

```bash
# Check QEMU installation
which qemu-system-x86_64

# Check KVM
[ -c /dev/kvm ] && echo "KVM available"

# Check Python
python3 --version

# Run diagnostic
./emulator/linux/run_cyberos.sh --check
```

---

## Windows Installation

### Using WSL 2 (Recommended)

If you have Windows 11, you can use WSL 2 (Windows Subsystem for Linux):

```powershell
# Install WSL 2 with Ubuntu
wsl --install -d Ubuntu-22.04

# Inside WSL, follow the Linux instructions above
```

### Using QEMU Directly

For native Windows installation:

1. Download QEMU for Windows: https://www.qemu.org/download/#windows

2. Run the installer and follow the setup wizard

3. Add QEMU to your PATH:
   - Right-click "This PC" or "My Computer" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", click "New"
   - Variable name: `QEMU_PATH`
   - Variable value: `C:\Program Files\QEMU` (or your installation path)
   - Click OK and restart your terminal

4. Verify installation:
   ```cmd
   qemu-system-x86_64 --version
   ```

5. Make scripts executable:
   ```cmd
   # You can run the Linux/macOS scripts in PowerShell or Git Bash
   # Or write .bat file equivalents
   ```

---

## GUI Setup

### macOS / Linux

The GUI application uses Python tkinter (included on most systems).

#### Verify tkinter is installed:

**macOS:**
```bash
python3 -c "import tkinter; print('Tkinter OK')"

# If missing, install via Homebrew:
brew install python-tk
```

**Linux:**
```bash
python3 -c "import tkinter; print('Tkinter OK')"

# If missing, install via apt:
sudo apt-get install python3-tk
```

#### Launch GUI:

```bash
cd /path/to/CyberOS
python3 emulator/gui/cyberos_emulator.py
```

The GUI provides:
- Easy VM configuration
- One-click launch
- Console output
- VM management
- Save/load configurations

---

## Troubleshooting

### QEMU Not Found on macOS

**Problem:** `qemu-system-x86_64: command not found`

**Solution:**
```bash
# Reinstall QEMU
brew uninstall qemu
brew install qemu

# Verify
which qemu-system-x86_64
```

### Permission Denied on Linux

**Problem:** `Permission denied: /dev/kvm`

**Solution:**
```bash
# Add your user to the kvm group
sudo usermod -a -G kvm $USER

# Log out and log back in, then verify
[ -r /dev/kvm ] && echo "KVM access OK"

# Or use the launcher with the --no-kvm flag
./run_cyberos.sh --no-kvm
```

### ISO File Not Found

**Problem:** `ISO file not found: iso/cyberos-0.1.0-alpha.iso`

**Solution:**
```bash
# Build the ISO first
cd /path/to/CyberOS
./scripts/build.sh

# Verify ISO was created
ls -lh iso/cyberos-*.iso
```

### Tkinter Import Error

**Problem:** `ModuleNotFoundError: No module named 'tkinter'`

**macOS:**
```bash
# Install Python with tkinter support
brew install python-tk@3.11

# Or use system Python
/usr/bin/python3 emulator/gui/cyberos_emulator.py
```

**Linux:**
```bash
# Install tkinter
sudo apt-get install python3-tk

# If that doesn't work, try python3-tk with your specific version
sudo apt-get install python3.10-tk  # for Python 3.10
```

### GUI Doesn't Display on macOS

**Problem:** GUI window doesn't appear

**Solution:**
```bash
# Grant Python permission in Privacy settings
# System Settings → Privacy & Security → Accessibility → Add Python

# Or use command-line interface instead
./emulator/macos/run_cyberos.sh -c 4 -m 1024
```

### Slow Performance

**Problem:** VM runs very slowly

**Solutions:**

1. **Enable KVM (Linux only):**
   ```bash
   # Verify KVM is enabled
   [ -c /dev/kvm ] && echo "KVM enabled"
   
   # If not enabled, run launcher without --no-kvm
   ./emulator/linux/run_cyberos.sh -c 4 -m 1024
   ```

2. **Allocate more resources:**
   ```bash
   # Use more CPU cores and RAM
   ./emulator/macos/run_cyberos.sh -c 4 -m 2048
   ```

3. **Check host system:**
   - Close other applications
   - Monitor system resources (Activity Monitor on macOS, top on Linux)
   - Ensure sufficient disk space for VM image

### Network Not Working

**Problem:** Networking doesn't work inside CyberOS

**Solution:**
```bash
# Enable networking when launching
./emulator/macos/run_cyberos.sh -n

# Or enable in GUI:
# 1. Check "Enable Networking" checkbox
# 2. Click "Launch CyberOS"
```

### VNC Connection Issues

**Problem:** Can't connect to VNC display

**Solution:**
```bash
# Start with VNC display
./emulator/macos/run_cyberos.sh --display vnc

# Connect to VNC server (default port 5900)
# macOS: open vnc://localhost:5900
# Linux: vncviewer localhost:5900
# Or use any VNC client: RealVNC, TigerVNC, etc.
```

### Host Keyboard/Mouse Issues

**Problem:** Keyboard/mouse not responding in VM

**Solution:**
- Click inside the VM window to give it focus
- Press Ctrl+Alt+G (or Ctrl+Alt on some systems) to release mouse
- Use USB passthrough if available:
  ```bash
  -usb -usbdevice mouse -usbdevice keyboard
  ```

### VM Won't Boot

**Problem:** VM starts but doesn't boot CyberOS

**Solutions:**
1. Verify ISO is not corrupted:
   ```bash
   file iso/cyberos-*.iso
   # Should show: ISO 9660 CD-ROM filesystem data with boot sector
   ```

2. Rebuild ISO:
   ```bash
   cd /path/to/CyberOS
   ./scripts/clean.sh
   ./scripts/build.sh
   ```

3. Check QEMU configuration in launcher script

## Getting Help

### Check Dependencies

```bash
# macOS
./emulator/macos/run_cyberos.sh --check

# Linux
./emulator/linux/run_cyberos.sh --check
```

### Verbose Output

```bash
# Enable debug output
DEBUG=1 ./emulator/macos/run_cyberos.sh

# Or with more details
DEBUG=1 python3 emulator/gui/cyberos_emulator.py
```

### Report Issues

If you encounter problems:

1. Check this troubleshooting guide
2. Review system requirements
3. Run diagnostics: `./run_cyberos.sh --check`
4. Collect output: `DEBUG=1 ./run_cyberos.sh 2>&1 | tee debug.log`
5. Report on GitHub: https://github.com/XL-Elite/CyberOS/issues

---

## Next Steps

After installation:

1. **Build CyberOS ISO:**
   ```bash
   cd /path/to/CyberOS
   ./scripts/build.sh
   ```

2. **Launch with GUI:**
   ```bash
   python3 emulator/gui/cyberos_emulator.py
   ```

3. **Or launch from command line:**
   ```bash
   ./emulator/macos/run_cyberos.sh -c 4 -m 1024 -n
   ```

4. **Boot CyberOS in the VM**

5. **Explore the system and enjoy!**

---

## Performance Tips

- **Use KVM (Linux):** Dramatically improves performance
- **Allocate adequate CPU:** Use `-c 2` or higher
- **Allocate adequate RAM:** Use `-m 512` or higher
- **Use SSD:** VM disk image should be on SSD for better performance
- **Disable GUI if not needed:** Use `--display serial` for text-only
- **Close other applications:** Free up host resources

---

## Further Reading

- [CyberOS README](../README.md)
- [QEMU Documentation](https://wiki.qemu.org/Documentation)
- [KVM Documentation](https://www.linux-kvm.org/)
- [VirtualBox Alternative](https://www.virtualbox.org/)

---

For more help, see the main [README.md](../README.md) or visit the [GitHub repository](https://github.com/XL-Elite/CyberOS).
