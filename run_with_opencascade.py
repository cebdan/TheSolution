#!/usr/bin/env python3
"""
Запуск TheSolution с OpenCASCADE из conda окружения
"""

import sys
import os
import subprocess

def run_with_conda():
    """Запускает Python скрипт в conda окружении с OpenCASCADE"""
    
    # Путь к Python в conda окружении
    conda_python = r"C:\Users\danch\miniconda3\envs\opencascade\python.exe"
    
    if not os.path.exists(conda_python):
        print("❌ Python в conda окружении не найден")
        return False
    
    print(f"🚀 Запуск с Python: {conda_python}")
    
    # Список скриптов для запуска
    scripts = [
        "test_opencascade.py",
        "geometry_operations.py",
        "test_basic_system.py"
    ]
    
    for script in scripts:
        if os.path.exists(script):
            print(f"\n📜 Запуск {script}...")
            try:
                result = subprocess.run([conda_python, script], 
                                      capture_output=True, text=True, encoding='utf-8')
                
                if result.returncode == 0:
                    print("✅ Успешно выполнено")
                    print(result.stdout)
                else:
                    print("❌ Ошибка выполнения")
                    print(result.stderr)
                    
            except Exception as e:
                print(f"❌ Ошибка запуска {script}: {e}")
        else:
            print(f"⚠️ Файл {script} не найден")
    
    return True

def test_opencascade_direct():
    """Прямое тестирование OpenCASCADE"""
    print("\n🔍 Прямое тестирование OpenCASCADE...")
    
    conda_python = r"C:\Users\danch\miniconda3\envs\opencascade\python.exe"
    
    test_code = '''
import sys
print("Python версия:", sys.version)

try:
    from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
    print("✅ OpenCASCADE импортирован успешно!")
    
    # Создаем куб
    box = BRepPrimAPI_MakeBox(10, 10, 10)
    shape = box.Shape()
    print(f"✅ Куб создан: {shape}")
    
    # Вычисляем объем
    from OCC.Core.BRepGProp import brepgprop_VolumeProperties
    from OCC.Core.GProp import GProp_GProps
    
    props = GProp_GProps()
    brepgprop_VolumeProperties(shape, props)
    volume = props.Mass()
    print(f"✅ Объем куба: {volume}")
    
    print("🎉 OpenCASCADE работает отлично!")
    
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
except Exception as e:
    print(f"❌ Ошибка: {e}")
'''
    
    try:
        result = subprocess.run([conda_python, "-c", test_code], 
                              capture_output=True, text=True, encoding='utf-8')
        
        print("Результат выполнения:")
        print(result.stdout)
        
        if result.stderr:
            print("Ошибки:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    print("🚀 TheSolution с OpenCASCADE")
    print("=" * 50)
    
    # Прямое тестирование
    test_opencascade_direct()
    
    # Запуск скриптов
    print("\n" + "=" * 50)
    run_with_conda()
    
    print("\n✅ Тестирование завершено")
