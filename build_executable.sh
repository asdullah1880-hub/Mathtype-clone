#!/bin/bash

# Build Script for MathType Clone Single Executable
# This script creates a standalone executable for Linux

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip is not installed."
    echo "Please install pip and try again."
    exit 1
fi

# Check if PyInstaller is installed
if ! python3 -m pyinstaller --version &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Check if dependencies are installed
if ! python3 -c "import PyQt5" 2> /dev/null; then
    echo "Installing dependencies..."
    pip3 install PyQt5 matplotlib latex2mathml
fi

echo "=========================================="
echo "Building MathType Clone Executable"
echo "=========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Clean up previous builds
echo "Cleaning up previous builds..."
rm -rf build/ dist/ MathTypeClone.spec

# Build the executable
echo "Building executable (this may take a few minutes)..."
echo ""

python3 -m pyinstaller \
    --onefile \
    --windowed \
    --name MathTypeClone \
    --clean \
    --icon=NONE \
    mathtype_clone.py

# Check if build was successful
if [ -f "dist/MathTypeClone" ]; then
    echo ""
    echo "=========================================="
    echo "Build Successful!"
    echo "=========================================="
    echo ""
    echo "Executable created: dist/MathTypeClone"
    echo ""
    echo "To run the executable:"
    echo "  ./dist/MathTypeClone"
    echo ""
    echo "To install system-wide:"
    echo "  sudo cp dist/MathTypeClone /usr/local/bin/"
    echo "  Then run: MathTypeClone"
    echo ""
    ls -lh dist/MathTypeClone
else
    echo ""
    echo "=========================================="
    echo "Build Failed!"
    echo "=========================================="
    echo ""
    echo "Please check the error messages above."
    echo "Make sure all dependencies are installed."
    exit 1
fi
