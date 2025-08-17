# GUI компоненты TheSolution CAD

## Обзор

GUI компоненты TheSolution CAD построены на основе Qt Designer и PySide6. Система использует .ui файлы для определения интерфейса, что позволяет легко редактировать дизайн в Qt Designer.

## Структура файлов

```
GUI/
├── thesolution_main.ui          # Главное окно приложения
├── create_object_dialog.ui      # Диалог создания объектов
├── ui_loader.py                 # Загрузчик UI файлов
└── README.md                    # Эта документация
```

## Основные компоненты

### 1. Главное окно (`thesolution_main.ui`)

Главное окно приложения содержит:

#### Левая панель - Дерево объектов
- **Дерево объектов** (`solutionTree`) - иерархическое представление объектов Solution
- **Кнопки создания объектов**:
  - Создать куб (`createBoxButton`)
  - Создать сферу (`createSphereButton`)
  - Создать цилиндр (`createCylinderButton`)
  - Создать сборку (`createAssemblyButton`)
  - Удалить объект (`deleteObjectButton`)

#### Центральная панель - 3D вид
- **Панель инструментов 3D** (`viewToolBar`) - инструменты навигации
- **3D вид** (`openGLWidget`) - область для отображения 3D объектов
- **Статусная строка 3D** (`viewStatusBar`) - информация о состоянии

#### Правая панель - Свойства
- **Редактор координат**:
  - X, Y, Z - позиционные координаты
  - A, B, C - ориентационные координаты
  - Кнопки "Применить" и "Сброс"
- **Таблица свойств** (`propertiesTable`) - дополнительные свойства объекта
- **Информационная панель** (`infoTextEdit`) - логи и сообщения

#### Главное меню
- **Файл** - операции с файлами (новый, открыть, сохранить, экспорт/импорт)
- **Правка** - стандартные операции редактирования
- **Вид** - управление отображением 3D
- **Инструменты** - дополнительные инструменты
- **Справка** - документация и информация

### 2. Диалог создания объектов (`create_object_dialog.ui`)

Диалоговое окно для создания новых объектов содержит:

- **Выбор типа объекта** (`objectTypeComboBox`) - куб, сфера, цилиндр, конус, тор, сборка
- **Имя объекта** (`objectNameEdit`) - поле для ввода имени
- **Параметры объекта** - специфичные для каждого типа параметры
- **Начальные координаты** - позиция и ориентация нового объекта

## Использование

### Загрузка UI файлов

```python
from GUI.ui_loader import TheSolutionMainWindow, CreateObjectDialog

# Создание главного окна
main_window = TheSolutionMainWindow()
main_window.show()

# Создание диалога
dialog = CreateObjectDialog(main_window)
if dialog.exec() == QDialog.Accepted:
    object_data = dialog.get_object_data()
    print(f"Создан объект: {object_data}")
```

### Работа с виджетами

```python
# Получение виджета по имени
tree_widget = main_window.ui_loader.get_widget_by_name(
    main_window.ui_widget, "solutionTree"
)

# Подключение сигналов
tree_widget.itemSelectionChanged.connect(on_selection_changed)
```

## Классы

### UILoader

Основной класс для загрузки UI файлов:

```python
loader = UILoader()
ui_widget = loader.load_ui_file("path/to/file.ui", parent_widget)
```

**Методы:**
- `load_ui_file(ui_file_path, parent=None)` - загружает UI файл
- `get_widget_by_name(ui_widget, widget_name)` - находит виджет по имени

### TheSolutionMainWindow

Главное окно приложения:

```python
window = TheSolutionMainWindow()
window.show()
```

**Основные методы:**
- `create_box()` - создание куба
- `create_sphere()` - создание сферы
- `create_cylinder()` - создание цилиндра
- `create_assembly()` - создание сборки
- `delete_object()` - удаление объекта
- `apply_coordinates()` - применение координат
- `reset_coordinates()` - сброс координат
- `log_info(message)` - логирование сообщений

### CreateObjectDialog

Диалог создания объектов:

```python
dialog = CreateObjectDialog(parent)
if dialog.exec() == QDialog.Accepted:
    data = dialog.get_object_data()
```

**Методы:**
- `get_object_data()` - получение данных объекта из диалога

## Редактирование в Qt Designer

### Открытие файлов

1. Запустите Qt Designer
2. Откройте файл `thesolution_main.ui` или `create_object_dialog.ui`
3. Внесите изменения в дизайн
4. Сохраните файл

### Рекомендации по дизайну

1. **Именование виджетов** - используйте понятные имена для виджетов
2. **Группировка** - группируйте связанные элементы в QGroupBox
3. **Размеры** - устанавливайте минимальные и максимальные размеры панелей
4. **Стили** - используйте CSS стили для кастомизации внешнего вида

### Добавление новых виджетов

1. Добавьте виджет в Qt Designer
2. Задайте уникальное имя (objectName)
3. В Python коде получите виджет по имени:
   ```python
   new_widget = ui_loader.get_widget_by_name(ui_widget, "newWidgetName")
   ```

## Интеграция с основным приложением

### Подключение к Solution системе

```python
import sys
sys.path.insert(0, '../Base Solution/python')
from base_solution import Solution
from solution_coordinate import SolutionCoordinate

class TheSolutionMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... загрузка UI ...
        self.solutions = []  # Список объектов Solution
    
    def create_box(self):
        # Создание объекта Solution
        box = Solution("Куб", SolutionCoordinate(0, 0, 0))
        self.solutions.append(box)
        self.update_tree()
        self.log_info("Куб создан")
```

### Обновление дерева объектов

```python
def update_tree(self):
    if not self.solution_tree:
        return
    
    self.solution_tree.clear()
    for solution in self.solutions:
        item = QTreeWidgetItem([solution.name])
        item.setData(0, Qt.UserRole, solution.id)
        self.solution_tree.addTopLevelItem(item)
```

## Тестирование

Для тестирования UI компонентов запустите:

```bash
cd GUI
python ui_loader.py
```

Это запустит тестовое приложение с загруженным UI.

## Расширение

### Добавление новых диалогов

1. Создайте .ui файл в Qt Designer
2. Создайте Python класс для работы с диалогом
3. Интегрируйте с основным приложением

### Добавление новых панелей

1. Добавьте панель в главное окно в Qt Designer
2. Создайте соответствующий класс в Python
3. Подключите сигналы и слоты

## Требования

- PySide6
- Qt Designer (для редактирования .ui файлов)
- Python 3.8+

## Лицензия

См. основной файл LICENSE проекта.
