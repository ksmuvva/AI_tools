#!/usr/bin/env python3
"""
ACCESSIBILITY TOOLS DEPENDENCY CHECKER
======================================

Check if all required dependencies for sophisticated accessibility testing are installed.
"""

import subprocess
import sys
import importlib

def check_command(command, name):
    """Check if a command line tool is available"""
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            print(f"✅ {name}: {version}")
            return True
        else:
            print(f"❌ {name}: Not installed")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {name}: Command timed out")
        return False
    except Exception as e:
        print(f"❌ {name}: Error - {str(e)}")
        return False

def check_python_package(package_name, display_name=None):
    """Check if a Python package is installed"""
    if display_name is None:
        display_name = package_name
    
    try:
        importlib.import_module(package_name)
        print(f"✅ {display_name}: Installed")
        return True
    except ImportError:
        print(f"❌ {display_name}: Not installed")
        return False

def main():
    print("🔍 CHECKING ACCESSIBILITY TOOLS DEPENDENCIES")
    print("=" * 80)
    
    print("\n📋 CORE SYSTEM TOOLS:")
    print("-" * 40)
    
    core_tools = [
        (["python", "--version"], "Python"),
        (["node", "--version"], "Node.js"),
        (["npm", "--version"], "npm")
    ]
    
    core_status = []
    for cmd, name in core_tools:
        core_status.append(check_command(cmd, name))
    
    print("\n🌐 ACCESSIBILITY TESTING TOOLS:")
    print("-" * 40)
    
    accessibility_tools = [
        (["lighthouse", "--version"], "Google Lighthouse"),
        (["pa11y", "--version"], "Pa11y"),
        (["axe", "--version"], "axe CLI (Optional)")
    ]
    
    tool_status = []
    for cmd, name in accessibility_tools:
        tool_status.append(check_command(cmd, name))
    
    print("\n🐍 PYTHON PACKAGES:")
    print("-" * 40)
    
    python_packages = [
        ("playwright", "Playwright"),
        ("requests", "Requests"),
        ("asyncio", "AsyncIO"),
        ("json", "JSON"),
        ("logging", "Logging"),
        ("subprocess", "Subprocess"),
        ("re", "Regular Expressions")
    ]
    
    package_status = []
    for package, name in python_packages:
        package_status.append(check_python_package(package, name))
    
    # Check if accessibility tools are importable
    print("\n♿ ACCESSIBILITY MODULES:")
    print("-" * 40)
    
    try:
        from accessiblity_tools import check_accessibility, check_color_contrast, get_wcag22_checklist
        print("✅ Accessibility Tools: All functions available")
        tools_available = True
    except ImportError as e:
        print(f"❌ Accessibility Tools: Import error - {str(e)}")
        tools_available = False
    
    # Summary
    print("\n📊 DEPENDENCY STATUS SUMMARY:")
    print("=" * 80)
    
    core_ok = all(core_status)
    tools_ok = any(tool_status[:2])  # At least lighthouse or pa11y
    packages_ok = all(package_status)
    
    print(f"🔧 Core System Tools: {'✅ READY' if core_ok else '❌ MISSING'}")
    print(f"🌐 Accessibility Tools: {'✅ READY' if tools_ok else '❌ MISSING'}")
    print(f"🐍 Python Packages: {'✅ READY' if packages_ok else '❌ MISSING'}")
    print(f"♿ Accessibility Modules: {'✅ READY' if tools_available else '❌ MISSING'}")
    
    if core_ok and tools_ok and packages_ok and tools_available:
        print("\n🎉 ALL DEPENDENCIES READY!")
        print("✨ You can run sophisticated accessibility testing!")
        
        print("\n🧪 QUICK TEST COMMANDS:")
        print("   python test_sophisticated_accessibility_tools.py")
        print("   python -c \"from accessiblity_tools import *; print('✅ Import successful')\"")
        
    else:
        print("\n⚠️  SOME DEPENDENCIES ARE MISSING!")
        print("\n📋 INSTALLATION INSTRUCTIONS:")
        
        if not core_ok:
            print("\n🔧 Install Core Tools:")
            print("   • Download Node.js: https://nodejs.org/")
            print("   • Verify Python installation")
        
        if not tools_ok:
            print("\n🌐 Install Accessibility Tools:")
            print("   npm install -g lighthouse pa11y")
        
        if not packages_ok:
            print("\n🐍 Install Python Packages:")
            print("   pip install playwright requests asyncio")
            print("   playwright install")
        
        print("\n📖 See INSTALL_DEPENDENCIES.md for detailed instructions")
    
    print("\n" + "=" * 80)
    return core_ok and tools_ok and packages_ok and tools_available

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 