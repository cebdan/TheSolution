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

# Add project paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))  # Go up to project root

# Check if the calculated path is correct, otherwise use current working directory
if not os.path.exists(os.path.join(project_root, "solution_data_types.py")):
    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, "solution_data_types.py")):
        project_root = cwd

sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "Base Solution", "python"))
sys.path.insert(0, os.path.join(project_root, "Root Solution", "python"))

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
    
    # Import 3D visualization system
    try:
        from visualization_3d import Visualization3D, LineStyle, GradientType, MaterialType, ColorScheme
        from visualization_dialog import VisualizationDialog
        VISUALIZATION_AVAILABLE = True
    except ImportError:
        VISUALIZATION_AVAILABLE = False
        print("WARNING: 3D visualization system not available")

    # Import 3D view widget
    try:
        from integrated_3d_view import Integrated3DViewManager
        OCC_3D_VIEW_AVAILABLE = True
    except ImportError:
        OCC_3D_VIEW_AVAILABLE = False
        print("WARNING: OpenCASCADE 3D view not available")

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
        
        # Initialize visualization settings
        self.visualization_settings = {}
        if VISUALIZATION_AVAILABLE:
            self.visualization_settings = {
                'material_type': MaterialType.METAL,
                'transparency': 0.0,
                'base_color': (0.8, 0.8, 0.9),
                'gradient_type': GradientType.NONE,
                'gradient_intensity': 50,
                'line_style': LineStyle.SOLID,
                'line_width': 1.0,
                'line_color': (0.8, 0.8, 0.8),
                'show_edges': True,
                'show_vertices': False,
                'wireframe_mode': False,
                'color_scheme': ColorScheme.CLASSIC,
                'show_grid': True,
                'grid_spacing': 1.0,
                'grid_size': 20.0,
                'show_axes': True,
                'show_labels': True
            }
        
        self.init_ui_from_file()
        self.setup_styles()
        
        # Check OpenCASCADE availability
        self.check_opencascade()
        
        # Initialize 3D view
        self.init_3d_view()
    
    def init_ui_from_file(self):
        """Initialize interface from UI file"""
        self.setWindowTitle("TheSolution CAD - 3D-Solution")
        self.setGeometry(100, 100, 1400, 900)
        
        # Load UI from file
        try:
            from PySide6.QtUiTools import QUiLoader
            ui_file_path = os.path.join(project_root, "Gui", "3D-Solution", "main.ui")
            
            if os.path.exists(ui_file_path):
                loader = QUiLoader()
                with open(ui_file_path, "r") as ui_file:
                    self.ui = loader.load(ui_file, self)
                
                # Get references to UI elements
                self.solution_tree = self.ui.solutionTree
                self.view_toolbar = self.ui.viewToolBar
                self.view_status_bar = self.ui.viewStatusBar
                self.open_gl_widget = self.ui.openGLWidget
                
                # Setup UI elements
                self.setup_ui_elements()
                
                print("✅ UI loaded from file successfully")
            else:
                print(f"❌ UI file not found: {ui_file_path}")
                self.create_fallback_ui()
                
        except Exception as e:
            print(f"❌ Failed to load UI from file: {e}")
            self.create_fallback_ui()
    
    def create_fallback_ui(self):
        """Create fallback UI if file loading fails"""
        self.setWindowTitle("TheSolution CAD - 3D-Solution (Fallback)")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create menu bar
        self.create_menu_bar()
        
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
    
    def setup_ui_elements(self):
        """Setup UI elements after loading from file"""
        # Setup solution tree
        self.solution_tree.setHeaderLabels(["Name", "Type", "ID", "Volume"])
        self.solution_tree.setColumnWidth(0, 120)
        self.solution_tree.setColumnWidth(1, 80)
        self.solution_tree.setColumnWidth(2, 60)
        self.solution_tree.setColumnWidth(3, 80)
        
        # Setup toolbar
        self.setup_toolbar()
    
    def setup_toolbar(self):
        """Setup toolbar for 3D view controls"""
        if not hasattr(self, 'view_toolbar'):
            return
        
        # Clear existing actions
        self.view_toolbar.clear()
        
        # Add basic actions (will be enhanced by 3D view manager)
        self.action_fit_all = QAction("Fit All", self)
        self.action_fit_all.triggered.connect(self.fit_all_objects)
        self.view_toolbar.addAction(self.action_fit_all)
        
        self.action_reset_view = QAction("Reset View", self)
        self.action_reset_view.triggered.connect(self.reset_view)
        self.view_toolbar.addAction(self.action_reset_view)
    
    def fit_all_objects(self):
        """Fit all objects to view"""
        if hasattr(self, 'occ_3d_view_manager'):
            self.occ_3d_view_manager.fit_all()
    
    def reset_view(self):
        """Reset view to default"""
        if hasattr(self, 'occ_3d_view_manager'):
            self.occ_3d_view_manager.reset_view()
        
        # Setup status bar
        self.view_status_bar.showMessage("Ready")
        
        # Create menu bar
        self.create_menu_bar()
    
    def create_menu_bar(self):
        """Create menu bar with visualization settings"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        # Add visualization settings action
        if VISUALIZATION_AVAILABLE:
            visualization_action = view_menu.addAction('3D Visualization Settings')
            visualization_action.triggered.connect(self.show_visualization_dialog)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
    
    def init_3d_view(self):
        """Initialize integrated 3D view"""
        if OCC_3D_VIEW_AVAILABLE:
            # Create integrated 3D view manager
            self.occ_3d_view_manager = Integrated3DViewManager(self)
            
            # Setup UI references if UI was loaded from file
            if hasattr(self, 'view_toolbar') and hasattr(self, 'view_status_bar') and hasattr(self, 'solution_tree') and hasattr(self, 'open_gl_widget'):
                self.occ_3d_view_manager.setup_ui_references(
                    self.view_toolbar,
                    self.view_status_bar,
                    self.solution_tree,
                    self.open_gl_widget
                )
            
            # Initialize OpenCASCADE display
            if self.occ_3d_view_manager.initialize_occ_display():
                print("✅ Integrated 3D view initialized successfully")
                
                # Connect signals
                self.occ_3d_view_manager.object_selected.connect(self.on_3d_object_selected)
                self.occ_3d_view_manager.object_moved.connect(self.on_3d_object_moved)
                self.occ_3d_view_manager.object_rotated.connect(self.on_3d_object_rotated)
                self.occ_3d_view_manager.object_scaled.connect(self.on_3d_object_scaled)
                self.occ_3d_view_manager.selection_changed.connect(self.on_3d_selection_changed)
            else:
                print("❌ Failed to initialize integrated 3D view")
        else:
            print("⚠️ OpenCASCADE 3D view not available")
    
    def on_3d_object_selected(self, object_id: str):
        """Handle object selection in 3D view"""
        print(f"Object selected in 3D view: {object_id}")
        # Update UI to reflect selection
    
    def on_3d_object_moved(self, object_id: str, x: float, y: float, z: float):
        """Handle object movement in 3D view"""
        print(f"Object moved in 3D view: {object_id} to ({x}, {y}, {z})")
        # Update object data and UI
    
    def on_3d_object_rotated(self, object_id: str, rx: float, ry: float, rz: float):
        """Handle object rotation in 3D view"""
        print(f"Object rotated in 3D view: {object_id} to ({rx}, {ry}, {rz})")
        # Update object data and UI
    
    def on_3d_object_scaled(self, object_id: str, sx: float, sy: float, sz: float):
        """Handle object scaling in 3D view"""
        print(f"Object scaled in 3D view: {object_id} to ({sx}, {sy}, {sz})")
        # Update object data and UI
    
    def on_3d_selection_changed(self, selected_objects: list):
        """Handle selection change in 3D view"""
        print(f"Selection changed in 3D view: {selected_objects}")
        # Update UI to reflect selection
    
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
        
        # 3D View area - will be handled by integrated manager
        if OCC_3D_VIEW_AVAILABLE:
            # Placeholder for integrated 3D view
            self.view_label = QLabel("3D View Area\n(Integrated OpenCASCADE view)")
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
            
            # Status label
            self.occ_status_label = QLabel("OpenCASCADE 3D View: Will be initialized")
            self.occ_status_label.setAlignment(Qt.AlignCenter)
            center_layout.addWidget(self.occ_status_label)
        else:
            # Fallback to placeholder
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
            self.occ_status_label = QLabel("OpenCASCADE: Not available")
            self.occ_status_label.setAlignment(Qt.AlignCenter)
            center_layout.addWidget(self.occ_status_label)
        
        # Visualization settings button
        if VISUALIZATION_AVAILABLE:
            self.visualization_btn = QPushButton("3D Visualization Settings")
            self.visualization_btn.clicked.connect(self.show_visualization_dialog)
            center_layout.addWidget(self.visualization_btn)
        
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
    
    def show_visualization_dialog(self):
        """Show 3D visualization settings dialog"""
        if not VISUALIZATION_AVAILABLE:
            QMessageBox.warning(self, "Warning", "3D visualization system is not available.")
            return
        
        try:
            dialog = VisualizationDialog(self)
            dialog.settings_changed.connect(self.apply_visualization_settings)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open visualization dialog: {e}")
    
    def apply_visualization_settings(self, settings: Dict[str, Any]):
        """Apply visualization settings to 3D view"""
        try:
            self.log_message("Applying 3D visualization settings...")
            
            # Store current settings
            self.visualization_settings = settings
            
            # Update 3D view with new settings
            self.update_3d_view_with_settings(settings)
            
            # Update real 3D view if available
            self.update_3d_view_visualization(settings)
            
            self.log_message("✅ 3D visualization settings applied successfully")
            
        except Exception as e:
            self.log_message(f"❌ Failed to apply visualization settings: {e}")
    
    def update_3d_view_with_settings(self, settings: Dict[str, Any]):
        """Update 3D view with visualization settings"""
        # This would integrate with actual 3D rendering
        # For now, just update the placeholder
        material_type = settings.get('material_type', 'Metal')
        gradient_type = settings.get('gradient_type', 'None')
        line_style = settings.get('line_style', 'Solid')
        
        self.view_label.setText(f"3D View Area\nMaterial: {material_type}\nGradient: {gradient_type}\nLine Style: {line_style}")
        
        # Update status
        self.occ_status_label.setText(f"3D Visualization: {material_type} + {gradient_type}")
    
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
        
        # Add to 3D view if available
        if OCC_3D_VIEW_AVAILABLE and hasattr(self, 'occ_3d_view_manager') and 'shape' in object_data:
            self.add_object_to_3d_view(object_data)
        
        # Hide progress
        self.progress_bar.setVisible(False)
        
        # Logging
        occ_status = "with OpenCASCADE" if object_data.get('occ_available', False) else "without OpenCASCADE"
        volume_info = f" (Volume: {object_data.get('volume', 0):.2f})" if 'volume' in object_data else ""
        self.log_message(f"✅ Created {object_data['name']} {occ_status}{volume_info}")
    
    def add_object_to_3d_view(self, object_data: Dict[str, Any]):
        """Add object to 3D view"""
        if not OCC_3D_VIEW_AVAILABLE or not hasattr(self, 'occ_3d_view_manager'):
            return
        
        try:
            # Get shape from object data
            shape = object_data.get('shape')
            if shape is None:
                self.log_message(f"❌ No shape data for object {object_data['id']}")
                return
            
            # Get visualization settings
            settings = self.visualization_settings if hasattr(self, 'visualization_settings') else {}
            
            # Get position from object data
            position = (object_data.get('x', 0), object_data.get('y', 0), object_data.get('z', 0))
            rotation = (0, 0, 0)  # Default rotation
            scale = (1, 1, 1)     # Default scale
            
            # Add to 3D view
            success = self.occ_3d_view_manager.add_shape(
                shape=shape,
                object_id=str(object_data['id']),
                color=settings.get('base_color', (0.8, 0.8, 0.9)),
                material_type=settings.get('material_type', MaterialType.METAL),
                line_style=settings.get('line_style', LineStyle.SOLID),
                gradient_type=settings.get('gradient_type', GradientType.NONE),
                transparency=settings.get('transparency', 0.0),
                position=position,
                rotation=rotation,
                scale=scale
            )
            
            if success:
                self.log_message(f"✅ Added object {object_data['id']} to 3D view")
            else:
                self.log_message(f"❌ Failed to add object {object_data['id']} to 3D view")
                
        except Exception as e:
            self.log_message(f"❌ Error adding object to 3D view: {e}")
    
    def remove_object_from_3d_view(self, object_id: str):
        """Remove object from 3D view"""
        if not OCC_3D_VIEW_AVAILABLE or not hasattr(self, 'occ_3d_view_manager'):
            return
        
        try:
            success = self.occ_3d_view_manager.remove_shape(object_id)
            if success:
                self.log_message(f"✅ Removed object {object_id} from 3D view")
            else:
                self.log_message(f"❌ Failed to remove object {object_id} from 3D view")
                
        except Exception as e:
            self.log_message(f"❌ Error removing object from 3D view: {e}")
    
    def update_3d_view_visualization(self, settings: Dict[str, Any]):
        """Update 3D view visualization settings"""
        if not OCC_3D_VIEW_AVAILABLE or not hasattr(self, 'occ_3d_view_manager'):
            return
        
        try:
            # Update all objects in 3D view
            for object_id in self.occ_3d_view_manager.ais_shapes.keys():
                self.occ_3d_view_manager.update_shape_visualization(
                    object_id=object_id,
                    color=settings.get('color'),
                    material_type=settings.get('material_type'),
                    line_style=settings.get('line_style'),
                    gradient_type=settings.get('gradient_type'),
                    transparency=settings.get('transparency')
                )
            
            self.log_message("✅ Updated 3D view visualization settings")
            
        except Exception as e:
            self.log_message(f"❌ Error updating 3D view visualization: {e}")
    
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
        
        # Remove from 3D view if available
        if OCC_3D_VIEW_AVAILABLE and hasattr(self, 'occ_3d_view_manager'):
            self.remove_object_from_3d_view(str(object_id))
        
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
