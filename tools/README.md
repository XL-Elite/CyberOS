# CyberOS Control Center

Master control interface for managing all aspects of the CyberOS project.

## Overview

The **CyberOS Control Center** is an all-in-one GUI application that provides unified control over:

- **Build System** - Create bootable ISO images
- **Emulator** - Launch and manage virtual machines
- **Dependencies** - Install and verify requirements
- **Project Management** - Configure builds and settings
- **Logging** - Monitor all system activities

## Features

### 🔨 Build System
- One-click ISO generation
- Build progress monitoring
- Real-time output logging
- Clean, rebuild, and optimize options
- Version and architecture configuration
- Compression settings

### 🎮 Emulator Management
- Quick launch with preset configurations
- Custom CPU, RAM, and disk settings
- Display mode selection (SDL, VNC, serial)
- Network configuration
- VM persistence and management
- VM disk storage browser

### 📦 Dependency Management
- Automatic dependency detection
- Status indicators for each tool
- One-click installation of missing dependencies
- System information display
- Platform-specific installation

### ⚙️ Project Settings
- Build configuration options
- Parallel job settings
- Project path information
- Settings persistence
- Optimization controls

### 📊 Dashboard
- Project status overview
- Quick access buttons
- Build status display
- File information

### 📜 Logging
- Complete operation history
- Timestamped log entries
- Log export functionality
- Log clearing options

## Installation

### macOS

```bash
# Clone/navigate to project
cd /path/to/CyberOS

# Run the control center
python3 tools/cyberos_control.py
```

### Linux

```bash
# Clone/navigate to project
cd /path/to/CyberOS

# Run the control center
python3 tools/cyberos_control.py
```

### Windows (WSL 2)

```bash
# Inside WSL 2 Ubuntu terminal
cd /path/to/CyberOS
python3 tools/cyberos_control.py
```

## Usage

### Launch the Application

```bash
# From project root
python3 tools/cyberos_control.py
```

### First Time Setup

1. **Check Dependencies** - Go to "Dependencies" tab, click "Check Dependencies"
2. **Install Missing Tools** - Click "Install Missing" to auto-install
3. **Build ISO** - Go to "Build" tab, click "Build ISO"
4. **Launch Emulator** - Go to "Emulator" tab, click "Launch Emulator GUI"

### Building CyberOS

1. **Simple Build** - Dashboard → "Build CyberOS"
2. **Advanced Build** - Build tab → Configure options → "Build ISO"
3. **Rebuild** - Build tab → "Rebuild All"
4. **Clean** - Build tab → "Clean"

### Running CyberOS

1. **GUI Emulator** - Dashboard or Emulator tab → "Launch Emulator GUI"
2. **Quick Start** - Emulator tab → "Quick Start (2 cores, 512 MB)"
3. **Performance** - Emulator tab → "Performance (4 cores, 1024 MB)"
4. **Custom** - Emulator tab → Configure → "Launch with Custom Config"

### Managing Configuration

1. **Project Settings** - Settings tab → Configure options → Save
2. **Emulator Settings** - Emulator tab → "Open Emulator Settings"
3. **VM Management** - Emulator tab → "Open VM Folder"

## Dashboard Overview

### Project Status
- ISO build status
- Build file locations
- Dependency status
- Project structure summary

### Quick Actions
- **Build** - ISO creation buttons
- **Emulator** - VM launch buttons
- **Project** - Folder and documentation links

## Build System

### Build Stages

1. **Prepare** - Create build directories
2. **Kernel** - Compile kernel image
3. **Rootfs** - Build root filesystem
4. **ISO** - Create bootable ISO with GRUB2
5. **Verify** - Check ISO integrity

### Build Options

| Option | Description | Default |
|--------|-------------|---------|
| Version | CyberOS version | 0.1.0 |
| Architecture | Target CPU type | x86_64 |
| Compression | ISO compression | xz |
| Optimize | Optimize images | Yes |

### Build Output

Real-time build log showing:
- Build progress
- Tool execution
- Compilation progress
- ISO creation status
- Build completion status

## Emulator Features

### Display Modes
- **SDL** - GUI window (default)
- **VNC** - Remote access (port 5900)
- **Serial** - Text console only

### Network Options
- Disabled (default)
- User-mode networking
- Port forwarding

### Resource Configuration
- CPU cores: 1-16
- RAM: 128-4096 MB
- Disk: 1-100 GB

### VM Management
- List saved VMs
- VM size display
- VM selection and info
- Open VM folder

## Dependency Management

### Checked Dependencies
- bash - Shell interpreter
- make - Build system
- gcc - C compiler
- grub-mkrescue - Bootloader tools
- xorriso - ISO creation
- qemu-system-x86_64 - Emulator
- python3 - Python interpreter
- git - Version control

### Installation

**macOS (via Homebrew):**
```bash
brew install qemu grub-common xorriso
```

**Linux (via APT):**
```bash
sudo apt-get install qemu-system-x86 grub-common xorriso build-essential
```

## Project Settings

### Build Configuration
- **Parallel Jobs** - Number of parallel build threads (1-16)
- **Optimize** - Enable build optimization
- **Preserve Old Builds** - Keep previous build artifacts

### Project Paths
Displays all critical project paths:
- Project root directory
- Build output directory
- ISO location
- Script locations
- Emulator locations

## Logging

### Log Features
- Timestamped entries
- Source identification
- Complete operation history
- Clear logs option
- Export to file

### Log Entries Include
- Build operations
- Emulator launches
- Dependency checks
- System events
- User actions

## Troubleshooting

### Application Won't Start
```bash
# Verify Python is installed
python3 --version

# Check required modules
python3 -c "import tkinter; print('OK')"

# Try running directly
python3 /path/to/tools/cyberos_control.py
```

### Dependencies Show as Missing
1. Check system PATH for tools
2. Install missing dependencies:
   - macOS: `brew install <package>`
   - Linux: `sudo apt-get install <package>`
3. Click "Check Dependencies" button

### Build Fails
1. Check build output for error messages
2. Verify all dependencies are installed
3. Ensure sufficient disk space (3+ GB)
4. Try "Clean" then rebuild
5. Check permissions on build scripts

### Emulator Won't Launch
1. Verify ISO is built (Dashboard → check ISO status)
2. Install QEMU if missing
3. Check emulator configuration
4. Try launching from command line for more details

### GUI Doesn't Display on macOS
1. Grant Python permission in Privacy settings
2. Try with XQuartz if native display fails
3. Use VNC display mode instead
4. Check system resources

## Architecture

### Components

```
tools/
├── cyberos_control.py    - Main GUI application (1200+ lines)
├── README.md             - This file
├── QUICKSTART.md         - Quick start guide
└── launch.sh             - Shell launcher script
```

### Dependencies
- Python 3.8+
- tkinter (GUI framework)
- subprocess (process management)
- tkinter.scrolledtext (text display)
- pathlib (file operations)
- json, threading, datetime (utilities)

### Integration Points

The Control Center integrates with:
- `scripts/build.sh` - ISO build process
- `scripts/clean.sh` - Build cleanup
- `emulator/gui/cyberos_emulator.py` - Emulator GUI
- `emulator/macos/run_cyberos.sh` - macOS launcher
- `emulator/linux/run_cyberos.sh` - Linux launcher
- `emulator/macos/install_dependencies.sh` - macOS setup
- `emulator/linux/install_dependencies.sh` - Linux setup

## Keyboard Shortcuts

- `Ctrl+W` / `Cmd+W` - Switch tabs
- `Ctrl+L` - Clear logs
- `Ctrl+Q` / `Cmd+Q` - Quit application

## Tips & Tricks

### Speed Up Builds
1. Settings tab → Set Parallel Jobs to higher value (4-8)
2. Enable "Optimize images"
3. Use "Clean" periodically

### Optimize Emulator Performance
1. Use KVM on Linux (automatic)
2. Allocate appropriate resources
3. Use VNC or serial for headless mode
4. Close other applications

### Multiple VMs
1. Emulator tab → Each launcher creates unique VM
2. Use different VM names for multiple instances
3. VMs stored in `~/.cyberos/vms/`
4. Open VM Folder to manage manually

## Advanced Usage

### Command Line Launch

```bash
# Show help
python3 tools/cyberos_control.py --help

# Launch specific tab
python3 tools/cyberos_control.py --tab build

# Debug mode
DEBUG=1 python3 tools/cyberos_control.py
```

### Environment Variables

```bash
# Enable debug output
DEBUG=1 python3 tools/cyberos_control.py

# Set project root
CYBEROS_ROOT=/path/to/project python3 tools/cyberos_control.py

# Use custom emulator
EMULATOR_PATH=/path/to/qemu python3 tools/cyberos_control.py
```

### Integration with Scripts

The Control Center calls:

```bash
# Build
./scripts/build.sh [options]

# Clean
./scripts/clean.sh

# Emulator
python3 emulator/gui/cyberos_emulator.py
./emulator/macos/run_cyberos.sh [options]
./emulator/linux/run_cyberos.sh [options]
```

## Contributing

To extend the Control Center:

1. **Add New Tab** - Follow the `create_*_tab()` pattern
2. **Add New Action** - Implement action method with threading
3. **Add Logging** - Use `self.log_entry()` for all actions
4. **Test** - Run on macOS and Linux

## Support

- 📖 [CyberOS README](../README.md)
- 🐛 [Report Issues](https://github.com/XL-Elite/CyberOS/issues)
- 💬 [Discussions](https://github.com/XL-Elite/CyberOS/discussions)

## License

CyberOS Control Center is part of the CyberOS project and is licensed under the GPL v2 License.

---

**Ready to control CyberOS?** Launch the Control Center: `python3 tools/cyberos_control.py`
