#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/eigen.h>
#include <string>
#include <memory>

// Включение заголовочных файлов
#include "../opencascade/visualization_3d.h"
#include "../../Base Solution/include/solution_base.h"
#include "../../Base Solution/include/geometry_primitives.h"

namespace py = pybind11;

// Биндинги для базовых классов
void bind_solution_base(py::module& m) {
    py::enum_<TheSolution::SolutionType>(m, "SolutionType")
        .value("BOX", TheSolution::SolutionType::BOX)
        .value("SPHERE", TheSolution::SolutionType::SPHERE)
        .value("CYLINDER", TheSolution::SolutionType::CYLINDER)
        .value("CONE", TheSolution::SolutionType::CONE)
        .value("TORUS", TheSolution::SolutionType::TORUS)
        .value("ASSEMBLY", TheSolution::SolutionType::ASSEMBLY)
        .value("CUSTOM", TheSolution::SolutionType::CUSTOM);

    py::class_<TheSolution::Solution, std::shared_ptr<TheSolution::Solution>>(m, "Solution")
        .def(py::init<>())
        .def(py::init<const std::string&, TheSolution::SolutionType>())
        .def("getName", &TheSolution::Solution::getName)
        .def("setName", &TheSolution::Solution::setName)
        .def("getType", &TheSolution::Solution::getType)
        .def("setType", &TheSolution::Solution::setType)
        .def("translate", &TheSolution::Solution::translate)
        .def("rotate", &TheSolution::Solution::rotate)
        .def("scale", &TheSolution::Solution::scale)
        .def("addChild", &TheSolution::Solution::addChild)
        .def("removeChild", &TheSolution::Solution::removeChild)
        .def("getChildren", &TheSolution::Solution::getChildren)
        .def("getParent", &TheSolution::Solution::getParent)
        .def("setParent", &TheSolution::Solution::setParent)
        .def("updateGeometry", &TheSolution::Solution::updateGeometry)
        .def("getVolume", &TheSolution::Solution::getVolume)
        .def("getSurfaceArea", &TheSolution::Solution::getSurfaceArea);
}

// Биндинги для геометрических примитивов
void bind_geometry_primitives(py::module& m) {
    py::class_<TheSolution::BoxSolution, TheSolution::Solution, std::shared_ptr<TheSolution::BoxSolution>>(m, "BoxSolution")
        .def(py::init<const std::string&, double, double, double>())
        .def("getWidth", &TheSolution::BoxSolution::getWidth)
        .def("getHeight", &TheSolution::BoxSolution::getHeight)
        .def("getDepth", &TheSolution::BoxSolution::getDepth)
        .def("setWidth", &TheSolution::BoxSolution::setWidth)
        .def("setHeight", &TheSolution::BoxSolution::setHeight)
        .def("setDepth", &TheSolution::BoxSolution::setDepth);

    py::class_<TheSolution::SphereSolution, TheSolution::Solution, std::shared_ptr<TheSolution::SphereSolution>>(m, "SphereSolution")
        .def(py::init<const std::string&, double>())
        .def("getRadius", &TheSolution::SphereSolution::getRadius)
        .def("setRadius", &TheSolution::SphereSolution::setRadius);

    py::class_<TheSolution::CylinderSolution, TheSolution::Solution, std::shared_ptr<TheSolution::CylinderSolution>>(m, "CylinderSolution")
        .def(py::init<const std::string&, double, double>())
        .def("getRadius", &TheSolution::CylinderSolution::getRadius)
        .def("getHeight", &TheSolution::CylinderSolution::getHeight)
        .def("setRadius", &TheSolution::CylinderSolution::setRadius)
        .def("setHeight", &TheSolution::CylinderSolution::setHeight);

    py::class_<TheSolution::ConeSolution, TheSolution::Solution, std::shared_ptr<TheSolution::ConeSolution>>(m, "ConeSolution")
        .def(py::init<const std::string&, double, double, double>())
        .def("getRadius1", &TheSolution::ConeSolution::getRadius1)
        .def("getRadius2", &TheSolution::ConeSolution::getRadius2)
        .def("getHeight", &TheSolution::ConeSolution::getHeight)
        .def("setRadius1", &TheSolution::ConeSolution::setRadius1)
        .def("setRadius2", &TheSolution::ConeSolution::setRadius2)
        .def("setHeight", &TheSolution::ConeSolution::setHeight);

    py::class_<TheSolution::TorusSolution, TheSolution::Solution, std::shared_ptr<TheSolution::TorusSolution>>(m, "TorusSolution")
        .def(py::init<const std::string&, double, double>())
        .def("getMajorRadius", &TheSolution::TorusSolution::getMajorRadius)
        .def("getMinorRadius", &TheSolution::TorusSolution::getMinorRadius)
        .def("setMajorRadius", &TheSolution::TorusSolution::setMajorRadius)
        .def("setMinorRadius", &TheSolution::TorusSolution::setMinorRadius);

    py::class_<TheSolution::AssemblySolution, TheSolution::Solution, std::shared_ptr<TheSolution::AssemblySolution>>(m, "AssemblySolution")
        .def(py::init<const std::string&>())
        .def("addComponent", &TheSolution::AssemblySolution::addComponent)
        .def("removeComponent", &TheSolution::AssemblySolution::removeComponent)
        .def("getComponents", &TheSolution::AssemblySolution::getComponents);

    // Фабрика геометрических примитивов
    py::class_<TheSolution::GeometryFactory>(m, "GeometryFactory")
        .def_static("createBox", &TheSolution::GeometryFactory::createBox)
        .def_static("createSphere", &TheSolution::GeometryFactory::createSphere)
        .def_static("createCylinder", &TheSolution::GeometryFactory::createCylinder)
        .def_static("createCone", &TheSolution::GeometryFactory::createCone)
        .def_static("createTorus", &TheSolution::GeometryFactory::createTorus)
        .def_static("createAssembly", &TheSolution::GeometryFactory::createAssembly);
}

// Биндинги для 3D визуализации
void bind_visualization_3d(py::module& m) {
    py::class_<TheSolution::Visualization3D>(m, "Visualization3D")
        .def(py::init<QWidget*>(), py::arg("parent") = nullptr)
        .def("addShape", &TheSolution::Visualization3D::addShape)
        .def("removeShape", &TheSolution::Visualization3D::removeShape)
        .def("clearShapes", &TheSolution::Visualization3D::clearShapes)
        .def("setViewFront", &TheSolution::Visualization3D::setViewFront)
        .def("setViewBack", &TheSolution::Visualization3D::setViewBack)
        .def("setViewLeft", &TheSolution::Visualization3D::setViewLeft)
        .def("setViewRight", &TheSolution::Visualization3D::setViewRight)
        .def("setViewTop", &TheSolution::Visualization3D::setViewTop)
        .def("setViewBottom", &TheSolution::Visualization3D::setViewBottom)
        .def("setViewIsometric", &TheSolution::Visualization3D::setViewIsometric)
        .def("setWireframeMode", &TheSolution::Visualization3D::setWireframeMode)
        .def("setShadedMode", &TheSolution::Visualization3D::setShadedMode)
        .def("setTransparency", &TheSolution::Visualization3D::setTransparency)
        .def("setLighting", &TheSolution::Visualization3D::setLighting)
        .def("setBackgroundColor", &TheSolution::Visualization3D::setBackgroundColor)
        .def("exportToImage", &TheSolution::Visualization3D::exportToImage)
        .def("exportToSTEP", &TheSolution::Visualization3D::exportToSTEP);

    py::class_<TheSolution::SceneManager>(m, "SceneManager")
        .def(py::init<>())
        .def("addObject", &TheSolution::SceneManager::addObject)
        .def("removeObject", &TheSolution::SceneManager::removeObject)
        .def("clearObjects", &TheSolution::SceneManager::clearObjects)
        .def("getObjects", &TheSolution::SceneManager::getObjects)
        .def("getObject", &TheSolution::SceneManager::getObject)
        .def("selectObject", &TheSolution::SceneManager::selectObject)
        .def("deselectObject", &TheSolution::SceneManager::deselectObject)
        .def("highlightObject", &TheSolution::SceneManager::highlightObject)
        .def("exportScene", &TheSolution::SceneManager::exportScene);
}

// Основная функция модуля
PYBIND11_MODULE(thesolution_operations, m) {
    m.doc() = "TheSolution Operations Module - C++ bindings for 3D operations and visualization";

    // Биндинги для базовых классов
    bind_solution_base(m);
    
    // Биндинги для геометрических примитивов
    bind_geometry_primitives(m);
    
    // Биндинги для 3D визуализации
    bind_visualization_3d(m);

    // Дополнительные утилиты
    m.def("create_box", [](const std::string& name, double width, double height, double depth) {
        return TheSolution::GeometryFactory::createBox(name, width, height, depth);
    }, "Create a box solution");

    m.def("create_sphere", [](const std::string& name, double radius) {
        return TheSolution::GeometryFactory::createSphere(name, radius);
    }, "Create a sphere solution");

    m.def("create_cylinder", [](const std::string& name, double radius, double height) {
        return TheSolution::GeometryFactory::createCylinder(name, radius, height);
    }, "Create a cylinder solution");

    m.def("create_cone", [](const std::string& name, double radius1, double radius2, double height) {
        return TheSolution::GeometryFactory::createCone(name, radius1, radius2, height);
    }, "Create a cone solution");

    m.def("create_torus", [](const std::string& name, double majorRadius, double minorRadius) {
        return TheSolution::GeometryFactory::createTorus(name, majorRadius, minorRadius);
    }, "Create a torus solution");

    m.def("create_assembly", [](const std::string& name) {
        return TheSolution::GeometryFactory::createAssembly(name);
    }, "Create an assembly solution");
}
