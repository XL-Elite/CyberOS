#!/bin/bash

################################################################################
# CyberOS Emulator - Linux Launcher
# 
# This script launches CyberOS in QEMU on Linux with a user-friendly interface.
# Features: KVM acceleration, configurable CPU/RAM/disk, networking, display modes
#
# Usage: ./run_cyberos.sh [options]
# Example: ./run_cyberos.sh -c 4 -m 1024 -n
################################################################################

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default configuration
CORES=2
MEMORY=512
DISK_SIZE=2
ENABLE_NETWORK=false
DISPLAY_MODE="sdl"
USE_KVM=true
VM_NAME="CyberOS-VM"
VM_DIR="${HOME}/.cyberos/vms"
CONFIG_FILE="${HOME}/.cyberos_vm.conf"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
ISO_FILE="${PROJECT_ROOT}/iso/cyberos-0.1.0-alpha.iso"
QEMU_BIN=""

################################################################################
# Functions
################################################################################

print_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║         🖥️  CyberOS Emulator - Linux Launcher             ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  INFO:${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓ SUCCESS:${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️  WARNING:${NC} $1"
}

print_error() {
    echo -e "${RED}✗ ERROR:${NC} $1"
}

show_help() {
    cat << 'EOF'
CyberOS Emulator - Linux Launcher

USAGE:
    ./run_cyberos.sh [OPTIONS]

OPTIONS:
    -c, --cores NUM        Number of CPU cores (default: 2)
    -m, --memory MB        RAM in megabytes (default: 512)
    -s, --size GB          Disk size in gigabytes (default: 2)
    -n, --network          Enable networking
    -d, --display MODE     Display mode: sdl, vnc, serial (default: sdl)
    -v, --vm-name NAME     VM name (default: CyberOS-VM)
    --create NAME          Create a new named VM
    --delete NAME          Delete an existing VM
    --list                 List all saved VMs
    --check                Check dependencies only
    --no-kvm               Disable KVM acceleration
    -h, --help             Show this help message

EXAMPLES:
    # Run with default settings
    ./run_cyberos.sh

    # Run with 4 cores and 2GB RAM
    ./run_cyberos.sh -c 4 -m 2048

    # Run with networking enabled
    ./run_cyberos.sh -n

    # Run with VNC display
    ./run_cyberos.sh --display vnc

    # Run without KVM (software emulation)
    ./run_cyberos.sh --no-kvm

CONFIGURATION:
    Create ~/.cyberos_vm.conf to set defaults:
        CORES=2
        MEMORY=512
        DISK_SIZE=2
        ENABLE_NETWORK=true
        DISPLAY=sdl
        USE_KVM=true

EOF
}

load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        print_info "Loading configuration from $CONFIG_FILE"
        # shellcheck disable=SC1090
        source "$CONFIG_FILE"
    fi
}

check_dependency() {
    local cmd=$1
    local package=$2
    
    if ! command -v "$cmd" &> /dev/null; then
        print_error "$cmd is not installed"
        echo "  Install with: sudo apt-get install $package"
        return 1
    fi
    print_success "$cmd found"
    return 0
}

check_dependencies() {
    print_info "Checking dependencies..."
    
    local all_found=true
    
    # Check QEMU
    if ! check_dependency "qemu-system-x86_64" "qemu-system-x86"; then
        all_found=false
    fi
    
    # Check KVM (optional but recommended)
    if [[ "$USE_KVM" == true ]]; then
        if ! command -v kvm &> /dev/null; then
            if [ -c /dev/kvm ]; then
                print_success "KVM device found"
            else
                print_warning "KVM device not found - using TCG emulation (slower)"
                USE_KVM=false
            fi
        else
            print_success "KVM found"
        fi
    fi
    
    # Find QEMU binary
    QEMU_BIN=$(which qemu-system-x86_64 2>/dev/null || echo "")
    
    if [[ -z "$QEMU_BIN" ]]; then
        print_error "qemu-system-x86_64 not found in PATH"
        return 1
    fi
    
    if [[ "$all_found" == true ]]; then
        print_success "All required dependencies installed"
        return 0
    else
        return 1
    fi
}

check_iso() {
    if [[ ! -f "$ISO_FILE" ]]; then
        print_error "ISO file not found: $ISO_FILE"
        echo ""
        echo "Please build CyberOS first:"
        echo "  cd $PROJECT_ROOT"
        echo "  ./scripts/build.sh"
        return 1
    fi
    print_success "ISO found: $(basename "$ISO_FILE")"
    return 0
}

setup_vm_directory() {
    mkdir -p "$VM_DIR"
    print_info "VM directory: $VM_DIR"
}

create_disk_image() {
    local disk_file=$1
    local size_gb=$2
    
    if [[ ! -f "$disk_file" ]]; then
        print_info "Creating disk image: $size_gb GB"
        qemu-img create -f qcow2 "$disk_file" "${size_gb}G"
        print_success "Disk image created"
    else
        print_info "Using existing disk image: $(basename "$disk_file")"
    fi
}

build_qemu_command() {
    local disk_file=$1
    local qemu_cmd=()
    
    # Basic configuration
    qemu_cmd+=("${QEMU_BIN}")
    qemu_cmd+=("-name" "$VM_NAME")
    
    # Machine type with acceleration
    if [[ "$USE_KVM" == true ]] && [ -c /dev/kvm ]; then
        qemu_cmd+=("-machine" "type=q35,accel=kvm")
    else
        qemu_cmd+=("-machine" "type=q35,accel=tcg")
    fi
    
    # CPU and memory
    qemu_cmd+=("-smp" "cores=$CORES")
    qemu_cmd+=("-m" "$MEMORY")
    
    # Storage
    qemu_cmd+=("-boot" "d")
    qemu_cmd+=("-cdrom" "$ISO_FILE")
    qemu_cmd+=("-drive" "file=$disk_file,format=qcow2")
    
    # Display
    case "$DISPLAY_MODE" in
        vnc)
            qemu_cmd+=("-vnc" ":0")
            qemu_cmd+=("-monitor" "stdio")
            ;;
        serial)
            qemu_cmd+=("-nographic")
            qemu_cmd+=("-serial" "stdio")
            qemu_cmd+=("-monitor" "none")
            ;;
        sdl|*)
            qemu_cmd+=("-display" "gtk")
            ;;
    esac
    
    # Networking
    if [[ "$ENABLE_NETWORK" == true ]]; then
        qemu_cmd+=("-nic" "user,model=virtio")
    else
        qemu_cmd+=("-nic" "none")
    fi
    
    echo "${qemu_cmd[@]}"
}

list_vms() {
    print_info "Saved VM images:"
    
    if [[ ! -d "$VM_DIR" ]] || [[ -z "$(ls -A "$VM_DIR" 2>/dev/null)" ]]; then
        echo "  (No VMs saved yet)"
        return
    fi
    
    local count=0
    for disk in "$VM_DIR"/*.qcow2; do
        if [[ -f "$disk" ]]; then
            local size=$(ls -lh "$disk" | awk '{print $5}')
            local name=$(basename "$disk" .qcow2)
            echo "  • $name ($size)"
            ((count++))
        fi
    done
    
    if [[ $count -eq 0 ]]; then
        echo "  (No VMs saved yet)"
    fi
}

delete_vm() {
    local vm_name=$1
    local disk_file="$VM_DIR/${vm_name}.qcow2"
    
    if [[ ! -f "$disk_file" ]]; then
        print_error "VM not found: $vm_name"
        return 1
    fi
    
    read -p "Delete VM '$vm_name'? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f "$disk_file"
        print_success "VM deleted: $vm_name"
    else
        print_warning "Deletion cancelled"
    fi
}

run_vm() {
    print_header
    
    print_info "Configuration:"
    echo "  CPU Cores:     $CORES"
    echo "  RAM:           ${MEMORY} MB"
    echo "  Disk Size:     ${DISK_SIZE} GB"
    echo "  Networking:    $([ "$ENABLE_NETWORK" == true ] && echo 'Enabled' || echo 'Disabled')"
    echo "  Display:       $DISPLAY_MODE"
    echo "  KVM:           $([ "$USE_KVM" == true ] && echo 'Enabled (faster)' || echo 'Disabled (slower)')"
    echo "  VM Name:       $VM_NAME"
    echo ""
    
    setup_vm_directory
    
    # Check dependencies
    if ! check_dependencies; then
        print_error "Missing dependencies. Install QEMU:"
        echo "  sudo apt-get install qemu-system-x86"
        return 1
    fi
    
    # Check ISO
    if ! check_iso; then
        return 1
    fi
    
    # Create disk
    local disk_file="$VM_DIR/${VM_NAME}.qcow2"
    create_disk_image "$disk_file" "$DISK_SIZE"
    
    echo ""
    print_info "Launching CyberOS..."
    print_info "Press Ctrl+C to stop the VM"
    echo ""
    
    # Build and run QEMU command
    local qemu_cmd=$(build_qemu_command "$disk_file")
    
    # Display command for debugging
    if [[ "${DEBUG:-}" == "1" ]]; then
        print_info "QEMU command:"
        echo "$qemu_cmd"
        echo ""
    fi
    
    # Run QEMU (allow errors/interrupts)
    set +e
    eval "$qemu_cmd"
    local exit_code=$?
    set -e
    
    if [[ $exit_code -eq 0 ]] || [[ $exit_code -eq 130 ]]; then
        print_success "VM stopped gracefully"
    elif [[ $exit_code -ne 130 ]]; then
        print_warning "VM exited with code $exit_code"
    fi
    
    echo ""
    print_info "VM data saved to: $disk_file"
}

################################################################################
# Main Script
################################################################################

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -c|--cores)
                CORES="$2"
                shift 2
                ;;
            -m|--memory)
                MEMORY="$2"
                shift 2
                ;;
            -s|--size)
                DISK_SIZE="$2"
                shift 2
                ;;
            -n|--network)
                ENABLE_NETWORK=true
                shift
                ;;
            -d|--display)
                DISPLAY_MODE="$2"
                shift 2
                ;;
            -v|--vm-name)
                VM_NAME="$2"
                shift 2
                ;;
            --no-kvm)
                USE_KVM=false
                shift
                ;;
            --create)
                VM_NAME="$2"
                shift 2
                ;;
            --delete)
                delete_vm "$2"
                exit $?
                ;;
            --list)
                setup_vm_directory
                list_vms
                exit 0
                ;;
            --check)
                print_header
                check_dependencies
                exit $?
                ;;
            -h|--help)
                print_header
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use -h or --help for help"
                exit 1
                ;;
        esac
    done
    
    # Load configuration file if it exists
    load_config
    
    # Run the VM
    run_vm
}

# Run main function
main "$@"
