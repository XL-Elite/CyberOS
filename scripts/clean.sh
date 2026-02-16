#!/bin/bash

################################################################################
# CyberOS - Clean Build Script
#
# Removes all build artifacts and temporary files.
################################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "[*] Cleaning CyberOS build artifacts..."

# Clean directories
declare -a CLEAN_DIRS=(
    "${PROJECT_ROOT}/build"
    "${PROJECT_ROOT}/iso"
    "${PROJECT_ROOT}/.build"
)

for dir in "${CLEAN_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "[*] Removing $dir"
        rm -rf "$dir"
    fi
done

# Clean temporary files
find "$PROJECT_ROOT" -name "*.tmp" -delete
find "$PROJECT_ROOT" -name ".DS_Store" -delete

echo "[✓] Clean complete"
echo ""
echo "To rebuild, run: ./scripts/build.sh"
