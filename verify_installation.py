#!/usr/bin/env python3
"""
VoiceMix Verification Script
Checks if the installation is correct and all components are accessible
"""

import sys
import os
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_status(message, success=True):
    """Print a status message with color"""
    symbol = "✓" if success else "✗"
    color = GREEN if success else RED
    print(f"{color}{symbol}{RESET} {message}")


def print_section(title):
    """Print a section header"""
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{title}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_status(f"Python {version.major}.{version.minor}.{version.micro}", True)
        return True
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)", False)
        return False


def check_dependencies():
    """Check if required dependencies are installed"""
    dependencies = {
        'PyQt6': 'PyQt6.QtWidgets',
        'numpy': 'numpy',
        'librosa': 'librosa',
        'soundfile': 'soundfile',
        'pydub': 'pydub',
        'scipy': 'scipy',
    }
    
    all_installed = True
    for name, module in dependencies.items():
        try:
            __import__(module.split('.')[0])
            print_status(f"{name} installed", True)
        except ImportError:
            print_status(f"{name} NOT installed", False)
            all_installed = False
    
    return all_installed


def check_project_structure():
    """Check if project structure is correct"""
    required_paths = [
        'src/voicemix_app.py',
        'src/audio_processor.py',
        'src/config.py',
        'src/__init__.py',
        'requirements.txt',
        'README.md',
        'docs/SETUP.md',
        'docs/USER_GUIDE.md',
        'tests/test_audio_processor.py',
    ]
    
    all_present = True
    for path in required_paths:
        if Path(path).exists():
            print_status(f"{path}", True)
        else:
            print_status(f"{path} NOT FOUND", False)
            all_present = False
    
    return all_present


def check_directories():
    """Check if required directories exist"""
    required_dirs = ['src', 'tests', 'docs', 'output', 'resources']
    
    all_present = True
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            print_status(f"{dir_name}/ directory", True)
        else:
            print_status(f"{dir_name}/ directory NOT FOUND", False)
            all_present = False
    
    return all_present


def verify_imports():
    """Verify that custom modules can be imported"""
    sys.path.insert(0, 'src')
    
    try:
        from audio_processor import AudioProcessor
        print_status("audio_processor module imports successfully", True)
        
        from config import APP_NAME, APP_VERSION
        print_status(f"config module imports successfully (App: {APP_NAME} v{APP_VERSION})", True)
        
        return True
    except Exception as e:
        print_status(f"Module import failed: {e}", False)
        return False


def main():
    """Main verification routine"""
    print(f"\n{BOLD}VoiceMix Installation Verification{RESET}")
    print(f"{'='*60}\n")
    
    # Check Python version
    print_section("1. Python Version")
    python_ok = check_python_version()
    
    # Check project structure
    print_section("2. Project Structure")
    structure_ok = check_project_structure()
    
    # Check directories
    print_section("3. Required Directories")
    dirs_ok = check_directories()
    
    # Check dependencies
    print_section("4. Python Dependencies")
    deps_ok = check_dependencies()
    
    # Verify module imports
    print_section("5. Module Imports")
    imports_ok = verify_imports()
    
    # Summary
    print_section("Summary")
    
    checks = {
        'Python Version': python_ok,
        'Project Structure': structure_ok,
        'Directories': dirs_ok,
        'Dependencies': deps_ok,
        'Module Imports': imports_ok,
    }
    
    all_ok = all(checks.values())
    
    for check, status in checks.items():
        print_status(f"{check}: {'PASS' if status else 'FAIL'}", status)
    
    print(f"\n{BOLD}{'='*60}{RESET}")
    if all_ok:
        print(f"{GREEN}{BOLD}✓ All checks passed! VoiceMix is ready to use.{RESET}")
        print(f"\n{BOLD}To access the interface:{RESET}")
        print(f"  ./run_app.sh     # macOS/Linux")
        print(f"  run_app.bat      # Windows")
        print(f"\n  or manually:")
        print(f"  cd src")
        print(f"  python voicemix_app.py")
        print(f"\n{BOLD}Need help?{RESET} See: docs/HOW_TO_RUN.md")
    elif not deps_ok:
        print(f"{YELLOW}{BOLD}⚠ Dependencies missing. Install them first:{RESET}")
        print(f"  pip install -r requirements.txt")
        print(f"\n  Or run the quick start script:")
        print(f"  ./quick_start.sh     # macOS/Linux")
        print(f"  quick_start.bat      # Windows")
    else:
        print(f"{RED}{BOLD}✗ Some checks failed. Please review the output above.{RESET}")
    
    print(f"{BOLD}{'='*60}{RESET}\n")
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
