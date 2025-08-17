#!/usr/bin/env python3
"""
Simple OpenCASCADE Test
"""

def test_occ():
    """Test OpenCASCADE"""
    print("Testing OpenCASCADE...")
    
    try:
        from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
        print("SUCCESS: BRepPrimAPI imported")
        
        # Create a box
        box_maker = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0)
        box = box_maker.Shape()
        print("SUCCESS: Box created")
        
        return True
        
    except ImportError as e:
        print(f"ERROR: Import failed - {e}")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_occ()
