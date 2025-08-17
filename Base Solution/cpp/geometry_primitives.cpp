#include "../include/geometry_primitives.h"
#include <opencascade/BRepBuilderAPI_Transform.hxx>
#include <opencascade/BRepGProp.hxx>
#include <opencascade/GProp_GProps.hxx>
#include <opencascade/gp_Pnt.hxx>
#include <opencascade/gp_Ax2.hxx>
#include <opencascade/gp_Dir.hxx>
#include <opencascade/gp_Vec.hxx>
#include <cmath>

namespace TheSolution {

// BoxSolution реализация
BoxSolution::BoxSolution(const std::string& name, double width, double height, double depth)
    : Solution(name, SolutionType::BOX)
    , width_(width)
    , height_(height)
    , depth_(depth)
{
    updateGeometry();
}

void BoxSolution::updateGeometry() {
    if (width_ <= 0 || height_ <= 0 || depth_ <= 0) {
        return;
    }
    
    // Создаем куб с помощью OpenCASCADE
    BRepPrimAPI_MakeBox boxMaker(width_, height_, depth_);
    if (boxMaker.IsDone()) {
        shape_ = boxMaker.Shape();
        updateTransformation();
    }
}

double BoxSolution::getVolume() const {
    return width_ * height_ * depth_;
}

double BoxSolution::getSurfaceArea() const {
    return 2.0 * (width_ * height_ + width_ * depth_ + height_ * depth_);
}

// SphereSolution реализация
SphereSolution::SphereSolution(const std::string& name, double radius)
    : Solution(name, SolutionType::SPHERE)
    , radius_(radius)
{
    updateGeometry();
}

void SphereSolution::updateGeometry() {
    if (radius_ <= 0) {
        return;
    }
    
    // Создаем сферу с помощью OpenCASCADE
    BRepPrimAPI_MakeSphere sphereMaker(radius_);
    if (sphereMaker.IsDone()) {
        shape_ = sphereMaker.Shape();
        updateTransformation();
    }
}

double SphereSolution::getVolume() const {
    return (4.0 / 3.0) * M_PI * radius_ * radius_ * radius_;
}

double SphereSolution::getSurfaceArea() const {
    return 4.0 * M_PI * radius_ * radius_;
}

// CylinderSolution реализация
CylinderSolution::CylinderSolution(const std::string& name, double radius, double height)
    : Solution(name, SolutionType::CYLINDER)
    , radius_(radius)
    , height_(height)
{
    updateGeometry();
}

void CylinderSolution::updateGeometry() {
    if (radius_ <= 0 || height_ <= 0) {
        return;
    }
    
    // Создаем цилиндр с помощью OpenCASCADE
    BRepPrimAPI_MakeCylinder cylinderMaker(radius_, height_);
    if (cylinderMaker.IsDone()) {
        shape_ = cylinderMaker.Shape();
        updateTransformation();
    }
}

double CylinderSolution::getVolume() const {
    return M_PI * radius_ * radius_ * height_;
}

double CylinderSolution::getSurfaceArea() const {
    return 2.0 * M_PI * radius_ * radius_ + 2.0 * M_PI * radius_ * height_;
}

// ConeSolution реализация
ConeSolution::ConeSolution(const std::string& name, double radius1, double radius2, double height)
    : Solution(name, SolutionType::CONE)
    , radius1_(radius1)
    , radius2_(radius2)
    , height_(height)
{
    updateGeometry();
}

void ConeSolution::updateGeometry() {
    if (radius1_ < 0 || radius2_ < 0 || height_ <= 0) {
        return;
    }
    
    // Создаем конус с помощью OpenCASCADE
    BRepPrimAPI_MakeCone coneMaker(radius1_, radius2_, height_);
    if (coneMaker.IsDone()) {
        shape_ = coneMaker.Shape();
        updateTransformation();
    }
}

double ConeSolution::getVolume() const {
    return (1.0 / 3.0) * M_PI * height_ * (radius1_ * radius1_ + radius1_ * radius2_ + radius2_ * radius2_);
}

double ConeSolution::getSurfaceArea() const {
    double slantHeight = sqrt(height_ * height_ + (radius1_ - radius2_) * (radius1_ - radius2_));
    return M_PI * (radius1_ + radius2_) * slantHeight + M_PI * radius1_ * radius1_ + M_PI * radius2_ * radius2_;
}

// TorusSolution реализация
TorusSolution::TorusSolution(const std::string& name, double majorRadius, double minorRadius)
    : Solution(name, SolutionType::TORUS)
    , majorRadius_(majorRadius)
    , minorRadius_(minorRadius)
{
    updateGeometry();
}

void TorusSolution::updateGeometry() {
    if (majorRadius_ <= 0 || minorRadius_ <= 0 || minorRadius_ >= majorRadius_) {
        return;
    }
    
    // Создаем тор с помощью OpenCASCADE
    BRepPrimAPI_MakeTorus torusMaker(majorRadius_, minorRadius_);
    if (torusMaker.IsDone()) {
        shape_ = torusMaker.Shape();
        updateTransformation();
    }
}

double TorusSolution::getVolume() const {
    return 2.0 * M_PI * M_PI * majorRadius_ * minorRadius_ * minorRadius_;
}

double TorusSolution::getSurfaceArea() const {
    return 4.0 * M_PI * M_PI * majorRadius_ * minorRadius_;
}

// AssemblySolution реализация
AssemblySolution::AssemblySolution(const std::string& name)
    : Solution(name, SolutionType::ASSEMBLY)
{
}

void AssemblySolution::updateGeometry() {
    // Для сборки геометрия обновляется автоматически при добавлении компонентов
    // Здесь можно добавить логику объединения всех компонентов
}

double AssemblySolution::getVolume() const {
    double totalVolume = 0.0;
    for (const auto& component : components_) {
        if (component) {
            totalVolume += component->getVolume();
        }
    }
    return totalVolume;
}

double AssemblySolution::getSurfaceArea() const {
    double totalArea = 0.0;
    for (const auto& component : components_) {
        if (component) {
            totalArea += component->getSurfaceArea();
        }
    }
    return totalArea;
}

void AssemblySolution::addComponent(std::shared_ptr<Solution> component) {
    if (component) {
        components_.push_back(component);
        addChild(component);
    }
}

void AssemblySolution::removeComponent(std::shared_ptr<Solution> component) {
    auto it = std::find(components_.begin(), components_.end(), component);
    if (it != components_.end()) {
        components_.erase(it);
        removeChild(component);
    }
}

// GeometryFactory реализация
std::shared_ptr<BoxSolution> GeometryFactory::createBox(const std::string& name, double width, double height, double depth) {
    return std::make_shared<BoxSolution>(name, width, height, depth);
}

std::shared_ptr<SphereSolution> GeometryFactory::createSphere(const std::string& name, double radius) {
    return std::make_shared<SphereSolution>(name, radius);
}

std::shared_ptr<CylinderSolution> GeometryFactory::createCylinder(const std::string& name, double radius, double height) {
    return std::make_shared<CylinderSolution>(name, radius, height);
}

std::shared_ptr<ConeSolution> GeometryFactory::createCone(const std::string& name, double radius1, double radius2, double height) {
    return std::make_shared<ConeSolution>(name, radius1, radius2, height);
}

std::shared_ptr<TorusSolution> GeometryFactory::createTorus(const std::string& name, double majorRadius, double minorRadius) {
    return std::make_shared<TorusSolution>(name, majorRadius, minorRadius);
}

std::shared_ptr<AssemblySolution> GeometryFactory::createAssembly(const std::string& name) {
    return std::make_shared<AssemblySolution>(name);
}

} // namespace TheSolution
