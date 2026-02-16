#!/bin/bash

################################################################################
# CyberOS - Master Build Script
# 
# This script orchestrates the complete CyberOS build process, from kernel
# compilation through ISO creation.
#
# Usage: ./scripts/build.sh [options]
# Options:
#   --clean      Clean previous builds before starting
#   --verbose    Show detailed build output
#   --help       Show this help message
################################################################################

set -e  # Exit on any error

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="${PROJECT_ROOT}/build"
ISO_DIR="${PROJECT_ROOT}/iso"
KERNEL_DIR="${PROJECT_ROOT}/kernel"
ROOTFS_DIR="${PROJECT_ROOT}/rootfs"
BOOTLOADER_DIR="${PROJECT_ROOT}/bootloader"
SCRIPTS_DIR="${PROJECT_ROOT}/scripts"

# Build flags
VERBOSE=0
CLEAN_BUILD=0
START_TIME=$(date +%s)

################################################################################
# Functions
################################################################################

# Print colored output
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Show help
show_help() {
    cat << EOF
CyberOS Master Build Script

Usage: ./scripts/build.sh [options]

Options:
    --clean     Clean previous builds before starting
    --verbose   Show detailed build output  
    --help      Show this help message

Examples:
    ./scripts/build.sh              # Standard build
    ./scripts/build.sh --clean      # Clean build
    ./scripts/build.sh --verbose    # Verbose output

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --clean)
                CLEAN_BUILD=1
                shift
                ;;
            --verbose)
                VERBOSE=1
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local required_tools=("gcc" "make" "bash" "cpio" "grub-mkrescue")
    local missing_tools=()
    
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        print_warning "Install with: sudo apt-get install build-essential grub-common"
        exit 1
    fi
    
    print_success "All prerequisites found"
}

# Clean previous builds
clean_builds() {
    if [ "$CLEAN_BUILD" -eq 1 ]; then
        print_status "Cleaning previous builds..."
        
        if [ -d "$BUILD_DIR" ]; then
            rm -rf "$BUILD_DIR"
            print_success "Cleaned build directory"
        fi
        
        if [ -d "$ISO_DIR" ]; then
            rm -rf "$ISO_DIR"
            print_success "Cleaned ISO directory"
        fi
    fi
}

# Create directories
create_directories() {
    print_status "Creating build directories..."
    
    mkdir -p "$BUILD_DIR"
    mkdir -p "$ISO_DIR"
    mkdir -p "$BUILD_DIR/kernel"
    mkdir -p "$BUILD_DIR/rootfs"
    mkdir -p "$BUILD_DIR/iso"
    
    print_success "Build directories created"
}

# Build kernel
build_kernel() {
    print_status "Building Linux kernel..."
    
    if [ "$VERBOSE" -eq 1 ]; then
        bash "$SCRIPTS_DIR/build_kernel.sh"
    else
        bash "$SCRIPTS_DIR/build_kernel.sh" > /dev/null 2>&1
    fi
    
    if [ $? -eq 0 ]; then
        print_success "Kernel built successfully"
    else
        print_error "Kernel build failed"
        exit 1
    fi
}

# Build rootfs
build_rootfs() {
    print_status "Building root filesystem..."
    
    if [ "$VERBOSE" -eq 1 ]; then
        bash "$SCRIPTS_DIR/build_rootfs.sh"
    else
        bash "$SCRIPTS_DIR/build_rootfs.sh" > /dev/null 2>&1
    fi
    
    if [ $? -eq 0 ]; then
        print_success "RootFS built successfully"
    else
        print_error "RootFS build failed"
        exit 1
    fi
}

# Create ISO
create_iso() {
    print_status "Creating ISO image..."
    
    if [ "$VERBOSE" -eq 1 ]; then
        bash "$SCRIPTS_DIR/create_iso.sh"
    else
        bash "$SCRIPTS_DIR/create_iso.sh" > /dev/null 2>&1
    fi
    
    if [ $? -eq 0 ]; then
        print_success "ISO image created successfully"
    else
        print_error "ISO creation failed"
        exit 1
    fi
}

# Print build summary
print_summary() {
    local end_time=$(date +%s)
    local duration=$((end_time - START_TIME))
    local minutes=$((duration / 60))
    local seconds=$((duration % 60))
    
    echo ""
    echo "=========================================="
    print_success "BUILD COMPLETE"
    echo "=========================================="
    echo ""
    echo "Build Time: ${minutes}m ${seconds}s"
    echo ""
    echo "Output files:"
    [ -f "$BUILD_DIR/kernel/vmlinuz" ] && echo "  - Kernel: $BUILD_DIR/kernel/vmlinuz"
    [ -d "$BUILD_DIR/rootfs" ] && echo "  - RootFS: $BUILD_DIR/rootfs/"
    [ -f "$ISO_DIR/cyberos.iso" ] && echo "  - ISO: $ISO_DIR/cyberos.iso"
    echo ""
    echo "Next steps:"
    echo "  1. Boot ISO on VirtualBox or KVM:"
    echo "     VirtualBox: Create VM, set boot media to $ISO_DIR/cyberos.iso"
    echo "     KVM: qemu-system-x86_64 -cdrom $ISO_DIR/cyberos.iso -boot d"
    echo "  2. Follow installation wizard"
    echo "  3. Login and enjoy CyberOS!"
    echo ""
}

################################################################################
# Main Build Process
################################################################################

main() {
    # Parse arguments
    parse_args "$@"
    
    # Print header
    echo "=========================================="
    echo -e "${BLUE}CyberOS Build System${NC}"
    echo "Version: 0.1.0-alpha"
    echo "=========================================="
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Clean if requested
    clean_builds
    
    # Create directories
    create_directories
    
    # Build components
    print_status "Starting CyberOS build process..."
    echo ""
    
    build_kernel
    build_rootfs
    create_iso
    
    # Print summary
    print_summary
}

# Run main
main "$@"
