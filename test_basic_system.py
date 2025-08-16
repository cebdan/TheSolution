#!/usr/bin/env python3
"""
Тестовый скрипт для проверки базовой системы TheSolution

Проверяет работу классов Solution и SolutionCoordinate
"""

import sys
import os

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Base Solution', 'python'))

# Прямые импорты вместо относительных
from solution_coordinate import SolutionCoordinate
from base_solution import Solution

def test_solution_coordinate():
    """Тестирует класс SolutionCoordinate"""
    print("🧪 Тестирование SolutionCoordinate...")
    
    # Создание координат
    coord1 = SolutionCoordinate(10, 20, 30)
    coord2 = SolutionCoordinate(5, 5, 5, 2.0, 1.5, 0.5)
    
    print(f"Координаты 1: {coord1}")
    print(f"Координаты 2: {coord2}")
    
    # Тест позиции и ориентации
    pos = coord1.get_position()
    orient = coord1.get_orientation()
    print(f"Позиция: {pos}")
    print(f"Ориентация: {orient}")
    
    # Тест матрицы трансформации
    matrix = coord1.get_transformation_matrix()
    print(f"Матрица трансформации:\n{matrix}")
    
    # Тест операций
    coord_sum = coord1 + coord2
    coord_diff = coord1 - coord2
    print(f"Сумма: {coord_sum}")
    print(f"Разность: {coord_diff}")
    
    # Тест расстояния
    distance = coord1.distance_to(coord2)
    print(f"Расстояние между координатами: {distance}")
    
    print("✅ SolutionCoordinate тесты пройдены\n")

def test_solution():
    """Тестирует класс Solution"""
    print("🧪 Тестирование Solution...")
    
    # Создание объектов
    root = Solution("Root", SolutionCoordinate(0, 0, 0))
    child1 = Solution("Child1", SolutionCoordinate(10, 0, 0))
    child2 = Solution("Child2", SolutionCoordinate(0, 10, 0))
    grandchild = Solution("GrandChild", SolutionCoordinate(5, 5, 0))
    
    print(f"Корневой объект: {root}")
    print(f"Дочерний объект: {child1}")
    
    # Тест иерархии
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)
    
    print(f"Дочерние элементы корня: {len(root.get_children())}")
    print(f"Родитель child1: {child1.get_parent()}")
    print(f"Потомки root: {len(root.get_descendants())}")
    
    # Тест координат
    print(f"Координаты child1: x={child1.x}, y={child1.y}, z={child1.z}")
    child1.x = 50
    print(f"Новые координаты child1: x={child1.x}")
    
    # Тест абсолютных координат
    abs_coord = grandchild.get_absolute_coordinate()
    print(f"Абсолютные координаты grandchild: {abs_coord}")
    
    # Тест свойств
    root.set_property("color", "red")
    root.set_property("material", "steel")
    print(f"Свойства root: {root.properties}")
    
    # Тест видимости и блокировки
    root.set_visible(False)
    root.set_locked(True)
    print(f"Root видимый: {root.is_visible()}")
    print(f"Root заблокирован: {root.is_locked()}")
    
    print("✅ Solution тесты пройдены\n")

def test_hierarchy():
    """Тестирует иерархическую структуру"""
    print("🧪 Тестирование иерархии...")
    
    # Создание сложной иерархии
    assembly = Solution("Assembly")
    
    # Создание компонентов
    base = Solution("Base", SolutionCoordinate(0, 0, 0))
    pillar1 = Solution("Pillar1", SolutionCoordinate(10, 0, 0))
    pillar2 = Solution("Pillar2", SolutionCoordinate(-10, 0, 0))
    top = Solution("Top", SolutionCoordinate(0, 0, 20))
    
    # Сборка
    assembly.add_child(base)
    assembly.add_child(pillar1)
    assembly.add_child(pillar2)
    assembly.add_child(top)
    
    # Проверка структуры
    print(f"Сборка содержит {len(assembly.get_children())} компонентов")
    print(f"Всего объектов в иерархии: {len(assembly.get_descendants()) + 1}")
    
    # Проверка корневого элемента
    root = pillar1.get_root()
    print(f"Корневой элемент для pillar1: {root.name}")
    
    # Проверка предков
    ancestors = top.get_ancestors()
    print(f"Предки top: {[a.name for a in ancestors]}")
    
    print("✅ Иерархия тесты пройдены\n")

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование базовой системы TheSolution")
    print("=" * 50)
    
    try:
        test_solution_coordinate()
        test_solution()
        test_hierarchy()
        
        print("🎉 Все тесты пройдены успешно!")
        print("\nБазовая система готова к использованию.")
        print("Следующие шаги:")
        print("1. Создать GUI компоненты")
        print("2. Добавить геометрические операции")
        print("3. Интегрировать с OpenCASCADE")
        
    except Exception as e:
        print(f"❌ Ошибка в тестах: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
