#!/usr/bin/env python3
"""
Тестовый скрипт для проверки C++ реализации 3D отображения с OpenCASCADE
"""

import sys
import os
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent))

def test_cpp_3d_visualization():
    """Тест C++ реализации 3D отображения"""
    print("🧪 Тестирование C++ реализации 3D отображения с OpenCASCADE")
    print("=" * 60)
    
    try:
        # Попытка импорта C++ модуля
        print("📦 Импорт C++ модуля thesolution_operations...")
        import thesolution_operations as ops
        print("✅ C++ модуль успешно импортирован!")
        
        # Тест создания геометрических примитивов
        print("\n🔷 Тест создания геометрических примитивов:")
        
        # Создание куба
        box = ops.create_box("Тестовый куб", 10.0, 10.0, 10.0)
        print(f"✅ Куб создан: {box.getName()}")
        print(f"   Размеры: {box.getWidth()} x {box.getHeight()} x {box.getDepth()}")
        print(f"   Объем: {box.getVolume():.2f}")
        print(f"   Площадь поверхности: {box.getSurfaceArea():.2f}")
        
        # Создание сферы
        sphere = ops.create_sphere("Тестовая сфера", 5.0)
        print(f"✅ Сфера создана: {sphere.getName()}")
        print(f"   Радиус: {sphere.getRadius()}")
        print(f"   Объем: {sphere.getVolume():.2f}")
        print(f"   Площадь поверхности: {sphere.getSurfaceArea():.2f}")
        
        # Создание цилиндра
        cylinder = ops.create_cylinder("Тестовый цилиндр", 3.0, 8.0)
        print(f"✅ Цилиндр создан: {cylinder.getName()}")
        print(f"   Радиус: {cylinder.getRadius()}, Высота: {cylinder.getHeight()}")
        print(f"   Объем: {cylinder.getVolume():.2f}")
        print(f"   Площадь поверхности: {cylinder.getSurfaceArea():.2f}")
        
        # Тест трансформаций
        print("\n🔄 Тест трансформаций:")
        box.translate(5.0, 0.0, 0.0)
        print(f"✅ Куб перемещен на (5, 0, 0)")
        
        sphere.rotate(45.0, 0.0, 0.0, 1.0)
        print(f"✅ Сфера повернута на 45° вокруг оси Z")
        
        cylinder.scale(1.5, 1.5, 1.5)
        print(f"✅ Цилиндр масштабирован в 1.5 раза")
        
        # Тест иерархии объектов
        print("\n🌳 Тест иерархии объектов:")
        assembly = ops.create_assembly("Тестовая сборка")
        assembly.addComponent(box)
        assembly.addComponent(sphere)
        assembly.addComponent(cylinder)
        print(f"✅ Сборка создана: {assembly.getName()}")
        print(f"   Количество компонентов: {len(assembly.getComponents())}")
        print(f"   Общий объем: {assembly.getVolume():.2f}")
        
        # Тест SceneManager
        print("\n🎬 Тест SceneManager:")
        scene_manager = ops.SceneManager()
        scene_manager.addObject(box.getShape(), "Куб в сцене")
        scene_manager.addObject(sphere.getShape(), "Сфера в сцене")
        scene_manager.addObject(cylinder.getShape(), "Цилиндр в сцене")
        print(f"✅ Объекты добавлены в сцену")
        print(f"   Количество объектов: {len(scene_manager.getObjects())}")
        
        # Тест экспорта
        print("\n💾 Тест экспорта:")
        try:
            scene_manager.exportScene("test_scene.step")
            print("✅ Сцена экспортирована в STEP файл")
        except Exception as e:
            print(f"⚠️ Экспорт STEP: {e}")
        
        print("\n🎉 Все тесты C++ реализации прошли успешно!")
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка импорта C++ модуля: {e}")
        print("💡 Убедитесь, что C++ компоненты собраны и установлены")
        return False
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False

def test_visualization_widget():
    """Тест виджета 3D визуализации"""
    print("\n🎨 Тест виджета 3D визуализации:")
    
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
        from PySide6.QtCore import Qt
        import thesolution_operations as ops
        
        # Создание приложения
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Создание главного окна
        window = QMainWindow()
        window.setWindowTitle("TheSolution 3D Visualization Test")
        window.resize(800, 600)
        
        # Создание центрального виджета
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        
        # Создание layout
        layout = QVBoxLayout(central_widget)
        
        # Создание виджета 3D визуализации
        viz_widget = ops.Visualization3D()
        layout.addWidget(viz_widget)
        
        # Добавление тестовых объектов
        box = ops.create_box("Тестовый куб", 10.0, 10.0, 10.0)
        sphere = ops.create_sphere("Тестовая сфера", 5.0)
        cylinder = ops.create_cylinder("Тестовый цилиндр", 3.0, 8.0)
        
        viz_widget.addShape(box.getShape(), "Куб")
        viz_widget.addShape(sphere.getShape(), "Сфера")
        viz_widget.addShape(cylinder.getShape(), "Цилиндр")
        
        # Настройка отображения
        viz_widget.setShadedMode(True)
        viz_widget.setLighting(True)
        viz_widget.setBackgroundColor(Qt.white)
        
        print("✅ Виджет 3D визуализации создан")
        print("✅ Тестовые объекты добавлены")
        print("✅ Окно открыто для тестирования")
        
        # Показ окна
        window.show()
        
        # Запуск приложения
        print("🔄 Запуск приложения (закройте окно для завершения)...")
        app.exec()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании виджета: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("🚀 Тестирование C++ реализации 3D отображения TheSolution")
    print("=" * 70)
    
    # Тест базовой функциональности
    if not test_cpp_3d_visualization():
        print("\n💔 Базовые тесты не прошли. Проверьте сборку C++ компонентов.")
        return False
    
    # Тест виджета визуализации
    print("\n" + "=" * 70)
    print("🎨 Тестирование виджета 3D визуализации...")
    
    response = input("Запустить тест виджета 3D визуализации? (y/n): ").lower().strip()
    if response in ['y', 'yes', 'да', 'д']:
        test_visualization_widget()
    
    print("\n🎉 Тестирование завершено!")
    return True

if __name__ == "__main__":
    main()
