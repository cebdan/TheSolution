#!/usr/bin/env python3
"""
3D Visualization System for TheSolution CAD
Features: Gradients, Line Styles, Material Rendering
"""

import sys
import os
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import math

# Add project paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, project_root)

try:
    from OCC.Core.AIS import AIS_Shape, AIS_Line, AIS_Point
    from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
    from OCC.Core.Graphic3d import Graphic3d_MaterialAspect, Graphic3d_NOM_METALIZED
    from OCC.Core.Aspect import Aspect_TOL_SOLID, Aspect_TOL_DASH, Aspect_TOL_DOT
    from OCC.Core.Prs3d import Prs3d_LineAspect, Prs3d_ShadingAspect
    from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
    from OCC.Core.TopExp import TopExp_Explorer
    from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
    from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Sphere
    from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
    from OCC.Core.BRepGProp import brepgprop_VolumeProperties
    from OCC.Core.GProp import GProp_GProps
    VISUALIZATION_AVAILABLE = True
    print("✅ OpenCASCADE visualization system imported successfully")
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Warning: OpenCASCADE visualization not available")
    
    # Define fallback classes for when OpenCASCADE is not available
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

class LineStyle(Enum):
    """Line styles for 3D visualization"""
    SOLID = "Solid"
    DASHED = "Dashed"
    DOTTED = "Dotted"
    DASH_DOT = "Dash-Dot"
    LONG_DASH = "Long Dash"
    DOUBLE_DASH = "Double Dash"

class GradientType(Enum):
    """Gradient types for 3D visualization"""
    NONE = "None"
    LINEAR = "Linear"
    RADIAL = "Radial"
    CONICAL = "Conical"
    SPHERICAL = "Spherical"

class MaterialType(Enum):
    """Material types for 3D visualization"""
    METAL = "Metal"
    PLASTIC = "Plastic"
    GLASS = "Glass"
    WOOD = "Wood"
    STONE = "Stone"
    CUSTOM = "Custom"

class ColorScheme(Enum):
    """Predefined color schemes"""
    CLASSIC = "Classic"
    MODERN = "Modern"
    DARK = "Dark"
    LIGHT = "Light"
    TECHNICAL = "Technical"
    ARTISTIC = "Artistic"

class Visualization3D:
    """Main 3D visualization system"""
    
    def __init__(self):
        self.line_styles = {
            LineStyle.SOLID: Aspect_TOL_SOLID,
            LineStyle.DASHED: Aspect_TOL_DASH,
            LineStyle.DOTTED: Aspect_TOL_DOT,
            LineStyle.DASH_DOT: Aspect_TOL_DASH,
            LineStyle.LONG_DASH: Aspect_TOL_DASH,
            LineStyle.DOUBLE_DASH: Aspect_TOL_DASH
        }
        
        # Define material types with fallbacks
        self.material_types = {}
        try:
            self.material_types = {
                MaterialType.METAL: Graphic3d_NOM_METALIZED,
                MaterialType.PLASTIC: getattr(Graphic3d_MaterialAspect, 'Graphic3d_NOM_PLASTIC', Graphic3d_NOM_METALIZED),
                MaterialType.GLASS: getattr(Graphic3d_MaterialAspect, 'Graphic3d_NOM_GLASS', Graphic3d_NOM_METALIZED),
                MaterialType.WOOD: getattr(Graphic3d_MaterialAspect, 'Graphic3d_NOM_WOOD', Graphic3d_NOM_METALIZED),
                MaterialType.STONE: getattr(Graphic3d_MaterialAspect, 'Graphic3d_NOM_STONE', Graphic3d_NOM_METALIZED)
            }
        except AttributeError:
            # Fallback to basic material types
            self.material_types = {
                MaterialType.METAL: Graphic3d_NOM_METALIZED,
                MaterialType.PLASTIC: Graphic3d_NOM_METALIZED,
                MaterialType.GLASS: Graphic3d_NOM_METALIZED,
                MaterialType.WOOD: Graphic3d_NOM_METALIZED,
                MaterialType.STONE: Graphic3d_NOM_METALIZED
            }
        
        self.color_schemes = {
            ColorScheme.CLASSIC: {
                'background': (0.1, 0.1, 0.1),
                'grid': (0.3, 0.3, 0.3),
                'axes': (1.0, 1.0, 1.0),
                'default': (0.8, 0.8, 0.8)
            },
            ColorScheme.MODERN: {
                'background': (0.05, 0.05, 0.08),
                'grid': (0.2, 0.2, 0.25),
                'axes': (0.9, 0.9, 0.9),
                'default': (0.7, 0.7, 0.8)
            },
            ColorScheme.DARK: {
                'background': (0.02, 0.02, 0.02),
                'grid': (0.15, 0.15, 0.15),
                'axes': (0.8, 0.8, 0.8),
                'default': (0.6, 0.6, 0.6)
            },
            ColorScheme.LIGHT: {
                'background': (0.95, 0.95, 0.95),
                'grid': (0.8, 0.8, 0.8),
                'axes': (0.2, 0.2, 0.2),
                'default': (0.3, 0.3, 0.3)
            },
            ColorScheme.TECHNICAL: {
                'background': (0.08, 0.12, 0.16),
                'grid': (0.25, 0.3, 0.35),
                'axes': (0.9, 0.9, 0.9),
                'default': (0.6, 0.7, 0.8)
            },
            ColorScheme.ARTISTIC: {
                'background': (0.15, 0.1, 0.2),
                'grid': (0.3, 0.25, 0.35),
                'axes': (0.9, 0.8, 0.9),
                'default': (0.8, 0.6, 0.9)
            }
        }
    
    def create_gradient_color(self, base_color: Tuple[float, float, float], 
                            gradient_type: GradientType, 
                            position: Tuple[float, float, float] = (0, 0, 0)) -> Quantity_Color:
        """Create gradient color based on type and position"""
        if not VISUALIZATION_AVAILABLE:
            return None
        
        r, g, b = base_color
        
        if gradient_type == GradientType.NONE:
            return Quantity_Color(r, g, b, Quantity_TOC_RGB)
        
        elif gradient_type == GradientType.LINEAR:
            # Linear gradient based on X position
            x, y, z = position
            factor = (x + 1.0) / 2.0  # Normalize to 0-1
            r = r * (0.5 + 0.5 * factor)
            g = g * (0.5 + 0.5 * factor)
            b = b * (0.5 + 0.5 * factor)
        
        elif gradient_type == GradientType.RADIAL:
            # Radial gradient from center
            x, y, z = position
            distance = math.sqrt(x*x + y*y)
            factor = min(1.0, distance / 2.0)
            r = r * (1.0 - 0.3 * factor)
            g = g * (1.0 - 0.3 * factor)
            b = b * (1.0 - 0.3 * factor)
        
        elif gradient_type == GradientType.CONICAL:
            # Conical gradient based on angle
            x, y, z = position
            angle = math.atan2(y, x)
            factor = (angle + math.pi) / (2 * math.pi)
            r = r * (0.7 + 0.3 * factor)
            g = g * (0.7 + 0.3 * factor)
            b = b * (0.7 + 0.3 * factor)
        
        elif gradient_type == GradientType.SPHERICAL:
            # Spherical gradient based on distance from origin
            x, y, z = position
            distance = math.sqrt(x*x + y*y + z*z)
            factor = min(1.0, distance / 2.0)
            r = r * (0.8 + 0.2 * factor)
            g = g * (0.8 + 0.2 * factor)
            b = b * (0.8 + 0.2 * factor)
        
        return Quantity_Color(r, g, b, Quantity_TOC_RGB)
    
    def create_line_aspect(self, color: Tuple[float, float, float], 
                          line_style: LineStyle, 
                          width: float = 1.0) -> Prs3d_LineAspect:
        """Create line aspect with specified style and color"""
        if not VISUALIZATION_AVAILABLE:
            return None
        
        occ_color = Quantity_Color(color[0], color[1], color[2], Quantity_TOC_RGB)
        aspect = Prs3d_LineAspect(occ_color, self.line_styles[line_style], width)
        return aspect
    
    def create_material_aspect(self, material_type: MaterialType, 
                             color: Tuple[float, float, float] = None,
                             transparency: float = 0.0) -> Graphic3d_MaterialAspect:
        """Create material aspect for 3D objects"""
        if not VISUALIZATION_AVAILABLE:
            return None
        
        material = Graphic3d_MaterialAspect(self.material_types[material_type])
        
        if color:
            occ_color = Quantity_Color(color[0], color[1], color[2], Quantity_TOC_RGB)
            material.SetColor(occ_color)
        
        if transparency > 0.0:
            material.SetTransparency(transparency)
        
        return material
    
    def create_ais_shape(self, shape, color: Tuple[float, float, float] = None,
                        material_type: MaterialType = MaterialType.METAL,
                        line_style: LineStyle = LineStyle.SOLID,
                        gradient_type: GradientType = GradientType.NONE,
                        transparency: float = 0.0) -> AIS_Shape:
        """Create AIS_Shape with specified visualization properties"""
        if not VISUALIZATION_AVAILABLE:
            return None
        
        ais_shape = AIS_Shape(shape)
        
        # Set color with gradient
        if color:
            # For gradient, we need to analyze the shape geometry
            if gradient_type != GradientType.NONE:
                # Create gradient based on shape bounds
                bounds = self.get_shape_bounds(shape)
                center = ((bounds[0] + bounds[1])/2, (bounds[2] + bounds[3])/2, (bounds[4] + bounds[5])/2)
                gradient_color = self.create_gradient_color(color, gradient_type, center)
                ais_shape.SetColor(gradient_color)
            else:
                occ_color = Quantity_Color(color[0], color[1], color[2], Quantity_TOC_RGB)
                ais_shape.SetColor(occ_color)
        
        # Set material
        material = self.create_material_aspect(material_type, color, transparency)
        if material:
            ais_shape.SetMaterial(material)
        
        # Set line style
        line_aspect = self.create_line_aspect(color or (0.8, 0.8, 0.8), line_style)
        if line_aspect:
            ais_shape.SetLineAspect(line_aspect)
        
        return ais_shape
    
    def get_shape_bounds(self, shape) -> Tuple[float, float, float, float, float, float]:
        """Get bounding box of shape (xmin, xmax, ymin, ymax, zmin, zmax)"""
        if not VISUALIZATION_AVAILABLE:
            return (0, 1, 0, 1, 0, 1)
        
        try:
            # Use BRepGProp to get bounding box
            props = GProp_GProps()
            brepgprop_VolumeProperties(shape, props)
            bounds = props.Bounds()
            return (bounds.XMin(), bounds.XMax(), 
                   bounds.YMin(), bounds.YMax(), 
                   bounds.ZMin(), bounds.ZMax())
        except:
            return (0, 1, 0, 1, 0, 1)
    
    def create_coordinate_system(self, size: float = 10.0, 
                               color_scheme: ColorScheme = ColorScheme.CLASSIC) -> List[AIS_Shape]:
        """Create coordinate system axes"""
        if not VISUALIZATION_AVAILABLE:
            return []
        
        colors = self.color_schemes[color_scheme]
        
        # Create axes
        axes = []
        
        # X-axis (Red)
        x_axis = self.create_line_aspect((1.0, 0.0, 0.0), LineStyle.SOLID, 2.0)
        # Y-axis (Green)
        y_axis = self.create_line_aspect((0.0, 1.0, 0.0), LineStyle.SOLID, 2.0)
        # Z-axis (Blue)
        z_axis = self.create_line_aspect((0.0, 0.0, 1.0), LineStyle.SOLID, 2.0)
        
        return axes
    
    def create_grid(self, size: float = 20.0, spacing: float = 1.0,
                   color_scheme: ColorScheme = ColorScheme.CLASSIC) -> List[AIS_Shape]:
        """Create grid for 3D visualization"""
        if not VISUALIZATION_AVAILABLE:
            return []
        
        colors = self.color_schemes[color_scheme]
        grid_color = colors['grid']
        
        grid_lines = []
        
        # Create grid lines
        for i in range(-int(size/spacing), int(size/spacing) + 1):
            x = i * spacing
            
            # Vertical lines (parallel to Y-axis)
            if x != 0:  # Skip center line
                line_aspect = self.create_line_aspect(grid_color, LineStyle.SOLID, 0.5)
                # Create line from (x, -size, 0) to (x, size, 0)
            
            # Horizontal lines (parallel to X-axis)
            y = i * spacing
            if y != 0:  # Skip center line
                line_aspect = self.create_line_aspect(grid_color, LineStyle.SOLID, 0.5)
                # Create line from (-size, y, 0) to (size, y, 0)
        
        return grid_lines
    
    def apply_visualization_style(self, ais_shape: AIS_Shape,
                                style_config: Dict[str, Any]) -> AIS_Shape:
        """Apply comprehensive visualization style to AIS_Shape"""
        if not VISUALIZATION_AVAILABLE or not ais_shape:
            return ais_shape
        
        # Apply color
        if 'color' in style_config:
            color = style_config['color']
            if 'gradient_type' in style_config:
                gradient_type = style_config['gradient_type']
                gradient_color = self.create_gradient_color(color, gradient_type)
                ais_shape.SetColor(gradient_color)
            else:
                occ_color = Quantity_Color(color[0], color[1], color[2], Quantity_TOC_RGB)
                ais_shape.SetColor(occ_color)
        
        # Apply material
        if 'material_type' in style_config:
            material_type = style_config['material_type']
            transparency = style_config.get('transparency', 0.0)
            material = self.create_material_aspect(material_type, 
                                                 style_config.get('color'), 
                                                 transparency)
            if material:
                ais_shape.SetMaterial(material)
        
        # Apply line style
        if 'line_style' in style_config:
            line_style = style_config['line_style']
            line_width = style_config.get('line_width', 1.0)
            color = style_config.get('color', (0.8, 0.8, 0.8))
            line_aspect = self.create_line_aspect(color, line_style, line_width)
            if line_aspect:
                ais_shape.SetLineAspect(line_aspect)
        
        return ais_shape

class VisualizationPresets:
    """Predefined visualization presets"""
    
    @staticmethod
    def get_metal_preset() -> Dict[str, Any]:
        return {
            'color': (0.8, 0.8, 0.9),
            'material_type': MaterialType.METAL,
            'line_style': LineStyle.SOLID,
            'gradient_type': GradientType.LINEAR,
            'transparency': 0.0,
            'line_width': 1.0
        }
    
    @staticmethod
    def get_glass_preset() -> Dict[str, Any]:
        return {
            'color': (0.9, 0.95, 1.0),
            'material_type': MaterialType.GLASS,
            'line_style': LineStyle.SOLID,
            'gradient_type': GradientType.SPHERICAL,
            'transparency': 0.3,
            'line_width': 0.5
        }
    
    @staticmethod
    def get_wood_preset() -> Dict[str, Any]:
        return {
            'color': (0.6, 0.4, 0.2),
            'material_type': MaterialType.WOOD,
            'line_style': LineStyle.SOLID,
            'gradient_type': GradientType.RADIAL,
            'transparency': 0.0,
            'line_width': 1.5
        }
    
    @staticmethod
    def get_plastic_preset() -> Dict[str, Any]:
        return {
            'color': (0.7, 0.7, 0.8),
            'material_type': MaterialType.PLASTIC,
            'line_style': LineStyle.SOLID,
            'gradient_type': GradientType.CONICAL,
            'transparency': 0.1,
            'line_width': 1.0
        }
    
    @staticmethod
    def get_technical_preset() -> Dict[str, Any]:
        return {
            'color': (0.6, 0.7, 0.8),
            'material_type': MaterialType.METAL,
            'line_style': LineStyle.DASHED,
            'gradient_type': GradientType.NONE,
            'transparency': 0.0,
            'line_width': 1.0
        }
    
    @staticmethod
    def get_artistic_preset() -> Dict[str, Any]:
        return {
            'color': (0.8, 0.6, 0.9),
            'material_type': MaterialType.PLASTIC,
            'line_style': LineStyle.DOTTED,
            'gradient_type': GradientType.RADIAL,
            'transparency': 0.2,
            'line_width': 0.8
        }
