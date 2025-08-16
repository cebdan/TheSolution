#!/usr/bin/env python3
"""
Простой тестовый GUI для проверки работы PySide6
"""

import sys
from pathlib import Path

# Добавляем пути к модулям
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "Base Solution" / "python"))
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "Root Solution" / "python"))

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
    from PySide6.QtCore import Qt
    print("✅ PySide6 импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта PySide6: {e}")
    sys.exit(1)

class SimpleTestGUI(QMainWindow):
    """Простое тестовое окно"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TheSolution CAD - Тестовый GUI")
        self.setGeometry(100, 100, 800, 600)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Создаем layout
        layout = QVBoxLayout(central_widget)
        
        # Заголовок
        title = QLabel("🎯 Let's Do Solution - Тестовый GUI")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db; margin: 20px;")
        layout.addWidget(title)
        
        # Подзаголовок
        subtitle = QLabel("TheSolution CAD Platform")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #bdc3c7; margin: 10px;")
        layout.addWidget(subtitle)
        
        # Кнопки
        self.create_button(layout, "🚀 Запустить 3D-Solution", self.launch_3d)
        self.create_button(layout, "🔸 Создать 3D объекты", self.create_objects)
        self.create_button(layout, "🏗️ Root Solution Launcher", self.launch_root)
        self.create_button(layout, "🎬 Демонстрация", self.run_demo)
        self.create_button(layout, "🧪 Тестирование", self.run_tests)
        
        # Статус
        self.status_label = QLabel("Статус: Готов к работе")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #27ae60; margin: 20px;")
        layout.addWidget(self.status_label)
        
        # Устанавливаем стиль окна
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
                color: white;
            }
        """)
    
    def create_button(self, layout, text, callback):
        """Создать кнопку"""
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border: 2px solid #2980b9;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                padding: 12px;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
                border: 2px solid #5dade2;
            }
        """)
        button.clicked.connect(callback)
        layout.addWidget(button)
    
    def launch_3d(self):
        """Запуск 3D-Solution"""
        self.status_label.setText("Статус: Запуск 3D-Solution...")
        print("🎯 Запуск 3D-Solution...")
        try:
            import subprocess
            subprocess.run([sys.executable, "Root Solution/3D-Solution/main_3d.py"])
            self.status_label.setText("Статус: 3D-Solution запущен")
        except Exception as e:
            self.status_label.setText(f"Статус: Ошибка - {e}")
    
    def create_objects(self):
        """Создание 3D объектов"""
        self.status_label.setText("Статус: Создание объектов...")
        print("🔸 Создание 3D объектов...")
        try:
            from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate, SolutionMaterial
            
            # Создаем куб
            box = SolutionDataUtils.create_minimal_solution_data(
                name="Тестовый Куб",
                solution_type=SolutionType.BOX,
                coordinate=SolutionCoordinate(0, 0, 0)
            )
            box.dimensions.width = 10.0
            box.dimensions.height = 10.0
            box.dimensions.depth = 10.0
            box.properties.material = SolutionMaterial(name="Steel", density=7.85)
            
            print(f"✅ Создан {box.properties.name} - объем: {box.dimensions.get_volume_box():.2f} куб.ед.")
            self.status_label.setText("Статус: Объекты созданы успешно")
            
        except Exception as e:
            self.status_label.setText(f"Статус: Ошибка - {e}")
    
    def launch_root(self):
        """Запуск Root Solution Launcher"""
        self.status_label.setText("Статус: Запуск Root Launcher...")
        print("🏗️ Запуск Root Solution Launcher...")
        try:
            import subprocess
            subprocess.run([sys.executable, "Root Solution/main.py"])
            self.status_label.setText("Статус: Root Launcher запущен")
        except Exception as e:
            self.status_label.setText(f"Статус: Ошибка - {e}")
    
    def run_demo(self):
        """Запуск демонстрации"""
        self.status_label.setText("Статус: Запуск демонстрации...")
        print("🎬 Запуск демонстрации...")
        try:
            import subprocess
            subprocess.run([sys.executable, "demo_root_solution.py"])
            self.status_label.setText("Статус: Демонстрация завершена")
        except Exception as e:
            self.status_label.setText(f"Статус: Ошибка - {e}")
    
    def run_tests(self):
        """Запуск тестов"""
        self.status_label.setText("Статус: Запуск тестов...")
        print("🧪 Запуск тестов...")
        try:
            import subprocess
            subprocess.run([sys.executable, "test_root_solution.py"])
            self.status_label.setText("Статус: Тесты завершены")
        except Exception as e:
            self.status_label.setText(f"Статус: Ошибка - {e}")

def main():
    """Главная функция"""
    print("🚀 Запуск простого тестового GUI...")
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = SimpleTestGUI()
    window.show()
    
    print("✅ GUI окно создано и показано")
    print("📱 Ищите окно 'TheSolution CAD - Тестовый GUI' на экране")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
