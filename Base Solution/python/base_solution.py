"""
Base Solution - базовый класс для всех объектов в CAD системе

Каждый объект в системе наследуется от этого класса
Содержит координаты, иерархическую структуру и базовый функционал
"""

import uuid
from typing import List, Optional, Dict, Any
from solution_coordinate import SolutionCoordinate

try:
    import thesolution_core as core
    HAS_CORE = True
except ImportError:
    HAS_CORE = False

class Solution:
    """
    Базовый класс для всех объектов в CAD системе TheSolution
    
    Args:
        name: Имя объекта
        coordinate: Координаты объекта (позиция и ориентация)
    
    Attributes:
        name: Имя объекта
        coordinate: Координаты объекта
        children: Список дочерних объектов
        parent: Родительский объект
        id: Уникальный идентификатор
        visible: Видимость объекта
        locked: Блокировка объекта
        properties: Дополнительные свойства объекта
    
    Example:
        # Создание простого объекта
        obj = Solution("MyObject", SolutionCoordinate(10, 20, 30))
        
        # Создание иерархии
        parent = Solution("Parent")
        child = Solution("Child")
        parent.add_child(child)
        
        # Работа с координатами
        obj.coordinate.x = 50
        obj.move_to(100, 200, 300)
    """
    
    def __init__(self, name: str = "Solution", coordinate: Optional[SolutionCoordinate] = None):
        self.name = name
        self.coordinate = coordinate or SolutionCoordinate()
        self.children: List['Solution'] = []
        self.parent: Optional['Solution'] = None
        self.id = self._generate_id()
        self.visible = True
        self.locked = False
        self.properties: Dict[str, Any] = {}
        
        # C++ объект (создается лениво)
        self._core_solution = None
    
    def _generate_id(self) -> str:
        """Генерирует уникальный идентификатор"""
        return str(uuid.uuid4())
    
    # Свойства для прямого доступа к координатам
    @property
    def x(self) -> float:
        return self.coordinate.x
    
    @x.setter
    def x(self, value: float):
        self.coordinate.x = value
    
    @property
    def y(self) -> float:
        return self.coordinate.y
    
    @y.setter
    def y(self, value: float):
        self.coordinate.y = value
    
    @property
    def z(self) -> float:
        return self.coordinate.z
    
    @z.setter
    def z(self, value: float):
        self.coordinate.z = value
    
    @property
    def a(self) -> float:
        return self.coordinate.a
    
    @a.setter
    def a(self, value: float):
        self.coordinate.a = value
    
    @property
    def b(self) -> float:
        return self.coordinate.b
    
    @b.setter
    def b(self, value: float):
        self.coordinate.b = value
    
    @property
    def c(self) -> float:
        return self.coordinate.c
    
    @c.setter
    def c(self, value: float):
        self.coordinate.c = value
    
    # Методы управления иерархией
    def add_child(self, child: 'Solution'):
        """Добавляет дочерний объект"""
        if child in self.children:
            return
        
        # Удаляем из предыдущего родителя
        if child.parent:
            child.parent.children.remove(child)
        
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: 'Solution'):
        """Удаляет дочерний объект"""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
    
    def get_children(self) -> List['Solution']:
        """Возвращает список дочерних объектов"""
        return self.children.copy()
    
    def get_parent(self) -> Optional['Solution']:
        """Возвращает родительский объект"""
        return self.parent
    
    def get_root(self) -> 'Solution':
        """Возвращает корневой объект иерархии"""
        current = self
        while current.parent:
            current = current.parent
        return current
    
    def get_ancestors(self) -> List['Solution']:
        """Возвращает список всех предков"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors
    
    def get_descendants(self) -> List['Solution']:
        """Возвращает список всех потомков"""
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants
    
    # Методы работы с координатами
    def move_to(self, x: float, y: float, z: float):
        """Перемещение в абсолютные координаты"""
        self.coordinate.x = x
        self.coordinate.y = y
        self.coordinate.z = z
    
    def translate(self, dx: float, dy: float, dz: float):
        """Относительное перемещение"""
        self.coordinate.x += dx
        self.coordinate.y += dy
        self.coordinate.z += dz
    
    def set_orientation(self, a: float, b: float, c: float):
        """Установка ориентации"""
        self.coordinate.a = a
        self.coordinate.b = b
        self.coordinate.c = c
    
    def get_absolute_coordinate(self) -> SolutionCoordinate:
        """Получение абсолютных координат с учетом родительских объектов"""
        if self.parent is None:
            return self.coordinate.copy()
        
        parent_coord = self.parent.get_absolute_coordinate()
        return self._combine_coordinates(parent_coord, self.coordinate)
    
    def _combine_coordinates(self, parent: SolutionCoordinate, child: SolutionCoordinate) -> SolutionCoordinate:
        """Комбинирует координаты родителя и дочернего объекта"""
        # Простое сложение позиций
        combined_x = parent.x + child.x
        combined_y = parent.y + child.y
        combined_z = parent.z + child.z
        
        # Простое умножение ориентаций
        combined_a = parent.a * child.a
        combined_b = parent.b * child.b
        combined_c = parent.c * child.c
        
        return SolutionCoordinate(combined_x, combined_y, combined_z, combined_a, combined_b, combined_c)
    
    # Методы управления видимостью и блокировкой
    def set_visible(self, visible: bool):
        """Устанавливает видимость объекта"""
        self.visible = visible
    
    def is_visible(self) -> bool:
        """Проверяет видимость объекта"""
        return self.visible
    
    def set_locked(self, locked: bool):
        """Устанавливает блокировку объекта"""
        self.locked = locked
    
    def is_locked(self) -> bool:
        """Проверяет блокировку объекта"""
        return self.locked
    
    # Методы для работы с C++ ядром
    def to_core_solution(self):
        """Создает C++ объект (если доступен)"""
        if HAS_CORE and self._core_solution is None:
            core_coord = self.coordinate.to_core()
            if core_coord:
                self._core_solution = core.CSolution(self.name, core_coord)
        return self._core_solution
    
    # Виртуальные методы для переопределения
    def get_type(self) -> str:
        """Возвращает тип объекта"""
        return "Solution"
    
    def is_valid(self) -> bool:
        """Проверяет валидность объекта"""
        return True
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Получает свойство объекта"""
        return self.properties.get(key, default)
    
    def set_property(self, key: str, value: Any):
        """Устанавливает свойство объекта"""
        self.properties[key] = value
    
    # Специальные методы
    def __str__(self) -> str:
        return f"{self.get_type()}(name='{self.name}', id='{self.id}')"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def copy(self) -> 'Solution':
        """Создает копию объекта"""
        new_obj = Solution(self.name, self.coordinate.copy())
        new_obj.visible = self.visible
        new_obj.locked = self.locked
        new_obj.properties = self.properties.copy()
        
        # Копируем дочерние объекты
        for child in self.children:
            new_obj.add_child(child.copy())
        
        return new_obj
