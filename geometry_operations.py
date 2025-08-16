#!/usr/bin/env python3
"""
Геометрические операции для TheSolution

Интеграция с OpenCASCADE для создания и модификации 3D объектов
"""

import sys
import os
from typing import Optional, Tuple, List

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Base Solution', 'python'))

from solution_coordinate import SolutionCoordinate
from base_solution import Solution

# Попытка импорта OpenCASCADE
try:
    from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeCylinder
    from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut, BRepAlgoAPI_Common
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
    from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_Ax2, gp_Dir
    from OCC.Core.TopoDS import TopoDS_Shape
    from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties
    from OCC.Core.GProp import GProp_GProps
    HAS_OPENCASCADE = True
    print("✅ OpenCASCADE доступен")
except ImportError:
    HAS_OPENCASCADE = False
    print("⚠️ OpenCASCADE не найден, используем упрощенную геометрию")

class GeometryShape:
    """Базовый класс для геометрических форм"""
    
    def __init__(self, name: str = "Shape", coordinate: Optional[SolutionCoordinate] = None):
        self.name = name
        self.coordinate = coordinate or SolutionCoordinate()
        self.shape: Optional[TopoDS_Shape] = None
        self._create_shape()
    
    def _create_shape(self):
        """Создает геометрическую форму (переопределяется в подклассах)"""
        pass
    
    def get_volume(self) -> float:
        """Возвращает объем формы"""
        if HAS_OPENCASCADE and self.shape:
            props = GProp_GProps()
            brepgprop_VolumeProperties(self.shape, props)
            return props.Mass()
        return 0.0
    
    def get_surface_area(self) -> float:
        """Возвращает площадь поверхности"""
        if HAS_OPENCASCADE and self.shape:
            props = GProp_GProps()
            brepgprop_SurfaceProperties(self.shape, props)
            return props.Mass()
        return 0.0
    
    def get_center_of_mass(self) -> Tuple[float, float, float]:
        """Возвращает центр масс"""
        if HAS_OPENCASCADE and self.shape:
            props = GProp_GProps()
            brepgprop_VolumeProperties(self.shape, props)
            cog = props.CentreOfMass()
            return (cog.X(), cog.Y(), cog.Z())
        return (0.0, 0.0, 0.0)
    
    def apply_transformation(self):
        """Применяет трансформацию на основе координат"""
        if HAS_OPENCASCADE and self.shape:
            # Создаем трансформацию
            trsf = gp_Trsf()
            trsf.SetTranslation(gp_Vec(self.coordinate.x, self.coordinate.y, self.coordinate.z))
            
            # Применяем трансформацию
            transform = BRepBuilderAPI_Transform(self.shape, trsf)
            self.shape = transform.Shape()

class BoxShape(GeometryShape):
    """Кубическая форма"""
    
    def __init__(self, name: str = "Box", width: float = 10.0, height: float = 10.0, 
                 depth: float = 10.0, coordinate: Optional[SolutionCoordinate] = None):
        self.width = width
        self.height = height
        self.depth = depth
        super().__init__(name, coordinate)
    
    def _create_shape(self):
        """Создает кубическую форму"""
        if HAS_OPENCASCADE:
            # Создаем куб
            box_maker = BRepPrimAPI_MakeBox(self.width, self.height, self.depth)
            self.shape = box_maker.Shape()
            self.apply_transformation()
        else:
            print(f"Создан куб {self.name}: {self.width}x{self.height}x{self.depth}")
    
    def get_volume(self) -> float:
        """Возвращает объем куба"""
        if HAS_OPENCASCADE and self.shape:
            return super().get_volume()
        return self.width * self.height * self.depth

class SphereShape(GeometryShape):
    """Сферическая форма"""
    
    def __init__(self, name: str = "Sphere", radius: float = 5.0, 
                 coordinate: Optional[SolutionCoordinate] = None):
        self.radius = radius
        super().__init__(name, coordinate)
    
    def _create_shape(self):
        """Создает сферическую форму"""
        if HAS_OPENCASCADE:
            # Создаем сферу
            sphere_maker = BRepPrimAPI_MakeSphere(self.radius)
            self.shape = sphere_maker.Shape()
            self.apply_transformation()
        else:
            print(f"Создана сфера {self.name}: радиус {self.radius}")
    
    def get_volume(self) -> float:
        """Возвращает объем сферы"""
        if HAS_OPENCASCADE and self.shape:
            return super().get_volume()
        import math
        return (4/3) * math.pi * (self.radius ** 3)

class CylinderShape(GeometryShape):
    """Цилиндрическая форма"""
    
    def __init__(self, name: str = "Cylinder", radius: float = 5.0, height: float = 10.0,
                 coordinate: Optional[SolutionCoordinate] = None):
        self.radius = radius
        self.height = height
        super().__init__(name, coordinate)
    
    def _create_shape(self):
        """Создает цилиндрическую форму"""
        if HAS_OPENCASCADE:
            # Создаем цилиндр
            axis = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
            cylinder_maker = BRepPrimAPI_MakeCylinder(axis, self.radius, self.height)
            self.shape = cylinder_maker.Shape()
            self.apply_transformation()
        else:
            print(f"Создан цилиндр {self.name}: радиус {self.radius}, высота {self.height}")

class GeometrySolution(Solution):
    """Solution объект с геометрической формой"""
    
    def __init__(self, name: str = "GeometrySolution", shape: Optional[GeometryShape] = None):
        super().__init__(name)
        self.geometry_shape = shape
    
    def set_shape(self, shape: GeometryShape):
        """Устанавливает геометрическую форму"""
        self.geometry_shape = shape
        if shape:
            self.coordinate = shape.coordinate
    
    def get_volume(self) -> float:
        """Возвращает объем геометрической формы"""
        if self.geometry_shape:
            return self.geometry_shape.get_volume()
        return 0.0
    
    def get_surface_area(self) -> float:
        """Возвращает площадь поверхности"""
        if self.geometry_shape:
            return self.geometry_shape.get_surface_area()
        return 0.0
    
    def get_center_of_mass(self) -> Tuple[float, float, float]:
        """Возвращает центр масс"""
        if self.geometry_shape:
            return self.geometry_shape.get_center_of_mass()
        return (0.0, 0.0, 0.0)

class GeometryOperations:
    """Класс для геометрических операций"""
    
    @staticmethod
    def create_box(name: str = "Box", width: float = 10.0, height: float = 10.0, 
                   depth: float = 10.0, coordinate: Optional[SolutionCoordinate] = None) -> GeometrySolution:
        """Создает кубический объект"""
        shape = BoxShape(name, width, height, depth, coordinate)
        solution = GeometrySolution(name)
        solution.set_shape(shape)
        return solution
    
    @staticmethod
    def create_sphere(name: str = "Sphere", radius: float = 5.0, 
                      coordinate: Optional[SolutionCoordinate] = None) -> GeometrySolution:
        """Создает сферический объект"""
        shape = SphereShape(name, radius, coordinate)
        solution = GeometrySolution(name)
        solution.set_shape(shape)
        return solution
    
    @staticmethod
    def create_cylinder(name: str = "Cylinder", radius: float = 5.0, height: float = 10.0,
                        coordinate: Optional[SolutionCoordinate] = None) -> GeometrySolution:
        """Создает цилиндрический объект"""
        shape = CylinderShape(name, radius, height, coordinate)
        solution = GeometrySolution(name)
        solution.set_shape(shape)
        return solution
    
    @staticmethod
    def boolean_union(solution1: GeometrySolution, solution2: GeometrySolution, 
                      name: str = "Union") -> Optional[GeometrySolution]:
        """Выполняет булеву операцию объединения"""
        if not HAS_OPENCASCADE:
            print("⚠️ OpenCASCADE недоступен для булевых операций")
            return None
        
        if not (solution1.geometry_shape and solution2.geometry_shape and 
                solution1.geometry_shape.shape and solution2.geometry_shape.shape):
            print("❌ Оба объекта должны иметь геометрические формы")
            return None
        
        try:
            # Выполняем объединение
            fuse = BRepAlgoAPI_Fuse(solution1.geometry_shape.shape, solution2.geometry_shape.shape)
            if fuse.IsDone():
                result_shape = fuse.Shape()
                
                # Создаем новый объект
                result = GeometrySolution(name)
                result.coordinate = solution1.coordinate  # Используем координаты первого объекта
                
                # Создаем временную форму для результата
                class ResultShape(GeometryShape):
                    def _create_shape(self):
                        self.shape = result_shape
                
                result.geometry_shape = ResultShape(name, result.coordinate)
                return result
            else:
                print("❌ Ошибка при выполнении булевой операции")
                return None
        except Exception as e:
            print(f"❌ Ошибка булевой операции: {e}")
            return None

def test_geometry():
    """Тестирует геометрические операции"""
    print("🧪 Тестирование геометрических операций...")
    
    # Создание объектов
    box = GeometryOperations.create_box("Тестовый куб", 10, 10, 10, SolutionCoordinate(0, 0, 0))
    sphere = GeometryOperations.create_sphere("Тестовая сфера", 5, SolutionCoordinate(15, 0, 0))
    
    print(f"Куб объем: {box.get_volume()}")
    print(f"Сфера объем: {sphere.get_volume()}")
    print(f"Центр масс куба: {box.get_center_of_mass()}")
    
    # Булева операция
    if HAS_OPENCASCADE:
        union = GeometryOperations.boolean_union(box, sphere, "Объединение")
        if union:
            print(f"Объединение объем: {union.get_volume()}")
    
    print("✅ Геометрические операции протестированы")

if __name__ == "__main__":
    test_geometry()
