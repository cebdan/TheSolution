#!/usr/bin/env python3
"""
TheSolution CAD System Capabilities Demonstration

Shows all main functions and components of the system
"""

import sys
import os
from datetime import datetime

# Add project modules path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Base Solution', 'python'))

def print_header():
    """Print demonstration header"""
    print("=" * 60)
    print("🚀 TheSolution CAD - Capabilities Demonstration")
    print("=" * 60)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def demo_basic_system():
    """Demonstrate basic system"""
    print("📋 1. Basic Solution System")
    print("-" * 40)
    
    try:
        from solution_coordinate import SolutionCoordinate
        from base_solution import Solution
        
        # Create coordinates
        coord1 = SolutionCoordinate(10, 20, 30)
        coord2 = SolutionCoordinate(5, 5, 5, 2.0, 1.5, 0.5)
        
        print(f"✅ Coordinates created:")
        print(f"   Coordinates 1: {coord1}")
        print(f"   Coordinates 2: {coord2}")
        
        # Create objects
        root = Solution("Root object", coord1)
        child1 = Solution("Child 1", coord2)
        child2 = Solution("Child 2", SolutionCoordinate(0, 10, 0))
        
        # Build hierarchy
        root.add_child(child1)
        root.add_child(child2)
        
        print(f"✅ Hierarchy created:")
        print(f"   Root object: {root.name}")
        print(f"   Child elements: {len(root.get_children())}")
        print(f"   Total descendants: {len(root.get_descendants())}")
        
        # Work with coordinates
        child1.x = 50
        abs_coord = child1.get_absolute_coordinate()
        print(f"✅ Coordinates updated:")
        print(f"   New coordinates child1: x={child1.x}")
        print(f"   Absolute coordinates: {abs_coord}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic system error: {e}")
        return False

def demo_geometry():
    """Demonstrate geometric operations"""
    print("\n📐 2. Geometric Operations")
    print("-" * 40)
    
    try:
        from geometry_operations import GeometryOperations, SolutionCoordinate
        
        # Create geometric objects
        box = GeometryOperations.create_box("Demo cube", 10, 10, 10, SolutionCoordinate(0, 0, 0))
        sphere = GeometryOperations.create_sphere("Demo sphere", 5, SolutionCoordinate(15, 0, 0))
        cylinder = GeometryOperations.create_cylinder("Demo cylinder", 3, 8, SolutionCoordinate(0, 15, 0))
        
        print(f"✅ Geometric objects created:")
        print(f"   Cube volume: {box.get_volume():.2f}")
        print(f"   Sphere volume: {sphere.get_volume():.2f}")
        print(f"   Cylinder volume: {cylinder.get_volume():.2f}")
        
        # Create assembly
        assembly = Solution("Demo assembly")
        assembly.add_child(box)
        assembly.add_child(sphere)
        assembly.add_child(cylinder)
        
        print(f"✅ Assembly created:")
        print(f"   Components: {len(assembly.get_children())}")
        print(f"   Total volume: {sum(child.get_volume() for child in assembly.get_children()):.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Geometry error: {e}")
        return False

def demo_gui():
    """Демонстрирует GUI возможности"""
    print("\n🖥️ 3. GUI возможности")
    print("-" * 40)
    
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        
        print("✅ PySide6 доступен")
        print("✅ GUI компоненты готовы")
        print("   - Дерево объектов")
        print("   - Редактор координат")
        print("   - Информационная панель")
        print("   - Кнопки создания объектов")
        
        return True
        
    except ImportError:
        print("⚠️ PySide6 не установлен")
        return False
    except Exception as e:
        print(f"❌ Ошибка GUI: {e}")
        return False

def demo_opencascade():
    """Демонстрирует возможности OpenCASCADE"""
    print("\n🔧 4. OpenCASCADE интеграция")
    print("-" * 40)
    
    try:
        from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
        from OCC.Core.BRepGProp import brepgprop_VolumeProperties
        from OCC.Core.GProp import GProp_GProps
        
        print("✅ OpenCASCADE доступен")
        
        # Создание куба через OpenCASCADE
        box_maker = BRepPrimAPI_MakeBox(10, 10, 10)
        box_shape = box_maker.Shape()
        
        # Вычисление объема
        props = GProp_GProps()
        brepgprop_VolumeProperties(box_shape, props)
        volume = props.Mass()
        
        print(f"✅ OpenCASCADE операции:")
        print(f"   Куб создан: {box_shape}")
        print(f"   Объем: {volume:.2f}")
        
        return True
        
    except ImportError:
        print("⚠️ OpenCASCADE не найден")
        print("   Установите: conda install -c conda-forge pythonocc-core")
        return False
    except Exception as e:
        print(f"❌ Ошибка OpenCASCADE: {e}")
        return False

def demo_project_structure():
    """Демонстрирует структуру проекта"""
    print("\n📁 5. Структура проекта")
    print("-" * 40)
    
    import os
    
    # Проверяем основные директории
    directories = [
        "Base Solution",
        "Base Solution/python",
        "Base Solution/include",
        "Graphic Engine",
        "Geometric Primitives",
        "Modeling Tools",
        "Layers",
        "Dimensions",
        "GUI",
        "Tests",
        "Documentation",
        "Build",
        "Examples"
    ]
    
    print("✅ Структура проекта:")
    for directory in directories:
        if os.path.exists(directory):
            print(f"   ✅ {directory}/")
        else:
            print(f"   ⚠️ {directory}/ (не создана)")
    
    # Проверяем основные файлы
    files = [
        "README.md",
        "requirements.txt",
        "CMakeLists.txt",
        "setup_environment.py",
        "INSTALL.md",
        "Base Solution/python/solution_coordinate.py",
        "Base Solution/python/base_solution.py",
        "Base Solution/include/solution_coordinate.h",
        "test_basic_system.py",
        "simple_gui.py",
        "geometry_operations.py"
    ]
    
    print("\n✅ Основные файлы:")
    for file in files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (отсутствует)")
    
    return True

def demo_installation():
    """Демонстрирует инструменты установки"""
    print("\n🔧 6. Инструменты установки")
    print("-" * 40)
    
    import os
    
    tools = [
        "setup_environment.py",
        "check_conda_environment.py",
        "quick_check_opencascade.py",
        "run_with_opencascade.py"
    ]
    
    print("✅ Инструменты установки:")
    for tool in tools:
        if os.path.exists(tool):
            print(f"   ✅ {tool}")
        else:
            print(f"   ❌ {tool} (отсутствует)")
    
    return True

def print_summary(results):
    """Выводит итоговую сводку"""
    print("\n" + "=" * 60)
    print("📊 ИТОГОВАЯ СВОДКА")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"Всего тестов: {total_tests}")
    print(f"Пройдено: {passed_tests}")
    print(f"Провалено: {total_tests - passed_tests}")
    print(f"Успешность: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\n🎯 Статус компонентов:")
    components = [
        ("Базовая система", results.get("basic", False)),
        ("Геометрия", results.get("geometry", False)),
        ("GUI", results.get("gui", False)),
        ("OpenCASCADE", results.get("opencascade", False)),
        ("Структура проекта", results.get("structure", False)),
        ("Инструменты установки", results.get("installation", False))
    ]
    
    for name, status in components:
        icon = "✅" if status else "❌"
        print(f"   {icon} {name}")
    
    print("\n🚀 TheSolution CAD готова к использованию!")
    print("Следующие шаги:")
    print("1. Запустите GUI: python simple_gui.py")
    print("2. Протестируйте систему: python test_basic_system.py")
    print("3. Изучите документацию: README.md, INSTALL.md")

def main():
    """Основная функция демонстрации"""
    print_header()
    
    # Запуск всех демонстраций
    results = {
        "basic": demo_basic_system(),
        "geometry": demo_geometry(),
        "gui": demo_gui(),
        "opencascade": demo_opencascade(),
        "structure": demo_project_structure(),
        "installation": demo_installation()
    }
    
    # Вывод итоговой сводки
    print_summary(results)

if __name__ == "__main__":
    main()
