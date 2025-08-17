{
  "project_name": "TheSolution CAD System",
  "project_type": "Python + C++ Hybrid CAD Platform",
  "primary_language": "python",
  "secondary_language": "cpp",
  "frameworks": ["PySide6", "OpenCASCADE", "pybind11", "Qt"],
  "architecture": "Root Solution Platform",
  
  "code_style": {
    "python": {
      "style": "clear_descriptive_names",
      "comments": "extensive_docstrings",
      "type_hints": "required_solution_types",
      "max_line_length": 88,
      "imports": "from data_types import SolutionReal, SolutionString, SolutionCoordinate"
    },
    "cpp": {
      "style": "minimal_essential_only",
      "standard": "C++17",
      "comments": "doxygen_style",
      "focus": "geometry_core_only"
    }
  },
  
  "file_organization": {
    "main_report": "DEVELOPMENT_REPORT.md - ГЛАВНЫЙ файл проекта",
    "entry_point": "Let's do Solution.py - точка входа",
    "data_types": "data_types/ - система типов данных",
    "root_solutions": "Root Solution/ - все решения платформы",
    "current_focus": "Root Solution/3D-Solution/ - текущий фокус",
    "core": "core/ - C++ ядро с pybind11"
  },
  
  "development_priorities": [
    "1. ОБЯЗАТЕЛЬНО обновлять DEVELOPMENT_REPORT.md при любых изменениях",
    "2. Root Solution архитектура - 8 типов решений, фокус на 3D",
    "3. Система типов данных как основа всего",
    "4. Минимальное C++ ядро + Python-первый подход",
    "5. Cursor-дружелюбный код с подробными комментариями",
    "6. Отчитываться Claude через отчет разработки"
  ],
  
  "current_stage": "Этап 2: Root Solution инфраструктура + 3D ядро",
  
  "key_files_priority": [
    "DEVELOPMENT_REPORT.md",
    "Let's do Solution.py",
    "Root Solution/3D-Solution/main_3d.py",
    "data_types/SolutionDataTypes.py",
    "core/cpp/solution_coordinate.h"
  ]
}