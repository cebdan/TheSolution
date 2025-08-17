#!/usr/bin/env python3
"""
Simple 3D View Widget for TheSolution CAD
Integrated 3D visualization with OpenCASCADE
"""

import sys
import os
from typing import Dict, Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

# Add project paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, project_root)

try:
    from OCC.Display.backend import load_backend
    from OCC.Display.SimpleGui import init_display
    from OCC.Core.AIS import AIS_Shape
    from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
    from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeCylinder
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
    from OCC.Core.gp import gp_Pnt
    from OCC.Core.TopoDS import TopoDS_Shape
    
    # Import visualization system
    try:
        from visualization_3d import Visualization3D, LineStyle, GradientType, MaterialType
        VISUALIZATION_AVAILABLE = True
    except ImportError:
        VISUALIZATION_AVAILABLE = False
        print("Warning: Visualization system not available")
        
        # Define fallback enums
        from enum import Enum
        class LineStyle(Enum):
            SOLID = "Solid"
            DASHED = "Dashed"
            DOTTED = "Dotted"
        
        class GradientType(Enum):
            NONE = "None"
            LINEAR = "Linear"
            RADIAL = "Radial"
        
        class MaterialType(Enum):
            METAL = "Metal"
            PLASTIC = "Plastic"
            GLASS = "Glass"

    OCC_AVAILABLE = True
    print("✅ Simple 3D view system imported successfully")
except ImportError as e:
    OCC_AVAILABLE = False
    VISUALIZATION_AVAILABLE = False
    print(f"❌ Failed to import Simple 3D view: {e}")
    
    # Define fallback classes
    class Quantity_Color:
        def __init__(self, r, g, b, toc):
            self.r = r
            self.g = g
            self.b = b
            self.toc = toc
    
    class Quantity_TOC_RGB:
        pass
    
    class AIS_Shape:
        def __init__(self, shape):
            self.shape = shape
        
        def SetColor(self, color):
            pass
        
        def SetMaterial(self, material):
            pass
    
    class TopoDS_Shape:
        pass
    
    class gp_Pnt:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

class Simple3DViewWidget(QWidget):
    """Simple OpenCASCADE 3D View Widget"""
    
    # Signals
    object_selected = Signal(str)  # Emits object ID when selected
    view_changed = Signal()  # Emits when view changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.display = None
        self.context = None
        self.ais_shapes = {}  # Dictionary to store AIS_Shape objects
        self.visualization = None
        
        self.setup_ui()
        self.initialize_occ_display()
    
    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        
        # 3D View area - will be replaced by OpenCASCADE widget
        self.view_widget = QWidget()
        self.view_widget.setMinimumSize(400, 300)
        self.view_widget.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                border: 2px solid #34495e;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.view_widget)
        
        # Control panel
        control_layout = QHBoxLayout()
        
        # View controls
        self.fit_all_btn = QPushButton("Fit All")
        self.fit_all_btn.clicked.connect(self.fit_all)
        control_layout.addWidget(self.fit_all_btn)
        
        self.reset_view_btn = QPushButton("Reset View")
        self.reset_view_btn.clicked.connect(self.reset_view)
        control_layout.addWidget(self.reset_view_btn)
        
        # Test button
        self.test_btn = QPushButton("Add Test Cube")
        self.test_btn.clicked.connect(self.add_test_cube)
        control_layout.addWidget(self.test_btn)
        
        layout.addLayout(control_layout)
        
        # Status label
        self.status_label = QLabel("3D View: Initializing...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
    
    def initialize_occ_display(self):
        """Initialize OpenCASCADE display"""
        if not OCC_AVAILABLE:
            self.status_label.setText("❌ OpenCASCADE not available")
            return
        
        try:
            # Initialize visualization system
            if VISUALIZATION_AVAILABLE:
                self.visualization = Visualization3D()
                print("✅ Visualization3D initialized for simple 3D view")
            
            # Load backend
            load_backend("pyside6")
            
            # Initialize display
            self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display(
                backend_str="pyside6",
                size=(400, 300)
            )
            
            # Get context
            self.context = self.display.GetContext()
            
            # Setup display
            self.setup_display()
            
            # Create coordinate system
            self.create_coordinate_system()
            
            # Add test cube
            self.add_test_cube()
            
            self.status_label.setText("✅ 3D View: Ready")
            print("✅ Simple OpenCASCADE 3D view initialized successfully")
            
        except Exception as e:
            self.status_label.setText(f"❌ Failed to initialize 3D view: {e}")
            print(f"❌ Failed to initialize Simple OpenCASCADE display: {e}")
    
    def setup_display(self):
        """Setup display properties"""
        if not self.display:
            return
        
        # Set background color
        self.display.View.SetBackgroundColor(Quantity_Color(0.1, 0.1, 0.1, Quantity_TOC_RGB))
        
        # Enable selection
        self.context.Activate(AIS_Shape.SelectionMode(0))
        
        # Setup default view
        self.display.View.FitAll()
    
    def create_coordinate_system(self):
        """Create coordinate system axes"""
        if not self.display:
            return
        
        try:
            # Origin point
            origin = gp_Pnt(0, 0, 0)
            
            # X-axis (Red)
            x_end = gp_Pnt(10, 0, 0)
            x_edge = BRepBuilderAPI_MakeEdge(origin, x_end).Edge()
            x_ais = AIS_Shape(x_edge)
            x_ais.SetColor(Quantity_Color(1.0, 0.0, 0.0, Quantity_TOC_RGB))
            self.context.Display(x_ais, True)
            
            # Y-axis (Green)
            y_end = gp_Pnt(0, 10, 0)
            y_edge = BRepBuilderAPI_MakeEdge(origin, y_end).Edge()
            y_ais = AIS_Shape(y_edge)
            y_ais.SetColor(Quantity_Color(0.0, 1.0, 0.0, Quantity_TOC_RGB))
            self.context.Display(y_ais, True)
            
            # Z-axis (Blue)
            z_end = gp_Pnt(0, 0, 10)
            z_edge = BRepBuilderAPI_MakeEdge(origin, z_end).Edge()
            z_ais = AIS_Shape(z_edge)
            z_ais.SetColor(Quantity_Color(0.0, 0.0, 1.0, Quantity_TOC_RGB))
            self.context.Display(z_ais, True)
            
            print("✅ Coordinate system created")
            
        except Exception as e:
            print(f"Warning: Failed to create coordinate system: {e}")
    
    def add_test_cube(self):
        """Add a test cube to verify 3D view is working"""
        if not self.display or not self.context:
            return
        
        try:
            # Create a simple test cube
            box_maker = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), 5, 5, 5)
            test_cube = box_maker.Shape()
            
            # Create AIS_Shape
            ais_cube = AIS_Shape(test_cube)
            ais_cube.SetColor(Quantity_Color(0.8, 0.2, 0.2, Quantity_TOC_RGB))  # Red color
            
            # Display in context
            self.context.Display(ais_cube, True)
            
            # Store for later removal
            self.ais_shapes["test_cube"] = ais_cube
            
            # Fit view to show the cube
            self.display.View.FitAll()
            
            print("✅ Test cube added successfully")
            self.status_label.setText("✅ 3D View: Ready (Test cube added)")
            
        except Exception as e:
            print(f"❌ Failed to add test cube: {e}")
            self.status_label.setText(f"❌ Test cube failed: {e}")
    
    def add_shape(self, shape: TopoDS_Shape, object_id: str, 
                  color: tuple = (0.8, 0.8, 0.9),
                  material_type: MaterialType = MaterialType.METAL,
                  line_style: LineStyle = LineStyle.SOLID,
                  gradient_type: GradientType = GradientType.NONE,
                  transparency: float = 0.0) -> bool:
        """Add shape to 3D view"""
        if not self.display or not self.context:
            return False
        
        try:
            # Create AIS_Shape
            if self.visualization:
                ais_shape = self.visualization.create_ais_shape(
                    shape, color, material_type, line_style, gradient_type, transparency
                )
            else:
                ais_shape = AIS_Shape(shape)
                occ_color = Quantity_Color(color[0], color[1], color[2], Quantity_TOC_RGB)
                ais_shape.SetColor(occ_color)
            
            if ais_shape:
                # Store in dictionary
                self.ais_shapes[object_id] = ais_shape
                
                # Display in context
                self.context.Display(ais_shape, True)
                
                # Update view
                self.display.View.FitAll()
                
                self.status_label.setText(f"✅ Added object: {object_id}")
                return True
            
        except Exception as e:
            self.status_label.setText(f"❌ Failed to add shape: {e}")
            print(f"❌ Failed to add shape: {e}")
        
        return False
    
    def remove_shape(self, object_id: str) -> bool:
        """Remove shape from 3D view"""
        if not self.context or object_id not in self.ais_shapes:
            return False
        
        try:
            ais_shape = self.ais_shapes[object_id]
            self.context.Erase(ais_shape, True)
            del self.ais_shapes[object_id]
            
            self.status_label.setText(f"✅ Removed object: {object_id}")
            return True
            
        except Exception as e:
            self.status_label.setText(f"❌ Failed to remove shape: {e}")
            print(f"❌ Failed to remove shape: {e}")
        
        return False
    
    def fit_all(self):
        """Fit all objects to view"""
        if self.display:
            self.display.View.FitAll()
            self.status_label.setText("✅ Fit all objects")
    
    def reset_view(self):
        """Reset view to default"""
        if self.display:
            self.display.View.Reset()
            self.display.View.FitAll()
            self.status_label.setText("✅ Reset view")
    
    def is_available(self) -> bool:
        """Check if 3D view is available"""
        return OCC_AVAILABLE and self.display is not None
