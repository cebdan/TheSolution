"""
Root Solution - Основная инфраструктура TheSolution CAD
Содержит 8 основных решений с фокусом на 3D моделирование
"""

__version__ = "1.0.0"
__author__ = "TheSolution Team"

# Основные решения Root Solution
ROOT_SOLUTIONS = [
    "3D-Solution",      # 3D моделирование и дизайн
    "2D-Solution",      # 2D черчение и эскизы
    "Assembly-Solution", # Сборки и монтаж
    "Analysis-Solution", # Анализ и расчеты
    "Simulation-Solution", # Симуляция и тестирование
    "Manufacturing-Solution", # Производство и CAM
    "Documentation-Solution", # Документооборот
    "Collaboration-Solution"  # Совместная работа
]

def get_root_solutions():
    """Возвращает список всех Root решений"""
    return ROOT_SOLUTIONS.copy()

def get_3d_solution_info():
    """Информация о 3D-Solution"""
    return {
        "name": "3D-Solution",
        "description": "Основное 3D моделирование и дизайн",
        "priority": "HIGH",
        "status": "ACTIVE"
    }
