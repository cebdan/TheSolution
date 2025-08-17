"""
SolutionCoordinate - система координат для Solution объектов

Содержит позиционные (x, y, z) и ориентационные (a, b, c) координаты
Все значения являются управляемыми параметрическими величинами
"""

import math
from typing import Tuple, Optional
import numpy as np

try:
    import thesolution_core as core
    HAS_CORE = True
except ImportError:
    HAS_CORE = False
    print("Warning: thesolution_core not available, using pure Python implementation")

class SolutionCoordinate:
    """
    Координаты Solution объекта в 3D пространстве
    
    Args:
        x: Координата X (смещение по оси X)
        y: Координата Y (смещение по оси Y) 
        z: Координата Z (смещение по оси Z)
        a: Вектор направления по оси X (по умолчанию 1.0)
        b: Вектор направления по оси Y (по умолчанию 1.0)
        c: Вектор направления по оси Z (по умолчанию 1.0)
    
    Example:
        coord = SolutionCoordinate(10, 20, 30)
        print(f"Позиция: {coord.x}, {coord.y}, {coord.z}")
        print(f"Ориентация: {coord.a}, {coord.b}, {coord.c}")
    """
    
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, 
                 a: float = 1.0, b: float = 1.0, c: float = 1.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
    
    def get_position(self) -> Tuple[float, float, float]:
        """Возвращает позиционный вектор (x, y, z)"""
        return (self.x, self.y, self.z)
    
    def get_orientation(self) -> Tuple[float, float, float]:
        """Возвращает вектор ориентации (a, b, c)"""
        return (self.a, self.b, self.c)
    
    def get_transformation_matrix(self) -> np.ndarray:
        """Возвращает матрицу трансформации 4x4 для OpenGL/OpenCASCADE"""
        matrix = np.eye(4)
        
        # Применение позиции
        matrix[0:3, 3] = [self.x, self.y, self.z]
        
        # Применение ориентации (упрощенная версия)
        # В реальной реализации здесь будет более сложная логика поворотов
        if self.a != 1.0 or self.b != 1.0 or self.c != 1.0:
            # Простое масштабирование по осям
            matrix[0, 0] = self.a
            matrix[1, 1] = self.b
            matrix[2, 2] = self.c
        
        return matrix
    
    def to_core(self) -> Optional['core.SolutionCoordinate']:
        """Конвертация в C++ объект (если доступен)"""
        if HAS_CORE:
            return core.SolutionCoordinate(self.x, self.y, self.z, self.a, self.b, self.c)
        return None
    
    def distance_to(self, other: 'SolutionCoordinate') -> float:
        """Вычисляет расстояние до другой координаты"""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def __add__(self, other: 'SolutionCoordinate') -> 'SolutionCoordinate':
        """Сложение координат"""
        return SolutionCoordinate(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
            self.a * other.a,
            self.b * other.b,
            self.c * other.c
        )
    
    def __sub__(self, other: 'SolutionCoordinate') -> 'SolutionCoordinate':
        """Вычитание координат"""
        return SolutionCoordinate(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
            self.a / other.a if other.a != 0 else self.a,
            self.b / other.b if other.b != 0 else self.b,
            self.c / other.c if other.c != 0 else self.c
        )
    
    def __eq__(self, other: 'SolutionCoordinate') -> bool:
        """Сравнение координат"""
        if not isinstance(other, SolutionCoordinate):
            return False
        return (abs(self.x - other.x) < 1e-6 and
                abs(self.y - other.y) < 1e-6 and
                abs(self.z - other.z) < 1e-6 and
                abs(self.a - other.a) < 1e-6 and
                abs(self.b - other.b) < 1e-6 and
                abs(self.c - other.c) < 1e-6)
    
    def __str__(self) -> str:
        return f"SolutionCoordinate(x={self.x}, y={self.y}, z={self.z}, a={self.a}, b={self.b}, c={self.c})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def copy(self) -> 'SolutionCoordinate':
        """Создает копию координат"""
        return SolutionCoordinate(self.x, self.y, self.z, self.a, self.b, self.c)
