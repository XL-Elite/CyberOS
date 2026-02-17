# CyberOS Control Center - Quick Start Guide

Get started with the CyberOS Control Center in 5 minutes!

## What is the Control Center?

The **CyberOS Control Center** is a single interface for managing everything related to the CyberOS project:
- Building bootable ISO images
- Launching and managing virtual machines
- Installing and checking dependencies
- Viewing project status and logs
- Managing project settings

## Requirements

- Python 3.8 or newer
- tkinter (usually included with Python)
- QEMU (for running VMs)
- Build tools (gcc, make, etc.)

## Quick Installation

### 1. Start the Control Center

```bash
# Navigate to CyberOS project
cd /path/to/CyberOS

# Launch the Control Center
python3 tools/cyberos_control.py

# Or use the launcher script
./tools/launch_control_center.sh
```

### 2. Check Your Setup

Go to the **Dependencies** tab and click **"Check Dependencies"**

This shows:
- ✓ FOUND - Tools are installed
- ✗ MISSING - You need to install the tool

### 3. Install Missing Tools

If dependencies are missing, click **"Install Missing"**

**macOS users:** May need to enter password for Homebrew
**Linux users:** May need to enter password for sudo

## Building CyberOS

### Method 1: Dashboard (Easiest)

1. Click the **"🔨 Build CyberOS"** button
2. Wait for build to complete
3. Check the status bar at the bottom

### Method 2: Build Tab (More Control)

1. Go to the **Build** tab
2. Configure options if needed:
   - Version
   - Architecture
   - Compression
3. Click **"Build ISO"**
4. Watch real-time output

### Method 3: Clean and Rebuild

1. Go to **Build** tab
2. Click **"Clean"** to remove old artifacts
3. Click **"Build ISO"** to rebuild

## Running CyberOS

### Method 1: Emulator GUI (Recommended)

1. Go to **Emulator** tab
2. Click **"Launch Emulator GUI"**
3. A new window opens with full VM control

### Method 2: Quick Launch

1. Go to **Emulator** tab
2. Click one of:
   - "Quick Start" - 2 cores, 512 MB RAM
   - "Performance" - 4 cores, 1024 MB RAM

### Method 3: Custom Configuration

1. Go to **Emulator** tab
2. Set CPU cores, RAM, disk size
3. Choose display mode (SDL/VNC/Serial)
4. Click **"Launch with Custom Config"**

## Understanding the Tabs

### 📊 Dashboard
- Project overview
- Quick access buttons
- Build status
- Dependency status

### 🔨 Build
- Create ISO images
- Build configuration
- Real-time build output
- Progress monitoring

### 🎮 Emulator
- Launch virtual machines
- VM management
- Configuration options
- VM disk browser

### 📦 Dependencies
- Check what tools are installed
- Install missing tools
- System information

### ⚙️ Settings
- Build configuration
- Project paths
- Optimization options
- Save settings

### 📜 Logs
- Complete history of all operations
- Timestamped entries
- Export logs to file
- Clear logs

### ℹ️ About
- Project information
- Feature overview
- Links and documentation

## Common Tasks

### Task: Build CyberOS

```
Dashboard → "Build CyberOS" button → Wait for completion
```

### Task: Run CyberOS in a VM

```
Dashboard → "Launch Emulator GUI" → Configure VM → Start
```

### Task: Install build tools

```
Dependencies tab → "Check Dependencies" → "Install Missing" → Done
```

### Task: View build output

```
Build tab → Build ISO → Watch real-time output
```

### Task: Manage VM disks

```
Emulator tab → "Open VM Folder" → Browse `.cyberos/vms` directory
```

### Task: Configure emulator settings

```
Emulator tab → "Open Emulator Settings" → Edit config file
```

## Tips & Tricks

### Speed Up Builds
- Settings → Increase "Parallel Build Jobs"
- Build tab → Enable "Optimize images"
- Use "Clean" before rebuilding

### Better Emulator Performance
- Settings → Allocate more CPU cores
- Use KVM (automatic on Linux)
- Close other applications

### Multiple VMs
- Each emulator launch creates a new VM
- VMs are stored in `~/.cyberos/vms/`
- Use different names to keep multiple VMs

### Monitor Progress
- Logs tab shows real-time activity
- Build tab shows live output
- Dashboard shows current status

## Troubleshooting

### "Python not found"
```bash
# Check Python installation
python3 --version

# Install if missing
brew install python@3.11  # macOS
sudo apt-get install python3  # Linux
```

### "tkinter not found"
```bash
# macOS
brew install python-tk

# Linux
sudo apt-get install python3-tk
```

### Build fails
1. Check build output for error messages
2. Go to Dependencies tab → Check Dependencies
3. Install missing tools if needed
4. Try "Clean" then rebuild

### Emulator won't start
1. Ensure ISO is built (Dashboard shows ✓)
2. Install QEMU if missing (Dependencies tab)
3. Check emulator output for errors

### GUI won't display on macOS
1. Grant Python permission: System Settings → Privacy & Security
2. Or use command-line emulator instead
3. Or use VNC display mode

## What Happens When You...

### Click "Build ISO"
- Prepares build directories
- Compiles Linux kernel
- Creates root filesystem
- Generates bootable ISO image
- Shows real-time progress

### Click "Launch Emulator GUI"
- Opens dedicated emulator interface
- Allows VM configuration
- Manages VM disks and settings
- Monitors VM console

### Click "Check Dependencies"
- Tests each required tool
- Shows install status (✓ or ✗)
- Provides install suggestions
- Updates system info

### Click "Clean"
- Removes old build artifacts
- Frees up disk space (1-2 GB)
- Doesn't delete ISO or config

## Keyboard Tips

- Use Tab to navigate between tabs
- Use Enter to click focused button
- Use Ctrl+C to stop running processes
- Use text widgets to scroll through output

## Next Steps

1. ✅ Install dependencies (Dependencies tab)
2. ✅ Build CyberOS (Build tab)
3. ✅ Launch emulator (Emulator tab)
4. ✅ Boot CyberOS in VM
5. ✅ Explore and enjoy!

## Need Help?

### View Logs
- Logs tab → Shows all operations

### Read Documentation
- About tab → Links to guides
- Dashboard → "Read Documentation"

### Visit GitHub
- Dashboard → "View on GitHub"
- Report issues at: https://github.com/XL-Elite/CyberOS/issues

### Check Command Line Help
```bash
python3 tools/cyberos_control.py --help
./tools/launch_control_center.sh --help
```

## System Requirements

**Minimum:**
- macOS 10.14 or Linux 20.04+
- 2 GB RAM
- 5 GB disk space
- Python 3.8+

**Recommended:**
- macOS 11+ or Linux 22.04+
- 4+ GB RAM
- 10 GB disk space
- Python 3.10+

## Getting More From Control Center

### Environment Variables

```bash
# Debug mode
DEBUG=1 python3 tools/cyberos_control.py

# Use custom project path
CYBEROS_ROOT=/path/to/project python3 tools/cyberos_control.py
```

### Command Line Options

```bash
# Start in Build tab
./tools/launch_control_center.sh --build

# Start in Emulator tab
./tools/launch_control_center.sh --emulator
```

---

**You're ready!** Launch the Control Center and start building CyberOS:

```bash
python3 tools/cyberos_control.py
```

Need more details? Check the full [README.md](README.md) or visit [GitHub](https://github.com/XL-Elite/CyberOS).
