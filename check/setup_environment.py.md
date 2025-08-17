#!/usr/bin/env python3
"""
Скрипт для проверки и установки необходимых компонентов для TheSolution CAD системы
"""

import sys
import subprocess
import platform
import os
from pathlib import Path

def run_command(command, check=True):
    """Выполнить команду и вернуть результат"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"Ошибка выполнения команды: {command}")
            print(f"Ошибка: {result.stderr}")
            return False
        return result
    except Exception as e:
        print(f"Исключение при выполнении команды {command}: {e}")
        return False

def check_python():
    """Проверить версию Python"""
    print("🔍 Проверка Python...")
    version = sys.version_info
    print(f"Python версия: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Требуется Python 3.8 или выше")
        return False
    
    print("✅ Python версия подходит")
    return True

def check_pip():
    """Проверить pip"""
    print("🔍 Проверка pip...")
    result = run_command("pip --version", check=False)
    if result and result.returncode == 0:
        print("✅ pip доступен")
        return True
    else:
        print("❌ pip не найден")
        return False

def check_conda():
    """Проверить conda"""
    print("🔍 Проверка conda...")
    result = run_command("conda --version", check=False)
    if result and result.returncode == 0:
        print("✅ conda доступен")
        return True
    else:
        print("ℹ️ conda не найден")
        return False

def install_python_packages():
    """Установить Python пакеты"""
    print("📦 Установка Python пакетов...")
    
    # Проверить, есть ли requirements.txt
    if not Path("requirements.txt").exists():
        print("❌ Файл requirements.txt не найден")
        return False
    
    # Установить пакеты через pip
    print("Устанавливаю пакеты через pip...")
    result = run_command("pip install -r requirements.txt")
    if result:
        print("✅ Python пакеты установлены")
        return True
    else:
        print("❌ Ошибка установки Python пакетов")
        return False

def check_cpp_tools():
    """Проверить инструменты для C++ разработки"""
    print("🔍 Проверка C++ инструментов...")
    
    # Проверить компилятор
    if platform.system() == "Windows":
        # Проверить Visual Studio
        result = run_command("cl", check=False)
        if result and result.returncode == 0:
            print("✅ Visual Studio компилятор найден")
        else:
            print("ℹ️ Visual Studio компилятор не найден")
            print("   Установите Visual Studio с компонентами C++")
    
    # Проверить CMake
    result = run_command("cmake --version", check=False)
    if result and result.returncode == 0:
        print("✅ CMake найден")
    else:
        print("ℹ️ CMake не найден")
        print("   Установите CMake с https://cmake.org/")

def check_qt():
    """Проверить Qt"""
    print("🔍 Проверка Qt...")
    
    # Проверить PySide6
    try:
        import PySide6
        print("✅ PySide6 установлен")
        return True
    except ImportError:
        print("ℹ️ PySide6 не установлен")
        return False

def check_opencascade():
    """Проверить OpenCASCADE"""
    print("🔍 Проверка OpenCASCADE...")
    print("ℹ️ OpenCASCADE нужно установить отдельно")
    print("   Для Windows: https://dev.opencascade.org/release")
    print("   Или через vcpkg: vcpkg install opencascade")

def create_virtual_environment():
    """Создать виртуальное окружение"""
    print("🔧 Создание виртуального окружения...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("ℹ️ Виртуальное окружение уже существует")
        return True
    
    result = run_command("python -m venv venv")
    if result:
        print("✅ Виртуальное окружение создано")
        print("   Активируйте его:")
        if platform.system() == "Windows":
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        return True
    else:
        print("❌ Ошибка создания виртуального окружения")
        return False

def main():
    """Основная функция"""
    print("🚀 Настройка окружения для TheSolution CAD системы")
    print("=" * 50)
    
    # Проверки
    python_ok = check_python()
    pip_ok = check_pip()
    conda_available = check_conda()
    
    if not python_ok:
        print("❌ Python не подходит. Установите Python 3.8+")
        return
    
    if not pip_ok:
        print("❌ pip не найден. Установите pip")
        return
    
    # Создать виртуальное окружение
    create_virtual_environment()
    
    # Установить пакеты
    install_python_packages()
    
    # Проверить дополнительные инструменты
    check_cpp_tools()
    check_qt()
    check_opencascade()
    
    print("\n" + "=" * 50)
    print("✅ Настройка завершена!")
    print("\nСледующие шаги:")
    print("1. Активируйте виртуальное окружение")
    print("2. Установите OpenCASCADE")
    print("3. Настройте CMake")
    print("4. Начните разработку!")

if __name__ == "__main__":
    main()
