#pragma once

#include "solution_base.h"
#include <opencascade/BRepPrimAPI_MakeBox.hxx>
#include <opencascade/BRepPrimAPI_MakeSphere.hxx>
#include <opencascade/BRepPrimAPI_MakeCylinder.hxx>
#include <opencascade/BRepPrimAPI_MakeCone.hxx>
#include <opencascade/BRepPrimAPI_MakeTorus.hxx>
#include <opencascade/BRepFilletAPI_MakeFillet.hxx>
#include <opencascade/BRepAlgoAPI_Fuse.hxx>
#include <opencascade/BRepAlgoAPI_Cut.hxx>
#include <opencascade/BRepAlgoAPI_Common.hxx>

namespace TheSolution {

// Класс для создания куба
class BoxSolution : public Solution {
public:
    BoxSolution(const std::string& name, double width, double height, double depth);
    ~BoxSolution() override = default;

    // Размеры
    double getWidth() const { return width_; }
    double getHeight() const { return height_; }
    double getDepth() const { return depth_; }
    
    void setWidth(double width) { width_ = width; updateGeometry(); }
    void setHeight(double height) { height_ = height; updateGeometry(); }
    void setDepth(double depth) { depth_ = depth; updateGeometry(); }

    // Переопределенные методы
    void updateGeometry() override;
    double getVolume() const override;
    double getSurfaceArea() const override;

private:
    double width_, height_, depth_;
};

// Класс для создания сферы
class SphereSolution : public Solution {
public:
    SphereSolution(const std::string& name, double radius);
    ~SphereSolution() override = default;

    // Радиус
    double getRadius() const { return radius_; }
    void setRadius(double radius) { radius_ = radius; updateGeometry(); }

    // Переопределенные методы
    void updateGeometry() override;
    double getVolume() const override;
    double getSurfaceArea() const override;

private:
    double radius_;
};

// Класс для создания цилиндра
class CylinderSolution : public Solution {
public:
    CylinderSolution(const std::string& name, double radius, double height);
    ~CylinderSolution() override = default;

    // Размеры
    double getRadius() const { return radius_; }
    double getHeight() const { return height_; }
    
    void setRadius(double radius) { radius_ = radius; updateGeometry(); }
    void setHeight(double height) { height_ = height; updateGeometry(); }

    // Переопределенные методы
    void updateGeometry() override;
    double getVolume() const override;
    double getSurfaceArea() const override;

private:
    double radius_, height_;
};

// Класс для создания конуса
class ConeSolution : public Solution {
public:
    ConeSolution(const std::string& name, double radius1, double radius2, double height);
    ~ConeSolution() override = default;

    // Размеры
    double getRadius1() const { return radius1_; }
    double getRadius2() const { return radius2_; }
    double getHeight() const { return height_; }
    
    void setRadius1(double radius) { radius1_ = radius; updateGeometry(); }
    void setRadius2(double radius) { radius2_ = radius; updateGeometry(); }
    void setHeight(double height) { height_ = height; updateGeometry(); }

    // Переопределенные методы
    void updateGeometry() override;
    double getVolume() const override;
    double getSurfaceArea() const override;

private:
    double radius1_, radius2_, height_;
};

// Класс для создания тора
class TorusSolution : public Solution {
public:
    TorusSolution(const std::string& name, double majorRadius, double minorRadius);
    ~TorusSolution() override = default;

    // Размеры
    double getMajorRadius() const { return majorRadius_; }
    double getMinorRadius() const { return minorRadius_; }
    
    void setMajorRadius(double radius) { majorRadius_ = radius; updateGeometry(); }
    void setMinorRadius(double radius) { minorRadius_ = radius; updateGeometry(); }

    // Переопределенные методы
    void updateGeometry() override;
    double getVolume() const override;
    double getSurfaceArea() const override;

private:
    double majorRadius_, minorRadius_;
};

// Класс для сборок
class AssemblySolution : public Solution {
public:
    AssemblySolution(const std::string& name);
    ~AssemblySolution() override = default;

    // Переопределенные методы
    void updateGeometry() override;
    double getVolume() const override;
    double getSurfaceArea() const override;

    // Специальные методы для сборок
    void addComponent(std::shared_ptr<Solution> component);
    void removeComponent(std::shared_ptr<Solution> component);
    std::vector<std::shared_ptr<Solution>> getComponents() const { return components_; }

private:
    std::vector<std::shared_ptr<Solution>> components_;
};

// Фабрика для создания геометрических примитивов
class GeometryFactory {
public:
    static std::shared_ptr<BoxSolution> createBox(const std::string& name, double width, double height, double depth);
    static std::shared_ptr<SphereSolution> createSphere(const std::string& name, double radius);
    static std::shared_ptr<CylinderSolution> createCylinder(const std::string& name, double radius, double height);
    static std::shared_ptr<ConeSolution> createCone(const std::string& name, double radius1, double radius2, double height);
    static std::shared_ptr<TorusSolution> createTorus(const std::string& name, double majorRadius, double minorRadius);
    static std::shared_ptr<AssemblySolution> createAssembly(const std::string& name);
};

} // namespace TheSolution
