#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug OpenCASCADE functionality
"""

def test_occ_basic():
    """Basic OpenCASCADE test"""
    print("Testing OpenCASCADE basic functionality...")
    
    try:
        from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
        from OCC.Core.BRepGProp import brepgprop
        from OCC.Core.GProp import GProp_GProps
        
        print("SUCCESS: Imports successful")
        
        # Test box creation - simple approach
        print("\nTesting box creation...")
        try:
            box_maker = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0)
            box = box_maker.Shape()
            print("SUCCESS: Box created")
            
            # Calculate volume
            props = GProp_GProps()
            brepgprop.VolumeProperties(box, props)
            volume = props.Mass()
            print(f"Box volume: {volume}")
        except Exception as e:
            print(f"ERROR: Box creation failed: {e}")
        
        # Test sphere creation
        print("\nTesting sphere creation...")
        try:
            sphere_maker = BRepPrimAPI_MakeSphere(5.0)
            sphere = sphere_maker.Shape()
            print("SUCCESS: Sphere created")
            
            # Calculate volume
            props = GProp_GProps()
            brepgprop.VolumeProperties(sphere, props)
            volume = props.Mass()
            print(f"Sphere volume: {volume}")
        except Exception as e:
            print(f"ERROR: Sphere creation failed: {e}")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_occ_basic()
