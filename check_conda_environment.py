#!/usr/bin/env python3
"""
Скрипт для проверки conda окружения и установленных пакетов
Особенно проверяет OpenCASCADE и другие компоненты для TheSolution
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

def check_conda():
    """Проверить conda и его окружения"""
    print("🔍 Проверка conda...")
    
    # Проверить conda
    result = run_command("conda --version", check=False)
    if result and result.returncode == 0:
        print(f"✅ conda найден: {result.stdout.strip()}")
    else:
        print("❌ conda не найден")
        return False
    
    # Список окружений
    print("\n📋 Список conda окружений:")
    result = run_command("conda env list", check=False)
    if result and result.returncode == 0:
        print(result.stdout)
    else:
        print("Не удалось получить список окружений")
    
    # Активное окружение
    print("\n🎯 Активное окружение:")
    result = run_command("conda info --envs", check=False)
    if result and result.returncode == 0:
        lines = result.stdout.split('\n')
        for line in lines:
            if '*' in line:
                print(f"Активное: {line}")
                break
    
    return True

def check_installed_packages():
    """Проверить установленные пакеты"""
    print("\n📦 Проверка установленных пакетов...")
    
    # Список всех установленных пакетов
    result = run_command("conda list", check=False)
    if result and result.returncode == 0:
        packages = result.stdout.split('\n')
        
        # Ищем важные пакеты
        important_packages = [
            'opencascade', 'occt', 'opencascade-occt',
            'qt', 'pyside', 'pyside6',
            'numpy', 'scipy',
            'cmake', 'make',
            'python', 'pip'
        ]
        
        found_packages = []
        for package in packages:
            for important in important_packages:
                if important.lower() in package.lower():
                    found_packages.append(package.strip())
                    break
        
        if found_packages:
            print("✅ Найденные важные пакеты:")
            for pkg in found_packages:
                print(f"  {pkg}")
        else:
            print("ℹ️ Важные пакеты не найдены")
        
        # Поиск OpenCASCADE
        print("\n🔍 Поиск OpenCASCADE...")
        opencascade_found = False
        for package in packages:
            if 'opencascade' in package.lower() or 'occt' in package.lower():
                print(f"✅ Найден: {package.strip()}")
                opencascade_found = True
        
        if not opencascade_found:
            print("❌ OpenCASCADE не найден в conda")
            print("   Попробуйте установить: conda install -c conda-forge opencascade")
        
        return opencascade_found
    else:
        print("❌ Не удалось получить список пакетов")
        return False

def check_opencascade_installation():
    """Проверить установку OpenCASCADE"""
    print("\n🔍 Детальная проверка OpenCASCADE...")
    
    # Проверить через conda
    result = run_command("conda list | grep -i opencascade", check=False)
    if result and result.returncode == 0 and result.stdout.strip():
        print(f"✅ OpenCASCADE в conda: {result.stdout.strip()}")
    else:
        print("ℹ️ OpenCASCADE не найден в conda")
    
    # Проверить через pip
    result = run_command("pip list | grep -i opencascade", check=False)
    if result and result.returncode == 0 and result.stdout.strip():
        print(f"✅ OpenCASCADE в pip: {result.stdout.strip()}")
    else:
        print("ℹ️ OpenCASCADE не найден в pip")
    
    # Проверить системную установку
    if platform.system() == "Windows":
        # Проверить стандартные пути Windows
        possible_paths = [
            "C:\\OpenCASCADE-7.6.0",
            "C:\\OpenCASCADE-7.5.0",
            "C:\\OpenCASCADE-7.4.0",
            "C:\\Program Files\\OpenCASCADE",
            "C:\\Program Files (x86)\\OpenCASCADE"
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                print(f"✅ OpenCASCADE найден в системе: {path}")
                return True
        
        print("ℹ️ OpenCASCADE не найден в стандартных путях Windows")
    
    # Проверить переменные окружения
    env_vars = ['OpenCASCADE_DIR', 'OCCT_DIR', 'OpenCASCADE_ROOT']
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ Переменная окружения {var}: {value}")
            return True
    
    return False

def check_qt_installation():
    """Проверить установку Qt"""
    print("\n🔍 Проверка Qt...")
    
    # Проверить через conda
    result = run_command("conda list | grep -i qt", check=False)
    if result and result.returncode == 0 and result.stdout.strip():
        print("✅ Qt найден в conda:")
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                print(f"  {line.strip()}")
    else:
        print("ℹ️ Qt не найден в conda")
    
    # Проверить PySide6
    try:
        import PySide6
        print(f"✅ PySide6 установлен: {PySide6.__version__}")
    except ImportError:
        print("ℹ️ PySide6 не установлен")
        print("   Установите: conda install -c conda-forge pyside6")

def check_python_packages():
    """Проверить Python пакеты"""
    print("\n🔍 Проверка Python пакетов...")
    
    packages_to_check = [
        'numpy', 'scipy', 'matplotlib',
        'PySide6', 'PyQt6',
        'pybind11', 'setuptools'
    ]
    
    for package in packages_to_check:
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {package}: {version}")
        except ImportError:
            print(f"❌ {package}: не установлен")

def suggest_installation():
    """Предложить установку недостающих компонентов"""
    print("\n💡 Рекомендации по установке:")
    
    print("\n1. Установка OpenCASCADE через conda:")
    print("   conda install -c conda-forge opencascade")
    
    print("\n2. Установка Qt через conda:")
    print("   conda install -c conda-forge qt pyside6")
    
    print("\n3. Установка Python пакетов:")
    print("   conda install -c conda-forge numpy scipy matplotlib")
    print("   conda install -c conda-forge pybind11")
    
    print("\n4. Создание нового окружения с всеми зависимостями:")
    print("   conda create -n thesolution python=3.9")
    print("   conda activate thesolution")
    print("   conda install -c conda-forge opencascade qt pyside6 numpy scipy matplotlib pybind11")

def main():
    """Основная функция"""
    print("🚀 Проверка conda окружения для TheSolution")
    print("=" * 60)
    
    # Проверки
    conda_ok = check_conda()
    if not conda_ok:
        print("❌ conda не найден. Установите Anaconda или Miniconda")
        return
    
    check_installed_packages()
    opencascade_ok = check_opencascade_installation()
    check_qt_installation()
    check_python_packages()
    
    print("\n" + "=" * 60)
    if opencascade_ok:
        print("✅ OpenCASCADE найден! Система готова к работе.")
    else:
        print("❌ OpenCASCADE не найден. Установите его для полной функциональности.")
    
    suggest_installation()

if __name__ == "__main__":
    main()
