#!/bin/bash

################################################################################
# CyberOS Emulator - Linux Installation Script
#
# This script sets up CyberOS Emulator on Linux with all dependencies.
# Installs QEMU, KVM, and configures the environment.
#
# Run: sudo ./install_dependencies.sh
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
echo "║     CyberOS Emulator - Linux Dependency Installation      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root or with sudo
if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}✗ ERROR:${NC} This script must be run with sudo"
    echo "Run: sudo ./install_dependencies.sh"
    exit 1
fi

# Detect Linux distribution
if [[ -f /etc/os-release ]]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    DISTRO=$ID
else
    echo -e "${RED}✗ ERROR:${NC} Could not detect Linux distribution"
    exit 1
fi

echo -e "${BLUE}ℹ️  INFO:${NC} Detected: $PRETTY_NAME"
echo ""

# Update package lists
echo -e "${BLUE}ℹ️  INFO:${NC} Updating package lists..."
apt-get update

# Install dependencies based on distribution
echo ""
echo -e "${BLUE}ℹ️  INFO:${NC} Installing QEMU and dependencies..."

apt-get install -y \
    qemu-system-x86 \
    qemu-utils \
    qemu-kvm \
    libvirt-clients

echo -e "${GREEN}✓ SUCCESS:${NC} QEMU and dependencies installed"

# Install Python and tkinter for GUI (optional)
echo ""
echo -e "${BLUE}ℹ️  INFO:${NC} Installing Python and optional GUI support..."

apt-get install -y \
    python3 \
    python3-tk

echo -e "${GREEN}✓ SUCCESS:${NC} Python 3 and tkinter installed"

# Set up user to use KVM without sudo (optional but recommended)
echo ""
echo -e "${BLUE}ℹ️  INFO:${NC} Setting up KVM access..."

# Check if kvm group exists
if getent group kvm > /dev/null; then
    echo -e "${GREEN}✓ SUCCESS:${NC} KVM group exists"
    
    # Get the calling user (when running with sudo)
    if [[ -n "${SUDO_USER:-}" ]]; then
        usermod -a -G kvm "$SUDO_USER"
        echo -e "${GREEN}✓ SUCCESS:${NC} Added $SUDO_USER to kvm group"
        echo -e "${YELLOW}⚠️  WARNING:${NC} You may need to log out and log back in for group changes to take effect"
    fi
else
    echo -e "${YELLOW}⚠️  WARNING:${NC} KVM group not found"
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

# Use KVM acceleration (true/false) - Linux only
USE_KVM=true
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
echo -e "${GREEN}✓ SUCCESS:${NC} Linux launcher made executable"

# Verify installation
echo ""
echo -e "${BLUE}ℹ️  INFO:${NC} Verifying installation..."

if command -v qemu-system-x86_64 &> /dev/null; then
    echo -e "${GREEN}✓ SUCCESS:${NC} QEMU found: $(qemu-system-x86_64 --version | head -n 1)"
else
    echo -e "${RED}✗ ERROR:${NC} QEMU not found"
    exit 1
fi

if [ -c /dev/kvm ]; then
    echo -e "${GREEN}✓ SUCCESS:${NC} KVM device available"
else
    echo -e "${YELLOW}⚠️  WARNING:${NC} KVM device not available (will use slower TCG emulation)"
fi

if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ SUCCESS:${NC} Python 3 found: $(python3 --version)"
else
    echo -e "${YELLOW}⚠️  WARNING:${NC} Python 3 not found"
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
