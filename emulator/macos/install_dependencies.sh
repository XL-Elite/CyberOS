#!/bin/bash

################################################################################
# CyberOS Emulator - macOS Installation Script
#
# This script sets up CyberOS Emulator on macOS with all dependencies.
# Installs QEMU and configures the environment.
#
# Run: ./install_dependencies.sh
################################################################################

set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║      CyberOS Emulator - macOS Dependency Installation     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo -e "${RED}✗ ERROR:${NC} Homebrew is not installed"
    echo ""
    echo "Please install Homebrew first:"
    echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

echo -e "${GREEN}✓ SUCCESS:${NC} Homebrew found"
echo ""

# Update Homebrew
echo -e "${BLUE}ℹ️  INFO:${NC} Updating Homebrew..."
brew update

# Install QEMU
echo ""
echo -e "${BLUE}ℹ️  INFO:${NC} Installing QEMU..."
if ! command -v qemu-system-x86_64 &> /dev/null; then
    brew install qemu
    echo -e "${GREEN}✓ SUCCESS:${NC} QEMU installed"
else
    echo -e "${YELLOW}⚠️  WARNING:${NC} QEMU already installed"
fi

# Create VM directory
echo ""
echo -e "${BLUE}ℹ️  INFO:${NC} Setting up VM directory..."
mkdir -p "$HOME/.cyberos/vms"
echo -e "${GREEN}✓ SUCCESS:${NC} VM directory created at ~/.cyberos/vms"

# Create config template
echo ""
echo -e "${BLUE}ℹ️  INFO:${NC} Creating configuration template..."

if [[ ! -f "$HOME/.cyberos_vm.conf" ]]; then
    cat > "$HOME/.cyberos_vm.conf" << 'EOF'
# CyberOS VM Configuration
# Customize these settings to your preferences

# CPU cores (1-16)
CORES=2

# RAM in MB (128-8192)
MEMORY=512

# Disk size in GB (1-100)
DISK_SIZE=2

# Enable networking (true/false)
ENABLE_NETWORK=true

# Display mode: sdl, vnc, serial
DISPLAY=sdl
EOF
    echo -e "${GREEN}✓ SUCCESS:${NC} Configuration file created at ~/.cyberos_vm.conf"
else
    echo -e "${YELLOW}⚠️  WARNING:${NC} Configuration file already exists"
fi

# Make launcher executable
echo ""
echo -e "${BLUE}ℹ️  INFO:${NC} Setting up launcher scripts..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

chmod +x "${SCRIPT_DIR}/run_cyberos.sh"
echo -e "${GREEN}✓ SUCCESS:${NC} macOS launcher made executable"

# Python setup (optional)
echo ""
echo -e "${BLUE}ℹ️  INFO:${NC} Checking Python setup..."

if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ SUCCESS:${NC} Python 3 found: $(python3 --version)"
    
    # Optional: Install tkinter for GUI
    echo ""
    echo -e "${BLUE}ℹ️  INFO:${NC} Python tkinter is required for the GUI"
    echo "If the GUI doesn't work, install tkinter:"
    echo "  brew install python-tk"
else
    echo -e "${YELLOW}⚠️  WARNING:${NC} Python 3 not found. GUI will not work."
    echo "Install Python:"
    echo "  brew install python@3.11"
fi

# Summary
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}         ${GREEN}Installation Complete!${NC}                        ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"

echo ""
echo "Next steps:"
echo ""
echo "1. Build CyberOS ISO:"
echo "   cd $PROJECT_ROOT"
echo "   ./scripts/build.sh"
echo ""
echo "2. Run CyberOS with GUI:"
echo "   python3 $PROJECT_ROOT/emulator/gui/cyberos_emulator.py"
echo ""
echo "3. Or run from command line:"
echo "   $SCRIPT_DIR/run_cyberos.sh"
echo ""
echo "For help:"
echo "   $SCRIPT_DIR/run_cyberos.sh --help"
echo ""
