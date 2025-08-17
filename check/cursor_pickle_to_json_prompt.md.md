# 🤖 Промт для Cursor: Замена pickle на JSON в TheSolution CAD

## 📋 ЗАДАЧА ДЛЯ CURSOR

**Контекст**: Проект TheSolution CAD - система CAD на основе Root Solution архитектуры с Python классами Solution, SolutionCoordinate и системой типов данных.

**Критическая задача безопасности**: Заменить все использования pickle на безопасный JSON формат для сериализации/десериализации проектов.

## 🎯 ЧТО НУЖНО СДЕЛАТЬ

### 1. СОЗДАТЬ СИСТЕМУ БЕЗОПАСНОЙ СЕРИАЛИЗАЦИИ

Создай файл `project/safe_serializer.py` с классами:

```python
class SolutionJSONEncoder:
    """Конвертирует Solution объекты в JSON-совместимые словари"""
    
    @staticmethod
    def solution_to_dict(solution) -> Dict[str, Any]:
        # Должен обрабатывать:
        # - Базовый класс Solution 
        # - BoxSolution, SphereSolution, CylinderSolution
        # - AssemblySolution с компонентами
        # - SolutionCoordinate (x,y,z,a,b,c)
        # - Иерархию parent/children
        # - Свойства properties
        # - Метаданные (created_at, version, etc)
        pass
    
    @staticmethod  
    def coordinate_to_dict(coordinate) -> Dict[str, float]:
        # Конвертирует SolutionCoordinate в простой словарь
        pass
    
    @staticmethod
    def project_to_dict(solutions: List, metadata: Dict = None) -> Dict[str, Any]:
        # Создает полную структуру проекта с заголовком, версией, контрольной суммой
        pass

class SolutionJSONDecoder:
    """Конвертирует JSON обратно в Solution объекты"""
    
    @staticmethod
    def dict_to_solution(data: Dict[str, Any], parent=None):
        # Создает правильный тип Solution на основе "type" поля
        # Восстанавливает все свойства и связи
        pass
    
    @staticmethod
    def dict_to_project(data: Dict[str, Any]) -> List:
        # Загружает весь проект с валидацией формата
        pass

class SafeProjectManager:
    """Основной API для сохранения/загрузки проектов"""
    
    @staticmethod
    def save_project(solutions: List, filename: str, metadata: Dict = None) -> bool:
        # Главный метод сохранения - заменяет все pickle.dump()
        pass
    
    @staticmethod  
    def load_project(filename: str) -> List:
        # Главный метод загрузки - заменяет все pickle.load()
        pass
    
    @staticmethod
    def validate_project_file(filename: str) -> bool:
        # Проверка файла без загрузки (для безопасности)
        pass
```

### 2. ОБНОВИТЬ СУЩЕСТВУЮЩИЕ ФАЙЛЫ

**Найди и замени ВСЕ использования pickle в проекте:**

В файлах вида:
- `project/project_manager.py` 
- `Root Solution/*/main_*.py`
- `**/file_handler.py`
- `**/save_load.py`

**Замени конструкции:**
```python
# ❌ УБРАТЬ:
import pickle
pickle.dump(data, file)
pickle.load(file) 
pickle.dumps(data)
pickle.loads(data)

# ✅ ЗАМЕНИТЬ НА:
from project.safe_serializer import SafeProjectManager
SafeProjectManager.save_project(solutions, filename)
SafeProjectManager.load_project(filename)
```

### 3. СОЗДАТЬ ТЕСТЫ

Создай `tests/test_safe_serialization.py`:

```python
def test_solution_serialization():
    """Тест сериализации базового Solution"""
    # Создай Solution объект
    # Сериализуй в JSON
    # Десериализуй обратно  
    # Проверь что все поля совпадают
    pass

def test_coordinate_serialization():
    """Тест SolutionCoordinate"""
    # Создай SolutionCoordinate
    # Проверь точность float значений
    pass

def test_hierarchy_serialization():
    """Тест иерархии parent/children"""
    # Создай дерево объектов
    # Проверь что связи восстанавливаются правильно
    pass

def test_complex_project():
    """Тест сложного проекта с разными типами Solution"""
    # BoxSolution, SphereSolution, AssemblySolution
    # Сохрани и загрузи
    # Проверь целостность
    pass

def test_malicious_json():
    """Тест безопасности - попытка загрузить вредоносный JSON"""
    # Создай JSON с подозрительными данными
    # Убедись что не выполняется код
    pass

def test_large_file_protection():
    """Тест защиты от слишком больших файлов"""
    pass

def test_migration_from_pickle():
    """Тест миграции старых pickle файлов"""
    pass
```

### 4. СОЗДАТЬ УТИЛИТЫ МИГРАЦИИ

Создай `scripts/migrate_pickle_to_json.py`:

```python
def migrate_project_files(directory: str):
    """Найти все .pickle файлы и конвертировать в .json"""
    # Найти файлы *.pickle, *.pkl
    # Конвертировать через SafeProjectManager
    # Создать резервные копии
    # Логировать процесс
    pass

def validate_migration(old_pickle: str, new_json: str):
    """Проверить что миграция прошла корректно"""
    pass

if __name__ == "__main__":
    # CLI интерфейс для миграции
    pass
```

### 5. ОБНОВИТЬ ДОКУМЕНТАЦИЮ

**В файле `отчет_разработки.md` добавь секцию:**

```markdown
## 🔒 Миграция на безопасную сериализацию (дата)

### ✅ Выполнено:
- Заменен pickle на JSON для всех операций сохранения/загрузки
- Создана система SafeProjectManager для безопасной работы с файлами
- Добавлены тесты безопасности и валидации
- Создан инструмент миграции старых файлов

### 🔧 Технические детали:
- JSON формат: TheSolution_JSON v1.0
- Поддержка всех типов Solution объектов
- Валидация и контрольные суммы
- Защита от больших файлов и вредоносного контента

### 📋 Файлы:
- `project/safe_serializer.py` - основная система
- `tests/test_safe_serialization.py` - тесты
- `scripts/migrate_pickle_to_json.py` - миграция
```

## 🎯 ОСОБЫЕ ТРЕБОВАНИЯ

### БЕЗОПАСНОСТЬ:
- ✅ НЕ используй `eval()`, `exec()`, `__import__()`
- ✅ Валидируй ВСЕ входные данные  
- ✅ Ограничивай размер файлов
- ✅ Проверяй формат и версию

### СОВМЕСТИМОСТЬ:
- ✅ Сохрани все существующие API
- ✅ Сделай обратную совместимость если возможно
- ✅ Добавь четкие сообщения об ошибках

### ПРОИЗВОДИТЕЛЬНОСТЬ:  
- ✅ JSON должен быть компактным
- ✅ Быстрая загрузка для больших проектов
- ✅ Ленивая загрузка если нужно

### ОТЛАДКА:
- ✅ JSON файлы должны быть читаемыми
- ✅ Красивое форматирование с отступами
- ✅ Подробное логирование ошибок

## 🧪 ПРОВЕРИТЬ РЕЗУЛЬТАТ

**После выполнения запусти тесты:**
```bash
python -m pytest tests/test_safe_serialization.py -v
python scripts/migrate_pickle_to_json.py --test
python test_basic_system.py  # Должен работать как раньше
python test_root_solution.py  # Должен работать как раньше
```

**Проверь что создались файлы:**
- `project/safe_serializer.py`
- `tests/test_safe_serialization.py` 
- `scripts/migrate_pickle_to_json.py`

**Убедись что заменились импорты pickle во всех файлах проекта.**

## 🚀 ДОПОЛНИТЕЛЬНЫЕ ЗАДАЧИ

1. **Создай пример использования** в `examples/save_load_example.py`
2. **Добавь поддержку** файлов `.3d_sol` через JSON
3. **Создай валидатор** JSON схемы для файлов проекта
4. **Добавь сжатие** больших JSON файлов (gzip)

---

**ВАЖНО**: Это критическая задача безопасности. Убедись что ВСЕ использования pickle удалены из проекта и заменены на безопасную JSON сериализацию!