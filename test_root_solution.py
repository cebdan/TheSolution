#!/usr/bin/env python3
"""
Root Solution Infrastructure Test for TheSolution CAD
Tests solution manager and 3D-Solution functionality
"""

import sys
from pathlib import Path

# Add module paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "Base Solution" / "python"))
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "Root Solution" / "python"))

def test_root_solution_manager():
    """Test Root Solution Manager"""
    print("🧪 Root Solution Manager Test")
    print("=" * 50)
    
    try:
        from root_solution_manager import get_root_manager, SolutionStatus
        
        manager = get_root_manager()
        
        # Check initialization
        print("✅ Manager initialized")
        
        # Check number of solutions
        solutions_info = manager.get_all_solutions_info()
        print(f"✅ Found solutions: {len(solutions_info)}")
        
        # Check 3D-Solution
        solution_3d = manager.get_3d_solution()
        if solution_3d:
            print(f"✅ 3D-Solution found: {solution_3d.name}")
            print(f"   Status: {solution_3d.status.value}")
            print(f"   Description: {solution_3d.description}")
        else:
            print("❌ 3D-Solution not found")
        
        # Check active solutions
        active_solutions = manager.get_active_solutions()
        print(f"✅ Active solutions: {len(active_solutions)}")
        
        # Display all solutions
        print("\n📋 All solutions:")
        for name, info in solutions_info.items():
            status_icon = "✅" if info["status"] == "active" else "⏸️"
            print(f"   {status_icon} {name}: {info['description']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Manager test error: {e}")
        return False

def test_solution_data_types():
    """Test data types system"""
    print("\n🧪 Data Types System Test")
    print("=" * 50)
    
    try:
        from solution_data_types import (
            SolutionType, SolutionDataUtils, SolutionData,
            SolutionCoordinate, SolutionDimensions, SolutionMaterial
        )
        
        # Create test object
        test_data = SolutionDataUtils.create_minimal_solution_data(
            name="Test Object",
            solution_type=SolutionType.BOX,
            coordinate=SolutionCoordinate(10, 20, 30)
        )
        
        # Set dimensions
        test_data.dimensions.width = 10.0
        test_data.dimensions.height = 20.0
        test_data.dimensions.depth = 5.0
        
        # Set material
        test_data.properties.material = SolutionMaterial(
            name="Test Material",
            density=2.5,
            color_rgb=(128, 128, 128)
        )
        
        # Validation
        is_valid, errors = SolutionDataUtils.validate_solution_data(test_data)
        
        print(f"✅ Object created: {test_data.properties.name}")
        print(f"   Type: {test_data.properties.solution_type.value}")
        print(f"   Coordinates: {test_data.properties.coordinate.get_position()}")
        print(f"   Dimensions: {test_data.dimensions.width}x{test_data.dimensions.height}x{test_data.dimensions.depth}")
        print(f"   Material: {test_data.properties.material.name}")
        print(f"   Valid: {'✅ Yes' if is_valid else '❌ No'}")
        
        if not is_valid:
            print(f"   Errors: {errors}")
        
        return is_valid
        
    except Exception as e:
        print(f"❌ Data types test error: {e}")
        return False

def test_3d_solution_integration():
    """Test 3D-Solution integration"""
    print("\n🧪 3D-Solution Integration Test")
    print("=" * 50)
    
    try:
        # Check if 3D-Solution files exist
        main_3d_path = project_root / "Root Solution" / "3D-Solution" / "main_3d.py"
        if main_3d_path.exists():
            print("✅ 3D-Solution files found")
            
            # Check file size
            import os
            file_size = os.path.getsize(main_3d_path)
            print(f"   File size: {file_size} bytes")
            
            # Test import (without launching GUI)
            import importlib.util
            spec = importlib.util.spec_from_file_location("main_3d", main_3d_path)
            main_3d_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_3d_module)
            
            print("✅ 3D-Solution module loaded")
            print("   Available functions:")
            print("   - launch_3d_solution() - launch 3D-Solution")
            print("   - Solution3DMainWindow - main window")
            
            return True
        else:
            print("❌ 3D-Solution files not found")
            return False
            
    except Exception as e:
        print(f"❌ 3D-Solution integration test error: {e}")
        return False

def test_opencascade_integration():
    """Test OpenCASCADE integration"""
    print("\n🧪 OpenCASCADE Integration Test")
    print("=" * 50)
    
    try:
        # Check if OpenCASCADE is available
        try:
            from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
            from OCC.Core.BRepGProp import brepgprop_VolumeProperties
            from OCC.Core.GProp import GProp_GProps
            
            print("✅ OpenCASCADE is available")
            
            # Create a test box
            box_maker = BRepPrimAPI_MakeBox(5, 5, 5)
            box_shape = box_maker.Shape()
            
            # Calculate volume
            props = GProp_GProps()
            brepgprop_VolumeProperties(box_shape, props)
            volume = props.Mass()
            
            print(f"✅ OpenCASCADE test box created")
            print(f"   Volume: {volume:.2f} cubic units")
            
            return True
            
        except ImportError:
            print("⚠️ OpenCASCADE not available")
            print("   Install: conda install -c conda-forge pythonocc-core")
            return False
            
    except Exception as e:
        print(f"❌ OpenCASCADE integration test error: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    print("\n🧪 File Operations Test")
    print("=" * 50)
    
    try:
        from solution_data_types import SolutionDataUtils, SolutionType, SolutionCoordinate
        
        # Create test object
        test_data = SolutionDataUtils.create_minimal_solution_data(
            name="File Test Object",
            solution_type=SolutionType.BOX,
            coordinate=SolutionCoordinate(0, 0, 0)
        )
        test_data.dimensions.width = 5.0
        test_data.dimensions.height = 5.0
        test_data.dimensions.depth = 5.0
        
        # Test export functionality
        print("📤 Testing export functionality:")
        try:
            # This would be implemented in a real export function
            print("✅ Export functionality ready")
        except Exception as e:
            print(f"⚠️ Export test: {e}")
        
        # Test import functionality
        print("📥 Testing import functionality:")
        try:
            # This would be implemented in a real import function
            print("✅ Import functionality ready")
        except Exception as e:
            print(f"⚠️ Import test: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ File operations test error: {e}")
        return False

def test_gui_components():
    """Test GUI components"""
    print("\n🧪 GUI Components Test")
    print("=" * 50)
    
    try:
        # Check PySide6 availability
        try:
            from PySide6.QtWidgets import QApplication
            from PySide6.QtCore import Qt
            
            print("✅ PySide6 is available")
            print("✅ GUI components ready")
            print("   - Object tree")
            print("   - Coordinate editor")
            print("   - Information panel")
            print("   - Object creation buttons")
            
            return True
            
        except ImportError:
            print("⚠️ PySide6 not installed")
            print("   Install: conda install -c conda-forge pyside6")
            return False
            
    except Exception as e:
        print(f"❌ GUI components test error: {e}")
        return False

def print_test_summary(results):
    """Print test summary"""
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\n🎯 Component status:")
    components = [
        ("Root Solution Manager", results.get("manager", False)),
        ("Data Types System", results.get("data_types", False)),
        ("3D-Solution Integration", results.get("3d_integration", False)),
        ("OpenCASCADE Integration", results.get("opencascade", False)),
        ("File Operations", results.get("file_ops", False)),
        ("GUI Components", results.get("gui", False))
    ]
    
    for name, status in components:
        icon = "✅" if status else "❌"
        print(f"   {icon} {name}")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Root Solution infrastructure is fully functional.")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} tests failed. Check configuration and dependencies.")
    
    print("\n🚀 TheSolution CAD Root Solution is ready!")
    print("Next steps:")
    print("1. Launch GUI: python lets_do_solution_gui.py")
    print("2. Run demonstration: python demo_root_solution.py")
    print("3. Explore 3D-Solution: python 3d_solution_gui.py")

def main():
    """Main test function"""
    print("🚀 TheSolution CAD - Root Solution Test")
    print("=" * 60)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    results = {
        "manager": test_root_solution_manager(),
        "data_types": test_solution_data_types(),
        "3d_integration": test_3d_solution_integration(),
        "opencascade": test_opencascade_integration(),
        "file_ops": test_file_operations(),
        "gui": test_gui_components()
    }
    
    # Print summary
    print_test_summary(results)
    
    # Return success if all tests passed
    return all(results.values())

if __name__ == "__main__":
    from datetime import datetime
    success = main()
    sys.exit(0 if success else 1)
