# Установка TheSolution CAD

📋 **Подробное руководство по установке и настройке TheSolution CAD**

## 🎯 Обзор

TheSolution CAD - это платформа для 3D моделирования, построенная на архитектуре Root Solution с интеграцией OpenCASCADE. Система требует Python 3.8+ и conda для управления зависимостями.

## 📋 Системные требования

### Минимальные требования
- **ОС**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.8 или выше
- **RAM**: 4 GB
- **Дисковое пространство**: 2 GB

### Рекомендуемые требования
- **ОС**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Python**: 3.9 или выше
- **RAM**: 8 GB или больше
- **Дисковое пространство**: 5 GB
- **GPU**: Поддержка OpenGL 3.3+

## 🚀 Быстрая установка

### 1. Установка Conda

#### Windows
```bash
# Скачайте и установите Miniconda
# https://docs.conda.io/en/latest/miniconda.html
```

#### macOS
```bash
# Скачайте и установите Miniconda
# https://docs.conda.io/en/latest/miniconda.html
```

#### Linux
```bash
# Скачайте и установите Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

### 2. Клонирование репозитория
```bash
git clone <repository-url>
cd TheSolution
```

### 3. Создание окружения
```bash
# Создание нового conda окружения
conda create -n thesolution python=3.9

# Активация окружения
conda activate thesolution
```

### 4. Установка зависимостей
```bash
# Установка OpenCASCADE и PySide6
conda install -c conda-forge pythonocc-core pyside6

# Установка дополнительных зависимостей
pip install -r requirements.txt
```

### 5. Проверка установки
```bash
# Проверка окружения
python check_conda_environment.py

# Запуск системы
python lets_do_solution_gui.py
```

## ⚙️ Детальная установка

### Этап 1: Подготовка системы

#### Windows
1. Установите [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Установите [Git for Windows](https://git-scm.com/download/win)
3. Установите [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

#### macOS
1. Установите [Xcode Command Line Tools](https://developer.apple.com/xcode/)
2. Установите [Homebrew](https://brew.sh/)
3. Установите [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

#### Linux (Ubuntu/Debian)
```bash
# Обновление системы
sudo apt update && sudo apt upgrade

# Установка необходимых пакетов
sudo apt install build-essential git cmake

# Установка Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

### Этап 2: Настройка Python окружения

```bash
# Создание окружения
conda create -n thesolution python=3.9

# Активация окружения
conda activate thesolution

# Обновление conda
conda update conda
```

### Этап 3: Установка OpenCASCADE

```bash
# Установка OpenCASCADE через conda-forge
conda install -c conda-forge pythonocc-core

# Проверка установки
python -c "from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox; print('OpenCASCADE установлен успешно')"
```

### Этап 4: Установка GUI компонентов

```bash
# Установка PySide6
conda install -c conda-forge pyside6

# Проверка установки
python -c "from PySide6.QtWidgets import QApplication; print('PySide6 установлен успешно')"
```

### Этап 5: Установка дополнительных зависимостей

```bash
# Установка из requirements.txt
pip install -r requirements.txt

# Установка дополнительных пакетов
pip install numpy scipy matplotlib
```

### Этап 6: Настройка проекта

```bash
# Клонирование репозитория
git clone <repository-url>
cd TheSolution

# Запуск скрипта настройки
python setup_environment.py
```

## 🔧 Проверка установки

### Автоматическая проверка
```bash
# Запуск проверки окружения
python check_conda_environment.py
```

### Ручная проверка компонентов

#### 1. Проверка Python
```bash
python --version
# Должно быть: Python 3.8.x или выше
```

#### 2. Проверка OpenCASCADE
```bash
python -c "
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepGProp import brepgprop_VolumeProperties
from OCC.Core.GProp import GProp_GProps

# Создание тестового куба
box = BRepPrimAPI_MakeBox(10, 10, 10).Shape()

# Расчет объема
props = GProp_GProps()
brepgprop_VolumeProperties(box, props)
volume = props.Mass()

print(f'OpenCASCADE работает! Объем куба: {volume:.2f}')
"
```

#### 3. Проверка PySide6
```bash
python -c "
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

app = QApplication([])
print('PySide6 работает!')
app.quit()
"
```

#### 4. Проверка системы типов данных
```bash
python -c "
from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate

# Создание тестового объекта
data = SolutionDataUtils.create_minimal_solution_data(
    name='Test Object',
    solution_type=SolutionType.BOX,
    coordinate=SolutionCoordinate(0, 0, 0)
)

print(f'Система типов данных работает! Создан объект: {data.properties.name}')
"
```

## 🚀 Запуск системы

### Основной запуск (рекомендуется)
```bash
# Активация окружения
conda activate thesolution

# Запуск главного GUI
python lets_do_solution_gui.py
```

### Альтернативный запуск
```bash
# Текстовый интерфейс
python lets_do_solution.py

# Прямой запуск 3D-Solution
python 3d_solution_gui.py
```

### Запуск с проверкой OpenCASCADE
```bash
# Запуск с дополнительными проверками
python run_with_opencascade.py
```

## 🛠️ Устранение неполадок

### Проблема: "ModuleNotFoundError: No module named 'OCC'"
**Решение:**
```bash
# Переустановка OpenCASCADE
conda remove pythonocc-core
conda install -c conda-forge pythonocc-core
```

### Проблема: "ModuleNotFoundError: No module named 'PySide6'"
**Решение:**
```bash
# Переустановка PySide6
conda remove pyside6
conda install -c conda-forge pyside6
```

### Проблема: "ImportError: DLL load failed" (Windows)
**Решение:**
1. Установите Visual Studio Build Tools
2. Переустановите conda окружение
3. Убедитесь, что используете правильную архитектуру (x64)

### Проблема: "GLIBCXX_3.4.29 not found" (Linux)
**Решение:**
```bash
# Обновление libstdc++
sudo apt update
sudo apt install libstdc++6
```

### Проблема: "Qt platform plugin could not be initialized"
**Решение:**
```bash
# Установка дополнительных Qt компонентов
conda install -c conda-forge qt
```

## 📦 Управление окружением

### Экспорт окружения
```bash
# Сохранение конфигурации
conda env export > environment.yml
```

### Восстановление окружения
```bash
# Создание окружения из файла
conda env create -f environment.yml
```

### Обновление зависимостей
```bash
# Обновление всех пакетов
conda update --all
pip list --outdated
pip install --upgrade <package-name>
```

## 🔄 Обновление системы

### Обновление кода
```bash
# Получение последних изменений
git pull origin main

# Обновление зависимостей
pip install -r requirements.txt --upgrade
```

### Обновление conda пакетов
```bash
# Обновление conda
conda update conda

# Обновление пакетов
conda update --all
```

## 📞 Поддержка

### Полезные команды
```bash
# Информация о conda окружении
conda info

# Список установленных пакетов
conda list

# Проверка путей Python
python -c "import sys; print('\n'.join(sys.path))"
```

### Логи и отладка
```bash
# Запуск с подробным выводом
python -v lets_do_solution_gui.py

# Проверка переменных окружения
echo $PATH
echo $PYTHONPATH
```

---

**Статус**: ✅ **УСТАНОВКА ЗАВЕРШЕНА**
**Следующий шаг**: Запуск `python lets_do_solution_gui.py`
