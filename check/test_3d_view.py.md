#!/usr/bin/env python3
"""
Test script for 3D View integration
"""

import sys
import os

# Add project paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "Root Solution", "3D-Solution"))

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont
    
    # Test 3D view widget
    try:
        import importlib.util
        
        # Load occ_3d_view module
        occ_3d_view_path = os.path.join(current_dir, "Root Solution", "3D-Solution", "occ_3d_view.py")
        spec = importlib.util.spec_from_file_location("occ_3d_view", occ_3d_view_path)
        occ_3d_view_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(occ_3d_view_module)
        
        OCC3DViewWidget = occ_3d_view_module.OCC3DViewWidget
        print("✅ 3D View widget imported successfully")
        
        class Test3DViewWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("3D View Test")
                self.setGeometry(200, 200, 800, 600)
                
                # Create central widget
                central_widget = QWidget()
                self.setCentralWidget(central_widget)
                
                layout = QVBoxLayout(central_widget)
                
                # Title
                title = QLabel("3D View Integration Test")
                title.setFont(QFont("Arial", 16, QFont.Bold))
                title.setAlignment(Qt.AlignCenter)
                layout.addWidget(title)
                
                # Status
                status_label = QLabel("Testing 3D View...")
                status_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(status_label)
                
                # 3D View widget
                try:
                    self.occ_3d_view = OCC3DViewWidget()
                    layout.addWidget(self.occ_3d_view)
                    
                    if self.occ_3d_view.is_available():
                        status_label.setText("✅ 3D View: Available and Ready")
                        print("✅ 3D View widget created successfully")
                    else:
                        status_label.setText("❌ 3D View: Not Available")
                        print("❌ 3D View widget not available")
                        
                except Exception as e:
                    status_label.setText(f"❌ 3D View Error: {e}")
                    print(f"❌ Failed to create 3D View widget: {e}")
                
                # Test button
                test_btn = QPushButton("Test 3D View")
                test_btn.clicked.connect(self.test_3d_view)
                layout.addWidget(test_btn)
            
            def test_3d_view(self):
                """Test 3D view functionality"""
                if hasattr(self, 'occ_3d_view') and self.occ_3d_view.is_available():
                    print("✅ 3D View test: Available")
                else:
                    print("❌ 3D View test: Not available")
        
        def main():
            app = QApplication(sys.argv)
            window = Test3DViewWindow()
            window.show()
            sys.exit(app.exec())
        
        if __name__ == "__main__":
            main()
            
    except ImportError as e:
        print(f"❌ Failed to import 3D View widget: {e}")
        
except ImportError as e:
    print(f"❌ Failed to import PySide6: {e}")
