#!/usr/bin/env python3
"""
Простое GUI приложение для TheSolution CAD системы

Демонстрирует базовую функциональность с использованием PySide6
"""

import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                               QWidget, QPushButton, QTreeWidget, QTreeWidgetItem,
                               QLabel, QLineEdit, QGroupBox, QGridLayout, QTextEdit,
                               QSplitter, QFrame)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Base Solution', 'python'))

from solution_coordinate import SolutionCoordinate
from base_solution import Solution

class SolutionTreeWidget(QTreeWidget):
    """Виджет дерева объектов Solution"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabel("Объекты Solution")
        self.setMinimumWidth(200)
        self.solutions = {}  # Словарь для хранения объектов
        
    def add_solution(self, solution):
        """Добавляет Solution объект в дерево"""
        item = QTreeWidgetItem([solution.name])
        item.setData(0, Qt.UserRole, solution.id)
        self.solutions[solution.id] = solution
        
        # Добавляем дочерние элементы
        for child in solution.get_children():
            child_item = self.add_solution(child)
            item.addChild(child_item)
        
        self.addTopLevelItem(item)
        return item
    
    def get_selected_solution(self):
        """Возвращает выбранный Solution объект"""
        current_item = self.currentItem()
        if current_item:
            solution_id = current_item.data(0, Qt.UserRole)
            return self.solutions.get(solution_id)
        return None

class CoordinateEditor(QWidget):
    """Виджет для редактирования координат"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_solution = None
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        
        # Группа координат
        coord_group = QGroupBox("Координаты")
        coord_layout = QGridLayout(coord_group)
        
        # Позиционные координаты
        coord_layout.addWidget(QLabel("X:"), 0, 0)
        self.x_edit = QLineEdit("0.0")
        coord_layout.addWidget(self.x_edit, 0, 1)
        
        coord_layout.addWidget(QLabel("Y:"), 1, 0)
        self.y_edit = QLineEdit("0.0")
        coord_layout.addWidget(self.y_edit, 1, 1)
        
        coord_layout.addWidget(QLabel("Z:"), 2, 0)
        self.z_edit = QLineEdit("0.0")
        coord_layout.addWidget(self.z_edit, 2, 1)
        
        # Ориентационные координаты
        coord_layout.addWidget(QLabel("A:"), 0, 2)
        self.a_edit = QLineEdit("1.0")
        coord_layout.addWidget(self.a_edit, 0, 3)
        
        coord_layout.addWidget(QLabel("B:"), 1, 2)
        self.b_edit = QLineEdit("1.0")
        coord_layout.addWidget(self.b_edit, 1, 3)
        
        coord_layout.addWidget(QLabel("C:"), 2, 2)
        self.c_edit = QLineEdit("1.0")
        coord_layout.addWidget(self.c_edit, 2, 3)
        
        layout.addWidget(coord_group)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.apply_btn = QPushButton("Применить")
        self.apply_btn.clicked.connect(self.apply_coordinates)
        button_layout.addWidget(self.apply_btn)
        
        self.reset_btn = QPushButton("Сброс")
        self.reset_btn.clicked.connect(self.reset_coordinates)
        button_layout.addWidget(self.reset_btn)
        
        layout.addLayout(button_layout)
        
    def set_solution(self, solution):
        """Устанавливает Solution объект для редактирования"""
        self.current_solution = solution
        if solution:
            self.update_coordinates()
        else:
            self.clear_coordinates()
    
    def update_coordinates(self):
        """Обновляет отображение координат"""
        if self.current_solution:
            coord = self.current_solution.coordinate
            self.x_edit.setText(f"{coord.x:.2f}")
            self.y_edit.setText(f"{coord.y:.2f}")
            self.z_edit.setText(f"{coord.z:.2f}")
            self.a_edit.setText(f"{coord.a:.2f}")
            self.b_edit.setText(f"{coord.b:.2f}")
            self.c_edit.setText(f"{coord.c:.2f}")
    
    def clear_coordinates(self):
        """Очищает поля координат"""
        self.x_edit.setText("0.0")
        self.y_edit.setText("0.0")
        self.z_edit.setText("0.0")
        self.a_edit.setText("1.0")
        self.b_edit.setText("1.0")
        self.c_edit.setText("1.0")
    
    def apply_coordinates(self):
        """Применяет изменения координат"""
        if self.current_solution:
            try:
                x = float(self.x_edit.text())
                y = float(self.y_edit.text())
                z = float(self.z_edit.text())
                a = float(self.a_edit.text())
                b = float(self.b_edit.text())
                c = float(self.c_edit.text())
                
                self.current_solution.coordinate = SolutionCoordinate(x, y, z, a, b, c)
                print(f"Координаты обновлены: {self.current_solution.coordinate}")
            except ValueError:
                print("Ошибка: введите корректные числовые значения")
    
    def reset_coordinates(self):
        """Сбрасывает координаты к исходным значениям"""
        if self.current_solution:
            self.update_coordinates()

class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.solutions = []  # Список всех Solution объектов
        self.setup_ui()
        self.create_sample_data()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle("TheSolution CAD - Простое GUI")
        self.setGeometry(100, 100, 1000, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        
        # Создаем сплиттер
        splitter = QSplitter(Qt.Horizontal)
        
        # Левая панель
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Дерево объектов
        self.tree_widget = SolutionTreeWidget()
        self.tree_widget.itemSelectionChanged.connect(self.on_solution_selected)
        left_layout.addWidget(QLabel("Объекты Solution:"))
        left_layout.addWidget(self.tree_widget)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        self.create_box_btn = QPushButton("Создать куб")
        self.create_box_btn.clicked.connect(self.create_box)
        button_layout.addWidget(self.create_box_btn)
        
        self.create_sphere_btn = QPushButton("Создать сферу")
        self.create_sphere_btn.clicked.connect(self.create_sphere)
        button_layout.addWidget(self.create_sphere_btn)
        
        left_layout.addLayout(button_layout)
        
        # Правая панель
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Редактор координат
        self.coord_editor = CoordinateEditor()
        right_layout.addWidget(QLabel("Редактор координат:"))
        right_layout.addWidget(self.coord_editor)
        
        # Информационная панель
        info_group = QGroupBox("Информация")
        info_layout = QVBoxLayout(info_group)
        
        self.info_text = QTextEdit()
        self.info_text.setMaximumHeight(150)
        self.info_text.setReadOnly(True)
        info_layout.addWidget(self.info_text)
        
        right_layout.addWidget(info_group)
        
        # Добавляем панели в сплиттер
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter)
        
    def create_sample_data(self):
        """Создает примерные данные"""
        # Создаем корневой объект
        root = Solution("Корневой объект", SolutionCoordinate(0, 0, 0))
        self.solutions.append(root)
        
        # Создаем дочерние объекты
        box1 = Solution("Куб 1", SolutionCoordinate(10, 0, 0))
        box2 = Solution("Куб 2", SolutionCoordinate(0, 10, 0))
        sphere = Solution("Сфера", SolutionCoordinate(0, 0, 10))
        
        root.add_child(box1)
        root.add_child(box2)
        root.add_child(sphere)
        
        self.solutions.extend([box1, box2, sphere])
        
        # Добавляем в дерево
        self.tree_widget.add_solution(root)
        
        self.update_info("Созданы примерные объекты")
    
    def create_box(self):
        """Создает новый куб"""
        box = Solution(f"Куб {len(self.solutions)}", SolutionCoordinate(0, 0, 0))
        self.solutions.append(box)
        
        # Добавляем к корневому объекту
        if self.solutions:
            root = self.solutions[0]
            root.add_child(box)
            
            # Обновляем дерево
            self.tree_widget.clear()
            self.tree_widget.add_solution(root)
            
        self.update_info(f"Создан новый куб: {box.name}")
    
    def create_sphere(self):
        """Создает новую сферу"""
        sphere = Solution(f"Сфера {len(self.solutions)}", SolutionCoordinate(0, 0, 0))
        self.solutions.append(sphere)
        
        # Добавляем к корневому объекту
        if self.solutions:
            root = self.solutions[0]
            root.add_child(sphere)
            
            # Обновляем дерево
            self.tree_widget.clear()
            self.tree_widget.add_solution(root)
            
        self.update_info(f"Создана новая сфера: {sphere.name}")
    
    def on_solution_selected(self):
        """Обработчик выбора объекта в дереве"""
        solution = self.tree_widget.get_selected_solution()
        if solution:
            self.coord_editor.set_solution(solution)
            self.update_info(f"Выбран объект: {solution.name}")
        else:
            self.coord_editor.set_solution(None)
            self.update_info("Объект не выбран")
    
    def update_info(self, message):
        """Обновляет информационную панель"""
        self.info_text.append(f"[{QTimer().remainingTime()}] {message}")

def main():
    """Основная функция"""
    app = QApplication(sys.argv)
    
    # Настройка стиля
    app.setStyle('Fusion')
    
    # Создание и отображение главного окна
    window = MainWindow()
    window.show()
    
    print("🚀 TheSolution CAD GUI запущено!")
    print("Функции:")
    print("- Создание объектов (кубы, сферы)")
    print("- Редактирование координат")
    print("- Иерархическая структура объектов")
    print("- Информационная панель")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
