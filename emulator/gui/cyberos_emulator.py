#!/usr/bin/env python3

"""
CyberOS Emulator GUI
A cross-platform graphical interface for running CyberOS in QEMU.

Supports macOS, Linux, and Windows with a native-looking interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os
import sys
import threading
import json
from pathlib import Path
from typing import Optional, List, Dict


class CyberOSEmulatorGUI:
    """Main GUI application for CyberOS Emulator."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("CyberOS Emulator")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Set minimum window size
        self.root.minsize(800, 600)
        
        # Configuration
        self.config_dir = Path.home() / ".cyberos"
        self.vm_dir = self.config_dir / "vms"
        self.config_file = Path.home() / ".cyberos_vm.conf"
        self.project_root = Path(__file__).parent.parent.parent
        self.iso_file = self.project_root / "iso" / "cyberos-0.1.0-alpha.iso"
        
        # Ensure directories exist
        self.config_dir.mkdir(exist_ok=True)
        self.vm_dir.mkdir(exist_ok=True)
        
        # Current VM process
        self.vm_process: Optional[subprocess.Popen] = None
        
        # Build GUI
        self.setup_styles()
        self.create_widgets()
        self.load_config()
        self.refresh_vm_list()
        
        # Window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_styles(self):
        """Configure ttk styles for the application."""
        style = ttk.Style()
        
        # Try to use a modern theme
        try:
            if sys.platform == "darwin":
                style.theme_use("aqua")
            elif sys.platform == "linux":
                style.theme_use("clam")
            else:
                style.theme_use("vista")
        except:
            pass
        
        # Custom colors
        style.configure("Title.TLabel", font=("Helvetica", 16, "bold"))
        style.configure("Heading.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("Info.TLabel", font=("Helvetica", 10))
    
    def create_widgets(self):
        """Create the main GUI widgets."""
        # Main container with tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_launcher_tab()
        self.create_vm_manager_tab()
        self.create_console_tab()
        self.create_about_tab()
    
    def create_launcher_tab(self):
        """Create the launcher/configuration tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🚀 Launcher")
        
        # Title
        title_label = ttk.Label(frame, text="Launch CyberOS", style="Title.TLabel")
        title_label.pack(pady=20, padx=20, anchor="w")
        
        # Configuration section
        config_frame = ttk.LabelFrame(frame, text="VM Configuration", padding=15)
        config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # VM Name
        ttk.Label(config_frame, text="VM Name:", style="Heading.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.vm_name_var = tk.StringVar(value="CyberOS-VM")
        vm_name_entry = ttk.Entry(config_frame, textvariable=self.vm_name_var, width=30)
        vm_name_entry.grid(row=0, column=1, sticky="w", pady=5, padx=10)
        
        # CPU Cores
        ttk.Label(config_frame, text="CPU Cores:", style="Heading.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.cores_var = tk.IntVar(value=2)
        cores_spin = ttk.Spinbox(config_frame, from_=1, to=16, textvariable=self.cores_var, width=10)
        cores_spin.grid(row=1, column=1, sticky="w", pady=5, padx=10)
        ttk.Label(config_frame, text="(1-16)", style="Info.TLabel").grid(row=1, column=2, sticky="w", padx=5)
        
        # RAM
        ttk.Label(config_frame, text="RAM (MB):", style="Heading.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.memory_var = tk.IntVar(value=512)
        memory_spin = ttk.Spinbox(config_frame, from_=128, to=8192, textvariable=self.memory_var, width=10)
        memory_spin.grid(row=2, column=1, sticky="w", pady=5, padx=10)
        ttk.Label(config_frame, text="(128-8192)", style="Info.TLabel").grid(row=2, column=2, sticky="w", padx=5)
        
        # Disk Size
        ttk.Label(config_frame, text="Disk Size (GB):", style="Heading.TLabel").grid(row=3, column=0, sticky="w", pady=5)
        self.disk_size_var = tk.IntVar(value=2)
        disk_spin = ttk.Spinbox(config_frame, from_=1, to=100, textvariable=self.disk_size_var, width=10)
        disk_spin.grid(row=3, column=1, sticky="w", pady=5, padx=10)
        ttk.Label(config_frame, text="(1-100)", style="Info.TLabel").grid(row=3, column=2, sticky="w", padx=5)
        
        # Display Mode
        ttk.Label(config_frame, text="Display Mode:", style="Heading.TLabel").grid(row=4, column=0, sticky="w", pady=5)
        self.display_var = tk.StringVar(value="sdl")
        display_combo = ttk.Combobox(config_frame, textvariable=self.display_var, 
                                     values=["sdl", "vnc", "serial"], state="readonly", width=10)
        display_combo.grid(row=4, column=1, sticky="w", pady=5, padx=10)
        ttk.Label(config_frame, text="SDL = GUI, VNC = Remote, Serial = Text", style="Info.TLabel").grid(row=4, column=2, sticky="w", padx=5)
        
        # Networking
        self.network_var = tk.BooleanVar(value=False)
        network_check = ttk.Checkbutton(config_frame, text="Enable Networking", variable=self.network_var)
        network_check.grid(row=5, column=1, sticky="w", pady=10)
        
        # Button section
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Launch button
        launch_btn = ttk.Button(button_frame, text="🚀 Launch CyberOS", command=self.launch_vm)
        launch_btn.pack(side=tk.LEFT, padx=5)
        
        # Save config button
        save_btn = ttk.Button(button_frame, text="💾 Save Configuration", command=self.save_config)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        stop_btn = ttk.Button(button_frame, text="⏹️  Stop VM", command=self.stop_vm, state=tk.DISABLED)
        self.stop_btn = stop_btn
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Status section
        status_frame = ttk.LabelFrame(frame, text="Status", padding=10)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=8, width=80, state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        self.add_status("Ready to launch CyberOS.\n")
        self.add_status("Ensure QEMU is installed: brew install qemu (macOS) or apt install qemu (Linux)\n")
    
    def create_vm_manager_tab(self):
        """Create the VM manager tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💾 VM Manager")
        
        # Title
        title_label = ttk.Label(frame, text="Virtual Machine Management", style="Title.TLabel")
        title_label.pack(pady=20, padx=20, anchor="w")
        
        # VM List
        list_frame = ttk.LabelFrame(frame, text="Saved VMs", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Listbox with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.vm_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Courier", 10))
        self.vm_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.vm_listbox.yview)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        refresh_btn = ttk.Button(button_frame, text="🔄 Refresh List", command=self.refresh_vm_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(button_frame, text="🗑️  Delete Selected", command=self.delete_vm)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        open_dir_btn = ttk.Button(button_frame, text="📁 Open VM Folder", command=self.open_vm_directory)
        open_dir_btn.pack(side=tk.LEFT, padx=5)
        
        # Info section
        info_frame = ttk.LabelFrame(frame, text="VM Information", padding=10)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.vm_info_label = ttk.Label(info_frame, text="Select a VM from the list above", wraplength=600)
        self.vm_info_label.pack(anchor="w")
        
        # Bind selection
        self.vm_listbox.bind("<<ListboxSelect>>", self.on_vm_selected)
    
    def create_console_tab(self):
        """Create the console/output tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📺 Console")
        
        # Title
        title_label = ttk.Label(frame, text="Console Output", style="Title.TLabel")
        title_label.pack(pady=20, padx=20, anchor="w")
        
        # Console output
        console_frame = ttk.LabelFrame(frame, text="VM Output", padding=10)
        console_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.console_text = scrolledtext.ScrolledText(console_frame, height=25, width=100, state=tk.DISABLED)
        self.console_text.pack(fill=tk.BOTH, expand=True)
        
        # Clear button
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        clear_btn = ttk.Button(button_frame, text="🧹 Clear Console", command=self.clear_console)
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def create_about_tab(self):
        """Create the about tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="ℹ️  About")
        
        # About text
        about_frame = ttk.Frame(frame)
        about_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        about_text = tk.Text(about_frame, height=30, width=80, state=tk.NORMAL, wrap=tk.WORD)
        about_text.pack(fill=tk.BOTH, expand=True)
        
        about_content = """CyberOS Emulator v1.0

A lightweight, cross-platform emulator for running CyberOS.

FEATURES:
• Easy-to-use graphical interface
• Configurable VM resources (CPU, RAM, disk)
• Multiple display modes (GUI, VNC, Serial)
• Network support
• VM management and persistence
• Cross-platform support (macOS, Linux, Windows)

REQUIREMENTS:
• QEMU (install via: brew install qemu or apt install qemu-system-x86-64)
• Python 3.8+

GETTING STARTED:
1. Build CyberOS: ./scripts/build.sh
2. Configure VM settings in the Launcher tab
3. Click "Launch CyberOS" to start
4. Monitor output in the Console tab

DOCUMENTATION:
For more information, visit:
https://github.com/XL-Elite/CyberOS

LICENSE:
CyberOS Emulator is part of the CyberOS project.
Licensed under GPL v2.

ARCHITECTURE:
• Hypervisor: QEMU/KVM
• Interface: Python tkinter
• Platform: macOS, Linux, Windows"""
        
        about_text.insert(1.0, about_content)
        about_text.config(state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(about_frame, orient=tk.VERTICAL, command=about_text.yview)
        about_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def add_status(self, text: str):
        """Add text to the status window."""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, text)
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()
    
    def add_console(self, text: str):
        """Add text to the console window."""
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, text)
        self.console_text.see(tk.END)
        self.console_text.config(state=tk.DISABLED)
        self.root.update()
    
    def clear_console(self):
        """Clear the console window."""
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete(1.0, tk.END)
        self.console_text.config(state=tk.DISABLED)
    
    def save_config(self):
        """Save current configuration to file."""
        config = {
            "cores": self.cores_var.get(),
            "memory": self.memory_var.get(),
            "disk_size": self.disk_size_var.get(),
            "enable_network": self.network_var.get(),
            "display": self.display_var.get(),
        }
        
        config_content = f"""# CyberOS VM Configuration
CORES={config['cores']}
MEMORY={config['memory']}
DISK_SIZE={config['disk_size']}
ENABLE_NETWORK={'true' if config['enable_network'] else 'false'}
DISPLAY={config['display']}
"""
        
        try:
            self.config_file.write_text(config_content)
            messagebox.showinfo("Success", "Configuration saved successfully!")
            self.add_status(f"Configuration saved to {self.config_file}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            self.add_status(f"Error saving configuration: {e}\n")
    
    def load_config(self):
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                config_content = self.config_file.read_text()
                for line in config_content.split('\n'):
                    if line.startswith('CORES='):
                        self.cores_var.set(int(line.split('=')[1]))
                    elif line.startswith('MEMORY='):
                        self.memory_var.set(int(line.split('=')[1]))
                    elif line.startswith('DISK_SIZE='):
                        self.disk_size_var.set(int(line.split('=')[1]))
                    elif line.startswith('ENABLE_NETWORK='):
                        self.network_var.set(line.split('=')[1].lower() == 'true')
                    elif line.startswith('DISPLAY='):
                        self.display_var.set(line.split('=')[1].strip())
            except Exception as e:
                self.add_status(f"Warning: Could not load configuration: {e}\n")
    
    def check_dependencies(self) -> bool:
        """Check if QEMU is installed."""
        try:
            subprocess.run(["which", "qemu-system-x86_64"], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            messagebox.showerror(
                "Missing Dependency",
                "QEMU is not installed.\n\nPlease install it:\n"
                "• macOS: brew install qemu\n"
                "• Linux: sudo apt-get install qemu-system-x86-64\n"
                "• Windows: https://www.qemu.org/download/"
            )
            return False
    
    def check_iso(self) -> bool:
        """Check if ISO file exists."""
        if not self.iso_file.exists():
            messagebox.showerror(
                "ISO Not Found",
                f"CyberOS ISO not found at:\n{self.iso_file}\n\n"
                "Please build CyberOS first:\n"
                f"cd {self.project_root}\n"
                "./scripts/build.sh"
            )
            return False
        return True
    
    def launch_vm(self):
        """Launch the CyberOS VM."""
        # Check dependencies
        if not self.check_dependencies():
            return
        
        # Check ISO
        if not self.check_iso():
            return
        
        # Disable launch button
        self.notebook.tab(0, state="disabled")
        self.stop_btn.config(state=tk.NORMAL)
        
        self.add_status(f"Launching {self.vm_name_var.get()}...\n")
        
        # Run in thread to avoid blocking GUI
        thread = threading.Thread(target=self._run_vm_thread)
        thread.daemon = True
        thread.start()
    
    def _run_vm_thread(self):
        """Run VM in a separate thread."""
        try:
            cores = self.cores_var.get()
            memory = self.memory_var.get()
            disk_size = self.disk_size_var.get()
            vm_name = self.vm_name_var.get()
            network = self.network_var.get()
            display = self.display_var.get()
            
            disk_file = self.vm_dir / f"{vm_name}.qcow2"
            
            self.add_status(f"Configuration:\n")
            self.add_status(f"  CPU Cores: {cores}\n")
            self.add_status(f"  RAM: {memory} MB\n")
            self.add_status(f"  Disk: {disk_size} GB\n")
            self.add_status(f"  Networking: {'Enabled' if network else 'Disabled'}\n")
            self.add_status(f"  Display: {display}\n\n")
            
            # Create disk image if needed
            if not disk_file.exists():
                self.add_status(f"Creating disk image: {disk_size} GB\n")
                subprocess.run(["qemu-img", "create", "-f", "qcow2", str(disk_file), f"{disk_size}G"], check=True)
                self.add_status(f"Disk image created.\n\n")
            
            # Build QEMU command
            qemu_cmd = [
                "qemu-system-x86_64",
                "-name", vm_name,
                "-machine", "type=q35,accel=tcg",
                "-smp", f"cores={cores}",
                "-m", str(memory),
                "-boot", "d",
                "-cdrom", str(self.iso_file),
                "-drive", f"file={disk_file},format=qcow2",
            ]
            
            # Add display mode
            if display == "vnc":
                qemu_cmd.extend(["-vnc", ":0"])
            elif display == "serial":
                qemu_cmd.extend(["-nographic", "-serial", "stdio"])
            else:
                qemu_cmd.extend(["-display", "default"])
            
            # Add networking
            if network:
                qemu_cmd.extend(["-nic", "user,model=virtio"])
            else:
                qemu_cmd.extend(["-nic", "none"])
            
            self.add_status(f"Starting QEMU...\n")
            self.add_console(f"Starting CyberOS in QEMU...\n")
            self.add_console(f"Command: {' '.join(qemu_cmd)}\n\n")
            
            self.vm_process = subprocess.Popen(
                qemu_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            self.add_status(f"VM launched with PID {self.vm_process.pid}\n")
            
            # Read output
            if self.vm_process.stdout:
                for line in self.vm_process.stdout:
                    self.add_console(line)
            
            self.vm_process.wait()
            
        except Exception as e:
            self.add_status(f"Error: {e}\n")
            self.add_console(f"Error: {e}\n")
            messagebox.showerror("Launch Error", f"Failed to launch VM:\n{e}")
        finally:
            self.vm_process = None
            self.notebook.tab(0, state="normal")
            self.stop_btn.config(state=tk.DISABLED)
            self.add_status(f"VM stopped.\n")
    
    def stop_vm(self):
        """Stop the running VM."""
        if self.vm_process:
            try:
                self.vm_process.terminate()
                self.vm_process.wait(timeout=5)
                self.add_status("VM stopped.\n")
            except subprocess.TimeoutExpired:
                self.vm_process.kill()
                self.add_status("VM killed.\n")
    
    def refresh_vm_list(self):
        """Refresh the list of saved VMs."""
        self.vm_listbox.delete(0, tk.END)
        
        if not self.vm_dir.exists():
            self.vm_listbox.insert(tk.END, "(No VMs saved yet)")
            return
        
        vms = list(self.vm_dir.glob("*.qcow2"))
        if not vms:
            self.vm_listbox.insert(tk.END, "(No VMs saved yet)")
            return
        
        for vm_file in sorted(vms):
            size_bytes = vm_file.stat().st_size
            size_gb = size_bytes / (1024 ** 3)
            vm_name = vm_file.stem
            self.vm_listbox.insert(tk.END, f"{vm_name} ({size_gb:.2f} GB)")
    
    def on_vm_selected(self, event):
        """Handle VM selection from listbox."""
        selection = self.vm_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        vms = list(self.vm_dir.glob("*.qcow2"))
        if index < len(vms):
            vm_file = sorted(vms)[index]
            vm_name = vm_file.stem
            size_bytes = vm_file.stat().st_size
            size_gb = size_bytes / (1024 ** 3)
            
            info = f"VM: {vm_name}\n"
            info += f"Size: {size_gb:.2f} GB\n"
            info += f"Path: {vm_file}\n"
            info += f"Modified: {vm_file.stat().st_mtime}"
            
            self.vm_info_label.config(text=info)
    
    def delete_vm(self):
        """Delete the selected VM."""
        selection = self.vm_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection", "Please select a VM to delete.")
            return
        
        index = selection[0]
        vms = list(self.vm_dir.glob("*.qcow2"))
        if index < len(vms):
            vm_file = sorted(vms)[index]
            
            if messagebox.askyesno("Confirm", f"Delete VM: {vm_file.stem}?\nThis cannot be undone."):
                vm_file.unlink()
                self.add_status(f"Deleted VM: {vm_file.stem}\n")
                self.refresh_vm_list()
    
    def open_vm_directory(self):
        """Open the VM directory in file explorer."""
        try:
            if sys.platform == "darwin":
                subprocess.run(["open", str(self.vm_dir)], check=True)
            elif sys.platform == "linux":
                subprocess.run(["xdg-open", str(self.vm_dir)], check=True)
            elif sys.platform == "win32":
                os.startfile(str(self.vm_dir))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open directory: {e}")
    
    def on_close(self):
        """Handle window close event."""
        if self.vm_process:
            if messagebox.askyesno("Confirm", "A VM is running. Do you want to stop it and quit?"):
                self.stop_vm()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = CyberOSEmulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
