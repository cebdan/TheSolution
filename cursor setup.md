# 🚀 Инструкции по настройке Cursor для TheSolution

## 📁 Файлы для копирования в проект

### 1. Скопируй эти файлы в корень проекта TheSolution:
- `cursor-settings.json` - настройки проекта
- `cursor-prompts.md` - промты для разных задач  
- `cursor-setup.md` - эта инструкция
- `отчет_разработки.md` - главный файл (мозг проекта)
- `SolutionDataTypes.py` - система типов данных

## ⚙️ Настройка Cursor IDE

### 1. Открой настройки Cursor (Ctrl+,)

### 2. В разделе "Chat" добавь основной промт:
```
Ты работаешь над проектом TheSolution - платформой CAD решений.

ОБЯЗАТЕЛЬНО:
- Читай файл отчет_разработки.md для понимания текущего состояния
- Используй систему типов из data_types/SolutionDataTypes.py
- Следуй Root Solution архитектуре (8 решений, фокус на 3D)
- Обновляй отчет_разработки.md при любых изменениях

ТЕКУЩИЙ ФОКУС: Root Solution инфраструктура + 3D-Solution
```

### 3. В разделе "Rules" добавь:
```
- Always update отчет_разработки.md when making changes
- Use SolutionReal, SolutionString types from data_types/
- Follow Root Solution architecture 
- Focus on 3D-Solution development
- Write detailed docstrings and comments
```

## 🎯 Как использовать промты

### Для разных задач используй соответствующие промты:

1. **Общая разработка** → Основной промт проекта
2. **Главное меню** → Промт для Root Solution  
3. **3D моделирование** → Промт для 3D-Solution
4. **C++ ядро** → Промт для C++ ядра
5. **После изменений** → Промт для отчетности

### Пример использования:
```
@cursor Используй промт для 3D-Solution. 
Создай файл main_3d.py как точку входа в 3D решение.
```

## 📂 Структура проекта для создания

### Выполни команды для создания структуры:
```bash
# Основные папки Root Solution
mkdir -p "Root Solution"/{3D-Solution,Draft-Solution,CAM-Solution,2D-Solution,Render-Solution,BOM-Solution,Script-Solution,System-Solution}

# Структура 3D-Solution
mkdir -p "Root Solution/3D-Solution"/{primitives,operations,gui,assembly}

# Остальные папки
mkdir -p data_types core/{cpp,python} gui/{main_selector,common_widgets,resources} project

# Основные файлы
touch "Let's do Solution.py"
touch "Root Solution/3D-Solution/main_3d.py"
touch "core/cpp/solution_coordinate.h"
touch "gui/main_selector/solution_selector.py"
```

## 🔧 Первые задачи

### 1. Проверь файлы:
- [ ] `отчет_разработки.md` - главный файл проекта
- [ ] `SolutionDataTypes.py` - система типов данных
- [ ] Структура папок создана

### 2. Создай главный файл:
- [ ] `Let's do Solution.py` - точка входа с главным меню
- [ ] Используй промт для Root Solution
- [ ] Обнови отчет разработки

### 3. Создай GUI селектор:
- [ ] `gui/main_selector/solution_selector.py` - меню выбора решений
- [ ] PySide6 интерфейс с 8 кнопками решений
- [ ] Обнови отчет разработки

## 📞 Связь с Claude координатором

### После любых изменений:
1. Обнови `отчет_разработки.md` с описанием что сделано
2. Обратись к Claude: 
```
Claude, я сделал изменения в [файлы]. 
Проверь отчет разработки и дай рекомендации.
```

## 🎯 Приоритеты

### Сегодня:
1. Создать структуру папок
2. Создать `Let's do Solution.py`  
3. Обновить отчет разработки
4. Получить код-ревью от Claude

### На неделю:
1. Главное меню работает
2. 3D-Solution точка входа
3. Базовый C++ setup
4. Первые 3D примитивы

---
**Помни: отчет_разработки.md - это мозг проекта, всегда обновляй его!**