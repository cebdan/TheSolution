# Инструкции по установке TheSolution

## Требования к системе

### Обязательные требования
- **Python 3.8+** - основной язык разработки
- **pip** - менеджер пакетов Python
- **Git** - система контроля версий

### Для C++ компонентов (опционально)
- **Visual Studio 2019/2022** (Windows) или **GCC 9+** (Linux)
- **CMake 3.16+** - система сборки
- **OpenCASCADE 7.6+** - геометрическое ядро
- **Qt6** - GUI фреймворк

## Быстрая установка (только Python)

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd TheSolution
```

### 2. Создание виртуального окружения
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. Установка Python зависимостей
```bash
pip install -r requirements.txt
```

### 4. Тестирование базовой системы
```bash
python test_basic_system.py
```

## Полная установка (с C++ компонентами)

### 1. Установка OpenCASCADE

#### Windows
1. Скачайте OpenCASCADE с https://dev.opencascade.org/release
2. Установите в `C:\OpenCASCADE-7.6.0`
3. Добавьте в PATH: `C:\OpenCASCADE-7.6.0\win64\vc14\bin`

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install libocct-dev
```

#### macOS
```bash
brew install opencascade
```

### 2. Установка Qt6

#### Windows
1. Скачайте Qt6 с https://www.qt.io/download
2. Установите Qt6 и Qt Creator

#### Linux
```bash
sudo apt-get install qt6-base-dev qt6-opengl-dev
```

#### macOS
```bash
brew install qt6
```

### 3. Установка CMake

#### Windows
1. Скачайте CMake с https://cmake.org/download/
2. Установите и добавьте в PATH

#### Linux
```bash
sudo apt-get install cmake
```

#### macOS
```bash
brew install cmake
```

### 4. Сборка C++ компонентов

```bash
# Создание директории сборки
mkdir build
cd build

# Конфигурация CMake
cmake ..

# Сборка
cmake --build . --config Release

# Установка
cmake --install .
```

## Автоматическая установка

Используйте скрипт автоматической установки:

```bash
python setup_environment.py
```

Этот скрипт:
- Проверит версию Python
- Создаст виртуальное окружение
- Установит Python зависимости
- Проверит наличие C++ инструментов
- Даст рекомендации по установке недостающих компонентов

## Проверка установки

### Тест Python компонентов
```bash
python test_basic_system.py
```

### Тест C++ компонентов (если установлены)
```python
import thesolution_core
print("C++ компоненты работают!")
```

## Устранение проблем

### Ошибка "ModuleNotFoundError: No module named 'thesolution_core'"
- C++ компоненты не собраны или не установлены
- Используйте только Python компоненты или соберите C++ модули

### Ошибка "ImportError: No module named 'PySide6'"
- Установите PySide6: `pip install PySide6`

### Ошибка сборки CMake
- Проверьте установку OpenCASCADE и Qt6
- Убедитесь, что CMake находит все зависимости

### Ошибка "OpenCASCADE not found"
- Установите OpenCASCADE
- Укажите путь к OpenCASCADE в CMake:
  ```bash
  cmake .. -DOpenCASCADE_DIR=/path/to/opencascade
  ```

## Структура после установки

```
TheSolution/
├── venv/                    # Виртуальное окружение Python
├── build/                   # Директория сборки C++
├── Base Solution/
│   └── python/             # Python модули (работают сразу)
├── Operation Solution/
│   └── python/             # Python операции
├── Gui/                    # GUI компоненты
├── requirements.txt        # Python зависимости
├── CMakeLists.txt         # Конфигурация сборки
├── test_basic_system.py   # Тесты
└── setup_environment.py   # Скрипт установки
```

## Следующие шаги

После успешной установки:

1. **Изучите базовые классы**:
   ```python
   from Base_Solution.python import Solution, SolutionCoordinate
   ```

2. **Запустите тесты**:
   ```bash
   python test_basic_system.py
   ```

3. **Начните разработку**:
   - Создавайте новые типы Solution
   - Добавляйте геометрические операции
   - Разрабатывайте GUI компоненты

## Поддержка

При возникновении проблем:

1. Проверьте версии всех компонентов
2. Убедитесь, что все зависимости установлены
3. Проверьте переменные окружения PATH
4. Создайте issue в репозитории проекта
