#!/usr/bin/env python3
"""
Быстрая проверка OpenCASCADE
"""

import sys
import subprocess
import os

def check_conda_opencascade():
    """Проверить OpenCASCADE в conda"""
    print("🔍 Проверка OpenCASCADE в conda...")
    
    try:
        result = subprocess.run("conda list | grep -i opencascade", shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print("✅ OpenCASCADE найден в conda:")
            print(result.stdout.strip())
            return True
        else:
            print("❌ OpenCASCADE не найден в conda")
            return False
    except Exception as e:
        print(f"Ошибка проверки conda: {e}")
        return False

def check_pip_opencascade():
    """Проверить OpenCASCADE в pip"""
    print("\n🔍 Проверка OpenCASCADE в pip...")
    
    try:
        result = subprocess.run("pip list | grep -i opencascade", shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print("✅ OpenCASCADE найден в pip:")
            print(result.stdout.strip())
            return True
        else:
            print("❌ OpenCASCADE не найден в pip")
            return False
    except Exception as e:
        print(f"Ошибка проверки pip: {e}")
        return False

def check_system_opencascade():
    """Проверить системную установку OpenCASCADE"""
    print("\n🔍 Проверка системной установки OpenCASCADE...")
    
    # Проверить переменные окружения
    env_vars = ['OpenCASCADE_DIR', 'OCCT_DIR', 'OpenCASCADE_ROOT']
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ Переменная окружения {var}: {value}")
            return True
    
    print("❌ Переменные окружения OpenCASCADE не найдены")
    return False

def suggest_installation():
    """Предложить установку"""
    print("\n💡 Для установки OpenCASCADE выполните:")
    print("1. conda install -c conda-forge opencascade")
    print("2. Или скачайте с https://dev.opencascade.org/release")

def main():
    print("🚀 Быстрая проверка OpenCASCADE")
    print("=" * 40)
    
    conda_ok = check_conda_opencascade()
    pip_ok = check_pip_opencascade()
    system_ok = check_system_opencascade()
    
    print("\n" + "=" * 40)
    if conda_ok or pip_ok or system_ok:
        print("✅ OpenCASCADE найден! Можно продолжать разработку.")
    else:
        print("❌ OpenCASCADE не найден. Установите его для полной функциональности.")
        suggest_installation()

if __name__ == "__main__":
    main()
