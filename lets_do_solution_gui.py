#!/usr/bin/env python3
"""
Let's Do Solution GUI - Красивый интерфейс для работы с решениями TheSolution CAD
Загружает UI файл из Qt Designer и предоставляет функциональность
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Добавляем пути к модулям
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "Base Solution" / "python"))
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "Root Solution" / "python"))

try:
    from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                                   QTreeWidgetItem, QFileDialog)
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QIcon, QFont
    from PySide6.QtUiTools import QUiLoader
except ImportError:
    print("❌ Ошибка: PySide6 не установлен")
    print("Установите: pip install PySide6")
    sys.exit(1)

class SolutionWorker(QThread):
    """Поток для выполнения операций с решениями"""
    log_signal = Signal(str)
    finished_signal = Signal(bool, str)
    
    def __init__(self, operation, *args):
        super().__init__()
        self.operation = operation
        self.args = args
    
    def run(self):
        try:
            if self.operation == "launch_3d":
                self.launch_3d_solution()
            elif self.operation == "create_3d_objects":
                self.create_3d_objects()
            elif self.operation == "demo":
                self.run_demo()
            elif self.operation == "test":
                self.run_tests()
            elif self.operation == "root_launcher":
                self.launch_root_launcher()
            else:
                self.finished_signal.emit(False, f"Неизвестная операция: {self.operation}")
        except Exception as e:
            self.finished_signal.emit(False, f"Ошибка: {e}")
    
    def launch_3d_solution(self):
        self.log_signal.emit("🎯 Запуск 3D-Solution GUI...")
        try:
            # Запускаем 3D-Solution GUI в отдельном процессе без блокировки
            subprocess.Popen([sys.executable, "3d_solution_gui.py"], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.log_signal.emit("✅ 3D-Solution GUI запущен в отдельном окне")
            self.finished_signal.emit(True, "3D-Solution GUI запущен")
        except Exception as e:
            self.log_signal.emit(f"❌ Ошибка запуска: {e}")
            self.finished_signal.emit(False, f"Ошибка: {e}")
    
    def create_3d_objects(self):
        self.log_signal.emit("🔸 Создание 3D объектов...")
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
            
            self.log_signal.emit(f"✅ Создан {box.properties.name} - объем: {box.dimensions.get_volume_box():.2f} куб.ед.")
            self.log_signal.emit(f"✅ Создана {sphere.properties.name} - объем: {sphere.dimensions.get_volume_sphere():.2f} куб.ед.")
            self.finished_signal.emit(True, "3D объекты созданы")
            
        except Exception as e:
            self.log_signal.emit(f"❌ Ошибка создания объектов: {e}")
            self.finished_signal.emit(False, f"Ошибка: {e}")
    
    def run_demo(self):
        self.log_signal.emit("🎬 Запуск демонстрации...")
        result = subprocess.run([sys.executable, "demo_root_solution.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            self.log_signal.emit("✅ Демонстрация завершена")
            self.finished_signal.emit(True, "Демонстрация выполнена")
        else:
            self.log_signal.emit(f"❌ Ошибка демонстрации: {result.stderr}")
            self.finished_signal.emit(False, f"Ошибка: {result.stderr}")
    
    def run_tests(self):
        self.log_signal.emit("🧪 Запуск тестов...")
        result = subprocess.run([sys.executable, "test_root_solution.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            self.log_signal.emit("✅ Тесты пройдены успешно")
            self.finished_signal.emit(True, "Тесты пройдены")
        else:
            self.log_signal.emit(f"❌ Ошибка тестов: {result.stderr}")
            self.finished_signal.emit(False, f"Ошибка: {result.stderr}")
    
    def launch_root_launcher(self):
        self.log_signal.emit("🏗️ Запуск Root Solution Launcher...")
        result = subprocess.run([sys.executable, "Root Solution/main.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            self.log_signal.emit("✅ Root Solution Launcher запущен")
            self.finished_signal.emit(True, "Root Solution Launcher запущен")
        else:
            self.log_signal.emit(f"❌ Ошибка запуска: {result.stderr}")
            self.finished_signal.emit(False, f"Ошибка: {result.stderr}")

class LetsDoSolutionGUI(QMainWindow):
    """Главное окно Let's Do Solution"""
    
    def __init__(self):
        super().__init__()
        self.workers = []  # Храним ссылки на потоки
        self.load_ui()
        self.setup_connections()
        self.load_solutions_tree()
        self.log_message("🚀 Let's Do Solution GUI запущен")
    
    def load_ui(self):
        """Загрузка UI из файла"""
        try:
            ui_file = Path(__file__).parent / "Gui" / "lets_do_solution.ui"
            if not ui_file.exists():
                raise FileNotFoundError(f"UI файл не найден: {ui_file}")
            
            loader = QUiLoader()
            self.ui = loader.load(str(ui_file))
            
            if not self.ui:
                raise RuntimeError("Ошибка загрузки UI файла")
            
            # Копируем все виджеты из загруженного UI
            for attr_name in dir(self.ui):
                if not attr_name.startswith('_'):
                    setattr(self, attr_name, getattr(self.ui, attr_name))
            
            self.setCentralWidget(self.ui.centralwidget)
            self.setWindowTitle("TheSolution CAD - Let's Do Solution")
            self.resize(1200, 800)
            
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load UI: {e}")
            sys.exit(1)
    
    def setup_connections(self):
        """Настройка соединений сигналов"""
        # 3D-Solution кнопки
        self.launch3DButton.clicked.connect(lambda: self.run_solution_operation("launch_3d"))
        self.create3DObjectsButton.clicked.connect(lambda: self.run_solution_operation("create_3d_objects"))
        self.geometryButton.clicked.connect(self.show_not_implemented)
        
        # Инструменты
        self.rootLauncherButton.clicked.connect(lambda: self.run_solution_operation("root_launcher"))
        self.demoButton.clicked.connect(lambda: self.run_solution_operation("demo"))
        self.testButton.clicked.connect(lambda: self.run_solution_operation("test"))
        self.infoButton.clicked.connect(self.show_solutions_info)
        self.refreshButton.clicked.connect(self.load_solutions_tree)
        
        # Все остальные кнопки решений (показывают "не реализовано")
        solution_buttons = [
            'launch2DButton', 'createDrawingsButton',
            'launchAssemblyButton', 'createAssembliesButton',
            'launchAnalysisButton', 'analysisButton',
            'launchSimulationButton', 'simulationButton',
            'launchManufacturingButton', 'manufacturingButton',
            'launchDocumentationButton', 'documentationButton',
            'launchCollaborationButton', 'collaborationButton'
        ]
        
        for button_name in solution_buttons:
            if hasattr(self, button_name):
                button = getattr(self, button_name)
                if hasattr(button, 'clicked'):
                    button.clicked.connect(self.show_not_implemented)
    
    def load_solutions_tree(self):
        """Загрузка дерева решений"""
        try:
            self.solutionsTree.clear()
            
            import importlib.util
            
            # Динамический импорт root_solution_manager
            spec = importlib.util.spec_from_file_location(
                "root_solution_manager", 
                Path(__file__).parent / "Root Solution" / "python" / "root_solution_manager.py"
            )
            root_solution_manager = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(root_solution_manager)
            
            manager = root_solution_manager.get_root_manager()
            solutions_info = manager.get_all_solutions_info()
            
            for name, info in solutions_info.items():
                item = QTreeWidgetItem(self.solutionsTree)
                item.setText(0, name)
                
                status_icon = "✅" if info["status"] == "active" else "⏸️"
                item.setText(1, status_icon)
                item.setText(2, info["solution_type"])
                
                # Устанавливаем цвет в зависимости от статуса
                if info["status"] == "active":
                    item.setBackground(0, Qt.green)
                else:
                    item.setBackground(0, Qt.gray)
            
            self.log_message("📋 Дерево решений обновлено")
            
        except Exception as e:
            self.log_message(f"❌ Ошибка загрузки дерева: {e}")
    
    def run_solution_operation(self, operation):
        """Запуск операции с решением в отдельном потоке"""
        self.log_message(f"🔄 Запуск операции: {operation}")
        self.statusLabel.setText(f"Статус: Выполняется {operation}")
        self.progressBar.setValue(50)
        
        # Создаем и запускаем поток
        worker = SolutionWorker(operation)
        worker.log_signal.connect(self.log_message)
        worker.finished_signal.connect(self.on_operation_finished)
        
        self.workers.append(worker)  # Сохраняем ссылку
        worker.start()
    
    def on_operation_finished(self, success, message):
        """Обработка завершения операции"""
        if success:
            self.statusLabel.setText("Статус: Операция завершена успешно")
            self.progressBar.setValue(100)
            self.log_message(f"✅ {message}")
        else:
            self.statusLabel.setText("Статус: Ошибка выполнения")
            self.progressBar.setValue(0)
            self.log_message(f"❌ {message}")
    
    def show_solutions_info(self):
        """Показать информацию о решениях"""
        try:
            import importlib.util
            
            # Динамический импорт root_solution_manager
            spec = importlib.util.spec_from_file_location(
                "root_solution_manager", 
                Path(__file__).parent / "Root Solution" / "python" / "root_solution_manager.py"
            )
            root_solution_manager = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(root_solution_manager)
            
            manager = root_solution_manager.get_root_manager()
            solutions_info = manager.get_all_solutions_info()
            
            info_text = "📋 Информация о решениях:\n"
            info_text += "=" * 40 + "\n\n"
            
            for name, info in solutions_info.items():
                status_icon = "✅" if info["status"] == "active" else "⏸️"
                info_text += f"{status_icon} {name}:\n"
                info_text += f"   Описание: {info['description']}\n"
                info_text += f"   Тип: {info['solution_type']}\n"
                info_text += f"   Статус: {info['status']}\n\n"
            
            active_count = len([s for s in solutions_info.values() if s["status"] == "active"])
            info_text += f"📊 Активных решений: {active_count}/{len(solutions_info)}"
            
            self.logTextEdit.setText(info_text)
            self.log_message("📋 Информация о решениях загружена")
            
        except Exception as e:
            self.log_message(f"❌ Ошибка получения информации: {e}")
    
    def show_not_implemented(self):
        """Показать сообщение о том, что функция не реализована"""
        sender = self.sender()
        if sender:
            button_text = sender.text()
            QMessageBox.information(self, "🚧 Function in development", 
                                  f"Функция '{button_text}' пока не реализована.\n\n"
                                  "✅ Доступные функции:\n"
                                  "• 🚀 Запустить 3D-Solution\n"
                                  "• 🔸 Создать 3D объекты\n"
                                  "• 🏗️ Root Solution Launcher\n"
                                  "• 🎬 Демонстрация возможностей\n"
                                  "• 🧪 Тестирование системы\n\n"
                                  "🔄 В разработке:\n"
                                  "• 2D-Solution\n"
                                  "• Assembly-Solution\n"
                                  "• Analysis-Solution\n"
                                  "• Simulation-Solution\n"
                                  "• Manufacturing-Solution\n"
                                  "• Documentation-Solution\n"
                                  "• Collaboration-Solution")
    
    def log_message(self, message):
        """Добавить сообщение в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        # Добавляем в текстовое поле
        self.logTextEdit.append(log_entry)
        
        # Прокручиваем к концу
        scrollbar = self.logTextEdit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        # Останавливаем все потоки
        for worker in self.workers:
            if worker.isRunning():
                worker.terminate()
                worker.wait()
        
        event.accept()

def main():
    """Главная функция"""
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль приложения
    app.setStyle('Fusion')
    
    # Создаем и показываем главное окно
    window = LetsDoSolutionGUI()
    window.show()
    
    # Запускаем приложение
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
