"""
Root Solution Manager - Менеджер основных решений TheSolution CAD
Управляет 8 основными решениями с фокусом на 3D моделирование
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum

# Добавляем пути к базовым модулям
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "Base Solution" / "python"))
sys.path.insert(0, str(project_root))

try:
    from solution_data_types import SolutionType, SolutionDataUtils, SolutionData
    from base_solution import Solution
    from solution_coordinate import SolutionCoordinate
except ImportError as e:
    print(f"❌ Ошибка импорта базовых классов: {e}")
    sys.exit(1)

class SolutionStatus(Enum):
    """Статусы решений"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEVELOPMENT = "development"
    DEPRECATED = "deprecated"

class RootSolution:
    """Базовый класс для Root решений"""
    
    def __init__(self, name: str, description: str, solution_type: SolutionType):
        self.name = name
        self.description = description
        self.solution_type = solution_type
        self.status = SolutionStatus.DEVELOPMENT
        self.data = SolutionDataUtils.create_minimal_solution_data(
            name=name,
            solution_type=solution_type
        )
        self.sub_solutions: List[RootSolution] = []
    
    def activate(self):
        """Активация решения"""
        self.status = SolutionStatus.ACTIVE
    
    def deactivate(self):
        """Деактивация решения"""
        self.status = SolutionStatus.INACTIVE
    
    def add_sub_solution(self, sub_solution: 'RootSolution'):
        """Добавление под-решения"""
        self.sub_solutions.append(sub_solution)
    
    def get_info(self) -> Dict[str, Any]:
        """Получение информации о решении"""
        return {
            "name": self.name,
            "description": self.description,
            "type": self.solution_type.value,
            "status": self.status.value,
            "sub_solutions_count": len(self.sub_solutions)
        }

class RootSolutionManager:
    """Менеджер Root решений"""
    
    def __init__(self):
        self.solutions: Dict[str, RootSolution] = {}
        self._initialize_solutions()
    
    def _initialize_solutions(self):
        """Инициализация 8 основных решений"""
        
        # 1. 3D-Solution - Основное 3D моделирование
        solution_3d = RootSolution(
            name="3D-Solution",
            description="Основное 3D моделирование и дизайн",
            solution_type=SolutionType.SOLID
        )
        solution_3d.activate()  # Приоритетное решение
        self.solutions["3D-Solution"] = solution_3d
        
        # 2. 2D-Solution - 2D черчение
        solution_2d = RootSolution(
            name="2D-Solution", 
            description="2D черчение и эскизы",
            solution_type=SolutionType.SKETCH
        )
        self.solutions["2D-Solution"] = solution_2d
        
        # 3. Assembly-Solution - Сборки
        solution_assembly = RootSolution(
            name="Assembly-Solution",
            description="Сборки и монтаж",
            solution_type=SolutionType.ASSEMBLY
        )
        self.solutions["Assembly-Solution"] = solution_assembly
        
        # 4. Analysis-Solution - Анализ
        solution_analysis = RootSolution(
            name="Analysis-Solution",
            description="Анализ и расчеты",
            solution_type=SolutionType.FEATURE
        )
        self.solutions["Analysis-Solution"] = solution_analysis
        
        # 5. Simulation-Solution - Симуляция
        solution_simulation = RootSolution(
            name="Simulation-Solution",
            description="Симуляция и тестирование",
            solution_type=SolutionType.FEATURE
        )
        self.solutions["Simulation-Solution"] = solution_simulation
        
        # 6. Manufacturing-Solution - Производство
        solution_manufacturing = RootSolution(
            name="Manufacturing-Solution",
            description="Производство и CAM",
            solution_type=SolutionType.FEATURE
        )
        self.solutions["Manufacturing-Solution"] = solution_manufacturing
        
        # 7. Documentation-Solution - Документооборот
        solution_documentation = RootSolution(
            name="Documentation-Solution",
            description="Документооборот",
            solution_type=SolutionType.FEATURE
        )
        self.solutions["Documentation-Solution"] = solution_documentation
        
        # 8. Collaboration-Solution - Совместная работа
        solution_collaboration = RootSolution(
            name="Collaboration-Solution",
            description="Совместная работа",
            solution_type=SolutionType.FEATURE
        )
        self.solutions["Collaboration-Solution"] = solution_collaboration
    
    def get_solution(self, name: str) -> Optional[RootSolution]:
        """Получение решения по имени"""
        return self.solutions.get(name)
    
    def get_active_solutions(self) -> List[RootSolution]:
        """Получение активных решений"""
        return [s for s in self.solutions.values() if s.status == SolutionStatus.ACTIVE]
    
    def get_3d_solution(self) -> Optional[RootSolution]:
        """Получение 3D-Solution (приоритетное)"""
        return self.get_solution("3D-Solution")
    
    def activate_solution(self, name: str) -> bool:
        """Активация решения"""
        solution = self.get_solution(name)
        if solution:
            solution.activate()
            return True
        return False
    
    def deactivate_solution(self, name: str) -> bool:
        """Деактивация решения"""
        solution = self.get_solution(name)
        if solution:
            solution.deactivate()
            return True
        return False
    
    def get_all_solutions_info(self) -> Dict[str, Dict[str, Any]]:
        """Получение информации о всех решениях"""
        return {name: solution.get_info() for name, solution in self.solutions.items()}
    
    def create_solution_hierarchy(self) -> Dict[str, Any]:
        """Создание иерархии решений"""
        hierarchy = {
            "root": "TheSolution CAD",
            "solutions": {}
        }
        
        for name, solution in self.solutions.items():
            hierarchy["solutions"][name] = {
                "info": solution.get_info(),
                "sub_solutions": [sub.get_info() for sub in solution.sub_solutions]
            }
        
        return hierarchy

# Глобальный экземпляр менеджера
root_manager = RootSolutionManager()

def get_root_manager() -> RootSolutionManager:
    """Получение глобального менеджера Root решений"""
    return root_manager

def launch_3d_solution():
    """Запуск 3D-Solution через менеджер"""
    manager = get_root_manager()
    solution_3d = manager.get_3d_solution()
    
    if solution_3d and solution_3d.status == SolutionStatus.ACTIVE:
        print(f"🎯 Запуск {solution_3d.name}: {solution_3d.description}")
        
        # Импорт и запуск 3D-Solution
        try:
            import importlib.util
            project_root = Path(__file__).parent.parent.parent
            main_3d_path = project_root / "Root Solution" / "3D-Solution" / "main_3d.py"
            spec = importlib.util.spec_from_file_location("main_3d", main_3d_path)
            main_3d_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_3d_module)
            return main_3d_module.launch_3d_solution()
        except ImportError:
            print("❌ 3D-Solution не найден")
            return None
    else:
        print("❌ 3D-Solution не активен")
        return None

if __name__ == "__main__":
    # Тестирование менеджера
    manager = get_root_manager()
    
    print("🏗️ Root Solution Manager - Тестирование")
    print("=" * 50)
    
    # Информация о всех решениях
    solutions_info = manager.get_all_solutions_info()
    for name, info in solutions_info.items():
        status_icon = "✅" if info["status"] == "active" else "⏸️"
        print(f"{status_icon} {name}: {info['description']}")
    
    print("\n🎯 Приоритетное решение:")
    solution_3d = manager.get_3d_solution()
    if solution_3d:
        print(f"   {solution_3d.name}: {solution_3d.description}")
    
    print("\n📊 Иерархия решений:")
    hierarchy = manager.create_solution_hierarchy()
    print(f"   Корень: {hierarchy['root']}")
    print(f"   Решений: {len(hierarchy['solutions'])}")
