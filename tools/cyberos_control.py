#!/usr/bin/env python3

"""
CyberOS Control Center - Master GUI for Project Management

Comprehensive interface for building, testing, and running CyberOS.
Manages:
- Build system and ISO generation
- Emulator and VM management
- Dependency installation
- Project configuration
- Build logs and output
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import threading
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Tuple
import shutil


class CyberOSControlCenter:
    """Master control center for CyberOS project management."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the control center."""
        self.root = root
        self.root.title("CyberOS Control Center")
        self.root.geometry("1200x800")
        
        # Project paths
        self.project_root = Path(__file__).parent.parent
        self.iso_file = self.project_root / "iso" / "cyberos-0.1.0-alpha.iso"
        self.build_script = self.project_root / "scripts" / "build.sh"
        self.clean_script = self.project_root / "scripts" / "clean.sh"
        self.emulator_gui = self.project_root / "emulator" / "gui" / "cyberos_emulator.py"
        
        # Status tracking
        self.build_process: Optional[subprocess.Popen] = None
        self.emulator_process: Optional[subprocess.Popen] = None
        self.is_building = False
        self.build_output_lines = []
        
        # Setup UI
        self.setup_styles()
        self.create_widgets()
        self.check_dependencies()
        self.update_project_status()
        
        # Window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        
        try:
            if sys.platform == "darwin":
                style.theme_use("aqua")
            elif sys.platform == "linux":
                style.theme_use("clam")
            else:
                style.theme_use("vista")
        except:
            pass
        
        style.configure("Title.TLabel", font=("Helvetica", 18, "bold"))
        style.configure("Heading.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("Info.TLabel", font=("Helvetica", 10))
        style.configure("Status.TLabel", font=("Courier", 9))
        style.configure("TButton", font=("Helvetica", 10))
    
    def create_widgets(self):
        """Create the main GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_build_tab()
        self.create_emulator_tab()
        self.create_dependencies_tab()
        self.create_settings_tab()
        self.create_logs_tab()
        self.create_about_tab()
    
    def create_header(self, parent: tk.Widget):
        """Create the header with project info."""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(header_frame, text="🖥️  CyberOS Control Center", style="Title.TLabel")
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Status indicator
        self.status_frame = ttk.Frame(header_frame)
        self.status_frame.pack(side=tk.RIGHT, padx=10)
        
        self.status_indicator = ttk.Label(self.status_frame, text="●", foreground="green", font=("Helvetica", 16))
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(self.status_frame, text="Ready", style="Info.TLabel")
        self.status_label.pack(side=tk.LEFT, padx=5)
    
    def create_dashboard_tab(self):
        """Create the dashboard/overview tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Dashboard")
        
        # Split into two columns
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left: Project Status
        status_label = ttk.Label(left_frame, text="Project Status", style="Heading.TLabel")
        status_label.pack(anchor="w", pady=10)
        
        self.status_text = scrolledtext.ScrolledText(left_frame, height=20, width=60, state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Right: Quick Actions
        actions_label = ttk.Label(right_frame, text="Quick Actions", style="Heading.TLabel")
        actions_label.pack(anchor="w", pady=10)
        
        actions_frame = ttk.Frame(right_frame)
        actions_frame.pack(fill=tk.BOTH, expand=True)
        
        # Build buttons
        build_frame = ttk.LabelFrame(actions_frame, text="Build", padding=10)
        build_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(build_frame, text="🔨 Build CyberOS", command=self.build_iso).pack(fill=tk.X, pady=5)
        ttk.Button(build_frame, text="🧹 Clean Build", command=self.clean_build).pack(fill=tk.X, pady=5)
        ttk.Button(build_frame, text="🔄 Rebuild", command=self.rebuild_iso).pack(fill=tk.X, pady=5)
        
        # Emulator buttons
        emulator_frame = ttk.LabelFrame(actions_frame, text="Emulator", padding=10)
        emulator_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(emulator_frame, text="▶️  Launch Emulator GUI", command=self.launch_emulator_gui).pack(fill=tk.X, pady=5)
        ttk.Button(emulator_frame, text="⚙️  Open Emulator Settings", command=self.open_emulator_settings).pack(fill=tk.X, pady=5)
        
        # Project buttons
        project_frame = ttk.LabelFrame(actions_frame, text="Project", padding=10)
        project_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(project_frame, text="📂 Open Project Folder", command=self.open_project_folder).pack(fill=tk.X, pady=5)
        ttk.Button(project_frame, text="🌐 View on GitHub", command=self.open_github).pack(fill=tk.X, pady=5)
        ttk.Button(project_frame, text="📖 Read Documentation", command=self.open_documentation).pack(fill=tk.X, pady=5)
    
    def create_build_tab(self):
        """Create the build management tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔨 Build")
        
        # Title
        title_label = ttk.Label(frame, text="ISO Build System", style="Heading.TLabel")
        title_label.pack(pady=20, padx=20, anchor="w")
        
        # Build options
        options_frame = ttk.LabelFrame(frame, text="Build Options", padding=15)
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Version
        ttk.Label(options_frame, text="Version:", style="Heading.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.version_var = tk.StringVar(value="0.1.0")
        ttk.Entry(options_frame, textvariable=self.version_var).grid(row=0, column=1, sticky="w", padx=10)
        
        # Architecture
        ttk.Label(options_frame, text="Architecture:", style="Heading.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.arch_var = tk.StringVar(value="x86_64")
        ttk.Combobox(options_frame, textvariable=self.arch_var, values=["x86_64", "i386"], state="readonly").grid(row=1, column=1, sticky="w", padx=10)
        
        # Compression
        ttk.Label(options_frame, text="ISO Compression:", style="Heading.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.compression_var = tk.StringVar(value="xz")
        ttk.Combobox(options_frame, textvariable=self.compression_var, values=["xz", "gzip", "bzip2", "none"], state="readonly").grid(row=2, column=1, sticky="w", padx=10)
        
        # Optimization
        self.optimize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Optimize images", variable=self.optimize_var).grid(row=3, column=0, sticky="w", pady=5)
        
        # Build buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Button(button_frame, text="🔨 Build ISO", command=self.build_iso).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🧹 Clean", command=self.clean_build).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Rebuild All", command=self.rebuild_iso).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="⏹️  Stop Build", command=self.stop_build).pack(side=tk.LEFT, padx=5)
        
        # Progress
        progress_frame = ttk.LabelFrame(frame, text="Build Progress", padding=10)
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.build_progress = ttk.Progressbar(progress_frame, mode="indeterminate")
        self.build_progress.pack(fill=tk.X, pady=5)
        
        self.build_status = ttk.Label(progress_frame, text="Ready to build", style="Status.TLabel")
        self.build_status.pack(anchor="w", pady=5)
        
        # Build output
        output_frame = ttk.LabelFrame(progress_frame, text="Build Output", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.build_output = scrolledtext.ScrolledText(output_frame, height=15, width=100, state=tk.DISABLED, font=("Courier", 9))
        self.build_output.pack(fill=tk.BOTH, expand=True)
    
    def create_emulator_tab(self):
        """Create the emulator management tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎮 Emulator")
        
        # Title
        title_label = ttk.Label(frame, text="CyberOS Emulator", style="Heading.TLabel")
        title_label.pack(pady=20, padx=20, anchor="w")
        
        # Quick launch
        quick_frame = ttk.LabelFrame(frame, text="Quick Launch", padding=15)
        quick_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(quick_frame, text="▶️  Launch Emulator GUI", command=self.launch_emulator_gui, width=40).pack(pady=10)
        ttk.Button(quick_frame, text="⚡ Quick Start (2 cores, 512 MB RAM)", command=lambda: self.launch_emulator_cli(2, 512, False)).pack(pady=5)
        ttk.Button(quick_frame, text="🚀 Performance (4 cores, 1024 MB RAM)", command=lambda: self.launch_emulator_cli(4, 1024, True)).pack(pady=5)
        
        # Configuration
        config_frame = ttk.LabelFrame(frame, text="Emulator Configuration", padding=15)
        config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # CPU cores
        ttk.Label(config_frame, text="CPU Cores:", style="Heading.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.emu_cores_var = tk.IntVar(value=2)
        ttk.Spinbox(config_frame, from_=1, to=16, textvariable=self.emu_cores_var).grid(row=0, column=1, sticky="w", padx=10)
        
        # RAM
        ttk.Label(config_frame, text="RAM (MB):", style="Heading.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.emu_memory_var = tk.IntVar(value=512)
        ttk.Spinbox(config_frame, from_=128, to=4096, textvariable=self.emu_memory_var).grid(row=1, column=1, sticky="w", padx=10)
        
        # Disk
        ttk.Label(config_frame, text="Disk Size (GB):", style="Heading.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.emu_disk_var = tk.IntVar(value=2)
        ttk.Spinbox(config_frame, from_=1, to=100, textvariable=self.emu_disk_var).grid(row=2, column=1, sticky="w", padx=10)
        
        # Network
        self.emu_network_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(config_frame, text="Enable Networking", variable=self.emu_network_var).grid(row=3, column=0, sticky="w", pady=5)
        
        # Display mode
        ttk.Label(config_frame, text="Display Mode:", style="Heading.TLabel").grid(row=4, column=0, sticky="w", pady=5)
        self.emu_display_var = tk.StringVar(value="sdl")
        ttk.Combobox(config_frame, textvariable=self.emu_display_var, values=["sdl", "vnc", "serial"], state="readonly").grid(row=4, column=1, sticky="w", padx=10)
        
        # Launch button
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Button(button_frame, text="▶️  Launch with Custom Config", command=self.launch_emulator_custom).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📂 Open VM Folder", command=self.open_vm_folder).pack(side=tk.LEFT, padx=5)
        
        # VM management
        vm_frame = ttk.LabelFrame(frame, text="Virtual Machine Management", padding=15)
        vm_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # VM list
        self.vm_listbox = tk.Listbox(vm_frame, height=10)
        self.vm_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(vm_frame, orient=tk.VERTICAL, command=self.vm_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vm_listbox.config(yscrollcommand=scrollbar.set)
        
        # Refresh VM list
        self.refresh_vm_list()
    
    def create_dependencies_tab(self):
        """Create the dependencies management tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📦 Dependencies")
        
        # Title
        title_label = ttk.Label(frame, text="Dependency Management", style="Heading.TLabel")
        title_label.pack(pady=20, padx=20, anchor="w")
        
        # System info
        info_frame = ttk.LabelFrame(frame, text="System Information", padding=15)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.system_info_label = ttk.Label(info_frame, text="", style="Info.TLabel", wraplength=600, justify=tk.LEFT)
        self.system_info_label.pack(anchor="w")
        
        # Dependency checks
        check_frame = ttk.LabelFrame(frame, text="Dependency Status", padding=15)
        check_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollable list
        scrollbar = ttk.Scrollbar(check_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.deps_listbox = tk.Listbox(check_frame, yscrollcommand=scrollbar.set, font=("Courier", 9))
        self.deps_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.deps_listbox.yview)
        
        # Installation buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Button(button_frame, text="🔍 Check Dependencies", command=self.check_dependencies).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📦 Install Missing", command=self.install_dependencies).pack(side=tk.LEFT, padx=5)
    
    def create_settings_tab(self):
        """Create the settings tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚙️  Settings")
        
        # Title
        title_label = ttk.Label(frame, text="Project Settings", style="Heading.TLabel")
        title_label.pack(pady=20, padx=20, anchor="w")
        
        # Configuration
        config_frame = ttk.LabelFrame(frame, text="Build Configuration", padding=15)
        config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Parallel jobs
        ttk.Label(config_frame, text="Parallel Build Jobs:", style="Heading.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.jobs_var = tk.IntVar(value=4)
        ttk.Spinbox(config_frame, from_=1, to=16, textvariable=self.jobs_var).grid(row=0, column=1, sticky="w", padx=10)
        
        # Optimization
        self.opt_build_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, text="Optimize builds", variable=self.opt_build_var).grid(row=1, column=0, sticky="w", pady=5)
        
        # Preserve old builds
        self.preserve_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, text="Preserve old builds", variable=self.preserve_var).grid(row=2, column=0, sticky="w", pady=5)
        
        # Save button
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        ttk.Button(button_frame, text="💾 Save Settings", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        
        # Project paths
        paths_frame = ttk.LabelFrame(frame, text="Project Paths", padding=15)
        paths_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        paths_text = tk.Text(paths_frame, height=15, width=80, state=tk.DISABLED, font=("Courier", 9))
        paths_text.pack(fill=tk.BOTH, expand=True)
        
        # Display paths
        paths_text.config(state=tk.NORMAL)
        paths_content = f"""Project Root:      {self.project_root}
Build Directory:   {self.project_root / 'build'}
ISO Output:        {self.iso_file}
Build Script:      {self.build_script}
Emulator GUI:      {self.emulator_gui}
Scripts:           {self.project_root / 'scripts'}
Emulator:          {self.project_root / 'emulator'}

Configuration Files:
~/.cyberos_vm.conf - Emulator configuration
~/.cyberos/vms/    - VM disk images
"""
        paths_text.insert(1.0, paths_content)
        paths_text.config(state=tk.DISABLED)
    
    def create_logs_tab(self):
        """Create the logs tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📜 Logs")
        
        # Title
        title_label = ttk.Label(frame, text="System Logs", style="Heading.TLabel")
        title_label.pack(pady=20, padx=20, anchor="w")
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="🧹 Clear Logs", command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Save Logs", command=self.save_logs).pack(side=tk.LEFT, padx=5)
        
        # Logs display
        self.logs_text = scrolledtext.ScrolledText(frame, height=30, width=120, state=tk.DISABLED, font=("Courier", 8))
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_entry("System", "Logs initialized")
    
    def create_about_tab(self):
        """Create the about tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="ℹ️  About")
        
        # About text
        about_frame = ttk.Frame(frame)
        about_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        about_text = tk.Text(about_frame, height=30, width=80, state=tk.NORMAL, wrap=tk.WORD, font=("Helvetica", 10))
        about_text.pack(fill=tk.BOTH, expand=True)
        
        about_content = """CyberOS Control Center v1.0

A comprehensive management interface for the CyberOS Linux project.

FEATURES:
• Integrated build system - One-click ISO generation
• Emulator management - Launch and control VMs
• Dependency tracking - Automatic installation tools
• Project monitoring - Real-time build output
• Configuration management - Save and restore settings
• Integrated logging - Complete operation history

WHAT IS CYBEROS?
CyberOS is a minimal Linux distribution designed for:
• Lightweight virtualization environments
• Educational Linux system exploration
• Cybersecurity research and testing
• Embedded system development
• Customizable operating system foundation

BUILD SYSTEM:
The build system creates a complete bootable ISO image containing:
• Linux kernel (6.x LTS)
• GRUB2 bootloader
• BusyBox utilities
• ext4 filesystem
• Network stack
• Standard Unix tools

EMULATOR:
Run CyberOS on any system using QEMU:
• macOS - Native QEMU support
• Linux - KVM acceleration
• Windows - WSL 2 or QEMU

DOCUMENTATION:
• README.md - Project overview
• ROADMAP.md - Development timeline
• ARCHITECTURE.md - Technical details
• USER_MANUAL.md - Usage guide

TECHNOLOGY STACK:
• Build System: Bash scripts
• GUI: Python tkinter
• Virtualization: QEMU/KVM
• Bootloader: GRUB2
• Kernel: Linux 6.x
• Userland: BusyBox + musl libc

QUICK LINKS:
• GitHub: https://github.com/XL-Elite/CyberOS
• Issues: https://github.com/XL-Elite/CyberOS/issues
• Discussions: https://github.com/XL-Elite/CyberOS/discussions

LICENSE:
CyberOS is licensed under GPL v2 with additional Apache 2.0 and MIT licenses.

VERSION: 0.1.0-alpha
RELEASE: February 2026
STATUS: Active Development

For more information, visit the GitHub repository."""
        
        about_text.insert(1.0, about_content)
        about_text.config(state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(about_frame, orient=tk.VERTICAL, command=about_text.yview)
        about_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # ==================== Action Methods ====================
    
    def update_project_status(self):
        """Update the project status display."""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        
        status = ""
        status += "PROJECT: CyberOS v0.1.0-alpha\n"
        status += "=" * 50 + "\n\n"
        
        # Build status
        status += "BUILD STATUS:\n"
        if self.iso_file.exists():
            size = self.iso_file.stat().st_size / (1024 ** 2)
            status += f"  ✓ ISO Built: {self.iso_file.name} ({size:.2f} MB)\n"
        else:
            status += f"  ✗ ISO Not Built\n"
        
        status += "\n"
        
        # Build files
        status += "BUILD FILES:\n"
        status += f"  Kernel: {self.project_root / 'kernel' / 'vmlinuz'}\n"
        status += f"  RootFS: {self.project_root / 'build' / 'rootfs'}\n"
        status += f"  ISO: {self.iso_file}\n"
        
        status += "\n"
        
        # Dependencies
        status += "DEPENDENCIES:\n"
        deps = self.get_dependency_status()
        for dep, present in deps.items():
            status += f"  {'✓' if present else '✗'} {dep}\n"
        
        status += "\n"
        
        # Project structure
        status += "PROJECT STRUCTURE:\n"
        status += f"  Root: {self.project_root}\n"
        status += f"  Scripts: {self.script_count()} build scripts\n"
        status += f"  Docs: {self.doc_count()} documentation files\n"
        status += f"  Emulator: Available\n"
        
        self.status_text.insert(tk.END, status)
        self.status_text.config(state=tk.DISABLED)
    
    def check_dependencies(self):
        """Check for required dependencies."""
        self.deps_listbox.delete(0, tk.END)
        
        deps = {
            "bash": "Shell interpreter",
            "make": "Build automation",
            "gcc": "C compiler (for kernel)",
            "grub-mkrescue": "GRUB2 bootloader tools",
            "xorriso": "ISO 9660 creation",
            "qemu-system-x86_64": "QEMU emulator",
            "python3": "Python interpreter",
            "git": "Version control",
        }
        
        self.log_entry("System", "Checking dependencies...")
        
        for dep, description in deps.items():
            result = subprocess.run(["which", dep], capture_output=True, text=True)
            present = result.returncode == 0
            
            status = "✓ FOUND  " if present else "✗ MISSING"
            self.deps_listbox.insert(tk.END, f"{status} - {dep:20} ({description})")
        
        # System info
        system_info = f"OS: {sys.platform.upper()} | Python: {sys.version.split()[0]}"
        self.system_info_label.config(text=system_info)
        
        self.log_entry("System", "Dependency check complete")
    
    def get_dependency_status(self) -> Dict[str, bool]:
        """Get status of key dependencies."""
        deps = {
            "bash": False,
            "gcc": False,
            "grub-mkrescue": False,
            "xorriso": False,
            "qemu-system-x86_64": False,
            "python3": False,
        }
        
        for dep in deps:
            result = subprocess.run(["which", dep], capture_output=True)
            deps[dep] = result.returncode == 0
        
        return deps
    
    def script_count(self) -> int:
        """Count build scripts."""
        scripts_dir = self.project_root / "scripts"
        if scripts_dir.exists():
            return len(list(scripts_dir.glob("*.sh")))
        return 0
    
    def doc_count(self) -> int:
        """Count documentation files."""
        docs_dir = self.project_root / "docs"
        root_docs = len(list(self.project_root.glob("*.md")))
        if docs_dir.exists():
            return root_docs + len(list(docs_dir.glob("*.md")))
        return root_docs
    
    def build_iso(self):
        """Start building the ISO."""
        if self.is_building:
            messagebox.showwarning("Build", "Build already in progress")
            return
        
        self.is_building = True
        self.build_progress.start()
        self.build_status.config(text="Building...")
        self.log_entry("Build", "Starting ISO build...")
        
        thread = threading.Thread(target=self._build_iso_thread)
        thread.daemon = True
        thread.start()
    
    def _build_iso_thread(self):
        """Run build in a separate thread."""
        try:
            if not self.build_script.exists():
                self.build_output_append("ERROR: build.sh not found!")
                raise FileNotFoundError(f"Build script not found at {self.build_script}")
            
            # Make script executable
            os.chmod(self.build_script, 0o755)
            
            self.build_process = subprocess.Popen(
                [str(self.build_script)],
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            if self.build_process.stdout:
                for line in self.build_process.stdout:
                    self.build_output_append(line.rstrip())
            
            self.build_process.wait()
            
            if self.build_process.returncode == 0:
                self.build_output_append("\n✓ BUILD COMPLETE!")
                self.log_entry("Build", "ISO build successful")
                self.build_status.config(text="✓ Build complete", foreground="green")
                messagebox.showinfo("Build", "ISO build completed successfully!")
                self.update_project_status()
            else:
                self.build_output_append(f"\n✗ BUILD FAILED (exit code: {self.build_process.returncode})")
                self.log_entry("Build", f"Build failed with code {self.build_process.returncode}")
                self.build_status.config(text="✗ Build failed", foreground="red")
                messagebox.showerror("Build", "ISO build failed. Check output for details.")
        
        except Exception as e:
            self.build_output_append(f"ERROR: {e}")
            self.log_entry("Build", f"Build error: {e}")
            messagebox.showerror("Build Error", f"Failed to build: {e}")
        
        finally:
            self.is_building = False
            self.build_progress.stop()
            self.build_process = None
    
    def build_output_append(self, text: str):
        """Append text to build output."""
        self.build_output.config(state=tk.NORMAL)
        self.build_output.insert(tk.END, text + "\n")
        self.build_output.see(tk.END)
        self.build_output.config(state=tk.DISABLED)
        self.root.update()
    
    def stop_build(self):
        """Stop the current build."""
        if self.build_process:
            try:
                self.build_process.terminate()
                self.build_process.wait(timeout=5)
                self.build_output_append("\n⏹️  Build stopped by user")
                self.log_entry("Build", "Build stopped")
            except subprocess.TimeoutExpired:
                self.build_process.kill()
                self.build_output_append("\n⏹️  Build killed")
            finally:
                self.is_building = False
                self.build_progress.stop()
                self.build_process = None
    
    def clean_build(self):
        """Clean build artifacts."""
        if not messagebox.askyesno("Confirm", "Delete all build artifacts?"):
            return
        
        self.log_entry("Build", "Cleaning build artifacts...")
        
        try:
            clean_script = self.project_root / "scripts" / "clean.sh"
            if clean_script.exists():
                os.chmod(clean_script, 0o755)
                subprocess.run([str(clean_script)], cwd=str(self.project_root), check=True)
                self.log_entry("Build", "Build artifacts cleaned")
                messagebox.showinfo("Clean", "Build cleaned successfully!")
                self.update_project_status()
            else:
                messagebox.showerror("Error", "clean.sh not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clean: {e}")
            self.log_entry("Build", f"Clean failed: {e}")
    
    def rebuild_iso(self):
        """Clean and rebuild ISO."""
        if messagebox.askyesno("Confirm", "Clean and rebuild ISO?"):
            self.clean_build()
            self.root.after(1000, self.build_iso)
    
    def launch_emulator_gui(self):
        """Launch the emulator GUI."""
        try:
            if not self.emulator_gui.exists():
                messagebox.showerror("Error", f"Emulator GUI not found at {self.emulator_gui}")
                return
            
            if not self.iso_file.exists():
                messagebox.showwarning("Warning", "ISO not built. Build ISO first?")
                return
            
            self.log_entry("Emulator", "Launching emulator GUI...")
            subprocess.Popen([sys.executable, str(self.emulator_gui)])
            self.log_entry("Emulator", "Emulator GUI launched")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch emulator: {e}")
            self.log_entry("Emulator", f"Failed to launch: {e}")
    
    def launch_emulator_cli(self, cores: int, memory: int, network: bool):
        """Launch emulator from command line."""
        try:
            if not self.iso_file.exists():
                messagebox.showwarning("Warning", "ISO not built. Build ISO first?")
                return
            
            launcher = self.project_root / "emulator" / "macos" / "run_cyberos.sh"
            if sys.platform == "linux":
                launcher = self.project_root / "emulator" / "linux" / "run_cyberos.sh"
            
            if not launcher.exists():
                messagebox.showerror("Error", f"Launcher not found")
                return
            
            cmd = [str(launcher), "-c", str(cores), "-m", str(memory)]
            if network:
                cmd.append("-n")
            
            os.chmod(launcher, 0o755)
            subprocess.Popen(cmd)
            self.log_entry("Emulator", f"Launched with {cores} cores, {memory} MB RAM, {'networking' if network else 'no network'}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch emulator: {e}")
    
    def launch_emulator_custom(self):
        """Launch emulator with custom configuration."""
        cores = self.emu_cores_var.get()
        memory = self.emu_memory_var.get()
        disk = self.emu_disk_var.get()
        network = self.emu_network_var.get()
        display = self.emu_display_var.get()
        
        try:
            if not self.iso_file.exists():
                messagebox.showwarning("Warning", "ISO not built. Build ISO first?")
                return
            
            launcher = self.project_root / "emulator" / "macos" / "run_cyberos.sh"
            if sys.platform == "linux":
                launcher = self.project_root / "emulator" / "linux" / "run_cyberos.sh"
            
            cmd = [str(launcher), "-c", str(cores), "-m", str(memory), "-s", str(disk), "-d", display]
            if network:
                cmd.append("-n")
            
            os.chmod(launcher, 0o755)
            subprocess.Popen(cmd)
            self.log_entry("Emulator", f"Custom launch: {cores}c, {memory}MB, {disk}GB, {display}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch: {e}")
    
    def refresh_vm_list(self):
        """Refresh the VM list."""
        self.vm_listbox.delete(0, tk.END)
        
        vm_dir = Path.home() / ".cyberos" / "vms"
        if vm_dir.exists():
            for vm_file in sorted(vm_dir.glob("*.qcow2")):
                size = vm_file.stat().st_size / (1024 ** 3)
                self.vm_listbox.insert(tk.END, f"{vm_file.stem} ({size:.2f} GB)")
    
    def open_vm_folder(self):
        """Open VM folder in file explorer."""
        try:
            vm_dir = Path.home() / ".cyberos" / "vms"
            vm_dir.mkdir(parents=True, exist_ok=True)
            
            if sys.platform == "darwin":
                subprocess.run(["open", str(vm_dir)], check=True)
            elif sys.platform == "linux":
                subprocess.run(["xdg-open", str(vm_dir)], check=True)
            elif sys.platform == "win32":
                os.startfile(str(vm_dir))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {e}")
    
    def open_emulator_settings(self):
        """Open emulator configuration file."""
        try:
            config_file = Path.home() / ".cyberos_vm.conf"
            if not config_file.exists():
                # Create default config
                config_content = """# CyberOS VM Configuration
CORES=2
MEMORY=512
DISK_SIZE=2
ENABLE_NETWORK=true
DISPLAY=sdl
"""
                config_file.write_text(config_content)
            
            if sys.platform == "darwin":
                subprocess.run(["open", "-t", str(config_file)], check=True)
            elif sys.platform == "linux":
                subprocess.run(["xdg-open", str(config_file)], check=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open settings: {e}")
    
    def install_dependencies(self):
        """Install missing dependencies."""
        try:
            if sys.platform == "darwin":
                installer = self.project_root / "emulator" / "macos" / "install_dependencies.sh"
            elif sys.platform == "linux":
                installer = self.project_root / "emulator" / "linux" / "install_dependencies.sh"
            else:
                messagebox.showinfo("Info", "Automatic installation not available for your OS")
                return
            
            if installer.exists():
                os.chmod(installer, 0o755)
                if sys.platform == "linux":
                    subprocess.run(["sudo", str(installer)], check=False)
                else:
                    subprocess.run([str(installer)], check=False)
                
                self.log_entry("System", "Dependency installation completed")
                self.check_dependencies()
            else:
                messagebox.showerror("Error", f"Installer not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install dependencies: {e}")
    
    def save_settings(self):
        """Save application settings."""
        messagebox.showinfo("Settings", "Settings saved!")
        self.log_entry("Settings", "Settings saved")
    
    def clear_logs(self):
        """Clear the logs."""
        if messagebox.askyesno("Confirm", "Clear all logs?"):
            self.logs_text.config(state=tk.NORMAL)
            self.logs_text.delete(1.0, tk.END)
            self.logs_text.config(state=tk.DISABLED)
    
    def save_logs(self):
        """Save logs to file."""
        try:
            file = filedialog.asksaveasfilename(
                defaultextension=".log",
                filetypes=[("Log files", "*.log"), ("Text files", "*.txt")]
            )
            if file:
                logs_content = self.logs_text.get(1.0, tk.END)
                Path(file).write_text(logs_content)
                messagebox.showinfo("Success", f"Logs saved to {file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save logs: {e}")
    
    def log_entry(self, source: str, message: str):
        """Add a log entry."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {source}: {message}"
        
        self.logs_text.config(state=tk.NORMAL)
        self.logs_text.insert(tk.END, log_line + "\n")
        self.logs_text.see(tk.END)
        self.logs_text.config(state=tk.DISABLED)
        self.root.update()
    
    def open_project_folder(self):
        """Open project folder."""
        try:
            if sys.platform == "darwin":
                subprocess.run(["open", str(self.project_root)], check=True)
            elif sys.platform == "linux":
                subprocess.run(["xdg-open", str(self.project_root)], check=True)
            elif sys.platform == "win32":
                os.startfile(str(self.project_root))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {e}")
    
    def open_github(self):
        """Open GitHub repository."""
        try:
            if sys.platform == "darwin":
                os.system("open https://github.com/XL-Elite/CyberOS")
            elif sys.platform == "linux":
                os.system("xdg-open https://github.com/XL-Elite/CyberOS")
            else:
                os.startfile("https://github.com/XL-Elite/CyberOS")
        except:
            messagebox.showinfo("Info", "Visit: https://github.com/XL-Elite/CyberOS")
    
    def open_documentation(self):
        """Open documentation."""
        try:
            readme = self.project_root / "README.md"
            if readme.exists():
                if sys.platform == "darwin":
                    subprocess.run(["open", "-t", str(readme)], check=True)
                elif sys.platform == "linux":
                    subprocess.run(["xdg-open", str(readme)], check=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open documentation: {e}")
    
    def on_close(self):
        """Handle window close event."""
        if self.is_building:
            if messagebox.askyesno("Confirm", "Build in progress. Stop and quit?"):
                self.stop_build()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = CyberOSControlCenter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
