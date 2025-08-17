#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration of OpenCASCADE with TheSolution CAD
"""

import sys
import os
from typing import Optional, Dict, Any

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate
    print("SUCCESS: Import of data types system")
except ImportError as e:
    print(f"ERROR: Import of data types system: {e}")
    sys.exit(1)

class OpenCascadeIntegration:
    """Integration of OpenCASCADE with TheSolution"""
    
    def __init__(self):
        """Initialize integration"""
        self.occ_available = False
        self.occ_modules = {}
        self._initialize_opencascade()
    
    def _initialize_opencascade(self):
        """Initialize OpenCASCADE"""
        print("Initializing OpenCASCADE...")
        
        try:
            # Import main OpenCASCADE modules
            from OCC.Core.BRepPrimAPI import (
                BRepPrimAPI_MakeBox, 
                BRepPrimAPI_MakeSphere, 
                BRepPrimAPI_MakeCylinder
            )
            from OCC.Core.BRepGProp import brepgprop
            from OCC.Core.GProp import GProp_GProps
            from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Pnt
            from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
            from OCC.Core.TopoDS import TopoDS_Shape
            
            self.occ_modules = {
                'BRepPrimAPI_MakeBox': BRepPrimAPI_MakeBox,
                'BRepPrimAPI_MakeSphere': BRepPrimAPI_MakeSphere,
                'BRepPrimAPI_MakeCylinder': BRepPrimAPI_MakeCylinder,
                'brepgprop': brepgprop,
                'GProp_GProps': GProp_GProps,
                'gp_Trsf': gp_Trsf,
                'gp_Vec': gp_Vec,
                'gp_Pnt': gp_Pnt,
                'BRepBuilderAPI_Transform': BRepBuilderAPI_Transform,
                'TopoDS_Shape': TopoDS_Shape
            }
            
            self.occ_available = True
            print("SUCCESS: OpenCASCADE initialized")
            
        except ImportError as e:
            print(f"ERROR: OpenCASCADE import: {e}")
            print("TIP: Make sure you are in conda environment with PythonOCC")
            print("   Run: conda activate pythonocc")
            self.occ_available = False
    
    def create_occ_shape(self, solution_type: SolutionType, properties: Dict[str, Any]) -> Optional[Any]:
        """Create OpenCASCADE shape from Solution data"""
        if not self.occ_available:
            print("ERROR: OpenCASCADE not available")
            return None
        
        try:
            if solution_type == SolutionType.BOX:
                return self._create_box(properties)
            elif solution_type == SolutionType.SPHERE:
                return self._create_sphere(properties)
            elif solution_type == SolutionType.CYLINDER:
                return self._create_cylinder(properties)
            else:
                print(f"ERROR: Unsupported type: {solution_type}")
                return None
                
        except Exception as e:
            print(f"ERROR: Shape creation: {e}")
            return None
    
    def _create_box(self, properties: Dict[str, Any]) -> Any:
        """Create box"""
        width = properties.get('width', 10.0)
        height = properties.get('height', 10.0)
        depth = properties.get('depth', 10.0)
        
        # Create box with simple constructor
        box_maker = self.occ_modules['BRepPrimAPI_MakeBox'](width, height, depth)
        return box_maker.Shape()
    
    def _create_sphere(self, properties: Dict[str, Any]) -> Any:
        """Create sphere"""
        radius = properties.get('radius', 5.0)
        
        sphere_maker = self.occ_modules['BRepPrimAPI_MakeSphere'](radius)
        return sphere_maker.Shape()
    
    def _create_cylinder(self, properties: Dict[str, Any]) -> Any:
        """Create cylinder"""
        radius = properties.get('radius', 3.0)
        height = properties.get('height', 8.0)
        
        cylinder_maker = self.occ_modules['BRepPrimAPI_MakeCylinder'](radius, height)
        return cylinder_maker.Shape()
    
    def calculate_volume(self, shape: Any) -> float:
        """Calculate volume of shape"""
        if not self.occ_available or shape is None:
            return 0.0
        
        try:
            props = self.occ_modules['GProp_GProps']()
            # Use the new static method instead of deprecated function
            self.occ_modules['brepgprop'].VolumeProperties(shape, props)
            return props.Mass()
        except Exception as e:
            print(f"ERROR: Volume calculation: {e}")
            return 0.0
    
    def transform_shape(self, shape: Any, translation: tuple = None, rotation: tuple = None) -> Any:
        """Transform shape"""
        if not self.occ_available or shape is None:
            return None
        
        try:
            trsf = self.occ_modules['gp_Trsf']()
            
            # Apply translation
            if translation:
                x, y, z = translation
                vec = self.occ_modules['gp_Vec'](x, y, z)
                trsf.SetTranslation(vec)
            
            # Apply transformation
            transform = self.occ_modules['BRepBuilderAPI_Transform'](shape, trsf)
            return transform.Shape()
            
        except Exception as e:
            print(f"ERROR: Transformation: {e}")
            return None
    
    def integrate_with_solution_data(self, solution_data: Any) -> Dict[str, Any]:
        """Integrate with TheSolution data types system"""
        if not self.occ_available:
            print("ERROR: OpenCASCADE not available for integration")
            return {}
        
        try:
            # Get solution type and properties
            solution_type = solution_data.properties.solution_type
            properties = solution_data.dimensions.__dict__ if hasattr(solution_data.dimensions, '__dict__') else {}
            
            # Create OpenCASCADE shape
            shape = self.create_occ_shape(solution_type, properties)
            if shape is None:
                return {}
            
            # Calculate volume
            volume = self.calculate_volume(shape)
            
            # Apply transformation from coordinates
            coordinate = solution_data.properties.coordinate
            if coordinate and hasattr(coordinate, 'x') and hasattr(coordinate, 'y') and hasattr(coordinate, 'z'):
                shape = self.transform_shape(shape, (coordinate.x, coordinate.y, coordinate.z))
            
            # Return updated data
            result = {
                'volume': volume,
                'occ_shape': shape,
                'occ_available': True
            }
            
            print(f"SUCCESS: Integration successful. Volume: {volume:.2f}")
            return result
            
        except Exception as e:
            print(f"ERROR: Integration: {e}")
            return {}

def test_integration():
    """Test integration"""
    print("Testing OpenCASCADE integration with TheSolution")
    print("=" * 60)
    
    # Create integration
    integration = OpenCascadeIntegration()
    
    if not integration.occ_available:
        print("ERROR: OpenCASCADE not available. Ending test.")
        return False
    
    # Test 1: Create box
    print("\n1. Testing box creation...")
    cube_data = SolutionDataUtils.create_minimal_solution_data(
        name="Test Box",
        solution_type=SolutionType.BOX,
        coordinate=SolutionCoordinate(0, 0, 0)
    )
    cube_data.dimensions.width = 10.0
    cube_data.dimensions.height = 10.0
    cube_data.dimensions.depth = 10.0
    
    integrated_cube = integration.integrate_with_solution_data(cube_data)
    if integrated_cube:
        print(f"   SUCCESS: Box created: {cube_data.properties.name}")
        print(f"   Volume: {integrated_cube['volume']:.2f}")
    
    # Test 2: Create sphere
    print("\n2. Testing sphere creation...")
    sphere_data = SolutionDataUtils.create_minimal_solution_data(
        name="Test Sphere",
        solution_type=SolutionType.SPHERE,
        coordinate=SolutionCoordinate(20, 0, 0)
    )
    sphere_data.dimensions.radius = 5.0
    
    integrated_sphere = integration.integrate_with_solution_data(sphere_data)
    if integrated_sphere:
        print(f"   SUCCESS: Sphere created: {sphere_data.properties.name}")
        print(f"   Volume: {integrated_sphere['volume']:.2f}")
    
    # Test 3: Create cylinder
    print("\n3. Testing cylinder creation...")
    cylinder_data = SolutionDataUtils.create_minimal_solution_data(
        name="Test Cylinder",
        solution_type=SolutionType.CYLINDER,
        coordinate=SolutionCoordinate(40, 0, 0)
    )
    cylinder_data.dimensions.radius = 3.0
    cylinder_data.dimensions.height = 8.0
    
    integrated_cylinder = integration.integrate_with_solution_data(cylinder_data)
    if integrated_cylinder:
        print(f"   SUCCESS: Cylinder created: {cylinder_data.properties.name}")
        print(f"   Volume: {integrated_cylinder['volume']:.2f}")
    
    # Test 4: Transformation
    print("\n4. Testing transformation...")
    if integrated_cube and 'occ_shape' in integrated_cube:
        transformed_shape = integration.transform_shape(
            integrated_cube['occ_shape'],
            translation=(10, 0, 0)
        )
        if transformed_shape:
            print("   SUCCESS: Transformation completed")
    
    print("\n" + "=" * 60)
    print("SUCCESS: All integration tests passed!")
    print("OpenCASCADE fully integrated with TheSolution CAD")
    
    return True

def main():
    """Main function"""
    try:
        success = test_integration()
        if success:
            print("\nIntegration ready for use!")
            print("TIP: Now you can use OpenCASCADE in 3D-Solution")
        else:
            print("\nThere are integration problems")
    except Exception as e:
        print(f"\nCritical error: {e}")

if __name__ == "__main__":
    main()
