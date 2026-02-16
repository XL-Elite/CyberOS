# CyberOS Bootloader Configuration

This directory contains bootloader-related files for CyberOS, primarily GRUB2 configuration.

## Files

- `grub.cfg` - Main GRUB2 configuration (auto-generated during build)
- `grub.cfg.template` - Template for GRUB configuration
- `boot.S` - Bootloader assembly code (if custom bootloader)

## GRUB2 Configuration

### Location
- Install: `/boot/grub/`
- Source: Generate during build process

### Key Parameters

```
timeout=3          # Menu display timeout in seconds
default=0          # Default menu entry (0-based index)
record_default     # Remember last selection

serial options     # Serial console configuration
terminal options   # Terminal type
```

### Boot Parameters

These kernel parameters are passed at boot time:

- `ro` - Mount root read-only initially
- `quiet` - Suppress most boot messages
- `console=tty0` - Kernel console output
- `vga=normal` - Video mode

## Customization

To customize GRUB entries:

1. Modify `/boot/grub/grub.cfg` on running system
2. Or modify configuration template before build
3. Run `grub-mkconfig -o /boot/grub/grub.cfg` if available

## Building

GRUB2 is created during the build process using:
```bash
./scripts/build.sh
```

## References

- [GRUB2 Manual](https://www.gnu.org/software/grub/manual/grub/)
- [GRUB2 Fedora Guide](https://docs.fedoraproject.org/en-US/fedora/latest/system-administrators-guide/kernel-module-driver-configuration/working-with-the-grub-2-bootloader/)
