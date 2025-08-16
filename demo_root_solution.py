#!/usr/bin/env python3
"""
Демонстрация Root Solution инфраструктуры TheSolution CAD
Показывает возможности менеджера решений и 3D-Solution
"""

import sys
from pathlib import Path

# Добавляем пути к модулям
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "Base Solution" / "python"))
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "Root Solution" / "python"))

def demo_root_solution_manager():
    """Демонстрация Root Solution Manager"""
    print("🎯 ДЕМОНСТРАЦИЯ ROOT SOLUTION MANAGER")
    print("=" * 50)
    
    try:
        from root_solution_manager import get_root_manager, SolutionStatus
        
        manager = get_root_manager()
        
        # Показываем все решения
        print("📋 Все решения TheSolution CAD:")
        solutions_info = manager.get_all_solutions_info()
        for name, info in solutions_info.items():
            status_icon = "✅" if info["status"] == "active" else "⏸️"
            print(f"   {status_icon} {name}: {info['description']}")
        
        # Активируем несколько решений
        print("\n🔄 Активация решений:")
        manager.activate_solution("2D-Solution")
        manager.activate_solution("Assembly-Solution")
        
        # Показываем активные решения
        active_solutions = manager.get_active_solutions()
        print(f"✅ Активных решений: {len(active_solutions)}")
        for solution in active_solutions:
            print(f"   - {solution.name}: {solution.description}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка демонстрации менеджера: {e}")
        return False

def demo_solution_data_types():
    """Демонстрация системы типов данных"""
    print("\n🎯 ДЕМОНСТРАЦИЯ СИСТЕМЫ ТИПОВ ДАННЫХ")
    print("=" * 50)
    
    try:
        from solution_data_types import (
            SolutionType, SolutionDataUtils, SolutionData,
            SolutionCoordinate, SolutionDimensions, SolutionMaterial
        )
        
        # Создаем различные типы объектов
        objects = []
        
        # Куб
        box_data = SolutionDataUtils.create_minimal_solution_data(
            name="Демо Куб",
            solution_type=SolutionType.BOX,
            coordinate=SolutionCoordinate(0, 0, 0)
        )
        box_data.dimensions.width = 10.0
        box_data.dimensions.height = 10.0
        box_data.dimensions.depth = 10.0
        box_data.properties.material = SolutionMaterial(
            name="Steel",
            density=7.85,
            color_rgb=(192, 192, 192)
        )
        objects.append(box_data)
        
        # Сфера
        sphere_data = SolutionDataUtils.create_minimal_solution_data(
            name="Демо Сфера",
            solution_type=SolutionType.SPHERE,
            coordinate=SolutionCoordinate(15, 0, 0)
        )
        sphere_data.dimensions.radius = 5.0
        sphere_data.properties.material = SolutionMaterial(
            name="Aluminum",
            density=2.7,
            color_rgb=(169, 169, 169)
        )
        objects.append(sphere_data)
        
        # Цилиндр
        cylinder_data = SolutionDataUtils.create_minimal_solution_data(
            name="Демо Цилиндр",
            solution_type=SolutionType.CYLINDER,
            coordinate=SolutionCoordinate(0, 15, 0)
        )
        cylinder_data.dimensions.radius = 3.0
        cylinder_data.dimensions.height = 8.0
        cylinder_data.properties.material = SolutionMaterial(
            name="Copper",
            density=8.96,
            color_rgb=(184, 115, 51)
        )
        objects.append(cylinder_data)
        
        # Показываем информацию об объектах
        print("📊 Созданные объекты:")
        for obj in objects:
            coord = obj.properties.coordinate
            material = obj.properties.material
            
            print(f"\n🔸 {obj.properties.name}:")
            print(f"   Тип: {obj.properties.solution_type.value}")
            print(f"   Позиция: ({coord.x}, {coord.y}, {coord.z})")
            print(f"   Материал: {material.name} (плотность: {material.density})")
            
            # Расчет объема
            if obj.properties.solution_type == SolutionType.BOX:
                volume = obj.dimensions.get_volume_box()
                print(f"   Объем: {volume:.2f} куб.ед.")
            elif obj.properties.solution_type == SolutionType.SPHERE:
                volume = obj.dimensions.get_volume_sphere()
                print(f"   Объем: {volume:.2f} куб.ед.")
            elif obj.properties.solution_type == SolutionType.CYLINDER:
                volume = obj.dimensions.get_volume_cylinder()
                print(f"   Объем: {volume:.2f} куб.ед.")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка демонстрации типов данных: {e}")
        return False

def demo_3d_solution_integration():
    """Демонстрация интеграции 3D-Solution"""
    print("\n🎯 ДЕМОНСТРАЦИЯ ИНТЕГРАЦИИ 3D-SOLUTION")
    print("=" * 50)
    
    try:
        # Проверяем наличие 3D-Solution
        main_3d_path = project_root / "Root Solution" / "3D-Solution" / "main_3d.py"
        if main_3d_path.exists():
            print("✅ 3D-Solution найден")
            
            # Показываем информацию о файле
            import os
            file_size = os.path.getsize(main_3d_path)
            print(f"   Размер файла: {file_size} байт")
            
            # Проверяем импорт (без запуска GUI)
            import importlib.util
            spec = importlib.util.spec_from_file_location("main_3d", main_3d_path)
            main_3d_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_3d_module)
            
            print("✅ Модуль 3D-Solution загружен")
            print("   Доступные функции:")
            print("   - launch_3d_solution() - запуск 3D-Solution")
            print("   - Solution3DMainWindow - главное окно")
            
            return True
        else:
            print("❌ 3D-Solution не найден")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка демонстрации 3D-Solution: {e}")
        return False

def demo_hierarchy():
    """Демонстрация иерархии решений"""
    print("\n🎯 ДЕМОНСТРАЦИЯ ИЕРАРХИИ РЕШЕНИЙ")
    print("=" * 50)
    
    try:
        from root_solution_manager import get_root_manager
        
        manager = get_root_manager()
        hierarchy = manager.create_solution_hierarchy()
        
        print(f"🏗️ Корень иерархии: {hierarchy['root']}")
        print(f"📊 Количество решений: {len(hierarchy['solutions'])}")
        
        print("\n📁 Детали иерархии:")
        for name, data in hierarchy['solutions'].items():
            info = data['info']
            sub_count = len(data['sub_solutions'])
            status_icon = "✅" if info['status'] == 'active' else "⏸️"
            
            print(f"   {status_icon} {name}:")
            print(f"      Описание: {info['description']}")
            print(f"      Тип: {info['type']}")
            print(f"      Под-решения: {sub_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка демонстрации иерархии: {e}")
        return False

def main():
    """Главная функция демонстрации"""
    print("🏗️ ДЕМОНСТРАЦИЯ ROOT SOLUTION ИНФРАСТРУКТУРЫ")
    print("TheSolution CAD - Платформа CAD решений")
    print("=" * 70)
    
    demos = [
        ("Root Solution Manager", demo_root_solution_manager),
        ("Система типов данных", demo_solution_data_types),
        ("Интеграция 3D-Solution", demo_3d_solution_integration),
        ("Иерархия решений", demo_hierarchy)
    ]
    
    results = []
    
    for demo_name, demo_func in demos:
        try:
            result = demo_func()
            results.append((demo_name, result))
        except Exception as e:
            print(f"❌ Критическая ошибка в демонстрации {demo_name}: {e}")
            results.append((demo_name, False))
    
    # Итоговый отчет
    print("\n" + "=" * 70)
    print("📊 ИТОГОВЫЙ ОТЧЕТ ДЕМОНСТРАЦИИ")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for demo_name, result in results:
        status = "✅ УСПЕШНО" if result else "❌ ОШИБКА"
        print(f"{status} {demo_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Результат: {passed}/{total} демонстраций успешно")
    
    if passed == total:
        print("🎉 Все демонстрации прошли успешно!")
        print("Root Solution инфраструктура полностью функциональна.")
    else:
        print("⚠️ Некоторые демонстрации не прошли.")
        print("Проверьте настройки и зависимости.")
    
    print("\n🚀 Следующие шаги:")
    print("1. Запустите Root Solution Launcher: python 'Root Solution/main.py'")
    print("2. Запустите 3D-Solution: python 'Root Solution/3D-Solution/main_3d.py'")
    print("3. Запустите тесты: python test_root_solution.py")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
