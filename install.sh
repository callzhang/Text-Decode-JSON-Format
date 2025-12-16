#!/bin/bash
# Installation script for Text Decode + JSON Format Sublime Text package

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Files to install
FILES=("auto_tools.py" "auto_tools_core.py" "auto_tools.sublime-commands")

# Function to find Sublime Text Packages/User directory
find_sublime_user_dir() {
    local home_dir="$HOME"
    local user_packages=""
    
    # macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Sublime Text 4
        if [ -d "$home_dir/Library/Application Support/Sublime Text/Packages/User" ]; then
            user_packages="$home_dir/Library/Application Support/Sublime Text/Packages/User"
        # Sublime Text 3
        elif [ -d "$home_dir/Library/Application Support/Sublime Text 3/Packages/User" ]; then
            user_packages="$home_dir/Library/Application Support/Sublime Text 3/Packages/User"
        else
            # Try to find any Sublime Text installation
            for item in "$home_dir/Library/Application Support"/*; do
                if [[ "$item" == *"Sublime Text"* ]] && [ -d "$item/Packages/User" ]; then
                    user_packages="$item/Packages/User"
                    break
                fi
            done
        fi
    # Linux
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Sublime Text 4
        if [ -d "$home_dir/.config/sublime-text/Packages/User" ]; then
            user_packages="$home_dir/.config/sublime-text/Packages/User"
        # Sublime Text 3
        elif [ -d "$home_dir/.config/sublime-text-3/Packages/User" ]; then
            user_packages="$home_dir/.config/sublime-text-3/Packages/User"
        fi
    fi
    
    echo "$user_packages"
}

# Main installation function
install_package() {
    local custom_path="$1"
    local user_packages=""
    
    echo "============================================================"
    echo "Text Decode + JSON Format - Installation Script"
    echo "============================================================"
    echo ""
    
    # Find or use custom path
    if [ -n "$custom_path" ]; then
        echo -e "${BLUE}🔍${NC} Using custom path: $custom_path"
        user_packages="$(cd "$custom_path" 2>/dev/null && pwd)" || {
            echo -e "${RED}❌${NC} Error: Custom path does not exist: $custom_path"
            return 1
        }
    else
        echo -e "${BLUE}🔍${NC} Looking for Sublime Text Packages/User directory..."
        user_packages="$(find_sublime_user_dir)"
        
        if [ -z "$user_packages" ] || [ ! -d "$user_packages" ]; then
            echo -e "${RED}❌${NC} Error: Could not find Sublime Text Packages/User directory."
            echo ""
            echo "Please ensure Sublime Text is installed and has been run at least once."
            echo ""
            echo "Expected locations:"
            echo "  macOS: ~/Library/Application Support/Sublime Text/Packages/User"
            echo "  Linux: ~/.config/sublime-text/Packages/User"
            echo ""
            echo "Alternatively, specify a custom path:"
            echo "  ./install.sh --path /path/to/Packages/User"
            return 1
        fi
    fi
    
    echo -e "${GREEN}✅${NC} Using: $user_packages"
    
    # Verify source files exist
    echo ""
    echo -e "${BLUE}📦${NC} Checking source files..."
    local missing_files=()
    for file in "${FILES[@]}"; do
        if [ -f "$SCRIPT_DIR/$file" ]; then
            echo -e "  ${GREEN}✅${NC} Found: $file"
        else
            echo -e "  ${RED}❌${NC} Missing: $file"
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        echo ""
        echo -e "${RED}❌${NC} Error: Missing required files: ${missing_files[*]}"
        return 1
    fi
    
    # Create User directory if it doesn't exist
    mkdir -p "$user_packages"
    
    # Copy files
    echo ""
    echo -e "${BLUE}📥${NC} Installing files to $user_packages..."
    local installed_count=0
    for file in "${FILES[@]}"; do
        if cp "$SCRIPT_DIR/$file" "$user_packages/$file" 2>/dev/null; then
            echo -e "  ${GREEN}✅${NC} Installed: $file"
            ((installed_count++))
        else
            echo -e "  ${RED}❌${NC} Failed to install: $file"
            return 1
        fi
    done
    
    echo ""
    echo -e "${GREEN}✅${NC} Successfully installed $installed_count file(s)!"
    echo ""
    echo -e "${BLUE}📝${NC} Next steps:"
    echo "  1. Restart Sublime Text (if it's running)"
    echo "  2. Open Command Palette (Cmd+Shift+P / Ctrl+Shift+P)"
    echo "  3. Look for:"
    echo "     - 'Auto Decode (URL+HTML+Unicode+Base64+Hex)'"
    echo "     - 'Auto JSON Format (Decode + Fix + Pretty)'"
    
    return 0
}

# Parse command-line arguments
CUSTOM_PATH=""
if [ $# -gt 0 ]; then
    case "$1" in
        --path|-p)
            if [ -z "$2" ]; then
                echo -e "${RED}❌${NC} Error: --path requires a path argument"
                exit 1
            fi
            CUSTOM_PATH="$2"
            ;;
        --help|-h)
            echo "Usage: ./install.sh [--path PATH]"
            echo ""
            echo "Options:"
            echo "  --path, -p PATH    Custom path to Sublime Text Packages/User directory"
            echo "  --help, -h         Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./install.sh"
            echo "  ./install.sh --path ~/Library/Application\\ Support/Sublime\\ Text/Packages/User"
            exit 0
            ;;
        *)
            echo -e "${RED}❌${NC} Unknown argument: $1"
            echo "Use --help for usage information."
            exit 1
            ;;
    esac
fi

# Run installation
if install_package "$CUSTOM_PATH"; then
    exit 0
else
    exit 1
fi
