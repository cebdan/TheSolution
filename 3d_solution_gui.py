#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D-Solution GUI с интеграцией OpenCASCADE
"""

import sys
import os
import time
import threading
from datetime import datetime
from typing import Dict, Any, Optional

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
        QWidget, QTreeWidget, QTreeWidgetItem, QPushButton, 
        QTextEdit, QLabel, QSpinBox, QComboBox, QGroupBox,
        QGridLayout, QMessageBox, QProgressBar, QSplitter
    )
    from PySide6.QtCore import Qt, QThread, Signal, QTimer
    from PySide6.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush
    
    # Import data types system
    from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate
    
    # Import OpenCASCADE integration
    try:
        from opencascade_integration import OpenCascadeIntegration
        OCC_AVAILABLE = True
    except ImportError:
        OCC_AVAILABLE = False
        print("WARNING: OpenCASCADE integration not available")
    
    print("SUCCESS: All imports successful")
    
except ImportError as e:
    print(f"ERROR: Import failed - {e}")
    sys.exit(1)

class ObjectCreationThread(QThread):
    """Thread for creating objects with OpenCASCADE"""
    object_created = Signal(dict)
    creation_failed = Signal(str)
    
    def __init__(self, object_data: Dict[str, Any]):
        super().__init__()
        self.object_data = object_data
    
    def run(self):
        """Create object in separate thread"""
        try:
            # Simulate object creation
            time.sleep(0.5)  # Simulate work
            
            # If OpenCASCADE is available, use it
            if OCC_AVAILABLE:
                try:
                    integration = OpenCascadeIntegration()
                    if integration.occ_available:
                        # Create SolutionData
                        solution_data = SolutionDataUtils.create_minimal_solution_data(
                            name=self.object_data['name'],
                            solution_type=self.object_data['type'],
                            coordinate=SolutionCoordinate(
                                self.object_data['x'], 
                                self.object_data['y'], 
                                self.object_data['z']
                            )
                        )
                        
                        # Set dimensions
                        if self.object_data['type'] == SolutionType.BOX:
                            solution_data.dimensions.width = self.object_data['width']
                            solution_data.dimensions.height = self.object_data['height']
                            solution_data.dimensions.depth = self.object_data['depth']
                        elif self.object_data['type'] == SolutionType.SPHERE:
                            solution_data.dimensions.radius = self.object_data['radius']
                        elif self.object_data['type'] == SolutionType.CYLINDER:
                            solution_data.dimensions.radius = self.object_data['radius']
                            solution_data.dimensions.height = self.object_data['height']
                        
                        # Integration with OpenCASCADE
                        result = integration.integrate_with_solution_data(solution_data)
                        
                        if result:
                            self.object_data['volume'] = result['volume']
                            self.object_data['occ_shape'] = result['occ_shape']
                            self.object_data['occ_available'] = True
                            self.object_created.emit(self.object_data)
                        else:
                            self.creation_failed.emit("OpenCASCADE integration failed")
                    else:
                        self.creation_failed.emit("OpenCASCADE not available")
                except Exception as e:
                    self.creation_failed.emit(f"OpenCASCADE error: {e}")
            else:
                # Fallback без OpenCASCADE
                self.object_data['volume'] = self._calculate_volume_fallback()
                self.object_data['occ_available'] = False
                self.object_created.emit(self.object_data)
            
        except Exception as e:
            self.creation_failed.emit(f"Object creation failed: {e}")
    
    def _calculate_volume_fallback(self) -> float:
        """Расчет объема без OpenCASCADE"""
        obj_type = self.object_data['type']
        
        if obj_type == SolutionType.BOX:
            return self.object_data['width'] * self.object_data['height'] * self.object_data['depth']
        elif obj_type == SolutionType.SPHERE:
            import math
            return (4/3) * math.pi * (self.object_data['radius'] ** 3)
        elif obj_type == SolutionType.CYLINDER:
            import math
            return math.pi * (self.object_data['radius'] ** 2) * self.object_data['height']
        else:
            return 0.0

class TheSolution3DWindow(QMainWindow):
    """Main window 3D-Solution with OpenCASCADE integration"""
    
    def __init__(self):
        super().__init__()
        self.objects = {}  # Objects dictionary
        self.object_counter = 0
        self.creation_threads = []  # List of active threads
        
        self.init_ui()
        self.setup_styles()
        
        # Check OpenCASCADE availability
        self.check_opencascade()
    
    def init_ui(self):
        """Initialize interface"""
        self.setWindowTitle("TheSolution CAD - 3D-Solution")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - object tree
        self.create_left_panel(splitter)
        
        # Center panel - 3D view (placeholder for now)
        self.create_center_panel(splitter)
        
        # Right panel - properties and log
        self.create_right_panel(splitter)
        
        # Set splitter proportions
        splitter.setSizes([300, 600, 500])
    
    def create_left_panel(self, parent):
        """Create left panel with object tree"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Header
        title_label = QLabel("3D Objects")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        left_layout.addWidget(title_label)
        
        # Object tree
        self.object_tree = QTreeWidget()
        self.object_tree.setHeaderLabels(["Name", "Type", "ID", "Volume"])
        self.object_tree.setColumnWidth(0, 120)
        self.object_tree.setColumnWidth(1, 80)
        self.object_tree.setColumnWidth(2, 60)
        self.object_tree.setColumnWidth(3, 80)
        left_layout.addWidget(self.object_tree)
        
        # Control buttons
        button_layout = QGridLayout()
        
        # Object creation buttons
        self.create_box_btn = QPushButton("Create Box")
        self.create_sphere_btn = QPushButton("Create Sphere")
        self.create_cylinder_btn = QPushButton("Create Cylinder")
        
        button_layout.addWidget(self.create_box_btn, 0, 0)
        button_layout.addWidget(self.create_sphere_btn, 0, 1)
        button_layout.addWidget(self.create_cylinder_btn, 1, 0)
        
        # Control buttons
        self.delete_btn = QPushButton("Delete Object")
        self.export_btn = QPushButton("Export")
        self.import_btn = QPushButton("Import")
        
        button_layout.addWidget(self.delete_btn, 1, 1)
        button_layout.addWidget(self.export_btn, 2, 0)
        button_layout.addWidget(self.import_btn, 2, 1)
        
        left_layout.addLayout(button_layout)
        
        # Connect signals
        self.create_box_btn.clicked.connect(lambda: self.create_object(SolutionType.BOX))
        self.create_sphere_btn.clicked.connect(lambda: self.create_object(SolutionType.SPHERE))
        self.create_cylinder_btn.clicked.connect(lambda: self.create_object(SolutionType.CYLINDER))
        self.delete_btn.clicked.connect(self.delete_selected_object)
        self.export_btn.clicked.connect(self.export_objects)
        self.import_btn.clicked.connect(self.import_objects)
        
        parent.addWidget(left_widget)
    
    def create_center_panel(self, parent):
        """Create center panel with 3D view"""
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        
        # Header
        title_label = QLabel("3D View")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        center_layout.addWidget(title_label)
        
        # Placeholder for 3D view
        self.view_label = QLabel("3D View Area\n(OpenCASCADE visualization coming soon)")
        self.view_label.setAlignment(Qt.AlignCenter)
        self.view_label.setStyleSheet("""
            QLabel {
                background-color: #2c3e50;
                color: white;
                border: 2px solid #34495e;
                border-radius: 10px;
                padding: 20px;
                font-size: 16px;
            }
        """)
        center_layout.addWidget(self.view_label)
        
        # OpenCASCADE status
        self.occ_status_label = QLabel("OpenCASCADE: Checking...")
        self.occ_status_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.occ_status_label)
        
        parent.addWidget(center_widget)
    
    def create_right_panel(self, parent):
        """Create right panel with properties and log"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Header
        title_label = QLabel("Properties & Log")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        right_layout.addWidget(title_label)
        
        # Properties group
        properties_group = QGroupBox("Object Properties")
        properties_layout = QGridLayout(properties_group)
        
        # Coordinates
        properties_layout.addWidget(QLabel("X:"), 0, 0)
        self.x_spinbox = QSpinBox()
        self.x_spinbox.setRange(-1000, 1000)
        self.x_spinbox.setValue(0)
        properties_layout.addWidget(self.x_spinbox, 0, 1)
        
        properties_layout.addWidget(QLabel("Y:"), 1, 0)
        self.y_spinbox = QSpinBox()
        self.y_spinbox.setRange(-1000, 1000)
        self.y_spinbox.setValue(0)
        properties_layout.addWidget(self.y_spinbox, 1, 1)
        
        properties_layout.addWidget(QLabel("Z:"), 2, 0)
        self.z_spinbox = QSpinBox()
        self.z_spinbox.setRange(-1000, 1000)
        self.z_spinbox.setValue(0)
        properties_layout.addWidget(self.z_spinbox, 2, 1)
        
        # Dimensions
        properties_layout.addWidget(QLabel("Width:"), 3, 0)
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 1000)
        self.width_spinbox.setValue(10)
        properties_layout.addWidget(self.width_spinbox, 3, 1)
        
        properties_layout.addWidget(QLabel("Height:"), 4, 0)
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(1, 1000)
        self.height_spinbox.setValue(10)
        properties_layout.addWidget(self.height_spinbox, 4, 1)
        
        properties_layout.addWidget(QLabel("Depth:"), 5, 0)
        self.depth_spinbox = QSpinBox()
        self.depth_spinbox.setRange(1, 1000)
        self.depth_spinbox.setValue(10)
        properties_layout.addWidget(self.depth_spinbox, 5, 1)
        
        properties_layout.addWidget(QLabel("Radius:"), 6, 0)
        self.radius_spinbox = QSpinBox()
        self.radius_spinbox.setRange(1, 500)
        self.radius_spinbox.setValue(5)
        properties_layout.addWidget(self.radius_spinbox, 6, 1)
        
        right_layout.addWidget(properties_group)
        
        # Event log
        log_group = QGroupBox("Event Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        log_layout.addWidget(self.log_text)
        
        right_layout.addWidget(log_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        right_layout.addWidget(self.progress_bar)
        
        parent.addWidget(right_widget)
    
    def setup_styles(self):
        """Setup styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
                color: white;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #34495e;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #3498db;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QTreeWidget {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                border-radius: 4px;
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:selected {
                background-color: #3498db;
            }
            QTextEdit {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                border-radius: 4px;
                color: white;
                font-family: 'Courier New';
            }
            QSpinBox {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                border-radius: 4px;
                color: white;
                padding: 4px;
            }
        """)
    
    def check_opencascade(self):
        """Check OpenCASCADE availability"""
        if OCC_AVAILABLE:
            try:
                integration = OpenCascadeIntegration()
                if integration.occ_available:
                    self.occ_status_label.setText("OpenCASCADE: ✅ Available")
                    self.occ_status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
                    self.log_message("OpenCASCADE integration loaded successfully")
                else:
                    self.occ_status_label.setText("OpenCASCADE: ❌ Not available")
                    self.occ_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
                    self.log_message("OpenCASCADE not available in current environment")
            except Exception as e:
                self.occ_status_label.setText("OpenCASCADE: ❌ Error")
                self.occ_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
                self.log_message(f"OpenCASCADE error: {e}")
        else:
            self.occ_status_label.setText("OpenCASCADE: ❌ Not installed")
            self.occ_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            self.log_message("OpenCASCADE integration not available")
    
    def create_object(self, obj_type: SolutionType):
        """Create object of specified type"""
        self.object_counter += 1
        
        # Get parameters from UI
        x = self.x_spinbox.value()
        y = self.y_spinbox.value()
        z = self.z_spinbox.value()
        width = self.width_spinbox.value()
        height = self.height_spinbox.value()
        depth = self.depth_spinbox.value()
        radius = self.radius_spinbox.value()
        
        # Create object data
        object_data = {
            'id': self.object_counter,
            'name': f"{obj_type.value.capitalize()}_{self.object_counter}",
            'type': obj_type,
            'x': x, 'y': y, 'z': z,
            'width': width, 'height': height, 'depth': depth,
            'radius': radius,
            'created_at': datetime.now().isoformat()
        }
        
        # Create thread for object creation
        thread = ObjectCreationThread(object_data)
        thread.object_created.connect(self.on_object_created)
        thread.creation_failed.connect(self.on_creation_failed)
        
        self.creation_threads.append(thread)
        thread.start()
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        self.log_message(f"Creating {obj_type.value} object...")
    
    def on_object_created(self, object_data: Dict[str, Any]):
        """Handle successful object creation"""
        # Add to objects dictionary
        self.objects[object_data['id']] = object_data
        
        # Add to tree
        item = QTreeWidgetItem()
        item.setText(0, object_data['name'])
        item.setText(1, object_data['type'].value)
        item.setText(2, str(object_data['id']))
        
        if 'volume' in object_data:
            volume_text = f"{object_data['volume']:.2f}"
            item.setText(3, volume_text)
            
            # Color coding by type
            if object_data['type'] == SolutionType.BOX:
                item.setBackground(0, QColor(52, 152, 219))  # Blue
            elif object_data['type'] == SolutionType.SPHERE:
                item.setBackground(0, QColor(46, 204, 113))  # Green
            elif object_data['type'] == SolutionType.CYLINDER:
                item.setBackground(0, QColor(155, 89, 182))  # Purple
        
        self.object_tree.addTopLevelItem(item)
        
        # Hide progress
        self.progress_bar.setVisible(False)
        
        # Logging
        occ_status = "with OpenCASCADE" if object_data.get('occ_available', False) else "without OpenCASCADE"
        volume_info = f" (Volume: {object_data.get('volume', 0):.2f})" if 'volume' in object_data else ""
        self.log_message(f"✅ Created {object_data['name']} {occ_status}{volume_info}")
    
    def on_creation_failed(self, error_message: str):
        """Handle object creation error"""
        self.progress_bar.setVisible(False)
        self.log_message(f"❌ {error_message}")
        
        QMessageBox.warning(self, "Creation Failed", f"Failed to create object:\n{error_message}")
    
    def delete_selected_object(self):
        """Delete selected object"""
        current_item = self.object_tree.currentItem()
        if not current_item:
            QMessageBox.information(self, "No Selection", "Please select an object to delete")
            return
        
        object_id = int(current_item.text(2))
        object_name = current_item.text(0)
        
        # Remove from dictionary
        if object_id in self.objects:
            del self.objects[object_id]
        
        # Remove from tree
        self.object_tree.takeTopLevelItem(self.object_tree.indexOfTopLevelItem(current_item))
        
        self.log_message(f"🗑️ Deleted object: {object_name}")
    
    def export_objects(self):
        """Export objects"""
        if not self.objects:
            QMessageBox.information(self, "No Objects", "No objects to export")
            return
        
        # Simple export to text file
        filename = f"thesolution_objects_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("TheSolution CAD - Exported Objects\n")
                f.write("=" * 40 + "\n\n")
                
                for obj_id, obj_data in self.objects.items():
                    f.write(f"Object ID: {obj_id}\n")
                    f.write(f"Name: {obj_data['name']}\n")
                    f.write(f"Type: {obj_data['type'].value}\n")
                    f.write(f"Position: ({obj_data['x']}, {obj_data['y']}, {obj_data['z']})\n")
                    
                    if 'volume' in obj_data:
                        f.write(f"Volume: {obj_data['volume']:.2f}\n")
                    
                    f.write(f"Created: {obj_data['created_at']}\n")
                    f.write("-" * 20 + "\n\n")
            
            self.log_message(f"📁 Exported {len(self.objects)} objects to {filename}")
            QMessageBox.information(self, "Export Success", f"Objects exported to {filename}")
            
        except Exception as e:
            self.log_message(f"❌ Export failed: {e}")
            QMessageBox.critical(self, "Export Failed", f"Failed to export objects:\n{e}")
    
    def import_objects(self):
        """Import objects"""
        QMessageBox.information(self, "Import", "Import functionality coming soon...")
        self.log_message("📥 Import functionality not implemented yet")
    
    def log_message(self, message: str):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        self.log_text.append(log_entry)
        
        # Auto-scroll to end
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = TheSolution3DWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
