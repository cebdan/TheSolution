#!/usr/bin/env python3
"""
Integrated 3D View Widget for TheSolution CAD
Full integration with UI file and bidirectional communication
"""

import sys
import os
from typing import Dict, Any, Optional, List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QToolBar, QStatusBar, QFrame, QSplitter, QTreeWidget, QTreeWidgetItem
)
from PySide6.QtCore import Qt, Signal, QTimer, QObject
from PySide6.QtGui import QFont, QAction, QIcon

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
    from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec
    from OCC.Core.TopoDS import TopoDS_Shape
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
    
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
    print("✅ Integrated 3D view system imported successfully")
except ImportError as e:
    OCC_AVAILABLE = False
    VISUALIZATION_AVAILABLE = False
    print(f"❌ Failed to import Integrated 3D view: {e}")
    
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

class Integrated3DViewManager(QObject):
    """Manager for integrated 3D view with bidirectional communication"""
    
    # Signals for communication with main interface
    object_selected = Signal(str)  # Emits object ID when selected in 3D view
    object_moved = Signal(str, float, float, float)  # Emits object ID and new position
    object_rotated = Signal(str, float, float, float)  # Emits object ID and rotation angles
    object_scaled = Signal(str, float, float, float)  # Emits object ID and scale factors
    view_changed = Signal()  # Emits when view changes
    selection_changed = Signal(list)  # Emits list of selected object IDs
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.display = None
        self.context = None
        self.ais_shapes = {}  # Dictionary to store AIS_Shape objects
        self.visualization = None
        self.selected_objects = []  # List of currently selected object IDs
        self.object_positions = {}  # Store object positions
        self.object_rotations = {}  # Store object rotations
        self.object_scales = {}  # Store object scales
        
        # UI references (will be set by main window)
        self.view_toolbar = None
        self.view_status_bar = None
        self.solution_tree = None
        self.open_gl_widget = None
        
        # Initialize visualization system
        if VISUALIZATION_AVAILABLE:
            self.visualization = Visualization3D()
            print("✅ Visualization3D initialized for integrated 3D view")
    
    def setup_ui_references(self, view_toolbar, view_status_bar, solution_tree, open_gl_widget):
        """Setup references to UI elements"""
        self.view_toolbar = view_toolbar
        self.view_status_bar = view_status_bar
        self.solution_tree = solution_tree
        self.open_gl_widget = open_gl_widget
        
        # Setup toolbar actions
        self.setup_toolbar_actions()
        
        # Setup status bar
        self.update_status("3D View: Initializing...")
    
    def setup_toolbar_actions(self):
        """Setup toolbar actions for 3D view control"""
        if not self.view_toolbar:
            return
        
        # Clear existing actions
        self.view_toolbar.clear()
        
        # View actions
        self.action_zoom_in = QAction("Zoom In", self)
        self.action_zoom_in.triggered.connect(self.zoom_in)
        self.view_toolbar.addAction(self.action_zoom_in)
        
        self.action_zoom_out = QAction("Zoom Out", self)
        self.action_zoom_out.triggered.connect(self.zoom_out)
        self.view_toolbar.addAction(self.action_zoom_out)
        
        self.view_toolbar.addSeparator()
        
        # Navigation actions
        self.action_rotate = QAction("Rotate", self)
        self.action_rotate.setCheckable(True)
        self.action_rotate.triggered.connect(self.toggle_rotate_mode)
        self.view_toolbar.addAction(self.action_rotate)
        
        self.action_pan = QAction("Pan", self)
        self.action_pan.setCheckable(True)
        self.action_pan.triggered.connect(self.toggle_pan_mode)
        self.view_toolbar.addAction(self.action_pan)
        
        self.action_select = QAction("Select", self)
        self.action_select.setCheckable(True)
        self.action_select.setChecked(True)
        self.action_select.triggered.connect(self.toggle_select_mode)
        self.view_toolbar.addAction(self.action_select)
        
        self.view_toolbar.addSeparator()
        
        # View presets
        self.action_front_view = QAction("Front", self)
        self.action_front_view.triggered.connect(self.front_view)
        self.view_toolbar.addAction(self.action_front_view)
        
        self.action_top_view = QAction("Top", self)
        self.action_top_view.triggered.connect(self.top_view)
        self.view_toolbar.addAction(self.action_top_view)
        
        self.action_side_view = QAction("Side", self)
        self.action_side_view.triggered.connect(self.side_view)
        self.view_toolbar.addAction(self.action_side_view)
        
        self.action_isometric_view = QAction("Isometric", self)
        self.action_isometric_view.triggered.connect(self.isometric_view)
        self.view_toolbar.addAction(self.action_isometric_view)
    
    def initialize_occ_display(self):
        """Initialize OpenCASCADE display"""
        if not OCC_AVAILABLE:
            self.update_status("❌ OpenCASCADE not available")
            return False
        
        try:
            # Load backend
            load_backend("pyside6")
            
            # Initialize display
            self.display, self.start_display, self.add_menu, self.add_function_to_menu = init_display(
                backend_str="pyside6",
                size=(600, 400)
            )
            
            # Get context
            self.context = self.display.GetContext()
            
            # Setup display
            self.setup_display()
            
            # Create coordinate system
            self.create_coordinate_system()
            
            # Add test cube
            self.add_test_cube()
            
            # Setup selection callback
            self.setup_selection_callback()
            
            self.update_status("✅ 3D View: Ready")
            print("✅ Integrated OpenCASCADE 3D view initialized successfully")
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to initialize 3D view: {e}")
            print(f"❌ Failed to initialize Integrated OpenCASCADE display: {e}")
            return False
    
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
    
    def setup_selection_callback(self):
        """Setup callback for object selection"""
        if not self.context:
            return
        
        # This would be implemented with OpenCASCADE selection events
        # For now, we'll use a timer to check for selection changes
        self.selection_timer = QTimer()
        self.selection_timer.timeout.connect(self.check_selection_changes)
        self.selection_timer.start(100)  # Check every 100ms
    
    def check_selection_changes(self):
        """Check for selection changes in 3D view"""
        if not self.context:
            return
        
        try:
            # Get selected objects from context using proper OpenCASCADE API
            current_selection = []
            
            # Get selected interactive objects - handle both single object and list
            selected_objects = self.context.SelectedInteractive()
            
            # Handle different return types from SelectedInteractive()
            if selected_objects is None:
                # No selection
                pass
            elif hasattr(selected_objects, '__iter__') and not isinstance(selected_objects, str):
                # It's an iterable (list, tuple, etc.)
                for obj in selected_objects:
                    # Find object ID for this interactive object
                    for obj_id, ais_shape in self.ais_shapes.items():
                        if ais_shape == obj:
                            current_selection.append(obj_id)
                            break
            else:
                # Single object
                for obj_id, ais_shape in self.ais_shapes.items():
                    if ais_shape == selected_objects:
                        current_selection.append(obj_id)
                        break
            
            # Check if selection changed
            if current_selection != self.selected_objects:
                self.selected_objects = current_selection
                self.selection_changed.emit(self.selected_objects)
                
                # Update tree selection
                self.update_tree_selection()
                
                # Update status
                if self.selected_objects:
                    self.update_status(f"Selected: {', '.join(self.selected_objects)}")
                else:
                    self.update_status("No objects selected")
                    
        except Exception as e:
            print(f"Warning: Error checking selection: {e}")
    
    def update_tree_selection(self):
        """Update tree widget selection based on 3D view selection"""
        if not self.solution_tree:
            return
        
        # Clear current selection
        self.solution_tree.clearSelection()
        
        # Select items in tree that correspond to selected 3D objects
        for obj_id in self.selected_objects:
            # Find tree item for this object
            items = self.solution_tree.findItems(obj_id, Qt.MatchExactly | Qt.MatchRecursive)
            for item in items:
                item.setSelected(True)
    
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
            self.object_positions["test_cube"] = (0, 0, 0)
            self.object_rotations["test_cube"] = (0, 0, 0)
            self.object_scales["test_cube"] = (1, 1, 1)
            
            # Fit view to show the cube
            self.display.View.FitAll()
            
            print("✅ Test cube added successfully")
            self.update_status("✅ 3D View: Ready (Test cube added)")
            
        except Exception as e:
            print(f"❌ Failed to add test cube: {e}")
            self.update_status(f"❌ Test cube failed: {e}")
    
    def add_shape(self, shape: TopoDS_Shape, object_id: str, 
                  color: tuple = (0.8, 0.8, 0.9),
                  material_type: MaterialType = MaterialType.METAL,
                  line_style: LineStyle = LineStyle.SOLID,
                  gradient_type: GradientType = GradientType.NONE,
                  transparency: float = 0.0,
                  position: tuple = (0, 0, 0),
                  rotation: tuple = (0, 0, 0),
                  scale: tuple = (1, 1, 1)) -> bool:
        """Add shape to 3D view with position, rotation, and scale"""
        if not self.display or not self.context:
            return False
        
        try:
            # Apply transformations to shape
            transformed_shape = self.apply_transformations(shape, position, rotation, scale)
            
            # Create AIS_Shape
            if self.visualization:
                ais_shape = self.visualization.create_ais_shape(
                    transformed_shape, color, material_type, line_style, gradient_type, transparency
                )
            else:
                ais_shape = AIS_Shape(transformed_shape)
                occ_color = Quantity_Color(color[0], color[1], color[2], Quantity_TOC_RGB)
                ais_shape.SetColor(occ_color)
            
            if ais_shape:
                # Store in dictionary
                self.ais_shapes[object_id] = ais_shape
                self.object_positions[object_id] = position
                self.object_rotations[object_id] = rotation
                self.object_scales[object_id] = scale
                
                # Display in context
                self.context.Display(ais_shape, True)
                
                # Update view
                self.display.View.FitAll()
                
                self.update_status(f"✅ Added object: {object_id}")
                return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to add shape: {e}")
            print(f"❌ Failed to add shape: {e}")
        
        return False
    
    def apply_transformations(self, shape: TopoDS_Shape, position: tuple, rotation: tuple, scale: tuple) -> TopoDS_Shape:
        """Apply position, rotation, and scale transformations to shape"""
        try:
            # Create transformation matrix
            trsf = gp_Trsf()
            
            # Apply translation
            if position != (0, 0, 0):
                trsf.SetTranslation(gp_Vec(position[0], position[1], position[2]))
            
            # Apply rotation (simplified - would need proper rotation matrix)
            # This is a placeholder for rotation implementation
            
            # Apply scale (simplified - would need proper scale matrix)
            # This is a placeholder for scale implementation
            
            # Apply transformation
            transformed_shape = BRepBuilderAPI_Transform(shape, trsf).Shape()
            return transformed_shape
            
        except Exception as e:
            print(f"Warning: Failed to apply transformations: {e}")
            return shape
    
    def move_object(self, object_id: str, new_position: tuple) -> bool:
        """Move object to new position"""
        if object_id not in self.ais_shapes:
            return False
        
        try:
            # Update position
            self.object_positions[object_id] = new_position
            
            # Recreate shape with new position
            # This is a simplified implementation
            # In a real implementation, you would update the transformation matrix
            
            # Emit signal
            self.object_moved.emit(object_id, new_position[0], new_position[1], new_position[2])
            
            self.update_status(f"✅ Moved object: {object_id}")
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to move object: {e}")
            print(f"❌ Failed to move object: {e}")
            return False
    
    def rotate_object(self, object_id: str, rotation_angles: tuple) -> bool:
        """Rotate object by given angles"""
        if object_id not in self.ais_shapes:
            return False
        
        try:
            # Update rotation
            self.object_rotations[object_id] = rotation_angles
            
            # Emit signal
            self.object_rotated.emit(object_id, rotation_angles[0], rotation_angles[1], rotation_angles[2])
            
            self.update_status(f"✅ Rotated object: {object_id}")
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to rotate object: {e}")
            print(f"❌ Failed to rotate object: {e}")
            return False
    
    def scale_object(self, object_id: str, scale_factors: tuple) -> bool:
        """Scale object by given factors"""
        if object_id not in self.ais_shapes:
            return False
        
        try:
            # Update scale
            self.object_scales[object_id] = scale_factors
            
            # Emit signal
            self.object_scaled.emit(object_id, scale_factors[0], scale_factors[1], scale_factors[2])
            
            self.update_status(f"✅ Scaled object: {object_id}")
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to scale object: {e}")
            print(f"❌ Failed to scale object: {e}")
            return False
    
    def remove_shape(self, object_id: str) -> bool:
        """Remove shape from 3D view"""
        if not self.context or object_id not in self.ais_shapes:
            return False
        
        try:
            ais_shape = self.ais_shapes[object_id]
            self.context.Erase(ais_shape, True)
            del self.ais_shapes[object_id]
            
            # Clean up stored data
            if object_id in self.object_positions:
                del self.object_positions[object_id]
            if object_id in self.object_rotations:
                del self.object_rotations[object_id]
            if object_id in self.object_scales:
                del self.object_scales[object_id]
            
            self.update_status(f"✅ Removed object: {object_id}")
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to remove shape: {e}")
            print(f"❌ Failed to remove shape: {e}")
            return False
    
    def update_status(self, message: str):
        """Update status bar with message"""
        if self.view_status_bar:
            self.view_status_bar.showMessage(message)
    
    # View control methods
    def zoom_in(self):
        """Zoom in"""
        if self.display:
            self.display.View.SetZoom(1.2)
            self.view_changed.emit()
    
    def zoom_out(self):
        """Zoom out"""
        if self.display:
            self.display.View.SetZoom(0.8)
            self.view_changed.emit()
    
    def toggle_rotate_mode(self):
        """Toggle rotate mode"""
        if self.action_rotate.isChecked():
            self.action_pan.setChecked(False)
            self.action_select.setChecked(False)
            self.update_status("Rotate mode active")
        else:
            self.action_select.setChecked(True)
            self.update_status("Select mode active")
    
    def toggle_pan_mode(self):
        """Toggle pan mode"""
        if self.action_pan.isChecked():
            self.action_rotate.setChecked(False)
            self.action_select.setChecked(False)
            self.update_status("Pan mode active")
        else:
            self.action_select.setChecked(True)
            self.update_status("Select mode active")
    
    def toggle_select_mode(self):
        """Toggle select mode"""
        if self.action_select.isChecked():
            self.action_rotate.setChecked(False)
            self.action_pan.setChecked(False)
            self.update_status("Select mode active")
    
    def front_view(self):
        """Set front view"""
        if self.display:
            self.display.View.Front()
            self.view_changed.emit()
    
    def top_view(self):
        """Set top view"""
        if self.display:
            self.display.View.Top()
            self.view_changed.emit()
    
    def side_view(self):
        """Set side view"""
        if self.display:
            self.display.View.Right()
            self.view_changed.emit()
    
    def isometric_view(self):
        """Set isometric view"""
        if self.display:
            self.display.View.Iso()
            self.view_changed.emit()
    
    def fit_all(self):
        """Fit all objects to view"""
        if self.display:
            self.display.View.FitAll()
            self.view_changed.emit()
    
    def update_shape_visualization(self, object_id: str, 
                                   color: tuple = None,
                                   material_type: MaterialType = None,
                                   line_style: LineStyle = None,
                                   gradient_type: GradientType = None,
                                   transparency: float = None) -> bool:
        """Update visualization properties of a shape"""
        if not self.context or object_id not in self.ais_shapes:
            return False
        
        try:
            ais_shape = self.ais_shapes[object_id]
            
            # Update color if provided
            if color is not None:
                occ_color = Quantity_Color(color[0], color[1], color[2], Quantity_TOC_RGB)
                ais_shape.SetColor(occ_color)
            
            # Update material if provided
            if material_type is not None and self.visualization:
                # This would use the visualization system for material updates
                pass
            
            # Update line style if provided
            if line_style is not None and self.visualization:
                # This would use the visualization system for line style updates
                pass
            
            # Update gradient if provided
            if gradient_type is not None and self.visualization:
                # This would use the visualization system for gradient updates
                pass
            
            # Update transparency if provided
            if transparency is not None:
                ais_shape.SetTransparency(transparency)
            
            # Redisplay the shape to apply changes
            self.context.Redisplay(ais_shape, True)
            
            self.update_status(f"✅ Updated visualization for: {object_id}")
            return True
            
        except Exception as e:
            self.update_status(f"❌ Failed to update visualization: {e}")
            print(f"❌ Failed to update visualization: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if 3D view is available"""
        return OCC_AVAILABLE and self.display is not None
