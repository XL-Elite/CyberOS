#!/bin/bash

################################################################################
# CyberOS - Root Filesystem Build Script
#
# This script creates the minimal root filesystem for CyberOS using BusyBox.
################################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="${PROJECT_ROOT}/build/rootfs"
ROOTFS_DIR="${PROJECT_ROOT}/rootfs"

echo "[*] Building root filesystem..."

# Create directories
mkdir -p "$BUILD_DIR"/{bin,sbin,etc,lib,usr,var,tmp,proc,sys,root,home,boot,dev,mnt}

# Create standard directory structure
mkdir -p "$BUILD_DIR"/{usr/{bin,sbin,lib,share},var/{log,run,tmp}}

# Create network configuration directory
mkdir -p "$BUILD_DIR/etc/network"
mkdir -p "$BUILD_DIR/etc/rc.d"
mkdir -p "$BUILD_DIR/etc/init.d"

# Create necessary files
cat > "$BUILD_DIR/etc/fstab" << 'EOF'
# CyberOS filesystem mount table
/dev/sda1   /   ext4   defaults,errors=remount-ro    0   1
proc        /proc   proc   defaults                     0   0
sysfs       /sys    sysfs  defaults                     0   0
EOF

cat > "$BUILD_DIR/etc/hostname" << 'EOF'
cyberos
EOF

cat > "$BUILD_DIR/etc/hosts" << 'EOF'
127.0.0.1       localhost
127.0.0.1       cyberos
::1             localhost
EOF

cat > "$BUILD_DIR/etc/inittab" << 'EOF'
# CyberOS init configuration
id:3:initdefault:
si::sysinit:/etc/rc.d/rc.sysinit
l0:0:wait:/etc/rc.d/rc 0
l1:1:wait:/etc/rc.d/rc 1
l2:2:wait:/etc/rc.d/rc 2
l3:3:wait:/etc/rc.d/rc 3
l6:6:wait:/etc/rc.d/rc 6
ca::ctrlaltdel:/sbin/shutdown -t3 -r now
1:2345:respawn:/sbin/getty 38400 tty1
EOF

cat > "$BUILD_DIR/etc/network/interfaces" << 'EOF'
# CyberOS network configuration
auto lo
iface lo inet loopback

# Uncomment and edit for static IP
# auto eth0
# iface eth0 inet static
#     address 192.168.1.10
#     netmask 255.255.255.0
#     gateway 192.168.1.1

# Or use DHCP (default)
auto eth0
iface eth0 inet dhcp
EOF

# Create system initialization script
cat > "$BUILD_DIR/etc/rc.d/rc.sysinit" << 'EOF'
#!/bin/sh
# System initialization script

echo "Initializing CyberOS..."
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t devtmpfs none /dev

echo "System initialization complete"
EOF

chmod +x "$BUILD_DIR/etc/rc.d/rc.sysinit"

# Create basic init scripts
cat > "$BUILD_DIR/etc/init.d/rcS" << 'EOF'
#!/bin/sh
# Main runlevel script
exec /etc/rc.local
EOF

chmod +x "$BUILD_DIR/etc/init.d/rcS"

# Create rc.local
cat > "$BUILD_DIR/etc/rc.local" << 'EOF'
#!/bin/sh
# Local runlevel configuration

echo "CyberOS v0.1.0-alpha"
echo "Type 'help' for available commands"

exit 0
EOF

chmod +x "$BUILD_DIR/etc/rc.local"

# Set permissions
chmod 755 "$BUILD_DIR"
chmod 700 "$BUILD_DIR/root"
chmod 1777 "$BUILD_DIR/tmp"
chmod 1777 "$BUILD_DIR/var/tmp"

echo "[✓] Root filesystem created"
echo "    Output: $BUILD_DIR"
