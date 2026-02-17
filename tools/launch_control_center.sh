#!/bin/bash

################################################################################
# CyberOS Control Center Launcher
# 
# Unified interface for managing all CyberOS project tasks.
# Handles: Building, emulator management, dependencies, logging, settings
#
# Run: ./launch_control_center.sh
################################################################################

set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONTROL_APP="${SCRIPT_DIR}/cyberos_control.py"

print_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║      🖥️  CyberOS Control Center - Launcher               ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  INFO:${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓ SUCCESS:${NC} $1"
}

print_error() {
    echo -e "${RED}✗ ERROR:${NC} $1"
}

show_help() {
    cat << 'EOF'
CyberOS Control Center Launcher

USAGE:
    ./launch_control_center.sh [OPTIONS]

OPTIONS:
    --build     Start in Build tab
    --emulator  Start in Emulator tab
    --deps      Start in Dependencies tab
    --logs      Start in Logs tab
    --help      Show this help message

EXAMPLES:
    # Launch Control Center
    ./launch_control_center.sh

    # Start with Build tab active
    ./launch_control_center.sh --build

    # Start with Emulator tab active
    ./launch_control_center.sh --emulator

EOF
}

# Check dependencies
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        echo ""
        echo "Install Python 3:"
        echo "  macOS: brew install python@3.11"
        echo "  Linux: sudo apt-get install python3"
        exit 1
    fi
    
    # Check Python version
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if (( $(echo "$python_version < 3.8" | bc -l) )); then
        print_error "Python 3.8+ required (found $python_version)"
        exit 1
    fi
    
    print_success "Python $python_version found"
}

check_tkinter() {
    if ! python3 -c "import tkinter" 2>/dev/null; then
        print_error "tkinter is not installed"
        echo ""
        echo "Install tkinter:"
        echo "  macOS: brew install python-tk"
        echo "  Linux: sudo apt-get install python3-tk"
        exit 1
    fi
    print_success "tkinter found"
}

launch_app() {
    local tab="${1:-}"
    
    print_info "Launching CyberOS Control Center..."
    
    if [[ -n "$tab" ]]; then
        print_info "Starting with $tab tab active"
        python3 "$CONTROL_APP" --tab "$tab"
    else
        python3 "$CONTROL_APP"
    fi
}

main() {
    print_header
    
    # Parse arguments
    tab=""
    while [[ $# -gt 0 ]]; do
        case $1 in
            --build)
                tab="build"
                shift
                ;;
            --emulator)
                tab="emulator"
                shift
                ;;
            --deps)
                tab="deps"
                shift
                ;;
            --logs)
                tab="logs"
                shift
                ;;
            --help)
                print_header
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Check prerequisites
    print_info "Checking requirements..."
    check_python
    check_tkinter
    
    print_success "All requirements met"
    echo ""
    
    # Launch application
    launch_app "$tab"
}

main "$@"
