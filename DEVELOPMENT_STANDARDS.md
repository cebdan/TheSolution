# Development Standards for TheSolution CAD

## Language Requirements

### Code Language Standards
- **Comments**: Must be in English
- **Variable names**: Must be in English, use snake_case
- **Function names**: Must be in English, use snake_case
- **Class names**: Must be in English, use PascalCase
- **File names**: Must be in English, use snake_case
- **Module names**: Must be in English, use snake_case

### Interface Language Standards
- **All dialogs**: Must be in English
- **All messages**: Must be in English
- **All buttons**: Must be in English
- **All menus**: Must be in English
- **Error messages**: Must be in English
- **User prompts**: Must be in English

### Documentation Language
- **Code documentation**: Can be in Russian or English
- **User documentation**: Can be in Russian or English
- **API documentation**: Should be in English

## Code Style Examples

### ✅ Correct Examples
```python
# Create a 3D object with specified parameters
def create_3d_object(object_type, dimensions):
    """Create a 3D object with specified type and dimensions"""
    object_name = f"{object_type}_object"
    return object_name

class SolutionManager:
    """Manager for handling solution objects"""
    
    def __init__(self):
        self.objects = []
    
    def add_object(self, obj):
        """Add object to the solution"""
        self.objects.append(obj)
```

### ❌ Incorrect Examples
```python
# Создание 3D объекта с указанными параметрами
def создать_3d_объект(тип_объекта, размеры):
    """Создает 3D объект с указанным типом и размерами"""
    имя_объекта = f"{тип_объекта}_объект"
    return имя_объекта

class МенеджерРешений:
    """Менеджер для обработки объектов решений"""
    
    def __init__(self):
        self.объекты = []
    
    def добавить_объект(self, объект):
        """Добавить объект в решение"""
        self.объекты.append(объект)
```

## GUI Standards

### Dialog Examples
```python
# ✅ Correct - English dialogs
QMessageBox.information(self, "Success", "Object created successfully")
QMessageBox.warning(self, "Warning", "Please select an object first")
QMessageBox.critical(self, "Error", "Failed to create object")

# ❌ Incorrect - Russian dialogs
QMessageBox.information(self, "Успех", "Объект создан успешно")
QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите объект")
QMessageBox.critical(self, "Ошибка", "Не удалось создать объект")
```

### Button Labels
```python
# ✅ Correct
create_button = QPushButton("Create Object")
delete_button = QPushButton("Delete Object")
export_button = QPushButton("Export")

# ❌ Incorrect
create_button = QPushButton("Создать объект")
delete_button = QPushButton("Удалить объект")
export_button = QPushButton("Экспорт")
```

## File Naming Standards

### ✅ Correct File Names
- `solution_manager.py`
- `3d_object_creator.py`
- `opencascade_integration.py`
- `gui_interface.py`
- `test_basic_system.py`

### ❌ Incorrect File Names
- `менеджер_решений.py`
- `создатель_3d_объектов.py`
- `интеграция_opencascade.py`
- `интерфейс_gui.py`
- `тест_базовой_системы.py`

## Import Standards

### ✅ Correct Imports
```python
from solution_data_types import SolutionType, SolutionDataUtils
from opencascade_integration import OpenCascadeIntegration
from gui_components import MainWindow, ObjectDialog
```

### ❌ Incorrect Imports
```python
from типы_данных_решений import ТипРешения, УтилитыДанныхРешений
from интеграция_opencascade import ИнтеграцияOpenCascade
from компоненты_gui import ГлавноеОкно, ДиалогОбъектов
```

## Testing Standards

### Test Function Names
```python
# ✅ Correct
def test_create_box():
    """Test box creation functionality"""
    pass

def test_calculate_volume():
    """Test volume calculation"""
    pass

# ❌ Incorrect
def тест_создания_куба():
    """Тест функциональности создания куба"""
    pass

def тест_расчета_объема():
    """Тест расчета объема"""
    pass
```

## Documentation Standards

### Docstrings
```python
def create_3d_object(object_type, dimensions):
    """
    Create a 3D object with specified type and dimensions.
    
    Args:
        object_type (SolutionType): Type of object to create
        dimensions (dict): Object dimensions
        
    Returns:
        dict: Created object data
        
    Raises:
        ValueError: If invalid object type
    """
    pass
```

## Enforcement

### Code Review Checklist
- [ ] All comments are in English
- [ ] All variable names are in English
- [ ] All function names are in English
- [ ] All class names are in English
- [ ] All GUI elements are in English
- [ ] All error messages are in English
- [ ] All file names are in English

### Automated Checks
- Use linting tools to check for non-English identifiers
- Use spell checkers to verify English comments
- Use automated tests to verify GUI language

## Migration Guide

If you have existing code with Russian identifiers:

1. **Rename variables and functions** to English equivalents
2. **Translate comments** to English
3. **Update GUI text** to English
4. **Update documentation** as needed
5. **Run tests** to ensure functionality is preserved

### Example Migration
```python
# Before (Russian)
def создать_куб(размер):
    """Создает куб с указанным размером"""
    объем = размер ** 3
    return объем

# After (English)
def create_cube(size):
    """Create a cube with specified size"""
    volume = size ** 3
    return volume
```
