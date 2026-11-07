# MathType Clone for Linux

A lightweight, single-executable LaTeX equation editor for Linux that serves as an alternative to MathType. Create, edit, and export mathematical equations using LaTeX syntax with real-time preview.

![MathType Clone Screenshot](https://img.shields.io/badge/Platform-Linux-green.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-yellow.svg)

## Features

✅ **Real-time LaTeX Preview** - See your equations render as you type
✅ **Single Executable** - Package the application as a standalone binary
✅ **Equation Templates** - Quick access to common mathematical symbols and structures
✅ **Save & Load** - Save equations as `.tex` files and load them later
✅ **Export Options** - Save equations as PNG images or copy LaTeX to clipboard
✅ **Adjustable Font Size** - Zoom in and out for better visibility
✅ **User-friendly GUI** - Intuitive interface with toolbar and template buttons

## Quick Start

### Method 1: Run Directly (Requires Python)

```bash
# Clone the repository
git clone https://github.com/asdullah1880-hub/Mathtype-clone.git
cd Mathtype-clone

# Install dependencies
pip install PyQt5 matplotlib

# Run the application
python3 mathtype_clone.py
```

### Method 2: Create a Standalone Executable

To create a single executable file that doesn't require Python to be installed:

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller --onefile --windowed --name MathTypeClone mathtype_clone.py

# The executable will be in the 'dist' folder
dist/MathTypeClone
```

**Note:** The executable will be large (20-50MB) because it bundles Python and all dependencies.

## Usage

### Basic Operations

1. **Enter LaTeX** in the text editor at the top
2. **Live preview** appears automatically below
3. Use **template buttons** to insert common symbols quickly
4. **Save** your equations as `.tex` files
5. **Export** as PNG images or copy LaTeX code

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New equation |
| `Ctrl+O` | Open equation |
| `Ctrl+S` | Save equation |
| `Ctrl+Shift+S` | Save as PNG |
| `Ctrl+E` | Export LaTeX to clipboard |
| `Ctrl++` | Zoom in (increase font size) |
| `Ctrl+-` | Zoom out (decrease font size) |
| `F1` | Show help |

### Common LaTeX Examples

| Description | LaTeX Code | Result |
|-------------|------------|--------|
| Fraction | `\frac{a}{b}` | a/b |
| Square root | `\sqrt{x}` | √x |
| Summation | `\sum_{i=1}^{n} i^2` | Σ i² from i=1 to n |
| Integral | `\int_{0}^{1} x^2 dx` | ∫ x² dx from 0 to 1 |
| Greek alpha | `\alpha` | α |
| Superscript | `x^2` | x² |
| Subscript | `x_1` | x₁ |
| Matrix | `\begin{matrix} a & b \\ c & d \end{matrix}` | 2x2 matrix |
| Bold vector | `\mathbf{v}` | **v** |

### Template Buttons

The application includes template buttons for:
- **Fractions**: `\frac{}{}`
- **Roots**: `\sqrt{}`
- **Summation**: `\sum_{}^{}`
- **Integral**: `\int_{}^{}`
- **Greek letters**: α, β, γ, δ, π, σ, ω
- **Formatting**: Bold, Italic, Vector, Hat, Bar, Dot
- **Scripts**: Superscript, Subscript
- **Matrices**: Various matrix environments
- **Brackets**: Left/Right parentheses
- **Symbols**: ∞, ∂, ≈, ≠, ≤, ≥, →, ←, ↑, ↓

## Installation

### Prerequisites

- **Linux** (Ubuntu, Fedora, Arch, etc.)
- **Python 3.8 or higher**
- **pip** (Python package manager)

### Install Dependencies

```bash
# For Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# For Fedora
sudo dnf install python3 python3-pip

# For Arch Linux
sudo pacman -S python python-pip
```

### Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 mathtype_clone.py
```

## Creating a Single Executable

To distribute the application as a single file:

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build the Executable

```bash
# For a windowed application (no terminal)
pyinstaller --onefile --windowed --name MathTypeClone mathtype_clone.py

# For a console application (shows terminal)
pyinstaller --onefile --name MathTypeClone mathtype_clone.py
```

### Step 3: Find the Executable

The executable will be created in the `dist/` directory:

```bash
ls -lh dist/
```

### Step 4: Run the Executable

```bash
./dist/MathTypeClone
```

### Step 5: Distribute (Optional)

You can copy the `MathTypeClone` file to any Linux machine and run it directly:

```bash
# Copy to /usr/local/bin for system-wide access
sudo cp dist/MathTypeClone /usr/local/bin/

# Or run from any directory
./MathTypeClone
```

**Note:** The first run may take a few seconds as it extracts the bundled Python runtime.

## File Formats

### Input/Output

- **`.tex` files** - Plain text files containing LaTeX code
- **`.txt` files** - Can also be used to save LaTeX code
- **PNG images** - Exported equations as high-quality images

### Example .tex File

```latex
\frac{d}{dx} \left( \int_{0}^{x} f(t) dt \right) = f(x)
```

## Troubleshooting

### Common Issues

1. **Matplotlib rendering issues**
   - Make sure you have the required fonts installed
   - Try: `sudo apt install texlive-latex-extra` (on Ubuntu)

2. **PyQt5 not found**
   - Install with: `pip install PyQt5`
   - If you get Qt platform errors, try: `export QT_DEBUG_PLUGINS=1`

3. **Large executable size**
   - This is normal for PyInstaller as it bundles Python and all dependencies
   - The size is typically 20-50MB

4. **Missing dependencies when running executable**
   - The executable is self-contained; no additional dependencies needed
   - If you get errors, try rebuilding with `--onefile` flag

### Debug Mode

Run with debug output:

```bash
python3 mathtype_clone.py --debug
```

## Contributing

Contributions are welcome! Please feel free to:

1. **Report bugs** - Open an issue on GitHub
2. **Suggest features** - Open an issue with your idea
3. **Submit code** - Fork the repository and create a pull request

### Development Setup

```bash
git clone https://github.com/asdullah1880-hub/Mathtype-clone.git
cd Mathtype-clone
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Requirements

The application requires the following Python packages:

```
PyQt5>=5.15.0
matplotlib>=3.0.0
```

See `requirements.txt` for the complete list.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the original **MathType** by Design Science
- Built with **PyQt5** for the GUI
- Uses **matplotlib** for LaTeX rendering
- Thanks to the open-source community for all the amazing tools

## Examples

### Simple Equation

```latex
E = mc^2
```

### Quadratic Formula

```latex
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
```

### Integral

```latex
\int_{a}^{b} x^2 dx = \left[ \frac{x^3}{3} \right]_{a}^{b}
```

### Matrix

```latex
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{bmatrix}
```

### Summation

```latex
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}
```

## Roadmap

Future enhancements planned:

- [ ] Equation library/collection management
- [ ] Drag-and-drop equation building
- [ ] Support for more LaTeX packages
- [ ] Export to SVG format
- [ ] Dark mode theme
- [ ] Customizable toolbar
- [ ] Equation history
- [ ] Multiple equation tabs

---

**Enjoy using MathType Clone!**

For questions, issues, or suggestions, please open an issue on GitHub.

© 2024 asdullah1880-hub
