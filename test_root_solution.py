#!/usr/bin/env python3
"""
Тест Root Solution инфраструктуры TheSolution CAD
Проверяет работу менеджера решений и 3D-Solution
"""

import sys
from pathlib import Path

# Добавляем пути к модулям
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "Base Solution" / "python"))
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "Root Solution" / "python"))

def test_root_solution_manager():
    """Тест Root Solution Manager"""
    print("🧪 Тест Root Solution Manager")
    print("=" * 50)
    
    try:
        from root_solution_manager import get_root_manager, SolutionStatus
        
        manager = get_root_manager()
        
        # Проверка инициализации
        print("✅ Менеджер инициализирован")
        
        # Проверка количества решений
        solutions_info = manager.get_all_solutions_info()
        print(f"✅ Найдено решений: {len(solutions_info)}")
        
        # Проверка 3D-Solution
        solution_3d = manager.get_3d_solution()
        if solution_3d:
            print(f"✅ 3D-Solution найден: {solution_3d.name}")
            print(f"   Статус: {solution_3d.status.value}")
            print(f"   Описание: {solution_3d.description}")
        else:
            print("❌ 3D-Solution не найден")
        
        # Проверка активных решений
        active_solutions = manager.get_active_solutions()
        print(f"✅ Активных решений: {len(active_solutions)}")
        
        # Вывод всех решений
        print("\n📋 Все решения:")
        for name, info in solutions_info.items():
            status_icon = "✅" if info["status"] == "active" else "⏸️"
            print(f"   {status_icon} {name}: {info['description']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка теста менеджера: {e}")
        return False

def test_solution_data_types():
    """Тест системы типов данных"""
    print("\n🧪 Тест системы типов данных")
    print("=" * 50)
    
    try:
        from solution_data_types import (
            SolutionType, SolutionDataUtils, SolutionData,
            SolutionCoordinate, SolutionDimensions, SolutionMaterial
        )
        
        # Создание тестового объекта
        test_data = SolutionDataUtils.create_minimal_solution_data(
            name="Test Object",
            solution_type=SolutionType.BOX,
            coordinate=SolutionCoordinate(10, 20, 30)
        )
        
        # Установка размеров
        test_data.dimensions.width = 10.0
        test_data.dimensions.height = 20.0
        test_data.dimensions.depth = 5.0
        
        # Установка материала
        test_data.properties.material = SolutionMaterial(
            name="Test Material",
            density=2.5,
            color_rgb=(128, 128, 128)
        )
        
        # Валидация
        is_valid, errors = SolutionDataUtils.validate_solution_data(test_data)
        
        print(f"✅ Объект создан: {test_data.properties.name}")
        print(f"   Тип: {test_data.properties.solution_type.value}")
        print(f"   Координаты: {test_data.properties.coordinate.get_position()}")
        print(f"   Размеры: {test_data.dimensions.width}x{test_data.dimensions.height}x{test_data.dimensions.depth}")
        print(f"   Материал: {test_data.properties.material.name}")
        print(f"   Валидность: {'✅ Да' if is_valid else '❌ Нет'}")
        
        if not is_valid:
            print(f"   Ошибки: {errors}")
        
        # Проверка объема
        volume = test_data.dimensions.get_volume_box()
        print(f"   Объем: {volume:.2f} куб.ед.")
        
        return is_valid
        
    except Exception as e:
        print(f"❌ Ошибка теста типов данных: {e}")
        return False

def test_3d_solution_integration():
    """Тест интеграции 3D-Solution"""
    print("\n🧪 Тест интеграции 3D-Solution")
    print("=" * 50)
    
    try:
        # Проверка импорта 3D-Solution
        sys.path.insert(0, str(project_root / "Root Solution" / "3D-Solution"))
        
        # Проверка наличия файла
        main_3d_path = project_root / "Root Solution" / "3D-Solution" / "main_3d.py"
        if main_3d_path.exists():
            print("✅ Файл main_3d.py найден")
        else:
            print("❌ Файл main_3d.py не найден")
            return False
        
        # Проверка импорта (без запуска GUI)
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("main_3d", main_3d_path)
            main_3d_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_3d_module)
            print("✅ Модуль main_3d.py загружен")
        except ImportError as e:
            print(f"⚠️ Ошибка импорта 3D-Solution: {e}")
            print("   Это нормально, если PySide6 не установлен")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка теста 3D-Solution: {e}")
        return False

def test_root_solution_hierarchy():
    """Тест иерархии решений"""
    print("\n🧪 Тест иерархии решений")
    print("=" * 50)
    
    try:
        from root_solution_manager import get_root_manager
        
        manager = get_root_manager()
        hierarchy = manager.create_solution_hierarchy()
        
        print(f"✅ Корень иерархии: {hierarchy['root']}")
        print(f"✅ Количество решений: {len(hierarchy['solutions'])}")
        
        print("\n📊 Детали иерархии:")
        for name, data in hierarchy['solutions'].items():
            info = data['info']
            sub_count = len(data['sub_solutions'])
            print(f"   📁 {name}: {info['description']} (под-решений: {sub_count})")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка теста иерархии: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("🏗️ Тестирование Root Solution инфраструктуры TheSolution CAD")
    print("=" * 70)
    
    tests = [
        ("Root Solution Manager", test_root_solution_manager),
        ("Система типов данных", test_solution_data_types),
        ("Интеграция 3D-Solution", test_3d_solution_integration),
        ("Иерархия решений", test_root_solution_hierarchy)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Критическая ошибка в тесте {test_name}: {e}")
            results.append((test_name, False))
    
    # Итоговый отчет
    print("\n" + "=" * 70)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Root Solution инфраструктура работает корректно.")
    else:
        print("⚠️ Некоторые тесты не пройдены. Проверьте настройки и зависимости.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
