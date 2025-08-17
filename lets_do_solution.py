#!/usr/bin/env python3
"""
Let's Do Solution - Quick access to TheSolution CAD solutions
Simple interface for working with solutions
"""

import sys
from pathlib import Path

# Add module paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "Base Solution" / "python"))
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "Root Solution" / "python"))

def show_solutions_menu():
    """Show solutions menu"""
    print("🏗️ LET'S DO SOLUTION - TheSolution CAD")
    print("=" * 50)
    print("Select a solution to work with:")
    print()
    print("🎯 3D-Solution (PRIORITY)")
    print("   1. Launch 3D-Solution")
    print("   2. Create 3D objects")
    print("   3. Work with geometry")
    print()
    print("📐 2D-Solution")
    print("   4. Launch 2D-Solution")
    print("   5. Create drawings")
    print()
    print("🔧 Assembly-Solution")
    print("   6. Launch Assembly-Solution")
    print("   7. Create assemblies")
    print()
    print("📊 Analysis-Solution")
    print("   8. Launch Analysis-Solution")
    print("   9. Analysis and calculations")
    print()
    print("🔄 Simulation-Solution")
    print("   10. Launch Simulation-Solution")
    print("   11. Simulation and testing")
    print()
    print("🏭 Manufacturing-Solution")
    print("   12. Launch Manufacturing-Solution")
    print("   13. Manufacturing and CAM")
    print()
    print("📄 Documentation-Solution")
    print("   14. Launch Documentation-Solution")
    print("   15. Documentation workflow")
    print()
    print("👥 Collaboration-Solution")
    print("   16. Launch Collaboration-Solution")
    print("   17. Collaborative work")
    print()
    print("🛠️ Tools")
    print("   18. Root Solution Launcher")
    print("   19. Capabilities demonstration")
    print("   20. System testing")
    print()
    print("❌ 0. Exit")
    print()

def launch_3d_solution():
    """Launch 3D-Solution"""
    print("🎯 Launching 3D-Solution...")
    try:
        import subprocess
        subprocess.run([sys.executable, "Root Solution/3D-Solution/main_3d.py"])
    except Exception as e:
        print(f"❌ Launch error: {e}")

def create_3d_objects():
    """Create 3D objects"""
    print("🔸 Creating 3D objects...")
    try:
        from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate, SolutionMaterial
        
        # Create a cube
        box = SolutionDataUtils.create_minimal_solution_data(
            name="My Cube",
            solution_type=SolutionType.BOX,
            coordinate=SolutionCoordinate(0, 0, 0)
        )
        box.dimensions.width = 10.0
        box.dimensions.height = 10.0
        box.dimensions.depth = 10.0
        box.properties.material = SolutionMaterial(name="Steel", density=7.85)
        
        # Create a sphere
        sphere = SolutionDataUtils.create_minimal_solution_data(
            name="My Sphere",
            solution_type=SolutionType.SPHERE,
            coordinate=SolutionCoordinate(15, 0, 0)
        )
        sphere.dimensions.radius = 5.0
        sphere.properties.material = SolutionMaterial(name="Aluminum", density=2.7)
        
        print(f"✅ Created {box.properties.name} - volume: {box.dimensions.get_volume_box():.2f} cubic units")
        print(f"✅ Created {sphere.properties.name} - volume: {sphere.dimensions.get_volume_sphere():.2f} cubic units")
        
    except Exception as e:
        print(f"❌ Object creation error: {e}")

def launch_root_launcher():
    """Launch Root Solution Launcher"""
    print("🏗️ Launching Root Solution Launcher...")
    try:
        import subprocess
        subprocess.run([sys.executable, "Root Solution/main.py"])
    except Exception as e:
        print(f"❌ Launch error: {e}")

def run_demo():
    """Run demonstration"""
    print("🎬 Running demonstration...")
    try:
        import subprocess
        subprocess.run([sys.executable, "demo_root_solution.py"])
    except Exception as e:
        print(f"❌ Launch error: {e}")

def run_tests():
    """Run tests"""
    print("🧪 Running tests...")
    try:
        import subprocess
        subprocess.run([sys.executable, "test_root_solution.py"])
    except Exception as e:
        print(f"❌ Launch error: {e}")

def show_solution_info():
    """Show information about solutions"""
    try:
        from root_solution_manager import get_root_manager
        
        manager = get_root_manager()
        solutions_info = manager.get_all_solutions_info()
        
        print("📋 Solutions information:")
        print("=" * 40)
        
        for name, info in solutions_info.items():
            status_icon = "✅" if info["status"] == "active" else "⏸️"
            print(f"{status_icon} {name}: {info['description']}")
        
        active_count = len([s for s in solutions_info.values() if s["status"] == "active"])
        print(f"\n📊 Active solutions: {active_count}/{len(solutions_info)}")
        
    except Exception as e:
        print(f"❌ Error getting information: {e}")

def main():
    """Main function"""
    while True:
        show_solutions_menu()
        
        try:
            choice = input("Enter your choice: ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                launch_3d_solution()
            elif choice == "2":
                create_3d_objects()
            elif choice == "18":
                launch_root_launcher()
            elif choice == "19":
                run_demo()
            elif choice == "20":
                run_tests()
            elif choice == "info":
                show_solution_info()
            else:
                print(f"⚠️ Function {choice} is not implemented yet")
                print("Available functions: 1, 2, 18, 19, 20")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
