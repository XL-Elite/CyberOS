# CyberOS Emulator

Official emulator launcher for running CyberOS on your computer. Works on macOS, Linux, and Windows.

## Features

- 🖥️ **Native GUI Application** - Easy-to-use graphical interface
- 🚀 **Quick Launch** - One-click VM creation and startup
- ⚙️ **Configurable** - Adjust CPU, RAM, disk size, and network settings
- 🌐 **Cross-Platform** - macOS, Linux, and Windows support
- 📦 **QEMU Integration** - Lightweight, open-source virtualization
- 💾 **VM Management** - Create, configure, and delete virtual machines
- 🔧 **Advanced Options** - Terminal access, snapshot support, custom drives

## Quick Start

### On macOS

**Option 1: GUI Application (Recommended)**
```bash
cd emulator/gui
python3 cyberos_emulator.py
```

**Option 2: Command Line**
```bash
./macos/run_cyberos.sh
```

### On Linux

```bash
./linux/run_cyberos.sh
```

## Requirements

### macOS

- **QEMU** (for virtualization):
  ```bash
  brew install qemu
  ```

- **Python 3.8+** (for GUI):
  ```bash
  # Usually pre-installed, verify with:
  python3 --version
  ```

### Linux

- **QEMU**:
  ```bash
  sudo apt-get install qemu-system-x86-64
  ```

## Installation

### Option 1: Homebrew (macOS)

```bash
brew tap xl-elite/cyberos
brew install cyberos-emulator
```

### Option 2: Manual Installation

```bash
# Clone or download CyberOS
git clone https://github.com/XL-Elite/CyberOS.git
cd CyberOS/emulator

# Make scripts executable
chmod +x macos/run_cyberos.sh
chmod +x linux/run_cyberos.sh
chmod +x gui/cyberos_emulator.py

# Run the GUI
python3 gui/cyberos_emulator.py
```

## Usage

### Launch with GUI

```bash
cd emulator/gui
python3 cyberos_emulator.py
```

The GUI provides:
- **Easy Configuration**: Set CPU cores, RAM (MB), disk size (GB)
- **Network Settings**: Enable networking, set port forwarding
- **VM Management**: Create, delete, or reconfigure VMs
- **Console Access**: Direct output from running VM
- **Quick Actions**: Start, stop, and reset your VM

### Launch via Command Line (macOS)

```bash
./emulator/macos/run_cyberos.sh [options]
```

**Options:**
- `-c, --cores N` - CPU cores (default: 2)
- `-m, --memory MB` - RAM in MB (default: 512)
- `-s, --size GB` - Disk size in GB (default: 2)
- `-n, --network` - Enable networking
- `-d, --display` - Display mode: sdl, vnc, or serial (default: sdl)
- `-h, --help` - Show help message

**Examples:**
```bash
# Run with 4 cores and 1GB RAM
./emulator/macos/run_cyberos.sh -c 4 -m 1024

# Run with networking enabled
./emulator/macos/run_cyberos.sh -n

# Run with VNC display (connect via VNC client)
./emulator/macos/run_cyberos.sh --display vnc
```

## Configuration

### VM Settings

Create a `.cyberos_vm.conf` file in your home directory to set defaults:

```bash
# CPU cores
CORES=2

# RAM in MB
MEMORY=512

# Disk size in GB
DISK_SIZE=2

# Enable networking
ENABLE_NETWORK=true

# Display mode: sdl, vnc, serial
DISPLAY=sdl

# Enable KVM acceleration (Linux only)
USE_KVM=true

# Port for VNC (if using VNC display)
VNC_PORT=5900
```

## Directory Structure

```
emulator/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── macos/
│   ├── run_cyberos.sh          # macOS launcher script
│   ├── install_dependencies.sh # Homebrew setup script
│   └── setup_vm.sh             # VM initialization script
├── linux/
│   ├── run_cyberos.sh          # Linux launcher script
│   └── install_dependencies.sh # APT setup script
├── gui/
│   ├── cyberos_emulator.py     # Python GUI application
│   ├── vm_manager.py           # VM management library
│   ├── requirements.txt         # Python dependencies
│   └── config.py               # Configuration handler
└── docs/
    ├── INSTALLATION.md         # Detailed installation guide
    ├── TROUBLESHOOTING.md      # Common issues and fixes
    ├── ADVANCED.md             # Advanced configuration
    └── ARCHITECTURE.md         # Technical details
```

## Troubleshooting

### QEMU not found on macOS

```bash
# Install QEMU
brew install qemu

# Link it globally
brew link qemu
```

### Permission denied when running scripts

```bash
# Make scripts executable
chmod +x emulator/macos/run_cyberos.sh
chmod +x emulator/linux/run_cyberos.sh
```

### ISO file not found

Ensure the CyberOS ISO is built:
```bash
cd /path/to/CyberOS
./scripts/build.sh
```

The ISO should be at: `iso/cyberos-0.1.0-alpha.iso`

### GUI doesn't start on macOS

```bash
# Verify Python 3 is installed
python3 --version

# Install tkinter if missing (macOS)
brew install python-tk

# Try running directly
python3 -c "import tkinter; print('Tkinter OK')"
```

## VM Management

### Create a New VM

```bash
# Using GUI - click "Create VM" button
# Or command line:
./emulator/macos/run_cyberos.sh --create "MyVM" -c 4 -m 2048
```

### List VMs

```bash
# Using GUI - shows in dropdown
# Or command line:
./emulator/macos/run_cyberos.sh --list
```

### Delete a VM

```bash
# Using GUI - select VM and click "Delete"
# Or command line:
./emulator/macos/run_cyberos.sh --delete "MyVM"
```

## Network Configuration

### Enable Port Forwarding

```bash
# In .cyberos_vm.conf or GUI:
PORT_FORWARD="22:2222,80:8080"

# Then access from host:
# SSH: ssh root@localhost -p 2222
# HTTP: http://localhost:8080
```

### Access via SSH

```bash
# Once CyberOS is running with networking enabled
ssh root@localhost -p 2222

# Or set up in ~/.ssh/config
Host cyberos-vm
  HostName localhost
  Port 2222
  User root
```

## Performance Tips

1. **Allocate Adequate CPU**
   - Use at least 2 cores: `-c 2` or higher
   - Match your host's available cores

2. **Set Appropriate RAM**
   - Minimum: 256 MB
   - Recommended: 512 MB - 2 GB
   - Depends on your host system

3. **Use Disk Image**
   - Smaller initial disk (2-4 GB) for faster startup
   - Can resize later if needed

4. **Enable KVM (Linux only)**
   - Dramatically improves performance
   - Automatically enabled in the script

5. **Disable GUI if Not Needed**
   - Use VNC or serial console for headless operation
   - Reduces resource usage

## Advanced Usage

### VNC Access

```bash
# Start with VNC display
./emulator/macos/run_cyberos.sh --display vnc

# Connect from another machine
vncviewer localhost:5900
```

### Serial Console

```bash
# Start with serial display (text-only)
./emulator/macos/run_cyberos.sh --display serial
```

### Custom QEMU Options

Edit the launcher script to add custom QEMU parameters:
```bash
# In emulator/macos/run_cyberos.sh, add:
QEMU_OPTS="-enable-kvm -cpu host"
```

## Contributing

To contribute improvements:

1. Fork the CyberOS repository
2. Create a feature branch: `git checkout -b feature/emulator-improvement`
3. Make your changes
4. Test on macOS and Linux
5. Commit: `git commit -am 'Add emulator feature'`
6. Push and create a Pull Request

## Support

- 📖 [Full Documentation](../docs/)
- 🐛 [Report Issues](https://github.com/XL-Elite/CyberOS/issues)
- 💬 [Discussions](https://github.com/XL-Elite/CyberOS/discussions)

## License

CyberOS Emulator is part of the CyberOS project and is licensed under the GPL v2 License.

See [LICENSE](../../LICENSE) for details.

---

**Ready to run CyberOS?** Start with the GUI: `python3 emulator/gui/cyberos_emulator.py`
