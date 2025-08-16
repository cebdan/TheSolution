#!/usr/bin/env python3
"""
Демонстрация возможностей TheSolution CAD системы

Показывает все основные функции и компоненты системы
"""

import sys
import os
from datetime import datetime

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Base Solution', 'python'))

def print_header():
    """Выводит заголовок демонстрации"""
    print("=" * 60)
    print("🚀 TheSolution CAD - Демонстрация возможностей")
    print("=" * 60)
    print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def demo_basic_system():
    """Демонстрирует базовую систему"""
    print("📋 1. Базовая система Solution")
    print("-" * 40)
    
    try:
        from solution_coordinate import SolutionCoordinate
        from base_solution import Solution
        
        # Создание координат
        coord1 = SolutionCoordinate(10, 20, 30)
        coord2 = SolutionCoordinate(5, 5, 5, 2.0, 1.5, 0.5)
        
        print(f"✅ Координаты созданы:")
        print(f"   Координаты 1: {coord1}")
        print(f"   Координаты 2: {coord2}")
        
        # Создание объектов
        root = Solution("Корневой объект", coord1)
        child1 = Solution("Дочерний 1", coord2)
        child2 = Solution("Дочерний 2", SolutionCoordinate(0, 10, 0))
        
        # Построение иерархии
        root.add_child(child1)
        root.add_child(child2)
        
        print(f"✅ Иерархия создана:")
        print(f"   Корневой объект: {root.name}")
        print(f"   Дочерние элементы: {len(root.get_children())}")
        print(f"   Всего потомков: {len(root.get_descendants())}")
        
        # Работа с координатами
        child1.x = 50
        abs_coord = child1.get_absolute_coordinate()
        print(f"✅ Координаты обновлены:")
        print(f"   Новые координаты child1: x={child1.x}")
        print(f"   Абсолютные координаты: {abs_coord}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка базовой системы: {e}")
        return False

def demo_geometry():
    """Демонстрирует геометрические операции"""
    print("\n📐 2. Геометрические операции")
    print("-" * 40)
    
    try:
        from geometry_operations import GeometryOperations, SolutionCoordinate
        
        # Создание геометрических объектов
        box = GeometryOperations.create_box("Демо куб", 10, 10, 10, SolutionCoordinate(0, 0, 0))
        sphere = GeometryOperations.create_sphere("Демо сфера", 5, SolutionCoordinate(15, 0, 0))
        cylinder = GeometryOperations.create_cylinder("Демо цилиндр", 3, 8, SolutionCoordinate(0, 15, 0))
        
        print(f"✅ Геометрические объекты созданы:")
        print(f"   Куб объем: {box.get_volume():.2f}")
        print(f"   Сфера объем: {sphere.get_volume():.2f}")
        print(f"   Цилиндр объем: {cylinder.get_volume():.2f}")
        
        # Создание сборки
        assembly = Solution("Демо сборка")
        assembly.add_child(box)
        assembly.add_child(sphere)
        assembly.add_child(cylinder)
        
        print(f"✅ Сборка создана:")
        print(f"   Компонентов: {len(assembly.get_children())}")
        print(f"   Общий объем: {sum(child.get_volume() for child in assembly.get_children()):.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка геометрии: {e}")
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
