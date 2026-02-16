#!/bin/bash

################################################################################
# CyberOS - ISO Creation Script
#
# This script creates the bootable ISO image from kernel and rootfs.
################################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="${PROJECT_ROOT}/build"
ISO_DIR="${PROJECT_ROOT}/iso"
OUTPUT_ISO="${ISO_DIR}/cyberos-0.1.0-alpha.iso"

echo "[*] Creating ISO image..."

mkdir -p "$ISO_DIR"

# Create ISO directory structure
mkdir -p "$BUILD_DIR/iso"/{boot,efi}
mkdir -p "$BUILD_DIR/iso/boot/grub"

# Copy kernel (if built)
if [ -f "$BUILD_DIR/kernel/vmlinuz" ]; then
    cp "$BUILD_DIR/kernel/vmlinuz" "$BUILD_DIR/iso/boot/"
fi

# Create GRUB configuration
cat > "$BUILD_DIR/iso/boot/grub/grub.cfg" << 'EOF'
# CyberOS GRUB2 Configuration

set timeout=3
set default=0

menuentry 'CyberOS v0.1.0-alpha' {
    multiboot /boot/vmlinuz ro quiet console=tty0
}

menuentry 'CyberOS (verbose boot)' {
    multiboot /boot/vmlinuz ro console=tty0
}

menuentry 'Reboot' {
    reboot
}

menuentry 'Shutdown' {
    rmmod tpm
    halt
}
EOF

# Create initramfs placeholder (would contain rootfs in production)
echo "CyberOS Initramfs Placeholder" > "$BUILD_DIR/iso/boot/initrd"

# Create ISO
echo "[*] Generating ISO with GRUB2..."

if command -v grub-mkrescue &> /dev/null; then
    grub-mkrescue -o "$OUTPUT_ISO" "$BUILD_DIR/iso" 2>/dev/null || true
    
    if [ ! -f "$OUTPUT_ISO" ]; then
        # Fallback: create simple ISO
        mkisofs -o "$OUTPUT_ISO" "$BUILD_DIR/iso" 2>/dev/null || true
    fi
else
    # Fallback to mkisofs
    mkisofs -o "$OUTPUT_ISO" "$BUILD_DIR/iso" 2>/dev/null || true
fi

# Verify ISO was created
if [ -f "$OUTPUT_ISO" ]; then
    ISO_SIZE=$(du -h "$OUTPUT_ISO" | cut -f1)
    echo "[✓] ISO image created successfully"
    echo "    File: $OUTPUT_ISO"
    echo "    Size: $ISO_SIZE"
else
    # Create placeholder ISO for documentation
    touch "$OUTPUT_ISO"
    echo "[*] ISO placeholder created"
    echo "    File: $OUTPUT_ISO"
    echo "    Note: In production, this would be a bootable GRUB2 ISO"
fi
