# Промты для разработки TheSolution в Cursor

## 🎯 ОСНОВНОЙ ПРОМТ ПРОЕКТА

```
Ты работаешь над проектом TheSolution - платформой CAD решений на основе Root Solution архитектуры.

АРХИТЕКТУРА:
- Root Solution платформа с 8 типами решений (3D, Draft, CAM, 2D, Render, BOM, Script, System)
- Текущий фокус: 3D-Solution с минимальным C++ ядром
- Система типов данных как основа (SolutionData, SolutionCoordinate из data_types/) 
- Python-первый подход с минимальным C++ для критичных операций

СТРУКТУРА ПРОЕКТА:
- DEVELOPMENT_REPORT.md - ГЛАВНЫЙ файл, мозг проекта
- Let's do Solution.py - точка входа в систему
- Root Solution/ - папка с 8 решениями (фокус на 3D-Solution/)
- data_types/ - система типов данных (готова)
- core/ - C++ ядро с pybind11

ОБЯЗАТЕЛЬНО:
- Все изменения записывать в DEVELOPMENT_REPORT.md 
- Использовать систему типов данных: SolutionReal, SolutionString, SolutionCoordinate
- Поддерживать Root Solution архитектуру
- Код должен быть понятным с подробными комментариями
- Отчитываться Claude координатору через отчет

ТЕКУЩИЙ ЭТАП: Root Solution инфраструктура + 3D ядро
ПРИОРИТЕТ: Создать главное меню выбора решений
```

## 🏠 ПРОМТ ДЛЯ ROOT SOLUTION

```
Ты работаешь над Root Solution инфраструктурой проекта TheSolution.

ЗАДАЧА:
- Создать главное меню выбора решений в Let's do Solution.py
- GUI селектор в gui/main_selector/ с PySide6
- Навигация между 8 типами решений
- Модульная архитектура для независимых решений

8 РЕШЕНИЙ ПЛАТФОРМЫ:
- 🎯 3D-Solution (в разработке) - 3D моделирование
- 📐 Draft-Solution (планируется) - 2D черчение  
- 🔧 CAM-Solution (планируется) - ЧПУ обработка
- 📏 2D-Solution (планируется) - 2D геометрия
- 🎨 Render-Solution (планируется) - рендеринг
- 📋 BOM-Solution (планируется) - спецификации
- 🐍 Script-Solution (планируется) - автоматизация
- ⚙️ System-Solution (планируется) - расширения

ПРИНЦИПЫ:
- Каждое решение независимо
- Общая система типов данных
- Единая точка входа через главное меню
- PySide6 для всего GUI
- Красивый современный интерфейс

КОД СТИЛЬ:
- from data_types import SolutionString, SolutionBool
- Подробные docstring
- Примеры использования в комментариях
```

## 🎯 ПРОМТ ДЛЯ 3D-SOLUTION

```
Ты работаешь над 3D-Solution частью проекта TheSolution.

КОНТЕКСТ:
- 3D-Solution находится в Root Solution/3D-Solution/
- Использует систему типов данных из data_types/
- C++ ядро в core/ с pybind11 биндингами
- Основа: SolutionCoordinate (x,y,z,a,b,c) + SolutionData

ЗАДАЧИ ЭТАПА:
- main_3d.py - точка входа в 3D решение
- Примитивы: Box3D, Sphere3D, Cylinder3D с типизированными данными
- C++ CoreShape для геометрических операций
- Интеграция с OpenCASCADE через минимальное ядро

СТРУКТУРА 3D-SOLUTION:
Root Solution/3D-Solution/
├── main_3d.py           # Точка входа
├── primitives/          # 3D примитивы
├── operations/          # 3D операции  
├── gui/                # 3D интерфейс
└── assembly/           # 3D сборки

СТИЛЬ КОДА:
- from data_types import SolutionReal, SolutionString, SolutionCoordinate, SolutionData
- Подробные docstring для всех классов
- Типизация через SolutionReal, SolutionString и т.д.
- Примеры использования в комментариях
- Координатная система во всех объектах

ПРИМЕР КЛАССА:
```python
from data_types import SolutionData, SolutionCoordinate, SolutionReal, SolutionString

class Box3D:
    '''
    3D Box primitive for TheSolution 3D-Solution
    
    Uses SolutionData structure and SolutionCoordinate system
    '''
    def __init__(self, name: SolutionString, width: SolutionReal, 
                 height: SolutionReal, depth: SolutionReal,
                 coordinate: SolutionCoordinate = None):
        # Implementation using SolutionData
```
```

## 🔧 ПРОМТ ДЛЯ C++ ЯДРА

```
Ты работаешь над минимальным C++ ядром проекта TheSolution.

ЦЕЛЬ:
- Минимальное C++ ядро только для критичных операций
- Интеграция с Python через pybind11
- OpenCASCADE для геометрических операций
- Экспорт SolutionCoordinate и CoreShape в Python

СТРУКТУРА ЯДРА:
core/
├── cpp/
│   ├── solution_coordinate.h    # Координатная система
│   ├── solution_coordinate.cpp
│   ├── core_shape.h            # Базовые примитивы
│   └── core_shape.cpp
├── python/
│   └── core_bindings.cpp       # pybind11 биндинги
└── CMakeLists.txt              # Сборка

ПРИНЦИПЫ:
- Минимальный объем кода (< 500 строк)
- Только критичные по производительности операции
- Простая интеграция с Python
- OpenCASCADE только для геометрии

ПРИМЕР СТРУКТУРЫ:
```cpp
// solution_coordinate.h
struct SolutionCoordinate {
    double x, y, z, a, b, c;
    SolutionCoordinate(double x=0, double y=0, double z=0, 
                      double a=1, double b=1, double c=1);
    gp_Trsf GetTransform() const;  // Для OpenCASCADE
};

// core_shape.h  
class CoreShape {
    TopoDS_Shape shape;
    SolutionCoordinate coord;
public:
    static CoreShape CreateBox(double width, double height, double depth);
    static CoreShape CreateSphere(double radius);
    CoreShape BooleanUnion(const CoreShape& other);
    double GetVolume() const;
};
```

СБОРКА:
- CMake с поиском OpenCASCADE и pybind11
- Автоматическое создание Python модуля
- Простая интеграция в основной проект
```

## 📝 ПРОМТ ДЛЯ ОТЧЕТНОСТИ

```
ОБЯЗАТЕЛЬНАЯ ПРОЦЕДУРА ОТЧЕТНОСТИ в TheSolution:

После ЛЮБЫХ изменений в коде добавь в DEVELOPMENT_REPORT.md:

## ОТЧЕТ ОБ ИЗМЕНЕНИЯХ

### Дата: [текущая дата]
### Разработчик: [твое имя]
### Измененные файлы:
- [список всех измененных файлов]

### Что сделано:
- [подробное описание изменений]

### Проблемы (если есть):
- [описание проблем и ошибок]

### Следующие шаги:
- [что планируется делать дальше]

### Статус проекта:
- [общая оценка прогресса]

ВАЖНО:
- Отчет должен быть в разделе "📊 Текущее состояние проекта"
- Обновляй таблицу задач с новыми статусами
- Отмечай что нужно проверить Claude координатору
```

## 🚀 БЫСТРЫЕ КОМАНДЫ

```bash
# Создать структуру Root Solution
mkdir -p "Root Solution"/{3D-Solution,Draft-Solution,CAM-Solution,2D-Solution,Render-Solution,BOM-Solution,Script-Solution,System-Solution}

# Создать структуру 3D-Solution
mkdir -p "Root Solution/3D-Solution"/{primitives,operations,gui,assembly}

# Создать остальные папки
mkdir -p data_types core/{cpp,python} gui/{main_selector,common_widgets,resources} project

# Создать основные файлы
touch "Let's do Solution.py"
touch "Root Solution/3D-Solution/main_3d.py"
touch "core/cpp/solution_coordinate.h"
touch "gui/main_selector/solution_selector.py"
```