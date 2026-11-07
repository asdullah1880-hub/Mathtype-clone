#!/usr/bin/env python3
"""
MathType Clone - A LaTeX Equation Editor for Linux
A simple but powerful equation editor that allows you to create and edit
mathematical equations using LaTeX syntax with real-time preview.
"""

import sys
import os

# Try to import required modules
try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTextEdit, QPushButton, QLabel, QFrame, QFileDialog,
        QToolBar, QAction, QInputDialog, QMessageBox, QScrollArea
    )
    from PyQt5.QtGui import QPixmap, QIcon, QFont, QTextCursor, QPalette, QColor
    from PyQt5.QtCore import Qt, QSize, QTimer
    QT_AVAILABLE = True
except ImportError as e:
    QT_AVAILABLE = False
    QT_ERROR = str(e)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    MATPLOTLIB_AVAILABLE = True
except ImportError as e:
    MATPLOTLIB_AVAILABLE = False
    MATPLOTLIB_ERROR = str(e)

import io
import base64

# Set matplotlib to use a non-interactive backend
rcParams['text.usetex'] = False
rcParams['text.latex.preamble'] = r'\usepackage{amsmath,amssymb}'

# Common LaTeX templates for the toolbar
TEMPLATES = {
    'Fraction': r'\frac{}{}',
    'Square Root': r'\sqrt{}',
    'Summation': r'\sum_{}^{}',
    'Integral': r'\int_{}^{}',
    'Greek Alpha': r'\alpha',
    'Greek Beta': r'\beta',
    'Greek Gamma': r'\gamma',
    'Greek Delta': r'\delta',
    'Greek Pi': r'\pi',
    'Greek Sigma': r'\sigma',
    'Greek Omega': r'\omega',
    'Superscript': r'^{}',
    'Subscript': r'_{}',
    'Bold': r'\mathbf{}',
    'Italic': r'\textit{}',
    'Vector': r'\vec{}',
    'Hat': r'\hat{}',
    'Bar': r'\bar{}',
    'Dot': r'\dot{}',
    'Matrix': r'\begin{matrix} & \\ & \end{matrix}',
    'BMatrix': r'\begin{bmatrix} & \\ & \end{bmatrix}',
    'PMatrix': r'\begin{pmatrix} & \\ & \end{pmatrix}',
    'Left/Right': r'\left( \right)',
    'Infinity': r'\infty',
    'Partial': r'\partial',
    'Approx': r'\approx',
    'Equals': r'=',
    'Plus/Minus': r'\pm',
    'Times': r'\times',
    'Division': r'\div',
    'Not Equal': r'\neq',
    'Less Than': r'<',
    'Greater Than': r'>',
    'Less Equal': r'\leq',
    'Greater Equal': r'\geq',
    'Arrow Right': r'\rightarrow',
    'Arrow Left': r'\leftarrow',
    'Arrow Both': r'\leftrightarrow',
    'Arrow Up': r'\uparrow',
    'Arrow Down': r'\downarrow',
}


class EquationRenderer:
    """Handles rendering of LaTeX equations to images."""
    
    def __init__(self, dpi=150, fontsize=14):
        self.dpi = dpi
        self.fontsize = fontsize
        self.fig = None
        self.ax = None
        
    def render_latex(self, latex_text, output_size=None):
        """Render LaTeX equation and return as QPixmap."""
        if not latex_text or latex_text.strip() == '':
            return QPixmap(100, 50)
        
        try:
            # Create figure
            self.fig = plt.figure(figsize=(0.5, 0.5), dpi=self.dpi)
            self.fig.patch.set_alpha(0.0)
            self.ax = self.fig.add_axes([0, 0, 1, 1], frame_on=False)
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.axis('off')
            
            # Render the text
            self.ax.text(0.5, 0.5, f'${latex_text}$', 
                        fontsize=self.fontsize, 
                        ha='center', va='center')
            
            # Save to buffer
            buf = io.BytesIO()
            self.fig.savefig(buf, format='png', dpi=self.dpi, 
                           bbox_inches='tight', pad_inches=0.1)
            buf.seek(0)
            
            # Create QPixmap from buffer
            data = buf.read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            
            plt.close(self.fig)
            
            return pixmap
            
        except Exception as e:
            print(f"Error rendering LaTeX: {e}")
            # Return error pixmap
            pixmap = QPixmap(300, 50)
            pixmap.fill(Qt.red)
            return pixmap


class MathTypeClone(QMainWindow):
    """Main application window for MathType Clone."""
    
    def __init__(self):
        super().__init__()
        self.renderer = EquationRenderer(dpi=150, fontsize=16)
        self.current_file = None
        self.init_ui()
        self.setWindowTitle("MathType Clone")
        self.setWindowIcon(self.create_icon())
        
    def create_icon(self):
        """Create a simple icon for the application."""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        return QIcon(pixmap)
    
    def init_ui(self):
        """Initialize the user interface."""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create editor and preview area
        self.create_editor_area(main_layout)
        
        # Create template buttons
        self.create_template_buttons(main_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Set minimum size
        self.resize(900, 700)
        self.setMinimumSize(600, 500)
        
        # Timer for delayed rendering
        self.render_timer = QTimer()
        self.render_timer.setInterval(500)  # 500ms delay
        self.render_timer.setSingleShot(True)
        self.render_timer.timeout.connect(self.update_preview)
    
    def create_toolbar(self):
        """Create the main toolbar with file operations."""
        toolbar = self.addToolBar("File Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        
        # New action
        new_action = QAction(QIcon.fromTheme("document-new"), "New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.setStatusTip("Create a new equation")
        new_action.triggered.connect(self.new_equation)
        toolbar.addAction(new_action)
        
        # Open action
        open_action = QAction(QIcon.fromTheme("document-open"), "Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open an equation file")
        open_action.triggered.connect(self.open_equation)
        toolbar.addAction(open_action)
        
        # Save action
        save_action = QAction(QIcon.fromTheme("document-save"), "Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save the current equation")
        save_action.triggered.connect(self.save_equation)
        toolbar.addAction(save_action)
        
        # Save as image action
        save_img_action = QAction(QIcon.fromTheme("image"), "Save as PNG", self)
        save_img_action.setShortcut("Ctrl+Shift+S")
        save_img_action.setStatusTip("Save equation as PNG image")
        save_img_action.triggered.connect(self.save_as_image)
        toolbar.addAction(save_img_action)
        
        # Export as LaTeX action
        export_action = QAction("Export LaTeX", self)
        export_action.setShortcut("Ctrl+E")
        export_action.setStatusTip("Export equation as LaTeX text")
        export_action.triggered.connect(self.export_latex)
        toolbar.addAction(export_action)
        
        # Add separator
        toolbar.addSeparator()
        
        # Zoom in action
        zoom_in_action = QAction(QIcon.fromTheme("zoom-in"), "Zoom In", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.setStatusTip("Increase font size")
        zoom_in_action.triggered.connect(self.zoom_in)
        toolbar.addAction(zoom_in_action)
        
        # Zoom out action
        zoom_out_action = QAction(QIcon.fromTheme("zoom-out"), "Zoom Out", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.setStatusTip("Decrease font size")
        zoom_out_action.triggered.connect(self.zoom_out)
        toolbar.addAction(zoom_out_action)
        
        # Help action
        help_action = QAction("Help", self)
        help_action.setShortcut("F1")
        help_action.setStatusTip("Show help")
        help_action.triggered.connect(self.show_help)
        toolbar.addAction(help_action)
    
    def create_editor_area(self, main_layout):
        """Create the editor and preview area."""
        # Editor frame
        editor_frame = QFrame()
        editor_frame.setFrameShape(QFrame.StyledPanel)
        editor_layout = QVBoxLayout(editor_frame)
        editor_layout.setContentsMargins(5, 5, 5, 5)
        
        # LaTeX input label
        latex_label = QLabel("LaTeX Input:")
        latex_label.setFont(QFont("Arial", 10, QFont.Bold))
        editor_layout.addWidget(latex_label)
        
        # LaTeX input area
        self.latex_input = QTextEdit()
        self.latex_input.setFont(QFont("Courier New", 12))
        self.latex_input.setPlaceholderText("Enter LaTeX equation here... (e.g., \\frac{x^2}{y} = \\sqrt{z})")
        self.latex_input.textChanged.connect(self.on_text_changed)
        editor_layout.addWidget(self.latex_input)
        
        # Preview frame
        preview_frame = QFrame()
        preview_frame.setFrameShape(QFrame.StyledPanel)
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setContentsMargins(5, 5, 5, 5)
        
        # Preview label
        preview_label = QLabel("Live Preview:")
        preview_label.setFont(QFont("Arial", 10, QFont.Bold))
        preview_layout.addWidget(preview_label)
        
        # Preview area with scroll
        self.preview_scroll = QScrollArea()
        self.preview_scroll.setWidgetResizable(True)
        self.preview_scroll.setAlignment(Qt.AlignCenter)
        
        self.preview_container = QWidget()
        self.preview_container_layout = QVBoxLayout(self.preview_container)
        self.preview_container_layout.setAlignment(Qt.AlignCenter)
        
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(200, 100)
        self.preview_label.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        self.preview_container_layout.addWidget(self.preview_label)
        
        self.preview_scroll.setWidget(self.preview_container)
        preview_layout.addWidget(self.preview_scroll)
        
        # Add to main layout
        main_layout.addWidget(editor_frame, stretch=1)
        main_layout.addWidget(preview_frame, stretch=2)
    
    def create_template_buttons(self, main_layout):
        """Create buttons for common LaTeX templates."""
        # Template toolbar frame
        template_frame = QFrame()
        template_frame.setFrameShape(QFrame.StyledPanel)
        template_layout = QVBoxLayout(template_frame)
        template_layout.setContentsMargins(5, 5, 5, 5)
        
        # Template label
        template_label = QLabel("Equation Templates:")
        template_label.setFont(QFont("Arial", 10, QFont.Bold))
        template_layout.addWidget(template_label)
        
        # Create rows of buttons
        row1_layout = QHBoxLayout()
        row2_layout = QHBoxLayout()
        row3_layout = QHBoxLayout()
        
        # Row 1: Fractions, Roots, Summation, Integral
        for name in ['Fraction', 'Square Root', 'Summation', 'Integral']:
            btn = QPushButton(name)
            btn.setToolTip(f"Insert {name}")
            btn.clicked.connect(lambda _, n=name: self.insert_template(n))
            row1_layout.addWidget(btn)
        
        # Row 2: Greek letters
        for name in ['Greek Alpha', 'Greek Beta', 'Greek Gamma', 'Greek Delta', 'Greek Pi', 'Greek Sigma']:
            btn = QPushButton(name.replace('Greek ', ''))
            btn.setToolTip(f"Insert {name}")
            btn.clicked.connect(lambda _, n=name: self.insert_template(n))
            row2_layout.addWidget(btn)
        
        # Row 3: Operators and symbols
        for name in ['Superscript', 'Subscript', 'Bold', 'Italic', 'Vector', 'Hat']:
            btn = QPushButton(name)
            btn.setToolTip(f"Insert {name}")
            btn.clicked.connect(lambda _, n=name: self.insert_template(n))
            row3_layout.addWidget(btn)
        
        template_layout.addLayout(row1_layout)
        template_layout.addLayout(row2_layout)
        template_layout.addLayout(row3_layout)
        
        main_layout.addWidget(template_frame)
    
    def on_text_changed(self):
        """Handle text changes with debouncing."""
        self.render_timer.start()
    
    def update_preview(self):
        """Update the preview with the current LaTeX."""
        latex_text = self.latex_input.toPlainText()
        
        if not latex_text.strip():
            self.preview_label.setText("Enter LaTeX to see preview")
            self.preview_label.setStyleSheet("background-color: white; border: 1px solid #ccc; color: #999;")
            return
        
        try:
            pixmap = self.renderer.render_latex(latex_text)
            if not pixmap.isNull():
                # Scale pixmap to fit
                max_width = 800
                max_height = 400
                scaled_pixmap = pixmap.scaled(max_width, max_height, 
                                             Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.preview_label.setPixmap(scaled_pixmap)
                self.preview_label.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        except Exception as e:
            self.preview_label.setText(f"Error: {str(e)}")
            self.preview_label.setStyleSheet("background-color: #ffebee; border: 1px solid #ef9a9a; color: #c62828;")
    
    def insert_template(self, template_name):
        """Insert a LaTeX template at the current cursor position."""
        template = TEMPLATES.get(template_name, '')
        if template:
            cursor = self.latex_input.textCursor()
            cursor.insertText(template)
            # Move cursor to the middle of the template if it has placeholders
            if '{}' in template:
                # Position cursor between the braces
                new_pos = cursor.position() - 1
                cursor.setPosition(new_pos)
                self.latex_input.setTextCursor(cursor)
            self.latex_input.setFocus()
    
    def new_equation(self):
        """Create a new equation."""
        self.latex_input.clear()
        self.preview_label.clear()
        self.current_file = None
        self.statusBar().showMessage("New equation created")
    
    def open_equation(self):
        """Open an equation file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Equation", "", 
            "LaTeX Files (*.tex);;Text Files (*.txt);;All Files (*)", 
            options=options
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.latex_input.setPlainText(content)
                self.current_file = file_path
                self.statusBar().showMessage(f"Opened: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")
    
    def save_equation(self):
        """Save the current equation."""
        latex_text = self.latex_input.toPlainText()
        
        if not self.current_file:
            self.save_equation_as()
            return
        
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(latex_text)
            self.statusBar().showMessage(f"Saved: {self.current_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
    
    def save_equation_as(self):
        """Save the equation as a new file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Equation", "", 
            "LaTeX Files (*.tex);;Text Files (*.txt);;All Files (*)", 
            options=options
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.latex_input.toPlainText())
                self.current_file = file_path
                self.statusBar().showMessage(f"Saved: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
    
    def save_as_image(self):
        """Save the current equation as a PNG image."""
        latex_text = self.latex_input.toPlainText()
        
        if not latex_text.strip():
            QMessageBox.warning(self, "Warning", "No equation to save as image")
            return
        
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save as PNG", "", 
            "PNG Images (*.png);;All Files (*)", 
            options=options
        )
        
        if file_path:
            try:
                # Ensure .png extension
                if not file_path.lower().endswith('.png'):
                    file_path += '.png'
                
                # Render the equation
                pixmap = self.renderer.render_latex(latex_text, output_size=(800, 400))
                if not pixmap.isNull():
                    pixmap.save(file_path, 'PNG')
                    self.statusBar().showMessage(f"Image saved: {file_path}")
                else:
                    QMessageBox.warning(self, "Error", "Could not render equation")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save image: {str(e)}")
    
    def export_latex(self):
        """Export the LaTeX code."""
        latex_text = self.latex_input.toPlainText()
        
        if not latex_text.strip():
            QMessageBox.warning(self, "Warning", "No equation to export")
            return
        
        # Copy to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(latex_text)
        self.statusBar().showMessage("LaTeX code copied to clipboard")
        
        # Also offer to save to file
        reply = QMessageBox.question(
            self, "Export LaTeX", 
            "LaTeX code copied to clipboard.\nDo you want to save it to a file?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.save_equation_as()
    
    def zoom_in(self):
        """Increase the font size."""
        self.renderer.fontsize += 2
        self.update_preview()
        self.statusBar().showMessage(f"Font size: {self.renderer.fontsize}")
    
    def zoom_out(self):
        """Decrease the font size."""
        if self.renderer.fontsize > 6:
            self.renderer.fontsize -= 2
            self.update_preview()
            self.statusBar().showMessage(f"Font size: {self.renderer.fontsize}")
    
    def show_help(self):
        """Show help information."""
        help_text = """
        <h1>MathType Clone - Help</h1>
        <p>A simple LaTeX equation editor for Linux.</p>
        
        <h2>Quick Start</h2>
        <ul>
        <li><b>Enter LaTeX</b> in the text area above</li>
        <li><b>Live preview</b> appears below</li>
        <li>Use <b>template buttons</b> to insert common symbols</li>
        </ul>
        
        <h2>Keyboard Shortcuts</h2>
        <ul>
        <li>Ctrl+N: New equation</li>
        <li>Ctrl+O: Open equation</li>
        <li>Ctrl+S: Save equation</li>
        <li>Ctrl+Shift+S: Save as PNG</li>
        <li>Ctrl+E: Export LaTeX</li>
        <li>Ctrl++: Zoom in</li>
        <li>Ctrl+-: Zoom out</li>
        <li>F1: Show help</li>
        </ul>
        
        <h2>Common LaTeX Examples</h2>
        <ul>
        <li>Fraction: <code>\\frac{a}{b}</code></li>
        <li>Square root: <code>\\sqrt{x}</code></li>
        <li>Summation: <code>\\sum_{i=1}^{n} i^2</code></li>
        <li>Integral: <code>\\int_{0}^{1} x^2 dx</code></li>
        <li>Greek letters: <code>\\alpha, \\beta, \\gamma</code></li>
        <li>Superscript: <code>x^2</code></li>
        <li>Subscript: <code>x_1</code></li>
        </ul>
        
        <h2>Features</h2>
        <ul>
        <li>Real-time LaTeX preview</li>
        <li>Save equations as .tex files</li>
        <li>Export equations as PNG images</li>
        <li>Copy LaTeX to clipboard</li>
        <li>Adjustable font size</li>
        <li>Template buttons for common symbols</li>
        </ul>
        """
        
        help_dialog = QMessageBox(self)
        help_dialog.setWindowTitle("MathType Clone - Help")
        help_dialog.setTextFormat(Qt.RichText)
        help_dialog.setText(help_text)
        help_dialog.setStandardButtons(QMessageBox.Ok)
        help_dialog.setMinimumSize(600, 500)
        help_dialog.exec_()
    
    def closeEvent(self, event):
        """Handle close event."""
        # Check if there's unsaved content
        if self.latex_input.toPlainText().strip():
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Do you want to save before exiting?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, 
                QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Yes:
                self.save_equation()
                event.accept()
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return
        
        event.accept()


def main():
    """Main entry point for the application."""
    # Check for required dependencies
    if not QT_AVAILABLE:
        print(f"Error: PyQt5 is not available. {QT_ERROR}")
        print("Please install PyQt5: pip install PyQt5")
        sys.exit(1)
    
    if not MATPLOTLIB_AVAILABLE:
        print(f"Error: matplotlib is not available. {MATPLOTLIB_ERROR}")
        print("Please install matplotlib: pip install matplotlib")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set palette for better appearance
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, Qt.black)
    app.setPalette(palette)
    
    window = MathTypeClone()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
