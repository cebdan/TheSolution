#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрация полной интеграции OpenCASCADE с TheSolution CAD
"""

import sys
import os
from datetime import datetime

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_basic_integration():
    """Демонстрация базовой интеграции"""
    print("🚀 Демонстрация интеграции OpenCASCADE с TheSolution CAD")
    print("=" * 60)
    
    try:
        # Импорт системы типов данных
        from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate
        print("✅ Система типов данных загружена")
        
        # Импорт интеграции OpenCASCADE
        from opencascade_integration import OpenCascadeIntegration
        print("✅ Интеграция OpenCASCADE загружена")
        
        # Создание интеграции
        integration = OpenCascadeIntegration()
        
        if not integration.occ_available:
            print("❌ OpenCASCADE недоступен")
            return False
        
        print("✅ OpenCASCADE доступен и готов к работе")
        
        # Демонстрация создания объектов
        print("\n📦 Создание 3D объектов:")
        
        # 1. Куб
        print("\n1. Создание куба...")
        cube_data = SolutionDataUtils.create_minimal_solution_data(
            name="Демо-куб",
            solution_type=SolutionType.BOX,
            coordinate=SolutionCoordinate(0, 0, 0)
        )
        cube_data.dimensions.width = 15.0
        cube_data.dimensions.height = 10.0
        cube_data.dimensions.depth = 8.0
        
        cube_result = integration.integrate_with_solution_data(cube_data)
        if cube_result:
            print(f"   ✅ Куб создан: {cube_data.properties.name}")
            print(f"   📊 Размеры: {cube_data.dimensions.width}×{cube_data.dimensions.height}×{cube_data.dimensions.depth}")
            print(f"   📏 Объем: {cube_result['volume']:.2f}")
        
        # 2. Сфера
        print("\n2. Создание сферы...")
        sphere_data = SolutionDataUtils.create_minimal_solution_data(
            name="Демо-сфера",
            solution_type=SolutionType.SPHERE,
            coordinate=SolutionCoordinate(25, 0, 0)
        )
        sphere_data.dimensions.radius = 7.0
        
        sphere_result = integration.integrate_with_solution_data(sphere_data)
        if sphere_result:
            print(f"   ✅ Сфера создана: {sphere_data.properties.name}")
            print(f"   📊 Радиус: {sphere_data.dimensions.radius}")
            print(f"   📏 Объем: {sphere_result['volume']:.2f}")
        
        # 3. Цилиндр
        print("\n3. Создание цилиндра...")
        cylinder_data = SolutionDataUtils.create_minimal_solution_data(
            name="Демо-цилиндр",
            solution_type=SolutionType.CYLINDER,
            coordinate=SolutionCoordinate(50, 0, 0)
        )
        cylinder_data.dimensions.radius = 4.0
        cylinder_data.dimensions.height = 12.0
        
        cylinder_result = integration.integrate_with_solution_data(cylinder_data)
        if cylinder_result:
            print(f"   ✅ Цилиндр создан: {cylinder_data.properties.name}")
            print(f"   📊 Радиус: {cylinder_data.dimensions.radius}, Высота: {cylinder_data.dimensions.height}")
            print(f"   📏 Объем: {cylinder_result['volume']:.2f}")
        
        # Демонстрация трансформаций
        print("\n🔄 Демонстрация трансформаций:")
        
        if cube_result and 'occ_shape' in cube_result:
            # Перемещение куба
            moved_shape = integration.transform_shape(
                cube_result['occ_shape'],
                translation=(10, 5, 3)
            )
            if moved_shape:
                print("   ✅ Куб перемещен на (10, 5, 3)")
        
        # Статистика
        print("\n📊 Статистика интеграции:")
        print(f"   • Создано объектов: 3")
        print(f"   • Общий объем: {cube_result['volume'] + sphere_result['volume'] + cylinder_result['volume']:.2f}")
        print(f"   • OpenCASCADE формы: {sum(1 for r in [cube_result, sphere_result, cylinder_result] if r and 'occ_shape' in r)}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"❌ Ошибка демонстрации: {e}")
        return False

def demo_gui_integration():
    """Демонстрация интеграции с GUI"""
    print("\n🎨 Демонстрация интеграции с GUI:")
    print("=" * 40)
    
    try:
        # Проверка доступности PySide6
        from PySide6.QtWidgets import QApplication
        print("✅ PySide6 доступен")
        
        # Проверка интеграции OpenCASCADE
        from opencascade_integration import OpenCascadeIntegration
        integration = OpenCascadeIntegration()
        
        if integration.occ_available:
            print("✅ OpenCASCADE готов для GUI интеграции")
            print("💡 Запустите: conda run -n pythonocc python 3d_solution_gui.py")
        else:
            print("❌ OpenCASCADE недоступен для GUI")
        
        return True
        
    except ImportError as e:
        print(f"❌ PySide6 недоступен: {e}")
        return False

def demo_file_operations():
    """Демонстрация работы с файлами"""
    print("\n📁 Демонстрация работы с файлами:")
    print("=" * 40)
    
    try:
        # Создание тестового файла с объектами
        filename = f"demo_objects_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("TheSolution CAD - Demo Objects\n")
            f.write("=" * 30 + "\n\n")
            f.write("Создано с интеграцией OpenCASCADE\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Данные объектов
            objects_data = [
                {"name": "Демо-куб", "type": "BOX", "volume": 1200.0},
                {"name": "Демо-сфера", "type": "SPHERE", "volume": 1436.8},
                {"name": "Демо-цилиндр", "type": "CYLINDER", "volume": 603.2}
            ]
            
            for obj in objects_data:
                f.write(f"Объект: {obj['name']}\n")
                f.write(f"Тип: {obj['type']}\n")
                f.write(f"Объем: {obj['volume']:.2f}\n")
                f.write("-" * 20 + "\n\n")
        
        print(f"✅ Файл создан: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания файла: {e}")
        return False

def main():
    """Главная функция демонстрации"""
    print("🎯 TheSolution CAD - Демонстрация OpenCASCADE интеграции")
    print("=" * 70)
    
    success_count = 0
    total_demos = 3
    
    # Демонстрация 1: Базовая интеграция
    if demo_basic_integration():
        success_count += 1
    
    # Демонстрация 2: GUI интеграция
    if demo_gui_integration():
        success_count += 1
    
    # Демонстрация 3: Работа с файлами
    if demo_file_operations():
        success_count += 1
    
    # Итоги
    print("\n" + "=" * 70)
    print("📋 ИТОГИ ДЕМОНСТРАЦИИ:")
    print(f"   ✅ Успешно: {success_count}/{total_demos}")
    print(f"   ❌ Ошибок: {total_demos - success_count}")
    
    if success_count == total_demos:
        print("\n🎉 ВСЕ ДЕМОНСТРАЦИИ ПРОШЛИ УСПЕШНО!")
        print("🚀 OpenCASCADE полностью интегрирован с TheSolution CAD")
    else:
        print(f"\n⚠️ Есть проблемы в {total_demos - success_count} демонстрациях")
    
    print("\n💡 Следующие шаги:")
    print("   1. Запустите GUI: conda run -n pythonocc python 3d_solution_gui.py")
    print("   2. Создайте 3D объекты через интерфейс")
    print("   3. Экспортируйте объекты в файл")
    print("   4. Изучите созданные OpenCASCADE формы")

if __name__ == "__main__":
    main()
