# ACCESSIBILITY TOOLS DEPENDENCIES INSTALLATION GUIDE
===============================================================

## 🔧 **REQUIRED DEPENDENCIES FOR FULL FUNCTIONALITY**

### 1. **Node.js and npm** (Required for CLI tools)
```bash
# Download and install Node.js from: https://nodejs.org/
# Verify installation:
node --version
npm --version
```

### 2. **Google Lighthouse** (Web page auditing)
```bash
npm install -g lighthouse
# Verify installation:
lighthouse --version
```

### 3. **Pa11y** (Accessibility testing CLI)
```bash
npm install -g pa11y
# Verify installation:
pa11y --version
```

### 4. **Optional: Additional Tools**
```bash
# axe-core CLI (alternative)
npm install -g @axe-core/cli

# HTML_CodeSniffer CLI
npm install -g html_codesniffer
```

## 🐍 **PYTHON DEPENDENCIES**
```bash
pip install playwright
pip install requests
pip install asyncio
pip install aiohttp
```

## 🌐 **BROWSER SETUP (for Playwright)**
```bash
playwright install
```

## ✅ **VERIFICATION SCRIPT**
Create and run this script to verify all dependencies:

```python
import subprocess
import sys

def check_dependency(command, name):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✅ {name}: Installed")
            return True
        else:
            print(f"❌ {name}: Not installed")
            return False
    except Exception:
        print(f"❌ {name}: Not installed")
        return False

dependencies = [
    (["node", "--version"], "Node.js"),
    (["npm", "--version"], "npm"), 
    (["lighthouse", "--version"], "Google Lighthouse"),
    (["pa11y", "--version"], "Pa11y"),
    (["python", "--version"], "Python")
]

print("🔍 Checking Accessibility Tools Dependencies...")
print("=" * 50)

all_good = True
for cmd, name in dependencies:
    if not check_dependency(cmd, name):
        all_good = False

if all_good:
    print("\n🎉 All dependencies are installed!")
else:
    print("\n⚠️  Some dependencies are missing. Please install them.")
```

## 🚀 **QUICK SETUP (Windows)**
```bash
# Install Node.js and tools
choco install nodejs
npm install -g lighthouse pa11y

# Install Python packages
pip install playwright requests asyncio

# Setup browsers
playwright install
```

## 🚀 **QUICK SETUP (macOS)**
```bash
# Install Node.js and tools
brew install node
npm install -g lighthouse pa11y

# Install Python packages
pip install playwright requests asyncio

# Setup browsers
playwright install
```

## 🚀 **QUICK SETUP (Linux)**
```bash
# Install Node.js and tools
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
npm install -g lighthouse pa11y

# Install Python packages
pip install playwright requests asyncio

# Setup browsers
playwright install
```

## 🧪 **TEST INSTALLATION**
Run the sophisticated accessibility test to verify everything works:
```bash
python test_sophisticated_accessibility_tools.py
``` 