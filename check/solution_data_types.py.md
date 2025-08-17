# TheSolution Data Types System
# Система базовых типов данных для CAD системы

from typing import List, Union, Optional, Any
from enum import Enum
import uuid
from dataclasses import dataclass

# ============================================================================
# БАЗОВЫЕ ТИПЫ ДАННЫХ
# ============================================================================

# Базовые примитивные типы
SolutionBool = bool
SolutionChar = str  # Одиночный символ
SolutionString = str
SolutionStringArray = List[str]
SolutionNatural = int  # Натуральные числа (>= 0)
SolutionInteger = int  # Целые числа
SolutionReal = float   # Вещественные числа

# ============================================================================
# СПЕЦИАЛИЗИРОВАННЫЕ ТИПЫ
# ============================================================================

class SolutionType(Enum):
    """Типы Solution объектов"""
    BASE = "base"
    POINT = "point"
    LINE = "line"
    CIRCLE = "circle"
    PLANE = "plane"
    BOX = "box"
    SPHERE = "sphere"
    CYLINDER = "cylinder"
    SOLID = "solid"
    ASSEMBLY = "assembly"
    SKETCH = "sketch"
    FEATURE = "feature"
    CUSTOM = "custom"

@dataclass
class SolutionCoordinate:
    """
    Координатная система Solution объекта
    x, y, z - позиция в 3D пространстве
    a, b, c - векторы ориентации/поворота
    """
    x: SolutionReal = 0.0
    y: SolutionReal = 0.0
    z: SolutionReal = 0.0
    a: SolutionReal = 1.0
    b: SolutionReal = 1.0
    c: SolutionReal = 1.0
    
    def get_position(self) -> tuple[SolutionReal, SolutionReal, SolutionReal]:
        """Возвращает позиционный вектор"""
        return (self.x, self.y, self.z)
    
    def get_orientation(self) -> tuple[SolutionReal, SolutionReal, SolutionReal]:
        """Возвращает вектор ориентации"""
        return (self.a, self.b, self.c)

class SolutionIndex:
    """
    Уникальный индекс для Solution объектов
    Используется для идентификации и поиска деталей
    """
    def __init__(self, custom_id: Optional[SolutionString] = None):
        self.uuid: SolutionString = str(uuid.uuid4())
        self.custom_id: Optional[SolutionString] = custom_id
        self.numeric_id: SolutionInteger = self._generate_numeric_id()
    
    def _generate_numeric_id(self) -> SolutionInteger:
        """Генерация числового ID для быстрого доступа"""
        return hash(self.uuid) % (10**8)  # 8-значный числовой ID
    
    def __str__(self) -> SolutionString:
        return self.custom_id if self.custom_id else self.uuid
    
    def __eq__(self, other) -> SolutionBool:
        if isinstance(other, SolutionIndex):
            return self.uuid == other.uuid
        return False

# ============================================================================
# СЛОЖНЫЕ ТИПЫ ДАННЫХ
# ============================================================================

@dataclass
class SolutionMaterial:
    """
    Материал Solution объекта (базовая версия для расширения)
    Будет расширен позже с физическими свойствами
    """
    name: SolutionString = "Default"
    density: SolutionReal = 1.0
    color_rgb: tuple[SolutionInteger, SolutionInteger, SolutionInteger] = (128, 128, 128)
    transparency: SolutionReal = 0.0  # 0.0 = непрозрачный, 1.0 = прозрачный
    
    def is_transparent(self) -> SolutionBool:
        return self.transparency > 0.0

@dataclass
class SolutionProperties:
    """
    Базовые свойства Solution объекта
    Минимальный набор данных, который можно расширять
    """
    name: SolutionString
    solution_type: SolutionType
    coordinate: SolutionCoordinate
    index: SolutionIndex
    visible: SolutionBool = True
    locked: SolutionBool = False
    material: Optional[SolutionMaterial] = None
    description: SolutionString = ""
    tags: SolutionStringArray = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.material is None:
            self.material = SolutionMaterial()

# ============================================================================
# ТИПЫ ДЛЯ ГЕОМЕТРИЧЕСКИХ ПАРАМЕТРОВ
# ============================================================================

@dataclass
class SolutionDimensions:
    """Размерные параметры для геометрических объектов"""
    width: SolutionReal = 0.0
    height: SolutionReal = 0.0
    depth: SolutionReal = 0.0
    radius: SolutionReal = 0.0
    length: SolutionReal = 0.0
    angle: SolutionReal = 0.0  # В радианах
    
    def get_volume_box(self) -> SolutionReal:
        """Объем прямоугольного параллелепипеда"""
        return self.width * self.height * self.depth
    
    def get_volume_sphere(self) -> SolutionReal:
        """Объем сферы"""
        import math
        return (4/3) * math.pi * (self.radius ** 3)
    
    def get_volume_cylinder(self) -> SolutionReal:
        """Объем цилиндра"""
        import math
        return math.pi * (self.radius ** 2) * self.height

# ============================================================================
# ТИПЫ ДЛЯ ИЕРАРХИЧЕСКОЙ СТРУКТУРЫ
# ============================================================================

class SolutionRelationship:
    """Отношения между Solution объектами"""
    def __init__(self):
        self.children_indices: List[SolutionIndex] = []
        self.parent_index: Optional[SolutionIndex] = None
    
    def add_child(self, child_index: SolutionIndex) -> None:
        """Добавление дочернего элемента"""
        if child_index not in self.children_indices:
            self.children_indices.append(child_index)
    
    def remove_child(self, child_index: SolutionIndex) -> SolutionBool:
        """Удаление дочернего элемента"""
        if child_index in self.children_indices:
            self.children_indices.remove(child_index)
            return True
        return False
    
    def has_children(self) -> SolutionBool:
        """Проверка наличия дочерних элементов"""
        return len(self.children_indices) > 0
    
    def has_parent(self) -> SolutionBool:
        """Проверка наличия родительского элемента"""
        return self.parent_index is not None

# ============================================================================
# МИНИМАЛЬНАЯ СТРУКТУРА ДАННЫХ SOLUTION
# ============================================================================

@dataclass
class SolutionData:
    """
    Минимальная структура данных для каждого Solution объекта
    Содержит только самое необходимое, легко расширяется
    """
    # Обязательные поля
    properties: SolutionProperties
    dimensions: SolutionDimensions
    relationships: SolutionRelationship
    
    # Дополнительные данные (расширяемые)
    custom_data: dict[SolutionString, Any] = None
    
    def __post_init__(self):
        if self.custom_data is None:
            self.custom_data = {}
    
    def set_custom_property(self, key: SolutionString, value: Any) -> None:
        """Добавление пользовательского свойства"""
        self.custom_data[key] = value
    
    def get_custom_property(self, key: SolutionString, default: Any = None) -> Any:
        """Получение пользовательского свойства"""
        return self.custom_data.get(key, default)
    
    def has_custom_property(self, key: SolutionString) -> SolutionBool:
        """Проверка наличия пользовательского свойства"""
        return key in self.custom_data

# ============================================================================
# УТИЛИТЫ ДЛЯ РАБОТЫ С ТИПАМИ
# ============================================================================

class SolutionDataUtils:
    """Утилиты для работы с типами данных Solution"""
    
    @staticmethod
    def create_minimal_solution_data(
        name: SolutionString,
        solution_type: SolutionType,
        coordinate: Optional[SolutionCoordinate] = None
    ) -> SolutionData:
        """Создание минимального набора данных Solution"""
        
        if coordinate is None:
            coordinate = SolutionCoordinate()
        
        properties = SolutionProperties(
            name=name,
            solution_type=solution_type,
            coordinate=coordinate,
            index=SolutionIndex(name)
        )
        
        dimensions = SolutionDimensions()
        relationships = SolutionRelationship()
        
        return SolutionData(
            properties=properties,
            dimensions=dimensions,
            relationships=relationships
        )
    
    @staticmethod
    def validate_solution_data(data: SolutionData) -> tuple[SolutionBool, List[SolutionString]]:
        """Валидация данных Solution"""
        errors = []
        
        # Проверка обязательных полей
        if not data.properties.name:
            errors.append("Name is required")
        
        if data.properties.solution_type not in SolutionType:
            errors.append("Invalid solution type")
        
        # Проверка координат
        coord = data.properties.coordinate
        if not all(isinstance(val, (int, float)) for val in [coord.x, coord.y, coord.z]):
            errors.append("Invalid coordinate values")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def copy_solution_data(source: SolutionData, new_name: Optional[SolutionString] = None) -> SolutionData:
        """Копирование данных Solution с новым индексом"""
        import copy
        
        new_data = copy.deepcopy(source)
        
        # Создание нового индекса
        new_data.properties.index = SolutionIndex(new_name)
        
        # Обновление имени если указано
        if new_name:
            new_data.properties.name = new_name
        
        # Сброс связей (копия не должна иметь те же связи)
        new_data.relationships = SolutionRelationship()
        
        return new_data

# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

def example_usage():
    """Примеры использования системы типов"""
    
    # Создание минимального Solution
    box_data = SolutionDataUtils.create_minimal_solution_data(
        name="Test Box",
        solution_type=SolutionType.BOX,
        coordinate=SolutionCoordinate(x=10.0, y=20.0, z=0.0)
    )
    
    # Установка размеров
    box_data.dimensions.width = 10.0
    box_data.dimensions.height = 20.0
    box_data.dimensions.depth = 5.0
    
    # Установка материала
    box_data.properties.material = SolutionMaterial(
        name="Steel",
        density=7.85,
        color_rgb=(192, 192, 192)
    )
    
    # Добавление пользовательских свойств
    box_data.set_custom_property("created_by", "User123")
    box_data.set_custom_property("creation_date", "2025-01-01")
    box_data.set_custom_property("revision", 1)
    
    # Валидация
    is_valid, errors = SolutionDataUtils.validate_solution_data(box_data)
    
    print(f"Box data valid: {is_valid}")
    print(f"Volume: {box_data.dimensions.get_volume_box()}")
    print(f"Position: {box_data.properties.coordinate.get_position()}")
    print(f"Custom property: {box_data.get_custom_property('created_by')}")

if __name__ == "__main__":
    example_usage()