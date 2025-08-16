#!/usr/bin/env python3
"""
Тестовый скрипт для проверки запуска 3D-Solution
"""

import sys
import subprocess
from pathlib import Path

def test_3d_launch():
    """Тест запуска 3D-Solution"""
    print("🧪 Тестирование запуска 3D-Solution...")
    
    try:
        # Проверяем, что файл существует
        if not Path("3d_solution_gui.py").exists():
            print("❌ Файл 3d_solution_gui.py не найден")
            return False
        
        print("✅ Файл 3d_solution_gui.py найден")
        
        # Запускаем 3D-Solution GUI
        print("🚀 Запуск 3D-Solution GUI...")
        process = subprocess.Popen([sys.executable, "3d_solution_gui.py"], 
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        print(f"✅ 3D-Solution GUI запущен (PID: {process.pid})")
        print("📱 Ищите окно 'TheSolution CAD - 3D-Solution' на экране")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        return False

if __name__ == "__main__":
    test_3d_launch()
