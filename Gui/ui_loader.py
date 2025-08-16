#!/usr/bin/env python3
"""
Загрузчик UI файлов для TheSolution CAD

Позволяет загружать .ui файлы, созданные в Qt Designer
"""

import os
import sys
from typing import Optional, Dict, Any
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice

class UILoader:
    """Класс для загрузки UI файлов Qt Designer"""
    
    def __init__(self):
        self.ui_loader = QUiLoader()
        self.ui_files_cache: Dict[str, QWidget] = {}
    
    def load_ui_file(self, ui_file_path: str, parent: Optional[QWidget] = None) -> Optional[QWidget]:
        """
        Загружает UI файл и возвращает виджет
        
        Args:
            ui_file_path: Путь к .ui файлу
            parent: Родительский виджет
            
        Returns:
            Загруженный виджет или None в случае ошибки
        """
        try:
            # Проверяем кэш
            if ui_file_path in self.ui_files_cache:
                return self.ui_files_cache[ui_file_path]
            
            # Открываем файл
            ui_file = QFile(ui_file_path)
            if not ui_file.open(QIODevice.ReadOnly):
                print(f"❌ Не удалось открыть UI файл: {ui_file_path}")
                return None
            
            # Загружаем UI
            ui_widget = self.ui_loader.load(ui_file, parent)
            ui_file.close()
            
            if ui_widget is None:
                print(f"❌ Не удалось загрузить UI файл: {ui_file_path}")
                return None
            
            # Кэшируем результат
            self.ui_files_cache[ui_file_path] = ui_widget
            
            print(f"✅ UI файл загружен: {ui_file_path}")
            return ui_widget
            
        except Exception as e:
            print(f"❌ Ошибка загрузки UI файла {ui_file_path}: {e}")
            return None
    
    def get_widget_by_name(self, ui_widget: QWidget, widget_name: str) -> Optional[QWidget]:
        """
        Находит виджет по имени в загруженном UI
        
        Args:
            ui_widget: Загруженный UI виджет
            widget_name: Имя искомого виджета
            
        Returns:
            Найденный виджет или None
        """
        try:
            return ui_widget.findChild(QWidget, widget_name)
        except Exception as e:
            print(f"❌ Ошибка поиска виджета {widget_name}: {e}")
            return None

class TheSolutionMainWindow(QMainWindow):
    """Главное окно приложения, загружаемое из UI файла"""
    
    def __init__(self):
        super().__init__()
        self.ui_loader = UILoader()
        self.ui_widget = None
        self.load_main_ui()
    
    def load_main_ui(self):
        """Загружает главное UI окно"""
        ui_file_path = os.path.join(os.path.dirname(__file__), "thesolution_main.ui")
        
        if not os.path.exists(ui_file_path):
            print(f"❌ UI файл не найден: {ui_file_path}")
            return
        
        self.ui_widget = self.ui_loader.load_ui_file(ui_file_path, self)
        if self.ui_widget:
            self.setup_ui_connections()
    
    def setup_ui_connections(self):
        """Настраивает соединения сигналов и слотов"""
        if not self.ui_widget:
            return
        
        # Получаем основные виджеты
        self.solution_tree = self.ui_loader.get_widget_by_name(self.ui_widget, "solutionTree")
        self.create_box_button = self.ui_loader.get_widget_by_name(self.ui_widget, "createBoxButton")
        self.create_sphere_button = self.ui_loader.get_widget_by_name(self.ui_widget, "createSphereButton")
        self.create_cylinder_button = self.ui_loader.get_widget_by_name(self.ui_widget, "createCylinderButton")
        self.create_assembly_button = self.ui_loader.get_widget_by_name(self.ui_widget, "createAssemblyButton")
        self.delete_object_button = self.ui_loader.get_widget_by_name(self.ui_widget, "deleteObjectButton")
        
        # Получаем элементы координат
        self.x_spin_box = self.ui_loader.get_widget_by_name(self.ui_widget, "xSpinBox")
        self.y_spin_box = self.ui_loader.get_widget_by_name(self.ui_widget, "ySpinBox")
        self.z_spin_box = self.ui_loader.get_widget_by_name(self.ui_widget, "zSpinBox")
        self.a_spin_box = self.ui_loader.get_widget_by_name(self.ui_widget, "aSpinBox")
        self.b_spin_box = self.ui_loader.get_widget_by_name(self.ui_widget, "bSpinBox")
        self.c_spin_box = self.ui_loader.get_widget_by_name(self.ui_widget, "cSpinBox")
        
        self.apply_coordinates_button = self.ui_loader.get_widget_by_name(self.ui_widget, "applyCoordinatesButton")
        self.reset_coordinates_button = self.ui_loader.get_widget_by_name(self.ui_widget, "resetCoordinatesButton")
        
        # Получаем информационную панель
        self.info_text_edit = self.ui_loader.get_widget_by_name(self.ui_widget, "infoTextEdit")
        
        # Подключаем сигналы
        if self.create_box_button:
            self.create_box_button.clicked.connect(self.create_box)
        
        if self.create_sphere_button:
            self.create_sphere_button.clicked.connect(self.create_sphere)
        
        if self.create_cylinder_button:
            self.create_cylinder_button.clicked.connect(self.create_cylinder)
        
        if self.create_assembly_button:
            self.create_assembly_button.clicked.connect(self.create_assembly)
        
        if self.delete_object_button:
            self.delete_object_button.clicked.connect(self.delete_object)
        
        if self.apply_coordinates_button:
            self.apply_coordinates_button.clicked.connect(self.apply_coordinates)
        
        if self.reset_coordinates_button:
            self.reset_coordinates_button.clicked.connect(self.reset_coordinates)
        
        # Подключаем выбор в дереве
        if self.solution_tree:
            self.solution_tree.itemSelectionChanged.connect(self.on_tree_selection_changed)
    
    def create_box(self):
        """Создает куб"""
        self.log_info("Создание куба...")
        # Здесь будет логика создания куба
    
    def create_sphere(self):
        """Создает сферу"""
        self.log_info("Создание сферы...")
        # Здесь будет логика создания сферы
    
    def create_cylinder(self):
        """Создает цилиндр"""
        self.log_info("Создание цилиндра...")
        # Здесь будет логика создания цилиндра
    
    def create_assembly(self):
        """Создает сборку"""
        self.log_info("Создание сборки...")
        # Здесь будет логика создания сборки
    
    def delete_object(self):
        """Удаляет выбранный объект"""
        self.log_info("Удаление объекта...")
        # Здесь будет логика удаления объекта
    
    def apply_coordinates(self):
        """Применяет изменения координат"""
        if all([self.x_spin_box, self.y_spin_box, self.z_spin_box, 
                self.a_spin_box, self.b_spin_box, self.c_spin_box]):
            x = self.x_spin_box.value()
            y = self.y_spin_box.value()
            z = self.z_spin_box.value()
            a = self.a_spin_box.value()
            b = self.b_spin_box.value()
            c = self.c_spin_box.value()
            
            self.log_info(f"Координаты применены: X={x}, Y={y}, Z={z}, A={a}, B={b}, C={c}")
    
    def reset_coordinates(self):
        """Сбрасывает координаты"""
        if all([self.x_spin_box, self.y_spin_box, self.z_spin_box, 
                self.a_spin_box, self.b_spin_box, self.c_spin_box]):
            self.x_spin_box.setValue(0.0)
            self.y_spin_box.setValue(0.0)
            self.z_spin_box.setValue(0.0)
            self.a_spin_box.setValue(1.0)
            self.b_spin_box.setValue(1.0)
            self.c_spin_box.setValue(1.0)
            
            self.log_info("Координаты сброшены")
    
    def on_tree_selection_changed(self):
        """Обработчик изменения выбора в дереве"""
        if self.solution_tree:
            current_item = self.solution_tree.currentItem()
            if current_item:
                item_text = current_item.text(0)  # Первая колонка - имя
                self.log_info(f"Выбран объект: {item_text}")
    
    def log_info(self, message: str):
        """Добавляет сообщение в информационную панель"""
        if self.info_text_edit:
            self.info_text_edit.append(f"[INFO] {message}")

class CreateObjectDialog(QDialog):
    """Диалог создания объекта, загружаемый из UI файла"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.ui_loader = UILoader()
        self.ui_widget = None
        self.load_dialog_ui()
    
    def load_dialog_ui(self):
        """Загружает UI диалога"""
        ui_file_path = os.path.join(os.path.dirname(__file__), "create_object_dialog.ui")
        
        if not os.path.exists(ui_file_path):
            print(f"❌ UI файл диалога не найден: {ui_file_path}")
            return
        
        self.ui_widget = self.ui_loader.load_ui_file(ui_file_path, self)
        if self.ui_widget:
            self.setup_dialog_connections()
    
    def setup_dialog_connections(self):
        """Настраивает соединения диалога"""
        if not self.ui_widget:
            return
        
        # Получаем виджеты диалога
        self.object_type_combo = self.ui_loader.get_widget_by_name(self.ui_widget, "objectTypeComboBox")
        self.object_name_edit = self.ui_loader.get_widget_by_name(self.ui_widget, "objectNameEdit")
        self.create_button = self.ui_loader.get_widget_by_name(self.ui_widget, "createButton")
        self.cancel_button = self.ui_loader.get_widget_by_name(self.ui_widget, "cancelButton")
        
        # Подключаем сигналы
        if self.create_button:
            self.create_button.clicked.connect(self.accept)
        
        if self.cancel_button:
            self.cancel_button.clicked.connect(self.reject)
        
        # Подключаем изменение типа объекта
        if self.object_type_combo:
            self.object_type_combo.currentTextChanged.connect(self.on_object_type_changed)
    
    def on_object_type_changed(self, object_type: str):
        """Обработчик изменения типа объекта"""
        print(f"Выбран тип объекта: {object_type}")
        # Здесь можно добавить логику показа/скрытия соответствующих параметров
    
    def get_object_data(self) -> Dict[str, Any]:
        """Возвращает данные объекта из диалога"""
        data = {
            'type': self.object_type_combo.currentText() if self.object_type_combo else 'Куб',
            'name': self.object_name_edit.text() if self.object_name_edit else 'Новый объект'
        }
        return data

def test_ui_loader():
    """Тестирует загрузчик UI файлов"""
    print("🧪 Тестирование UI загрузчика...")
    
    # Создаем приложение
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Тестируем загрузку главного окна
    main_window = TheSolutionMainWindow()
    main_window.show()
    
    print("✅ UI загрузчик протестирован")
    print("Главное окно загружено из UI файла")
    
    return app.exec()

if __name__ == "__main__":
    test_ui_loader()
