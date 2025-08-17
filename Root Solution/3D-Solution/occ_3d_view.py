#!/usr/bin/env python3
"""
OpenCASCADE 3D View Widget for TheSolution CAD
Real 3D visualization with OpenCASCADE
"""

import sys
import os
from typing import List, Optional, Dict, Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont

# Add project paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, project_root)

try:
    from OCC.Display.backend import load_backend
    from OCC.Display.SimpleGui import init_display
    from OCC.Core.AIS import AIS_Shape, AIS_Line, AIS_Point
    from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
    from OCC.Core.Graphic3d import Graphic3d_MaterialAspect, Graphic3d_NOM_METALIZED
    from OCC.Core.Aspect import Aspect_TOL_SOLID, Aspect_TOL_DASH, Aspect_TOL_DOT
    from OCC.Core.Prs3d import Prs3d_LineAspect, Prs3d_ShadingAspect
    from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
    from OCC.Core.TopExp import TopExp_Explorer
    from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
    from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Sphere
    from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Trsf
    from OCC.Core.BRepGProp import brepgprop_VolumeProperties
    from OCC.Core.GProp import GProp_GProps
    from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeCylinder
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform, BRepBuilderAPI_MakeEdge
    from OCC.Core.TopoDS import TopoDS_Shape
    
    # Import visualization system
    try:
        from visualization_3d import Visualization3D, LineStyle, GradientType, MaterialType, ColorScheme
        VISUALIZATION_AVAILABLE = True
    except ImportError:
        VISUALIZATION_AVAILABLE = False
        print("Warning: Visualization system not available")

    OCC_AVAILABLE = True
    print("✅ OpenCASCADE 3D view system imported successfully")
except ImportError as e:
    OCC_AVAILABLE = False
    VISUALIZATION_AVAILABLE = False
    print(f"❌ Failed to import OpenCASCADE 3D view: {e}")

# Define fallback enums if not imported
if not VISUALIZATION_AVAILABLE:
    from enum import Enum
    class LineStyle(Enum):
        SOLID = "Solid"
        DASHED = "Dashed"
        DOTTED = "Dotted"
        DASH_DOT = "Dash-Dot"
        LONG_DASH = "Long Dash"
        DOUBLE_DASH = "Double Dash"
    
    class GradientType(Enum):
        NONE = "None"
        LINEAR = "Linear"
        RADIAL = "Radial"
        CONICAL = "Conical"
        SPHERICAL = "Spherical"
    
    class MaterialType(Enum):
        METAL = "Metal"
        PLASTIC = "Plastic"
        GLASS = "Glass"
        WOOD = "Wood"
        STONE = "Stone"
        CUSTOM = "Custom"
    
    class ColorScheme(Enum):
        CLASSIC = "Classic"
        MODERN = "Modern"
        DARK = "Dark"
        LIGHT = "Light"
        TECHNICAL = "Technical"
        ARTISTIC = "Artistic"

# Define fallback classes for when OpenCASCADE is not available
if not OCC_AVAILABLE:
    class Quantity_Color:
        def __init__(self, r, g, b, toc):
            self.r = r
            self.g = g
            self.b = b
            self.toc = toc
    
    class Quantity_TOC_RGB:
        pass
    
    class Graphic3d_MaterialAspect:
        def __init__(self, material_type):
            self.material_type = material_type
        
        def SetColor(self, color):
            pass
        
        def SetTransparency(self, transparency):
            pass
    
    class Graphic3d_NOM_METALIZED:
        pass
    
    class Aspect_TOL_SOLID:
        pass
    
    class Aspect_TOL_DASH:
        pass
    
    class Aspect_TOL_DOT:
        pass
    
    class Prs3d_LineAspect:
        def __init__(self, color, style, width):
            self.color = color
            self.style = style
            self.width = width
    
    class AIS_Shape:
        def __init__(self, shape):
            self.shape = shape
        
        def SetColor(self, color):
            pass
        
        def SetMaterial(self, material):
            pass
        
        def SetLineAspect(self, aspect):
            pass
    
    class TopoDS_Shape:
        pass
    
    class gp_Pnt:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
    
    class BRepBuilderAPI_MakeEdge:
        def __init__(self, start, end):
            self.start = start
            self.end = end
        
        def Edge(self):
            return TopoDS_Shape()

class OCC3DViewWidget(QWidget):
    """OpenCASCADE 3D View Widget"""
    
    # Signals
    object_selected = Signal(str)  # Emits object ID when selected
    view_changed = Signal()  # Emits when view changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.display = None
        self.context = None
        self.viewer = None
        self.ais_shapes = {}  # Dictionary to store AIS_Shape objects
        self.visualization = None
        self.current_settings = {}
        
        self.setup_ui()
        self.initialize_occ_display()
    
    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        
        # 3D View area
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
        
        # Display controls
        self.wireframe_btn = QPushButton("Wireframe")
        self.wireframe_btn.setCheckable(True)
        self.wireframe_btn.clicked.connect(self.toggle_wireframe)
        control_layout.addWidget(self.wireframe_btn)
        
        self.shaded_btn = QPushButton("Shaded")
        self.shaded_btn.setCheckable(True)
        self.shaded_btn.setChecked(True)
        self.shaded_btn.clicked.connect(self.toggle_shaded)
        control_layout.addWidget(self.shaded_btn)
        
        # Grid controls
        self.grid_btn = QPushButton("Grid")
        self.grid_btn.setCheckable(True)
        self.grid_btn.setChecked(True)
        self.grid_btn.clicked.connect(self.toggle_grid)
        control_layout.addWidget(self.grid_btn)
        
        # Axes controls
        self.axes_btn = QPushButton("Axes")
        self.axes_btn.setCheckable(True)
        self.axes_btn.setChecked(True)
        self.axes_btn.clicked.connect(self.toggle_axes)
        control_layout.addWidget(self.axes_btn)
        
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
                print("✅ Visualization3D initialized for 3D view")
            
            # Load backend and create display
            load_backend("pyside6")
            
            # Initialize display
            self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display(
                backend_str="pyside6",
                size=(400, 300)
            )
            
            # Get context and viewer
            self.context = self.display.GetContext()
            self.viewer = self.display.GetViewer()
            
            # Setup display
            self.setup_display()
            
            # Create coordinate system
            self.create_coordinate_system()
            
            # Create grid
            self.create_grid()
            
            # Replace our view widget with the OpenCASCADE widget
            if hasattr(self.display, 'GetWidget'):
                occ_widget = self.display.GetWidget()
                if occ_widget:
                    # Remove our placeholder widget
                    layout = self.layout()
                    layout.removeWidget(self.view_widget)
                    self.view_widget.deleteLater()
                    
                    # Add OpenCASCADE widget
                    self.view_widget = occ_widget
                    layout.insertWidget(0, self.view_widget)
            
            self.status_label.setText("✅ 3D View: Ready")
            print("✅ OpenCASCADE 3D view initialized successfully")
            
            # Add a test cube to verify display is working
            self.add_test_cube()
            
        except Exception as e:
            self.status_label.setText(f"❌ Failed to initialize 3D view: {e}")
            print(f"❌ Failed to initialize OpenCASCADE display: {e}")
    
    def add_test_cube(self):
        """Add a test cube to verify 3D view is working"""
        if not self.display or not self.context:
            return
        
        try:
            # Create a simple test cube
            from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
            from OCC.Core.gp import gp_Pnt
            
            # Create cube at origin with size 5
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
        # Note: Zoom method signature may vary between OpenCASCADE versions
        try:
            self.display.View.Zoom(0.8)
        except:
            pass  # Skip zoom if not supported
    
    def create_coordinate_system(self):
        """Create coordinate system axes"""
        if not self.display:
            return
        
        try:
            # Create axes
            from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2
            from OCC.Core.Geom import Geom_CartesianPoint
            from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
            from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex, BRepBuilderAPI_MakeEdge
            
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
            
        except Exception as e:
            print(f"Warning: Failed to create coordinate system: {e}")
    
    def create_grid(self):
        """Create grid for 3D view"""
        if not self.display:
            return
        
        try:
            # Create grid lines
            for i in range(-10, 11):
                if i == 0:
                    continue  # Skip center lines
                
                # Vertical lines (parallel to Y-axis)
                start = gp_Pnt(i, -10, 0)
                end = gp_Pnt(i, 10, 0)
                edge = BRepBuilderAPI_MakeEdge(start, end).Edge()
                ais = AIS_Shape(edge)
                ais.SetColor(Quantity_Color(0.3, 0.3, 0.3, Quantity_TOC_RGB))
                self.context.Display(ais, True)
                
                # Horizontal lines (parallel to X-axis)
                start = gp_Pnt(-10, i, 0)
                end = gp_Pnt(10, i, 0)
                edge = BRepBuilderAPI_MakeEdge(start, end).Edge()
                ais = AIS_Shape(edge)
                ais.SetColor(Quantity_Color(0.3, 0.3, 0.3, Quantity_TOC_RGB))
                self.context.Display(ais, True)
                
        except Exception as e:
            print(f"Warning: Failed to create grid: {e}")
    
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
    
    def update_shape_visualization(self, object_id: str, settings: Dict[str, Any]) -> bool:
        """Update shape visualization with new settings"""
        if not self.context or object_id not in self.ais_shapes:
            return False
        
        try:
            ais_shape = self.ais_shapes[object_id]
            
            if self.visualization:
                self.visualization.apply_visualization_style(ais_shape, settings)
            
            self.context.Update(ais_shape, True)
            self.status_label.setText(f"✅ Updated visualization: {object_id}")
            return True
            
        except Exception as e:
            self.status_label.setText(f"❌ Failed to update visualization: {e}")
            print(f"❌ Failed to update visualization: {e}")
        
        return False
    
    def clear_all(self):
        """Clear all shapes from 3D view"""
        if not self.context:
            return
        
        try:
            self.context.RemoveAll(True)
            self.ais_shapes.clear()
            self.status_label.setText("✅ Cleared all objects")
            
        except Exception as e:
            self.status_label.setText(f"❌ Failed to clear objects: {e}")
            print(f"❌ Failed to clear objects: {e}")
    
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
    
    def toggle_wireframe(self):
        """Toggle wireframe display mode"""
        if self.display:
            if self.wireframe_btn.isChecked():
                self.display.View.SetComputedMode(False)
                self.shaded_btn.setChecked(False)
            else:
                self.display.View.SetComputedMode(True)
                self.shaded_btn.setChecked(True)
    
    def toggle_shaded(self):
        """Toggle shaded display mode"""
        if self.display:
            if self.shaded_btn.isChecked():
                self.display.View.SetComputedMode(True)
                self.wireframe_btn.setChecked(False)
            else:
                self.display.View.SetComputedMode(False)
                self.wireframe_btn.setChecked(True)
    
    def toggle_grid(self):
        """Toggle grid display"""
        # Implementation depends on how grid is stored
        self.status_label.setText("Grid toggle: " + ("ON" if self.grid_btn.isChecked() else "OFF"))
    
    def toggle_axes(self):
        """Toggle coordinate axes display"""
        # Implementation depends on how axes are stored
        self.status_label.setText("Axes toggle: " + ("ON" if self.axes_btn.isChecked() else "OFF"))
    
    def get_view_widget(self) -> QWidget:
        """Get the main view widget"""
        return self.view_widget
    
    def is_available(self) -> bool:
        """Check if 3D view is available"""
        return OCC_AVAILABLE and self.display is not None
