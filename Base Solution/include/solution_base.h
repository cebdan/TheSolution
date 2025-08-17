#pragma once

#include <memory>
#include <string>
#include <vector>
#include <opencascade/TopoDS_Shape.hxx>
#include <opencascade/gp_Pnt.hxx>
#include <opencascade/gp_Ax2.hxx>
#include <opencascade/gp_Trsf.hxx>

namespace TheSolution {

// Перечисление типов объектов
enum class SolutionType {
    BOX,
    SPHERE,
    CYLINDER,
    CONE,
    TORUS,
    ASSEMBLY,
    CUSTOM
};

// Базовый класс для всех объектов TheSolution
class Solution {
public:
    Solution();
    Solution(const std::string& name, SolutionType type);
    virtual ~Solution();

    // Основные свойства
    std::string getName() const { return name_; }
    void setName(const std::string& name) { name_ = name; }
    
    SolutionType getType() const { return type_; }
    void setType(SolutionType type) { type_ = type; }

    // Координатная система
    gp_Pnt getPosition() const { return position_; }
    void setPosition(const gp_Pnt& position);
    
    gp_Ax2 getOrientation() const { return orientation_; }
    void setOrientation(const gp_Ax2& orientation);

    // OpenCASCADE геометрия
    TopoDS_Shape getShape() const { return shape_; }
    void setShape(const TopoDS_Shape& shape) { shape_ = shape; }
    
    // Трансформации
    void translate(double dx, double dy, double dz);
    void rotate(double angle, double ax, double ay, double az);
    void scale(double sx, double sy, double sz);

    // Иерархия объектов
    void addChild(std::shared_ptr<Solution> child);
    void removeChild(std::shared_ptr<Solution> child);
    std::vector<std::shared_ptr<Solution>> getChildren() const { return children_; }
    
    std::shared_ptr<Solution> getParent() const { return parent_; }
    void setParent(std::shared_ptr<Solution> parent) { parent_ = parent; }

    // Виртуальные методы для переопределения
    virtual void updateGeometry() = 0;
    virtual double getVolume() const = 0;
    virtual double getSurfaceArea() const = 0;

protected:
    std::string name_;
    SolutionType type_;
    gp_Pnt position_;
    gp_Ax2 orientation_;
    TopoDS_Shape shape_;
    
    std::shared_ptr<Solution> parent_;
    std::vector<std::shared_ptr<Solution>> children_;
    
    // Внутренние методы
    void updateTransformation();
    gp_Trsf calculateTransformation() const;
};

} // namespace TheSolution
