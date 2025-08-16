#!/usr/bin/env python3
"""
3D-Solution File Handler - Обработчик файлов формата .3d_sol
Позволяет сохранять и загружать 3D объекты в специальном формате TheSolution CAD
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Добавляем пути к модулям
project_root = Path(__file__).parent
import sys
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "Root Solution" / "python"))

try:
    from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate, SolutionMaterial
    print("✅ Система типов данных импортирована")
except ImportError as e:
    print(f"⚠️ Ошибка импорта системы типов: {e}")

class ThreeDSolutionFileHandler:
    """Обработчик файлов формата .3d_sol"""
    
    def __init__(self):
        self.file_version = "1.0"
        self.supported_versions = ["1.0"]
        self.file_extension = ".3d_sol"
        
    def save_to_file(self, filename: str, objects_list: List, 
                    assemblies: Optional[List] = None,
                    constraints: Optional[List] = None,
                    view_settings: Optional[Dict] = None) -> bool:
        """
        Сохранить 3D объекты в файл формата .3d_sol
        
        Args:
            filename: Имя файла для сохранения
            objects_list: Список 3D объектов
            assemblies: Список сборок (опционально)
            constraints: Список ограничений (опционально)
            view_settings: Настройки отображения (опционально)
        
        Returns:
            bool: True если сохранение успешно
        """
        try:
            # Добавляем расширение если его нет
            if not filename.endswith(self.file_extension):
                filename += self.file_extension
            
            with open(filename, 'w', encoding='utf-8') as f:
                # Записываем заголовок
                f.write(self._create_header())
                
                # Записываем настройки
                f.write(self._create_settings())
                
                # Записываем материалы
                f.write(self._create_materials_section(objects_list))
                
                # Записываем объекты
                f.write(self._create_objects_section(objects_list))
                
                # Записываем сборки
                if assemblies:
                    f.write(self._create_assemblies_section(assemblies))
                
                # Записываем ограничения
                if constraints:
                    f.write(self._create_constraints_section(constraints))
                
                # Записываем свойства системы
                f.write(self._create_properties_section(objects_list))
                
                # Записываем настройки отображения
                if view_settings:
                    f.write(self._create_view_settings_section(view_settings))
                else:
                    f.write(self._create_default_view_settings())
                
                # Записываем освещение
                f.write(self._create_lighting_section())
                
                # Записываем аннотации
                f.write(self._create_annotations_section(objects_list))
                
                # Записываем историю
                f.write(self._create_history_section())
                
                # Записываем конец файла
                f.write(self._create_end_section())
            
            print(f"✅ Файл сохранен: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сохранения файла: {e}")
            return False
    
    def load_from_file(self, filename: str) -> Dict[str, Any]:
        """
        Загрузить 3D объекты из файла формата .3d_sol
        
        Args:
            filename: Имя файла для загрузки
        
        Returns:
            Dict: Словарь с данными из файла
        """
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"Файл не найден: {filename}")
            
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Парсим секции файла
            data = {
                'header': self._parse_section(content, 'HEADER'),
                'settings': self._parse_section(content, 'SETTINGS'),
                'materials': self._parse_section(content, 'MATERIALS'),
                'objects': self._parse_section(content, 'OBJECTS'),
                'assemblies': self._parse_section(content, 'ASSEMBLIES'),
                'constraints': self._parse_section(content, 'CONSTRAINTS'),
                'properties': self._parse_section(content, 'PROPERTIES'),
                'view_settings': self._parse_section(content, 'VIEW_SETTINGS'),
                'lighting': self._parse_section(content, 'LIGHTING'),
                'annotations': self._parse_section(content, 'ANNOTATIONS'),
                'history': self._parse_section(content, 'HISTORY')
            }
            
            # Создаем объекты из данных
            objects_list = self._create_objects_from_data(data['objects'])
            
            result = {
                'filename': filename,
                'data': data,
                'objects': objects_list,
                'success': True
            }
            
            print(f"✅ Файл загружен: {filename}")
            print(f"   Объектов: {len(objects_list)}")
            
            return result
            
        except Exception as e:
            print(f"❌ Ошибка загрузки файла: {e}")
            return {'success': False, 'error': str(e)}
    
    def _create_header(self) -> str:
        """Создать секцию заголовка"""
        return f"""# TheSolution CAD - 3D-Solution File Format
# Version: {self.file_version}
# Created: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}
# Description: Файл системы 3D-Solution для сохранения 3D объектов

[HEADER]
format_version={self.file_version}
creation_date={datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}
author=TheSolution CAD System
description=3D-Solution файл с объектами
units=millimeters

"""
    
    def _create_settings(self) -> str:
        """Создать секцию настроек"""
        return """[SETTINGS]
coordinate_system=cartesian
precision=0.001
material_library=default
render_quality=high

"""
    
    def _create_materials_section(self, objects_list: List) -> str:
        """Создать секцию материалов"""
        materials = set()
        for obj in objects_list:
            if hasattr(obj, 'properties') and hasattr(obj.properties, 'material'):
                materials.add(obj.properties.material.name)
        
        section = "[MATERIALS]\n"
        for i, material_name in enumerate(materials, 1):
            # Получаем свойства материала
            density = 7.85  # По умолчанию сталь
            color = "#4682B4"  # По умолчанию синий
            
            if material_name.lower() == "aluminum":
                density = 2.7
                color = "#C0C0C0"
            elif material_name.lower() == "copper":
                density = 8.96
                color = "#B87333"
            
            section += f"material_{i}={material_name}\n"
            section += f"material_{i}_density={density}\n"
            section += f"material_{i}_color={color}\n"
        
        section += "\n"
        return section
    
    def _create_objects_section(self, objects_list: List) -> str:
        """Создать секцию объектов"""
        section = "[OBJECTS]\n"
        
        for i, obj in enumerate(objects_list, 1):
            section += f"# Объект {i}: {obj.properties.name}\n"
            section += f"object_{i}_name={obj.properties.name}\n"
            section += f"object_{i}_type={obj.properties.solution_type.value}\n"
            section += f"object_{i}_id={obj.properties.index.numeric_id}\n"
            
            # Координаты
            section += f"object_{i}_position_x={obj.properties.coordinate.x}\n"
            section += f"object_{i}_position_y={obj.properties.coordinate.y}\n"
            section += f"object_{i}_position_z={obj.properties.coordinate.z}\n"
            section += f"object_{i}_rotation_a={obj.properties.coordinate.a}\n"
            section += f"object_{i}_rotation_b={obj.properties.coordinate.b}\n"
            section += f"object_{i}_rotation_c={obj.properties.coordinate.c}\n"
            
            # Размеры в зависимости от типа
            if obj.properties.solution_type == SolutionType.BOX:
                section += f"object_{i}_width={obj.dimensions.width}\n"
                section += f"object_{i}_height={obj.dimensions.height}\n"
                section += f"object_{i}_depth={obj.dimensions.depth}\n"
                volume = obj.dimensions.get_volume_box()
            elif obj.properties.solution_type == SolutionType.SPHERE:
                section += f"object_{i}_radius={obj.dimensions.radius}\n"
                volume = obj.dimensions.get_volume_sphere()
            elif obj.properties.solution_type == SolutionType.CYLINDER:
                section += f"object_{i}_radius={obj.dimensions.radius}\n"
                section += f"object_{i}_height={obj.dimensions.height}\n"
                volume = obj.dimensions.get_volume_cylinder()
            else:
                volume = 0.0
            
            # Материал и свойства
            material_name = obj.properties.material.name if hasattr(obj.properties, 'material') else "Steel"
            material_density = obj.properties.material.density if hasattr(obj.properties, 'material') else 7.85
            
            section += f"object_{i}_material={material_name}\n"
            section += f"object_{i}_volume={volume:.1f}\n"
            section += f"object_{i}_mass={volume * material_density:.1f}\n"
            section += f"object_{i}_visible=true\n"
            section += f"object_{i}_locked=false\n\n"
        
        return section
    
    def _create_assemblies_section(self, assemblies: List) -> str:
        """Создать секцию сборок"""
        section = "[ASSEMBLIES]\n"
        
        for i, assembly in enumerate(assemblies, 1):
            section += f"# Сборка {i}: {assembly.get('name', f'Сборка {i}')}\n"
            section += f"assembly_{i}_name={assembly.get('name', f'Сборка {i}')}\n"
            section += f"assembly_{i}_id={assembly.get('id', f'ASM{i:03d}')}\n"
            section += f"assembly_{i}_objects={','.join(map(str, assembly.get('objects', [])))}\n"
            section += f"assembly_{i}_position_x={assembly.get('position_x', 0.0)}\n"
            section += f"assembly_{i}_position_y={assembly.get('position_y', 0.0)}\n"
            section += f"assembly_{i}_position_z={assembly.get('position_z', 0.0)}\n"
            section += f"assembly_{i}_rotation_a={assembly.get('rotation_a', 0.0)}\n"
            section += f"assembly_{i}_rotation_b={assembly.get('rotation_b', 0.0)}\n"
            section += f"assembly_{i}_rotation_c={assembly.get('rotation_c', 0.0)}\n\n"
        
        return section
    
    def _create_constraints_section(self, constraints: List) -> str:
        """Создать секцию ограничений"""
        section = "[CONSTRAINTS]\n"
        
        for i, constraint in enumerate(constraints, 1):
            section += f"# Ограничение {i}\n"
            section += f"constraint_{i}_type={constraint.get('type', 'distance')}\n"
            section += f"constraint_{i}_object1={constraint.get('object1', '')}\n"
            section += f"constraint_{i}_object2={constraint.get('object2', '')}\n"
            section += f"constraint_{i}_value={constraint.get('value', 0.0)}\n"
            section += f"constraint_{i}_tolerance={constraint.get('tolerance', 0.1)}\n\n"
        
        return section
    
    def _create_properties_section(self, objects_list: List) -> str:
        """Создать секцию свойств системы"""
        total_volume = 0.0
        total_mass = 0.0
        
        for obj in objects_list:
            if obj.properties.solution_type == SolutionType.BOX:
                volume = obj.dimensions.get_volume_box()
            elif obj.properties.solution_type == SolutionType.SPHERE:
                volume = obj.dimensions.get_volume_sphere()
            elif obj.properties.solution_type == SolutionType.CYLINDER:
                volume = obj.dimensions.get_volume_cylinder()
            else:
                volume = 0.0
            
            total_volume += volume
            
            material_density = obj.properties.material.density if hasattr(obj.properties, 'material') else 7.85
            total_mass += volume * material_density
        
        return f"""[PROPERTIES]
# Свойства системы
total_objects={len(objects_list)}
total_assemblies=0
total_constraints=0
total_volume={total_volume:.1f}
total_mass={total_mass:.1f}
bounding_box_min_x=-10.0
bounding_box_min_y=-10.0
bounding_box_min_z=-10.0
bounding_box_max_x=25.0
bounding_box_max_y=25.0
bounding_box_max_z=10.0

"""
    
    def _create_view_settings_section(self, view_settings: Dict) -> str:
        """Создать секцию настроек отображения"""
        return f"""[VIEW_SETTINGS]
# Настройки отображения
camera_position_x={view_settings.get('camera_x', 50.0)}
camera_position_y={view_settings.get('camera_y', 50.0)}
camera_position_z={view_settings.get('camera_z', 30.0)}
camera_target_x={view_settings.get('target_x', 7.5)}
camera_target_y={view_settings.get('target_y', 7.5)}
camera_target_z={view_settings.get('target_z', 0.0)}
camera_up_x=0.0
camera_up_y=0.0
camera_up_z=1.0
perspective=true
field_of_view=45.0
near_clip=0.1
far_clip=1000.0

"""
    
    def _create_default_view_settings(self) -> str:
        """Создать секцию настроек отображения по умолчанию"""
        return """[VIEW_SETTINGS]
# Настройки отображения
camera_position_x=50.0
camera_position_y=50.0
camera_position_z=30.0
camera_target_x=7.5
camera_target_y=7.5
camera_target_z=0.0
camera_up_x=0.0
camera_up_y=0.0
camera_up_z=1.0
perspective=true
field_of_view=45.0
near_clip=0.1
far_clip=1000.0

"""
    
    def _create_lighting_section(self) -> str:
        """Создать секцию освещения"""
        return """[LIGHTING]
# Настройки освещения
light_1_type=directional
light_1_position_x=1.0
light_1_position_y=1.0
light_1_position_z=1.0
light_1_color=#FFFFFF
light_1_intensity=1.0
light_1_enabled=true

light_2_type=ambient
light_2_position_x=0.0
light_2_position_y=0.0
light_2_position_z=0.0
light_2_color=#404040
light_2_intensity=0.3
light_2_enabled=true

"""
    
    def _create_annotations_section(self, objects_list: List) -> str:
        """Создать секцию аннотаций"""
        section = "[ANNOTATIONS]\n"
        
        # Добавляем размеры для объектов
        for i, obj in enumerate(objects_list, 1):
            if obj.properties.solution_type == SolutionType.BOX:
                section += f"# Размеры для {obj.properties.name}\n"
                section += f"annotation_{i}_type=linear_dimension\n"
                section += f"annotation_{i}_start_x={obj.properties.coordinate.x}\n"
                section += f"annotation_{i}_start_y={obj.properties.coordinate.y}\n"
                section += f"annotation_{i}_start_z={obj.properties.coordinate.z}\n"
                section += f"annotation_{i}_end_x={obj.properties.coordinate.x + obj.dimensions.width}\n"
                section += f"annotation_{i}_end_y={obj.properties.coordinate.y}\n"
                section += f"annotation_{i}_end_z={obj.properties.coordinate.z}\n"
                section += f"annotation_{i}_text={obj.dimensions.width} мм\n"
                section += f"annotation_{i}_visible=true\n\n"
        
        return section
    
    def _create_history_section(self) -> str:
        """Создать секцию истории"""
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        return f"""[HISTORY]
# История изменений
history_1_date={timestamp}
history_1_action=created
history_1_description=Создан файл с объектами
history_1_user=system

"""
    
    def _create_end_section(self) -> str:
        """Создать секцию конца файла"""
        return """[END]
# Конец файла 3D-Solution
"""
    
    def _parse_section(self, content: str, section_name: str) -> Dict[str, str]:
        """Парсить секцию файла"""
        pattern = rf'\[{section_name}\](.*?)(?=\[|$)'
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            return {}
        
        section_content = match.group(1).strip()
        result = {}
        
        for line in section_content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                result[key.strip()] = value.strip()
        
        return result
    
    def _create_objects_from_data(self, objects_data: Dict) -> List:
        """Создать объекты из данных файла"""
        objects_list = []
        
        try:
            # Группируем данные по объектам
            object_groups = {}
            for key, value in objects_data.items():
                if '_' in key:
                    parts = key.split('_')
                    if len(parts) >= 3:
                        obj_num = parts[1]
                        if obj_num not in object_groups:
                            object_groups[obj_num] = {}
                        object_groups[obj_num]['_'.join(parts[2:])] = value
            
            # Создаем объекты
            for obj_num, obj_data in object_groups.items():
                try:
                    # Создаем базовый объект
                    obj = SolutionDataUtils.create_minimal_solution_data(
                        name=obj_data.get('name', f'Объект {obj_num}'),
                        solution_type=SolutionType(obj_data.get('type', 'BOX')),
                        coordinate=SolutionCoordinate(
                            float(obj_data.get('position_x', 0.0)),
                            float(obj_data.get('position_y', 0.0)),
                            float(obj_data.get('position_z', 0.0))
                        )
                    )
                    
                    # Устанавливаем размеры в зависимости от типа
                    obj_type = obj_data.get('type', 'BOX')
                    if obj_type == 'BOX':
                        obj.dimensions.width = float(obj_data.get('width', 10.0))
                        obj.dimensions.height = float(obj_data.get('height', 10.0))
                        obj.dimensions.depth = float(obj_data.get('depth', 10.0))
                    elif obj_type == 'SPHERE':
                        obj.dimensions.radius = float(obj_data.get('radius', 5.0))
                    elif obj_type == 'CYLINDER':
                        obj.dimensions.radius = float(obj_data.get('radius', 5.0))
                        obj.dimensions.height = float(obj_data.get('height', 10.0))
                    
                    # Устанавливаем материал
                    material_name = obj_data.get('material', 'Steel')
                    material_density = float(obj_data.get('material_density', 7.85))
                    obj.properties.material = SolutionMaterial(name=material_name, density=material_density)
                    
                    objects_list.append(obj)
                    
                except Exception as e:
                    print(f"⚠️ Ошибка создания объекта {obj_num}: {e}")
                    continue
            
        except Exception as e:
            print(f"❌ Ошибка парсинга объектов: {e}")
        
        return objects_list

def main():
    """Демонстрация работы с файлами .3d_sol"""
    print("🚀 Демонстрация работы с файлами .3d_sol")
    
    # Создаем обработчик
    handler = ThreeDSolutionFileHandler()
    
    # Создаем тестовые объекты
    try:
        from solution_data_types import SolutionType, SolutionDataUtils, SolutionCoordinate, SolutionMaterial
        
        objects = []
        
        # Куб
        box = SolutionDataUtils.create_minimal_solution_data(
            name="Тестовый Куб",
            solution_type=SolutionType.BOX,
            coordinate=SolutionCoordinate(0, 0, 0)
        )
        box.dimensions.width = 10.0
        box.dimensions.height = 10.0
        box.dimensions.depth = 10.0
        box.properties.material = SolutionMaterial(name="Steel", density=7.85)
        objects.append(box)
        
        # Сфера
        sphere = SolutionDataUtils.create_minimal_solution_data(
            name="Тестовая Сфера",
            solution_type=SolutionType.SPHERE,
            coordinate=SolutionCoordinate(15, 0, 0)
        )
        sphere.dimensions.radius = 5.0
        sphere.properties.material = SolutionMaterial(name="Aluminum", density=2.7)
        objects.append(sphere)
        
        # Сохраняем в файл
        success = handler.save_to_file("test_objects.3d_sol", objects)
        
        if success:
            print("✅ Файл создан успешно")
            
            # Загружаем из файла
            result = handler.load_from_file("test_objects.3d_sol")
            
            if result['success']:
                print(f"✅ Загружено объектов: {len(result['objects'])}")
                for obj in result['objects']:
                    print(f"   - {obj.properties.name} ({obj.properties.solution_type.value})")
            else:
                print(f"❌ Ошибка загрузки: {result.get('error', 'Неизвестная ошибка')}")
        
    except Exception as e:
        print(f"❌ Ошибка демонстрации: {e}")

if __name__ == "__main__":
    main()
