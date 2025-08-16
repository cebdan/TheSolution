#!/usr/bin/env python3
"""
3D-Solution - Основное 3D решение TheSolution CAD
Точка входа в 3D моделирование и дизайн
"""

import sys
import os
from pathlib import Path

# Добавляем пути к базовым модулям
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "Base Solution" / "python"))
sys.path.insert(0, str(project_root))

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTreeWidget, QTreeWidgetItem
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont
except ImportError:
    print("❌ PySide6 не установлен")
    sys.exit(1)

# Импорт базовых классов TheSolution
try:
    from solution_coordinate import SolutionCoordinate
    from base_solution import Solution
    from solution_data_types import SolutionType, SolutionDataUtils, SolutionData, SolutionDimensions, SolutionMaterial
except ImportError as e:
    print(f"❌ Ошибка импорта базовых классов: {e}")
    sys.exit(1)

# Импорт Root Solution Manager
try:
    sys.path.insert(0, str(project_root / "Root Solution" / "python"))
    from root_solution_manager import get_root_manager, SolutionStatus
except ImportError as e:
    print(f"⚠️ Root Solution Manager не найден: {e}")

class Solution3DMainWindow(QMainWindow):
    """
    Главное окно 3D-Solution
    Интерфейс для 3D моделирования
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TheSolution 3D-Solution")
        self.setGeometry(100, 100, 1400, 900)
        
        # Инициализация Root Solution Manager
        try:
            self.root_manager = get_root_manager()
            self.solution_3d = self.root_manager.get_3d_solution()
        except:
            self.root_manager = None
            self.solution_3d = None
        
        # Список 3D объектов с типизированными данными
        self.objects_3d: List[SolutionData] = []
        
        self.setup_ui()
        self.create_sample_objects()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Левая панель - дерево объектов и инструменты
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Центральная панель - 3D вид
        center_panel = self.create_center_panel()
        main_layout.addWidget(center_panel, 3)
        
        # Правая панель - свойства
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
    
    def create_left_panel(self):
        """Левая панель с деревом объектов"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Заголовок
        title = QLabel("3D Объекты")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Дерево объектов
        self.objects_tree = QTreeWidget()
        self.objects_tree.setHeaderLabels(["Имя", "Тип", "Координаты"])
        layout.addWidget(self.objects_tree)
        
        # Кнопки создания примитивов
        layout.addWidget(QLabel("Создать примитивы:"))
        
        primitives = [
            ("Куб", self.create_box),
            ("Сфера", self.create_sphere),
            ("Цилиндр", self.create_cylinder),
            ("Конус", self.create_cone)
        ]
        
        for name, callback in primitives:
            btn = QPushButton(name)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        return widget
    
    def create_center_panel(self):
        """Центральная панель с 3D видом"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Заголовок
        title = QLabel("3D Вид")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Заглушка для 3D вида
        view_placeholder = QLabel("[3D Вид]\n\nЗдесь будет OpenGL/VTK виджет\nдля отображения 3D сцены")
        view_placeholder.setAlignment(Qt.AlignCenter)
        view_placeholder.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                background-color: #f9f9f9;
                min-height: 400px;
                font-size: 16px;
                color: #666;
            }
        """)
        layout.addWidget(view_placeholder)
        
        return widget
    
    def create_right_panel(self):
        """Правая панель со свойствами"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Заголовок
        title = QLabel("Свойства")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Информация об объекте
        self.info_label = QLabel("Выберите объект для\nпросмотра свойств")
        self.info_label.setStyleSheet("""
            QLabel {
                border: 1px solid #ddd;
                padding: 10px;
                background-color: #f5f5f5;
            }
        """)
        layout.addWidget(self.info_label)
        
        layout.addStretch()
        
        return widget
    
    def create_sample_objects(self):
        """Создание примеров объектов с типизированными данными"""
        
        # Создаем куб с типизированными данными
        box_data = SolutionDataUtils.create_minimal_solution_data(
            name="Куб 1",
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
        
        # Создаем сферу
        sphere_data = SolutionDataUtils.create_minimal_solution_data(
            name="Сфера 1",
            solution_type=SolutionType.SPHERE,
            coordinate=SolutionCoordinate(10, 0, 0)
        )
        sphere_data.dimensions.radius = 5.0
        sphere_data.properties.material = SolutionMaterial(
            name="Aluminum",
            density=2.7,
            color_rgb=(169, 169, 169)
        )
        
        # Создаем цилиндр
        cylinder_data = SolutionDataUtils.create_minimal_solution_data(
            name="Цилиндр 1",
            solution_type=SolutionType.CYLINDER,
            coordinate=SolutionCoordinate(0, 10, 0)
        )
        cylinder_data.dimensions.radius = 3.0
        cylinder_data.dimensions.height = 8.0
        cylinder_data.properties.material = SolutionMaterial(
            name="Copper",
            density=8.96,
            color_rgb=(184, 115, 51)
        )
        
        self.objects_3d.extend([box_data, sphere_data, cylinder_data])
        self.update_objects_tree()
    
    def update_objects_tree(self):
        """Обновление дерева объектов с типизированными данными"""
        self.objects_tree.clear()
        
        for obj_data in self.objects_3d:
            coord = obj_data.properties.coordinate
            item = QTreeWidgetItem([
                obj_data.properties.name,
                obj_data.properties.solution_type.value,
                f"({coord.x:.1f}, {coord.y:.1f}, {coord.z:.1f})"
            ])
            
            # Добавляем информацию о материале
            material_info = f"Материал: {obj_data.properties.material.name}"
            item.setToolTip(2, material_info)
            
            self.objects_tree.addTopLevelItem(item)
    
    # Методы создания примитивов с типизированными данными
    def create_box(self):
        """Создание куба с типизированными данными"""
        count = len([o for o in self.objects_3d if "Куб" in o.properties.name]) + 1
        
        box_data = SolutionDataUtils.create_minimal_solution_data(
            name=f"Куб {count}",
            solution_type=SolutionType.BOX,
            coordinate=SolutionCoordinate(count * 5, 0, 0)
        )
        box_data.dimensions.width = 10.0
        box_data.dimensions.height = 10.0
        box_data.dimensions.depth = 10.0
        box_data.properties.material = SolutionMaterial(
            name="Steel",
            density=7.85,
            color_rgb=(192, 192, 192)
        )
        
        self.objects_3d.append(box_data)
        self.update_objects_tree()
        
        coord = box_data.properties.coordinate
        print(f"✅ Создан {box_data.properties.name} в позиции ({coord.x}, {coord.y}, {coord.z})")
        print(f"   Объем: {box_data.dimensions.get_volume_box():.2f} куб.ед.")
    
    def create_sphere(self):
        """Создание сферы с типизированными данными"""
        count = len([o for o in self.objects_3d if "Сфера" in o.properties.name]) + 1
        
        sphere_data = SolutionDataUtils.create_minimal_solution_data(
            name=f"Сфера {count}",
            solution_type=SolutionType.SPHERE,
            coordinate=SolutionCoordinate(0, count * 5, 0)
        )
        sphere_data.dimensions.radius = 5.0
        sphere_data.properties.material = SolutionMaterial(
            name="Aluminum",
            density=2.7,
            color_rgb=(169, 169, 169)
        )
        
        self.objects_3d.append(sphere_data)
        self.update_objects_tree()
        
        coord = sphere_data.properties.coordinate
        print(f"✅ Создана {sphere_data.properties.name} в позиции ({coord.x}, {coord.y}, {coord.z})")
        print(f"   Объем: {sphere_data.dimensions.get_volume_sphere():.2f} куб.ед.")
    
    def create_cylinder(self):
        """Создание цилиндра с типизированными данными"""
        count = len([o for o in self.objects_3d if "Цилиндр" in o.properties.name]) + 1
        
        cylinder_data = SolutionDataUtils.create_minimal_solution_data(
            name=f"Цилиндр {count}",
            solution_type=SolutionType.CYLINDER,
            coordinate=SolutionCoordinate(0, 0, count * 5)
        )
        cylinder_data.dimensions.radius = 3.0
        cylinder_data.dimensions.height = 8.0
        cylinder_data.properties.material = SolutionMaterial(
            name="Copper",
            density=8.96,
            color_rgb=(184, 115, 51)
        )
        
        self.objects_3d.append(cylinder_data)
        self.update_objects_tree()
        
        coord = cylinder_data.properties.coordinate
        print(f"✅ Создан {cylinder_data.properties.name} в позиции ({coord.x}, {coord.y}, {coord.z})")
        print(f"   Объем: {cylinder_data.dimensions.get_volume_cylinder():.2f} куб.ед.")
    
    def create_cone(self):
        """Создание конуса с типизированными данными"""
        count = len([o for o in self.objects_3d if "Конус" in o.properties.name]) + 1
        
        cone_data = SolutionDataUtils.create_minimal_solution_data(
            name=f"Конус {count}",
            solution_type=SolutionType.CUSTOM,  # Пока используем CUSTOM для конуса
            coordinate=SolutionCoordinate(count * 3, count * 3, 0)
        )
        cone_data.dimensions.radius = 4.0
        cone_data.dimensions.height = 6.0
        cone_data.properties.material = SolutionMaterial(
            name="Plastic",
            density=1.2,
            color_rgb=(255, 165, 0)
        )
        
        self.objects_3d.append(cone_data)
        self.update_objects_tree()
        
        coord = cone_data.properties.coordinate
        print(f"✅ Создан {cone_data.properties.name} в позиции ({coord.x}, {coord.y}, {coord.z})")

def launch_3d_solution():
    """Запуск 3D-Solution"""
    print("🎯 Запуск 3D-Solution...")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = Solution3DMainWindow()
    window.show()
    
    return window

def main():
    """Главная функция для прямого запуска"""
    app = QApplication(sys.argv)
    window = launch_3d_solution()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())