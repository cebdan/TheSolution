#!/usr/bin/env python3
"""
Demo script for 3D Visualization System
Tests gradients, line styles, and material rendering
"""

import sys
import os
from typing import Dict, Any

# Add project paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "Root Solution", "3D-Solution"))

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTextEdit
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont
    
    # Import visualization system
    try:
        import importlib.util
        
        # Load visualization_3d module
        viz_3d_path = os.path.join(current_dir, "Root Solution", "3D-Solution", "visualization_3d.py")
        spec = importlib.util.spec_from_file_location("visualization_3d", viz_3d_path)
        viz_3d_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(viz_3d_module)
        
        # Load visualization_dialog module
        viz_dialog_path = os.path.join(current_dir, "Root Solution", "3D-Solution", "visualization_dialog.py")
        spec = importlib.util.spec_from_file_location("visualization_dialog", viz_dialog_path)
        viz_dialog_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(viz_dialog_module)
        
        # Import classes
        Visualization3D = viz_3d_module.Visualization3D
        LineStyle = viz_3d_module.LineStyle
        GradientType = viz_3d_module.GradientType
        MaterialType = viz_3d_module.MaterialType
        ColorScheme = viz_3d_module.ColorScheme
        VisualizationPresets = viz_3d_module.VisualizationPresets
        VisualizationDialog = viz_dialog_module.VisualizationDialog
        
        VISUALIZATION_AVAILABLE = True
        print("✅ 3D Visualization system imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import visualization system: {e}")
        VISUALIZATION_AVAILABLE = False
    
except ImportError as e:
    VISUALIZATION_AVAILABLE = False
    print(f"❌ Failed to import 3D visualization system: {e}")

class VisualizationDemo(QMainWindow):
    """Demo window for 3D visualization system"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Visualization System Demo")
        self.setGeometry(200, 200, 800, 600)
        
        # Initialize visualization system
        self.visualization = None
        if VISUALIZATION_AVAILABLE:
            try:
                self.visualization = Visualization3D()
                print("✅ Visualization3D initialized")
            except Exception as e:
                print(f"❌ Failed to initialize Visualization3D: {e}")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("3D Visualization System Demo")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Status
        status_text = "✅ Available" if VISUALIZATION_AVAILABLE else "❌ Not Available"
        status_label = QLabel(f"Visualization System: {status_text}")
        status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(status_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Test buttons
        self.test_gradients_btn = QPushButton("Test Gradients")
        self.test_gradients_btn.clicked.connect(self.test_gradients)
        button_layout.addWidget(self.test_gradients_btn)
        
        self.test_line_styles_btn = QPushButton("Test Line Styles")
        self.test_line_styles_btn.clicked.connect(self.test_line_styles)
        button_layout.addWidget(self.test_line_styles_btn)
        
        self.test_materials_btn = QPushButton("Test Materials")
        self.test_materials_btn.clicked.connect(self.test_materials)
        button_layout.addWidget(self.test_materials_btn)
        
        self.test_presets_btn = QPushButton("Test Presets")
        self.test_presets_btn.clicked.connect(self.test_presets)
        button_layout.addWidget(self.test_presets_btn)
        
        layout.addLayout(button_layout)
        
        # Settings dialog button
        self.settings_btn = QPushButton("Open Visualization Settings")
        self.settings_btn.clicked.connect(self.open_settings_dialog)
        layout.addWidget(self.settings_btn)
        
        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(200)
        layout.addWidget(self.log_area)
        
        # Disable buttons if visualization not available
        if not VISUALIZATION_AVAILABLE:
            self.test_gradients_btn.setEnabled(False)
            self.test_line_styles_btn.setEnabled(False)
            self.test_materials_btn.setEnabled(False)
            self.test_presets_btn.setEnabled(False)
            self.settings_btn.setEnabled(False)
    
    def log_message(self, message: str):
        """Add message to log area"""
        self.log_area.append(f"[{self.get_timestamp()}] {message}")
    
    def get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def test_gradients(self):
        """Test gradient functionality"""
        if not self.visualization:
            self.log_message("❌ Visualization system not available")
            return
        
        self.log_message("🧪 Testing Gradients...")
        
        try:
            base_color = (0.8, 0.8, 0.9)
            
            # Test different gradient types
            gradient_types = [
                GradientType.NONE,
                GradientType.LINEAR,
                GradientType.RADIAL,
                GradientType.CONICAL,
                GradientType.SPHERICAL
            ]
            
            for gradient_type in gradient_types:
                color = self.visualization.create_gradient_color(
                    base_color, gradient_type, (0.5, 0.3, 0.2)
                )
                if color:
                    self.log_message(f"✅ {gradient_type.value}: Color created successfully")
                else:
                    self.log_message(f"❌ {gradient_type.value}: Failed to create color")
            
            self.log_message("🎉 Gradient testing completed")
            
        except Exception as e:
            self.log_message(f"❌ Gradient test failed: {e}")
    
    def test_line_styles(self):
        """Test line styles functionality"""
        if not self.visualization:
            self.log_message("❌ Visualization system not available")
            return
        
        self.log_message("🧪 Testing Line Styles...")
        
        try:
            color = (0.8, 0.8, 0.8)
            
            # Test different line styles
            line_styles = [
                LineStyle.SOLID,
                LineStyle.DASHED,
                LineStyle.DOTTED,
                LineStyle.DASH_DOT,
                LineStyle.LONG_DASH,
                LineStyle.DOUBLE_DASH
            ]
            
            for line_style in line_styles:
                aspect = self.visualization.create_line_aspect(color, line_style, 2.0)
                if aspect:
                    self.log_message(f"✅ {line_style.value}: Line aspect created successfully")
                else:
                    self.log_message(f"❌ {line_style.value}: Failed to create line aspect")
            
            self.log_message("🎉 Line styles testing completed")
            
        except Exception as e:
            self.log_message(f"❌ Line styles test failed: {e}")
    
    def test_materials(self):
        """Test materials functionality"""
        if not self.visualization:
            self.log_message("❌ Visualization system not available")
            return
        
        self.log_message("🧪 Testing Materials...")
        
        try:
            color = (0.8, 0.8, 0.9)
            
            # Test different material types
            material_types = [
                MaterialType.METAL,
                MaterialType.PLASTIC,
                MaterialType.GLASS,
                MaterialType.WOOD,
                MaterialType.STONE
            ]
            
            for material_type in material_types:
                material = self.visualization.create_material_aspect(material_type, color, 0.1)
                if material:
                    self.log_message(f"✅ {material_type.value}: Material created successfully")
                else:
                    self.log_message(f"❌ {material_type.value}: Failed to create material")
            
            self.log_message("🎉 Materials testing completed")
            
        except Exception as e:
            self.log_message(f"❌ Materials test failed: {e}")
    
    def test_presets(self):
        """Test visualization presets"""
        if not self.visualization:
            self.log_message("❌ Visualization system not available")
            return
        
        self.log_message("🧪 Testing Presets...")
        
        try:
            # Test all presets
            presets = [
                ("Metal", VisualizationPresets.get_metal_preset()),
                ("Glass", VisualizationPresets.get_glass_preset()),
                ("Wood", VisualizationPresets.get_wood_preset()),
                ("Plastic", VisualizationPresets.get_plastic_preset()),
                ("Technical", VisualizationPresets.get_technical_preset()),
                ("Artistic", VisualizationPresets.get_artistic_preset())
            ]
            
            for name, preset in presets:
                if preset and isinstance(preset, dict):
                    self.log_message(f"✅ {name} Preset: {preset.get('material_type', 'Unknown')} + {preset.get('gradient_type', 'Unknown')}")
                else:
                    self.log_message(f"❌ {name} Preset: Invalid preset data")
            
            self.log_message("🎉 Presets testing completed")
            
        except Exception as e:
            self.log_message(f"❌ Presets test failed: {e}")
    
    def open_settings_dialog(self):
        """Open visualization settings dialog"""
        if not VISUALIZATION_AVAILABLE:
            self.log_message("❌ Visualization system not available")
            return
        
        try:
            self.log_message("🔧 Opening visualization settings dialog...")
            dialog = VisualizationDialog(self)
            dialog.settings_changed.connect(self.on_settings_changed)
            dialog.exec()
            self.log_message("✅ Settings dialog closed")
            
        except Exception as e:
            self.log_message(f"❌ Failed to open settings dialog: {e}")
    
    def on_settings_changed(self, settings: Dict[str, Any]):
        """Handle settings changes"""
        self.log_message("⚙️ Visualization settings changed:")
        self.log_message(f"   Material: {settings.get('material_type', 'Unknown')}")
        self.log_message(f"   Gradient: {settings.get('gradient_type', 'Unknown')}")
        self.log_message(f"   Line Style: {settings.get('line_style', 'Unknown')}")
        self.log_message(f"   Transparency: {settings.get('transparency', 0.0)}")

def main():
    """Main function"""
    print("🚀 Starting 3D Visualization System Demo...")
    
    app = QApplication(sys.argv)
    
    # Create demo window
    demo = VisualizationDemo()
    demo.show()
    
    print("✅ Demo window created and shown")
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
