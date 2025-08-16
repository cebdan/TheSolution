#!/usr/bin/env python3
"""
3D-Solution GUI - Главное окно 3D моделирования TheSolution CAD
Загружает UI файл 3D-solution_main.ui и предоставляет функциональность
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
                                   QTreeWidgetItem, QFileDialog, QSplitter)
    from PySide6.QtCore import Qt, QThread, Signal
    from PySide6.QtGui import QIcon, QFont
    from PySide6.QtUiTools import QUiLoader
    print("✅ PySide6 импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта PySide6: {e}")
    print("Установите: pip install PySide6")
    sys.exit(1)

class ObjectCreationWorker(QThread):
    """Поток для создания 3D объектов"""
    log_signal = Signal(str)
    finished_signal = Signal(bool, str)
    
    def __init__(self, object_type, name, params):
        super().__init__()
        self.object_type = object_type
        self.name = name
        self.params = params
    
    def run(self):
        try:
            from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate, SolutionMaterial
            
            # Создаем объект в зависимости от типа
            if self.object_type == "box":
                obj_data = SolutionDataUtils.create_minimal_solution_data(
                    name=self.name,
                    solution_type=SolutionType.BOX,
                    coordinate=SolutionCoordinate(0, 0, 0)
                )
                obj_data.dimensions.width = self.params.get('width', 10.0)
                obj_data.dimensions.height = self.params.get('height', 10.0)
                obj_data.dimensions.depth = self.params.get('depth', 10.0)
                volume = obj_data.dimensions.get_volume_box()
                
            elif self.object_type == "sphere":
                obj_data = SolutionDataUtils.create_minimal_solution_data(
                    name=self.name,
                    solution_type=SolutionType.SPHERE,
                    coordinate=SolutionCoordinate(0, 0, 0)
                )
                obj_data.dimensions.radius = self.params.get('radius', 5.0)
                volume = obj_data.dimensions.get_volume_sphere()
                
            elif self.object_type == "cylinder":
                obj_data = SolutionDataUtils.create_minimal_solution_data(
                    name=self.name,
                    solution_type=SolutionType.CYLINDER,
                    coordinate=SolutionCoordinate(0, 0, 0)
                )
                obj_data.dimensions.radius = self.params.get('radius', 5.0)
                obj_data.dimensions.height = self.params.get('height', 10.0)
                volume = obj_data.dimensions.get_volume_cylinder()
                
            else:
                raise ValueError(f"Неизвестный тип объекта: {self.object_type}")
            
            # Устанавливаем материал
            material_name = self.params.get('material', 'Steel')
            material_density = self.params.get('density', 7.85)
            obj_data.properties.material = SolutionMaterial(name=material_name, density=material_density)
            
            self.log_signal.emit(f"✅ Создан {obj_data.properties.name} - объем: {volume:.2f} куб.ед.")
            self.log_signal.emit(f"   Материал: {material_name} (плотность: {material_density})")
            self.finished_signal.emit(True, f"Объект {self.name} создан успешно")
            
        except Exception as e:
            self.log_signal.emit(f"❌ Ошибка создания объекта: {e}")
            self.finished_signal.emit(False, f"Ошибка: {e}")

class TheSolution3DMainWindow(QMainWindow):
    """Главное окно 3D-Solution"""
    
    def __init__(self):
        super().__init__()
        self.workers = []  # Храним ссылки на потоки
        self.objects_list = []  # Список созданных объектов
        self.load_ui()
        self.setup_connections()
        self.create_sample_objects()
        self.log_message("🚀 3D-Solution GUI запущен")
    
    def load_ui(self):
        """Загрузка UI из файла"""
        try:
            ui_file = Path(__file__).parent / "Gui" / "3D-solution_main.ui"
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
            self.setWindowTitle("TheSolution CAD - 3D-Solution")
            self.resize(1400, 900)
            
            # Устанавливаем стили
            self.setup_styles()
            
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Не удалось загрузить UI: {e}")
            sys.exit(1)
    
    def setup_styles(self):
        """Настройка стилей"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
                color: white;
            }
            
            QTreeWidget {
                background: rgba(44, 62, 80, 0.9);
                border: 2px solid #34495e;
                border-radius: 8px;
                color: white;
                font-size: 13px;
            }
            
            QTreeWidget::item {
                padding: 8px;
                border-bottom: 1px solid #34495e;
            }
            
            QTreeWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border: 2px solid #2980b9;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                padding: 8px;
                font-size: 12px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
                border: 2px solid #5dade2;
            }
            
            QTextEdit {
                background: rgba(44, 62, 80, 0.9);
                border: 2px solid #34495e;
                border-radius: 8px;
                color: white;
                font-family: "Consolas", monospace;
                font-size: 12px;
            }
            
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
    
    def setup_connections(self):
        """Настройка соединений сигналов"""
        # Кнопки создания объектов
        if hasattr(self, 'createBoxButton'):
            self.createBoxButton.clicked.connect(lambda: self.create_object_dialog("box"))
        if hasattr(self, 'createSphereButton'):
            self.createSphereButton.clicked.connect(lambda: self.create_object_dialog("sphere"))
        if hasattr(self, 'createCylinderButton'):
            self.createCylinderButton.clicked.connect(lambda: self.create_object_dialog("cylinder"))
        
        # Кнопки операций
        if hasattr(self, 'deleteObjectButton'):
            self.deleteObjectButton.clicked.connect(self.delete_selected_object)
        if hasattr(self, 'exportButton'):
            self.exportButton.clicked.connect(self.export_objects)
        if hasattr(self, 'importButton'):
            self.importButton.clicked.connect(self.import_objects)
    
    def create_sample_objects(self):
        """Создание примерных объектов"""
        try:
            from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate, SolutionMaterial
            
            # Создаем куб
            box = SolutionDataUtils.create_minimal_solution_data(
                name="Примерный Куб",
                solution_type=SolutionType.BOX,
                coordinate=SolutionCoordinate(0, 0, 0)
            )
            box.dimensions.width = 10.0
            box.dimensions.height = 10.0
            box.dimensions.depth = 10.0
            box.properties.material = SolutionMaterial(name="Steel", density=7.85)
            self.objects_list.append(box)
            
            # Создаем сферу
            sphere = SolutionDataUtils.create_minimal_solution_data(
                name="Примерная Сфера",
                solution_type=SolutionType.SPHERE,
                coordinate=SolutionCoordinate(15, 0, 0)
            )
            sphere.dimensions.radius = 5.0
            sphere.properties.material = SolutionMaterial(name="Aluminum", density=2.7)
            self.objects_list.append(sphere)
            
            # Создаем цилиндр
            cylinder = SolutionDataUtils.create_minimal_solution_data(
                name="Примерный Цилиндр",
                solution_type=SolutionType.CYLINDER,
                coordinate=SolutionCoordinate(0, 15, 0)
            )
            cylinder.dimensions.radius = 3.0
            cylinder.dimensions.height = 8.0
            cylinder.properties.material = SolutionMaterial(name="Copper", density=8.96)
            self.objects_list.append(cylinder)
            
            self.update_objects_tree()
            self.log_message("✅ Примерные объекты созданы")
            
        except Exception as e:
            self.log_message(f"❌ Ошибка создания примерных объектов: {e}")
    
    def update_objects_tree(self):
        """Обновление дерева объектов"""
        try:
            from solution_data_types import SolutionType
            
            if hasattr(self, 'solutionTree'):
                self.solutionTree.clear()
                
                for obj in self.objects_list:
                    item = QTreeWidgetItem(self.solutionTree)
                    item.setText(0, obj.properties.name)
                    item.setText(1, obj.properties.solution_type.value)
                    item.setText(2, f"ID: {obj.properties.index.numeric_id}")
                    
                    # Добавляем информацию о материале как tooltip
                    material_info = f"Материал: {obj.properties.material.name}\nПлотность: {obj.properties.material.density}"
                    item.setToolTip(0, material_info)
                    
                    # Устанавливаем цвет в зависимости от типа
                    if obj.properties.solution_type == SolutionType.BOX:
                        item.setBackground(0, Qt.blue)
                    elif obj.properties.solution_type == SolutionType.SPHERE:
                        item.setBackground(0, Qt.green)
                    elif obj.properties.solution_type == SolutionType.CYLINDER:
                        item.setBackground(0, Qt.yellow)
                
                self.log_message(f"📋 Дерево объектов обновлено: {len(self.objects_list)} объектов")
                
        except Exception as e:
            self.log_message(f"❌ Ошибка обновления дерева: {e}")
    
    def create_object_dialog(self, object_type):
        """Диалог создания объекта"""
        try:
            # Простой диалог для создания объекта
            name, ok = QFileDialog.getSaveFileName(
                self, 
                f"Создать {object_type}", 
                f"Новый_{object_type}",
                "All Files (*)"
            )
            
            if ok and name:
                # Параметры по умолчанию
                params = {
                    'box': {'width': 10.0, 'height': 10.0, 'depth': 10.0, 'material': 'Steel', 'density': 7.85},
                    'sphere': {'radius': 5.0, 'material': 'Aluminum', 'density': 2.7},
                    'cylinder': {'radius': 3.0, 'height': 8.0, 'material': 'Copper', 'density': 8.96}
                }
                
                # Создаем объект в отдельном потоке
                worker = ObjectCreationWorker(object_type, name, params[object_type])
                worker.log_signal.connect(self.log_message)
                worker.finished_signal.connect(self.on_object_created)
                
                self.workers.append(worker)
                worker.start()
                
        except Exception as e:
            self.log_message(f"❌ Ошибка создания диалога: {e}")
    
    def on_object_created(self, success, message):
        """Обработка создания объекта"""
        if success:
            self.log_message(f"✅ {message}")
            # Здесь можно добавить объект в список и обновить дерево
        else:
            self.log_message(f"❌ {message}")
    
    def delete_selected_object(self):
        """Удаление выбранного объекта"""
        try:
            if hasattr(self, 'solutionTree'):
                current_item = self.solutionTree.currentItem()
                if current_item:
                    object_name = current_item.text(0)
                    # Здесь можно добавить логику удаления объекта
                    self.log_message(f"🗑️ Удаление объекта: {object_name}")
                else:
                    self.log_message("⚠️ Выберите объект для удаления")
        except Exception as e:
            self.log_message(f"❌ Ошибка удаления: {e}")
    
    def export_objects(self):
        """Экспорт объектов"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                "Экспорт объектов", 
                "thesolution_objects.json",
                "JSON Files (*.json)"
            )
            if filename:
                self.log_message(f"📤 Экспорт объектов в: {filename}")
        except Exception as e:
            self.log_message(f"❌ Ошибка экспорта: {e}")
    
    def import_objects(self):
        """Импорт объектов"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, 
                "Импорт объектов", 
                "",
                "JSON Files (*.json)"
            )
            if filename:
                self.log_message(f"📥 Импорт объектов из: {filename}")
        except Exception as e:
            self.log_message(f"❌ Ошибка импорта: {e}")
    
    def log_message(self, message):
        """Добавить сообщение в лог"""
        try:
            if hasattr(self, 'logTextEdit'):
                timestamp = datetime.now().strftime("%H:%M:%S")
                log_entry = f"[{timestamp}] {message}"
                
                self.logTextEdit.append(log_entry)
                
                # Прокручиваем к концу
                scrollbar = self.logTextEdit.verticalScrollBar()
                scrollbar.setValue(scrollbar.maximum())
            else:
                print(message)
        except Exception as e:
            print(f"Ошибка логирования: {e}")
    
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
    print("🚀 Запуск 3D-Solution GUI...")
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = TheSolution3DMainWindow()
    window.show()
    
    print("✅ 3D-Solution GUI окно создано и показано")
    print("📱 Ищите окно 'TheSolution CAD - 3D-Solution' на экране")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
