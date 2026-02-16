# CyberOS - Contributing Guidelines

Thank you for your interest in contributing to CyberOS! We welcome contributions from developers, designers, and documentation writers of all skill levels.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Workflow](#development-workflow)
5. [Coding Standards](#coding-standards)
6. [Commit Messages](#commit-messages)
7. [Pull Request Process](#pull-request-process)
8. [Testing](#testing)
9. [Documentation](#documentation)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. We pledge that everyone participating in the CyberOS community will treat others with respect and kindness.

### Our Standards

Examples of behavior that contributes to creating a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing opinions and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement

Instances of unacceptable behavior may be reported to the project maintainers. All reports will be kept confidential.

---

## Getting Started

### Prerequisites

- Linux development environment
- Git
- gcc, make, and build tools
- QEMU/KVM or VirtualBox for testing
- Basic understanding of Linux systems

### Setup Development Environment

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/CyberOS.git
cd CyberOS

# 3. Add upstream remote
git remote add upstream https://github.com/XL-Elite/CyberOS.git

# 4. Install development dependencies
# On Ubuntu/Debian:
sudo apt-get update
sudo apt-get install build-essential git gcc make qemu-system-x86 grub-common

# 5. Verify build tools
make --version
gcc --version
```

---

## How to Contribute

### Types of Contributions

We welcome all types of contributions:

1. **Code Contributions**
   - Bug fixes
   - Feature implementations
   - Performance optimizations
   - Code refactoring

2. **Documentation**
   - User guides
   - API documentation
   - Tutorial creation
   - Typo fixes

3. **Testing & QA**
   - Bug reports
   - Testing on different hypervisors
   - Performance testing
   - Compatibility verification

4. **Design & UI**
   - Web interface improvements
   - Logo and branding
   - User experience enhancements

---

## Development Workflow

### 1. Branch Naming Convention

```
<type>/<short-description>
```

Types:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `test/` - Testing
- `perf/` - Performance improvements
- `refactor/` - Code refactoring

Examples:
```
feature/package-manager
fix/boot-timeout-issue
docs/installation-guide
```

### 2. Creating a Feature Branch

```bash
# Update main branch
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 3. Making Changes

```bash
# Make your changes
# Test thoroughly
# Build and verify

# Stage changes
git add .

# Commit with clear message
git commit -m "Description of changes"

# Push to your fork
git push origin feature/your-feature-name
```

---

## Coding Standards

### Shell Scripts

```bash
#!/bin/bash
# Use bash shebang for shell scripts

# Add header comment
# Description of script
# Usage: ./script.sh [options]

# Use meaningful variable names
BUILD_DIR="./build"
SOURCE_DIR="./src"

# Quote variables
echo "$BUILD_DIR"

# Use [[ ]] for conditionals
if [[ -d "$BUILD_DIR" ]]; then
    echo "Build directory exists"
fi

# Use functions
build_kernel() {
    echo "Building kernel..."
    # implementation
}

# Error handling
set -e  # Exit on error
```

### C Code (Kernel/Bootloader)

```c
/*
 * File: module.c
 * Description: Brief description
 * Author: Your Name
 * License: GPL v2
 */

#include <stdio.h>
#include <stdlib.h>

/* Function comment */
void important_function(int param) {
    /* Implementation */
}
```

### Documentation

- Use Markdown for documentation
- Use clear headings and structure
- Include code examples where relevant
- Add table of contents for long documents
- Use consistent formatting

---

## Commit Messages

### Format

```
<type>: <subject>

<body>

<footer>
```

### Example

```
feat: implement package manager core

Add basic package manager functionality including:
- Package format specification
- Dependency resolution
- Installation mechanism

Closes #123
```

### Guidelines

- First line: 50 characters max
- Use imperative mood ("add" not "added")
- Capitalize first letter
- Reference issues/PRs using `#123` or `Closes #123`

---

## Pull Request Process

### Before Submitting

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test your changes**
   ```bash
   ./scripts/test.sh
   ./scripts/build.sh
   ```

3. **Check code quality**
   ```bash
   # Run linters if available
   # Review your own code
   ```

### Creating a Pull Request

1. Push your branch to your fork
2. Go to GitHub and create a Pull Request
3. Fill out the PR template completely:
   - Describe what you changed
   - Explain why you made these changes
   - Reference related issues
   - List testing performed

### PR Review Process

- Maintainers will review your PR
- Address feedback and suggestions
- Update your PR with changes
- PRs require approval before merging

---

## Testing

### Running Tests

```bash
# Full test suite
./scripts/test.sh

# Specific test
./scripts/test.sh kernel

# Manual testing on VirtualBox
./scripts/build.sh
# Boot ISO in VirtualBox and test functionality
```

### Testing on Different Hypervisors

- VirtualBox 6.x+
- KVM/QEMU
- VMware Workstation
- Hyper-V (optional)

### Bug Testing

When testing for bugs:
1. Document the steps to reproduce
2. Note the expected behavior
3. Describe the actual behavior
4. Include system information
5. Provide screenshots/logs if relevant

---

## Documentation

### Writing Documentation

1. **Install Guide** (`docs/INSTALLATION.md`)
   - Prerequisites
   - Step-by-step instructions
   - Troubleshooting

2. **Architecture** (`docs/ARCHITECTURE.md`)
   - System components
   - Design decisions
   - Data flow diagrams

3. **API Documentation**
   - Function descriptions
   - Parameters and return values
   - Usage examples

4. **README Updates**
   - Keep main README current
   - Add new features to overview
   - Update version information

---

## Issue Tracking

### Creating an Issue

1. Check if issue already exists
2. Use clear, descriptive title
3. Provide detailed description
4. Include steps to reproduce (for bugs)
5. Attach screenshots/logs if relevant
6. Add appropriate labels

### Issue Labels

- `bug` - Something isn't working
- `feature` - Feature request
- `documentation` - Documentation improvements
- `good first issue` - Good for new contributors
- `help wanted` - Need assistance
- `in progress` - Currently being worked on

---

## Recognition

### Contributors

All contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- PROJECT README

### Support

Have questions?
- Check existing issues/discussions
- Create a discussion post
- Email: dev@cyberos.dev

---

## Additional Resources

- [Linux Kernel Coding Style](https://www.kernel.org/doc/html/latest/process/coding-style.html)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Mark down Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

---

## Questions?

If you have questions about contributing, please:
1. Check the FAQ
2. Review existing issues
3. Create a discussion
4. Contact maintainers

---

**Thank you for contributing to CyberOS!**

Last Updated: February 16, 2025
