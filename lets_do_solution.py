#!/usr/bin/env python3
"""
Let's Do Solution - Быстрый доступ к решениям TheSolution CAD
Простой интерфейс для работы с решениями
"""

import sys
from pathlib import Path

# Добавляем пути к модулям
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "Base Solution" / "python"))
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "Root Solution" / "python"))

def show_solutions_menu():
    """Показать меню решений"""
    print("🏗️ LET'S DO SOLUTION - TheSolution CAD")
    print("=" * 50)
    print("Выберите решение для работы:")
    print()
    print("🎯 3D-Solution (ПРИОРИТЕТ)")
    print("   1. Запустить 3D-Solution")
    print("   2. Создать 3D объекты")
    print("   3. Работа с геометрией")
    print()
    print("📐 2D-Solution")
    print("   4. Запустить 2D-Solution")
    print("   5. Создать чертежи")
    print()
    print("🔧 Assembly-Solution")
    print("   6. Запустить Assembly-Solution")
    print("   7. Создать сборки")
    print()
    print("📊 Analysis-Solution")
    print("   8. Запустить Analysis-Solution")
    print("   9. Анализ и расчеты")
    print()
    print("🔄 Simulation-Solution")
    print("   10. Запустить Simulation-Solution")
    print("   11. Симуляция и тестирование")
    print()
    print("🏭 Manufacturing-Solution")
    print("   12. Запустить Manufacturing-Solution")
    print("   13. Производство и CAM")
    print()
    print("📄 Documentation-Solution")
    print("   14. Запустить Documentation-Solution")
    print("   15. Документооборот")
    print()
    print("👥 Collaboration-Solution")
    print("   16. Запустить Collaboration-Solution")
    print("   17. Совместная работа")
    print()
    print("🛠️ Инструменты")
    print("   18. Root Solution Launcher")
    print("   19. Демонстрация возможностей")
    print("   20. Тестирование системы")
    print()
    print("❌ 0. Выход")
    print()

def launch_3d_solution():
    """Запуск 3D-Solution"""
    print("🎯 Запуск 3D-Solution...")
    try:
        import subprocess
        subprocess.run([sys.executable, "Root Solution/3D-Solution/main_3d.py"])
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

def create_3d_objects():
    """Создание 3D объектов"""
    print("🔸 Создание 3D объектов...")
    try:
        from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate, SolutionMaterial
        
        # Создаем куб
        box = SolutionDataUtils.create_minimal_solution_data(
            name="Мой Куб",
            solution_type=SolutionType.BOX,
            coordinate=SolutionCoordinate(0, 0, 0)
        )
        box.dimensions.width = 10.0
        box.dimensions.height = 10.0
        box.dimensions.depth = 10.0
        box.properties.material = SolutionMaterial(name="Steel", density=7.85)
        
        # Создаем сферу
        sphere = SolutionDataUtils.create_minimal_solution_data(
            name="Моя Сфера",
            solution_type=SolutionType.SPHERE,
            coordinate=SolutionCoordinate(15, 0, 0)
        )
        sphere.dimensions.radius = 5.0
        sphere.properties.material = SolutionMaterial(name="Aluminum", density=2.7)
        
        print(f"✅ Создан {box.properties.name} - объем: {box.dimensions.get_volume_box():.2f} куб.ед.")
        print(f"✅ Создана {sphere.properties.name} - объем: {sphere.dimensions.get_volume_sphere():.2f} куб.ед.")
        
    except Exception as e:
        print(f"❌ Ошибка создания объектов: {e}")

def launch_root_launcher():
    """Запуск Root Solution Launcher"""
    print("🏗️ Запуск Root Solution Launcher...")
    try:
        import subprocess
        subprocess.run([sys.executable, "Root Solution/main.py"])
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

def run_demo():
    """Запуск демонстрации"""
    print("🎬 Запуск демонстрации...")
    try:
        import subprocess
        subprocess.run([sys.executable, "demo_root_solution.py"])
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

def run_tests():
    """Запуск тестов"""
    print("🧪 Запуск тестов...")
    try:
        import subprocess
        subprocess.run([sys.executable, "test_root_solution.py"])
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

def show_solution_info():
    """Показать информацию о решениях"""
    try:
        from root_solution_manager import get_root_manager
        
        manager = get_root_manager()
        solutions_info = manager.get_all_solutions_info()
        
        print("📋 Информация о решениях:")
        print("=" * 40)
        
        for name, info in solutions_info.items():
            status_icon = "✅" if info["status"] == "active" else "⏸️"
            print(f"{status_icon} {name}: {info['description']}")
        
        active_count = len([s for s in solutions_info.values() if s["status"] == "active"])
        print(f"\n📊 Активных решений: {active_count}/{len(solutions_info)}")
        
    except Exception as e:
        print(f"❌ Ошибка получения информации: {e}")

def main():
    """Главная функция"""
    while True:
        show_solutions_menu()
        
        try:
            choice = input("Введите номер выбора: ").strip()
            
            if choice == "0":
                print("👋 До свидания!")
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
                print(f"⚠️ Функция {choice} пока не реализована")
                print("Доступные функции: 1, 2, 18, 19, 20")
            
            input("\nНажмите Enter для продолжения...")
            
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            input("Нажмите Enter для продолжения...")

if __name__ == "__main__":
    main()
