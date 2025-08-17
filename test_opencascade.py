#!/usr/bin/env python3
"""
Тест OpenCASCADE/PythonOCC
"""

def test_opencascade():
    """Тестирование OpenCASCADE"""
    print("🚀 Тестирование OpenCASCADE/PythonOCC")
    print("=" * 50)
    
    # Тест 1: Импорт основных модулей
    print("1. Тестирование импорта модулей...")
    
    try:
        from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
        print("   ✅ BRepPrimAPI импортирован")
    except ImportError as e:
        print(f"   ❌ Ошибка импорта BRepPrimAPI: {e}")
        return False
    
    try:
        from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
        print("   ✅ BRepPrimAPI_MakeSphere импортирован")
    except ImportError as e:
        print(f"   ❌ Ошибка импорта BRepPrimAPI_MakeSphere: {e}")
        return False
    
    try:
        from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
        print("   ✅ BRepPrimAPI_MakeCylinder импортирован")
    except ImportError as e:
        print(f"   ❌ Ошибка импорта BRepPrimAPI_MakeCylinder: {e}")
        return False
    
    # Тест 2: Создание простых геометрических объектов
    print("\n2. Тестирование создания геометрических объектов...")
    
    try:
        # Создание куба
        box_maker = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0)
        box = box_maker.Shape()
        print("   ✅ Куб создан успешно")
        
        # Создание сферы
        sphere_maker = BRepPrimAPI_MakeSphere(5.0)
        sphere = sphere_maker.Shape()
        print("   ✅ Сфера создана успешно")
        
        # Создание цилиндра
        cylinder_maker = BRepPrimAPI_MakeCylinder(3.0, 8.0)
        cylinder = cylinder_maker.Shape()
        print("   ✅ Цилиндр создан успешно")
        
    except Exception as e:
        print(f"   ❌ Ошибка создания объектов: {e}")
        return False
    
    # Тест 3: Проверка свойств объектов
    print("\n3. Тестирование свойств объектов...")
    
    try:
        from OCC.Core.BRepGProp import brepgprop_VolumeProperties
        from OCC.Core.GProp import GProp_GProps
        
        # Расчет объема куба
        props = GProp_GProps()
        brepgprop_VolumeProperties(box, props)
        volume = props.Mass()
        print(f"   ✅ Объем куба: {volume:.2f}")
        
        # Расчет объема сферы
        props = GProp_GProps()
        brepgprop_VolumeProperties(sphere, props)
        volume = props.Mass()
        print(f"   ✅ Объем сферы: {volume:.2f}")
        
        # Расчет объема цилиндра
        props = GProp_GProps()
        brepgprop_VolumeProperties(cylinder, props)
        volume = props.Mass()
        print(f"   ✅ Объем цилиндра: {volume:.2f}")
        
    except Exception as e:
        print(f"   ❌ Ошибка расчета свойств: {e}")
        return False
    
    # Тест 4: Проверка трансформаций
    print("\n4. Тестирование трансформаций...")
    
    try:
        from OCC.Core.gp import gp_Trsf, gp_Vec
        from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
        
        # Перемещение куба
        trsf = gp_Trsf()
        trsf.SetTranslation(gp_Vec(10, 0, 0))
        transform = BRepBuilderAPI_Transform(box, trsf)
        moved_box = transform.Shape()
        print("   ✅ Трансформация куба выполнена")
        
    except Exception as e:
        print(f"   ❌ Ошибка трансформации: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Все тесты OpenCASCADE прошли успешно!")
    print("🎉 OpenCASCADE готов к использованию в TheSolution CAD")
    
    return True

def main():
    """Главная функция"""
    try:
        success = test_opencascade()
        if success:
            print("\n🚀 Можно продолжать разработку 3D-Solution!")
        else:
            print("\n❌ Есть проблемы с OpenCASCADE")
    except Exception as e:
        print(f"\n💥 Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
