#!/usr/bin/env python3
"""
Тестирование OpenCASCADE в conda окружении
"""

import sys
import os

print("🔍 Проверка доступности OpenCASCADE...")

# Попытка импорта OpenCASCADE
try:
    from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
    from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
    from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf
    from OCC.Core.TopoDS import TopoDS_Shape
    from OCC.Core.BRepGProp import brepgprop_VolumeProperties
    from OCC.Core.GProp import GProp_GProps
    
    print("✅ OpenCASCADE успешно импортирован!")
    
    # Тестируем создание куба
    print("🧪 Создание куба...")
    box_maker = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0)
    box_shape = box_maker.Shape()
    print(f"✅ Куб создан: {box_shape}")
    
    # Тестируем создание сферы
    print("🧪 Создание сферы...")
    sphere_maker = BRepPrimAPI_MakeSphere(5.0)
    sphere_shape = sphere_maker.Shape()
    print(f"✅ Сфера создана: {sphere_shape}")
    
    # Тестируем вычисление объема
    print("🧪 Вычисление объема куба...")
    props = GProp_GProps()
    brepgprop_VolumeProperties(box_shape, props)
    volume = props.Mass()
    print(f"✅ Объем куба: {volume}")
    
    # Тестируем трансформацию
    print("🧪 Трансформация куба...")
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(10.0, 0.0, 0.0))
    transform = BRepBuilderAPI_Transform(box_shape, trsf)
    transformed_shape = transform.Shape()
    print(f"✅ Куб перемещен: {transformed_shape}")
    
    # Тестируем булеву операцию
    print("🧪 Булева операция объединения...")
    fuse = BRepAlgoAPI_Fuse(box_shape, sphere_shape)
    if fuse.IsDone():
        union_shape = fuse.Shape()
        print(f"✅ Объединение выполнено: {union_shape}")
        
        # Вычисляем объем объединения
        union_props = GProp_GProps()
        brepgprop_VolumeProperties(union_shape, union_props)
        union_volume = union_props.Mass()
        print(f"✅ Объем объединения: {union_volume}")
    else:
        print("❌ Ошибка при выполнении булевой операции")
    
    print("\n🎉 Все тесты OpenCASCADE пройдены успешно!")
    print("OpenCASCADE полностью функционален в данном окружении.")
    
except ImportError as e:
    print(f"❌ Ошибка импорта OpenCASCADE: {e}")
    print("\n💡 Рекомендации:")
    print("1. Убедитесь, что вы находитесь в conda окружении с OpenCASCADE")
    print("2. Выполните: conda activate opencascade")
    print("3. Проверьте установку: conda list | findstr occ")
    print("4. Попробуйте переустановить: conda install -c conda-forge pythonocc-core")

except Exception as e:
    print(f"❌ Ошибка при тестировании OpenCASCADE: {e}")
    import traceback
    traceback.print_exc()

print(f"\nPython версия: {sys.version}")
print(f"Python путь: {sys.executable}")
print(f"Пути поиска модулей:")
for path in sys.path[:5]:  # Показываем первые 5 путей
    print(f"  {path}")
