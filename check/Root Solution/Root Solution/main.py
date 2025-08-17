#!/usr/bin/env python3
"""
Root Solution - Главный запускающий файл TheSolution CAD
Управляет 8 основными решениями с фокусом на 3D моделирование
"""

import sys
import os
from pathlib import Path

# Добавляем пути к модулям
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "Base Solution" / "python"))
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "Root Solution" / "python"))

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QTreeWidget, QTreeWidgetItem
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont
except ImportError:
    print("❌ PySide6 не установлен")
    sys.exit(1)

try:
    from root_solution_manager import get_root_manager, SolutionStatus
    from solution_data_types import SolutionType
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)

class RootSolutionLauncher(QMainWindow):
    """
    Главное окно Root Solution Launcher
    Интерфейс для управления всеми решениями TheSolution CAD
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TheSolution CAD - Root Solution Launcher")
        self.setGeometry(100, 100, 1200, 800)
        
        # Инициализация менеджера
        self.root_manager = get_root_manager()
        
        self.setup_ui()
        self.load_solutions_info()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Левая панель - список решений
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Центральная панель - информация и управление
        center_panel = self.create_center_panel()
        main_layout.addWidget(center_panel, 2)
        
        # Правая панель - статус и логи
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
    
    def create_left_panel(self):
        """Левая панель со списком решений"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Заголовок
        title = QLabel("Root Solutions")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Дерево решений
        self.solutions_tree = QTreeWidget()
        self.solutions_tree.setHeaderLabels(["Решение", "Статус", "Тип"])
        self.solutions_tree.itemClicked.connect(self.on_solution_selected)
        layout.addWidget(self.solutions_tree)
        
        # Кнопки управления
        layout.addWidget(QLabel("Управление:"))
        
        btn_launch_3d = QPushButton("🚀 Launch 3D-Solution")
        btn_launch_3d.clicked.connect(self.launch_3d_solution)
        layout.addWidget(btn_launch_3d)
        
        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.clicked.connect(self.load_solutions_info)
        layout.addWidget(btn_refresh)
        
        return widget
    
    def create_center_panel(self):
        """Центральная панель с информацией"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Заголовок
        title = QLabel("Информация о решении")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Информация о выбранном решении
        self.solution_info = QTextEdit()
        self.solution_info.setReadOnly(True)
        self.solution_info.setMaximumHeight(200)
        layout.addWidget(self.solution_info)
        
        # Кнопки управления решением
        layout.addWidget(QLabel("Действия:"))
        
        btn_activate = QPushButton("✅ Activate")
        btn_activate.clicked.connect(self.activate_selected_solution)
        layout.addWidget(btn_activate)
        
        btn_deactivate = QPushButton("⏸️ Deactivate")
        btn_deactivate.clicked.connect(self.deactivate_selected_solution)
        layout.addWidget(btn_deactivate)
        
        layout.addStretch()
        
        return widget
    
    def create_right_panel(self):
        """Правая панель со статусом"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Заголовок
        title = QLabel("Статус системы")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Статус
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)
        
        return widget
    
    def load_solutions_info(self):
        """Загрузка информации о решениях"""
        self.solutions_tree.clear()
        
        solutions_info = self.root_manager.get_all_solutions_info()
        
        for name, info in solutions_info.items():
            # Определяем иконку статуса
            status_icon = "✅" if info["status"] == "active" else "⏸️"
            
            item = QTreeWidgetItem([
                name,
                f"{status_icon} {info['status']}",
                info["type"]
            ])
            
            # Устанавливаем данные для идентификации
            item.setData(0, Qt.UserRole, name)
            
            self.solutions_tree.addTopLevelItem(item)
        
        # Обновляем статус
        self.update_status()
    
    def on_solution_selected(self, item, column):
        """Обработка выбора решения"""
        solution_name = item.data(0, Qt.UserRole)
        solution = self.root_manager.get_solution(solution_name)
        
        if solution:
            info = solution.get_info()
            
            info_text = f"""
🎯 Решение: {info['name']}
📝 Описание: {solution.description}
🔧 Тип: {info['type']}
📊 Статус: {info['status']}
🔗 Под-решения: {info['sub_solutions_count']}

💡 Действия:
• Двойной клик для активации/деактивации
• Используйте кнопки управления
• 3D-Solution можно запустить отдельно
            """
            
            self.solution_info.setText(info_text)
    
    def activate_selected_solution(self):
        """Активация выбранного решения"""
        current_item = self.solutions_tree.currentItem()
        if current_item:
            solution_name = current_item.data(0, Qt.UserRole)
            if self.root_manager.activate_solution(solution_name):
                self.load_solutions_info()
                self.update_status()
                print(f"✅ Решение {solution_name} активировано")
    
    def deactivate_selected_solution(self):
        """Деактивация выбранного решения"""
        current_item = self.solutions_tree.currentItem()
        if current_item:
            solution_name = current_item.data(0, Qt.UserRole)
            if self.root_manager.deactivate_solution(solution_name):
                self.load_solutions_info()
                self.update_status()
                print(f"⏸️ Решение {solution_name} деактивировано")
    
    def launch_3d_solution(self):
        """Запуск 3D-Solution"""
        print("🎯 Запуск 3D-Solution...")
        
        try:
            # Импорт и запуск 3D-Solution
            sys.path.insert(0, str(project_root / "Root Solution" / "3D-Solution"))
            from main_3d import launch_3d_solution
            
            window = launch_3d_solution()
            if window:
                print("✅ 3D-Solution успешно запущен")
                self.update_status()
            else:
                print("❌ Ошибка запуска 3D-Solution")
                
        except ImportError as e:
            print(f"❌ Ошибка импорта 3D-Solution: {e}")
        except Exception as e:
            print(f"❌ Ошибка запуска: {e}")
    
    def update_status(self):
        """Обновление статуса системы"""
        active_solutions = self.root_manager.get_active_solutions()
        total_solutions = len(self.root_manager.solutions)
        
        status_text = f"""
🏗️ TheSolution CAD - Root Solution Manager

📊 Статистика:
• Всего решений: {total_solutions}
• Активных: {len(active_solutions)}
• Неактивных: {total_solutions - len(active_solutions)}

🎯 Приоритетное решение:
• 3D-Solution: {'✅ Активно' if self.root_manager.get_3d_solution() and self.root_manager.get_3d_solution().status == SolutionStatus.ACTIVE else '⏸️ Неактивно'}

🚀 Доступные действия:
• Запуск 3D-Solution
• Активация/деактивация решений
• Управление иерархией

💡 Подсказка: Выберите решение в левой панели для получения подробной информации
        """
        
        self.status_text.setText(status_text)

def main():
    """Главная функция"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    print("🏗️ Запуск Root Solution Manager...")
    
    window = RootSolutionLauncher()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
