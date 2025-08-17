#include "../include/solution_base.h"
#include <opencascade/BRepBuilderAPI_Transform.hxx>
#include <opencascade/gp_Vec.hxx>
#include <opencascade/gp_Ax1.hxx>
#include <opencascade/gp_Dir.hxx>
#include <opencascade/gp_XYZ.hxx>
#include <algorithm>

namespace TheSolution {

Solution::Solution() 
    : name_("Unnamed")
    , type_(SolutionType::CUSTOM)
    , position_(0, 0, 0)
    , orientation_(gp::Origin(), gp::DZ())
    , parent_(nullptr)
{
}

Solution::Solution(const std::string& name, SolutionType type)
    : name_(name)
    , type_(type)
    , position_(0, 0, 0)
    , orientation_(gp::Origin(), gp::DZ())
    , parent_(nullptr)
{
}

Solution::~Solution() {
    // Удаляем ссылки на родителя у всех детей
    for (auto& child : children_) {
        if (child) {
            child->setParent(nullptr);
        }
    }
    children_.clear();
}

void Solution::setPosition(const gp_Pnt& position) {
    position_ = position;
    updateTransformation();
}

void Solution::setOrientation(const gp_Ax2& orientation) {
    orientation_ = orientation;
    updateTransformation();
}

void Solution::translate(double dx, double dy, double dz) {
    gp_Vec translation(dx, dy, dz);
    position_.Translate(translation);
    updateTransformation();
}

void Solution::rotate(double angle, double ax, double ay, double az) {
    gp_Dir axis(ax, ay, az);
    gp_Ax1 rotationAxis(position_, axis);
    orientation_.Rotate(rotationAxis, angle);
    updateTransformation();
}

void Solution::scale(double sx, double sy, double sz) {
    // Масштабирование относительно текущей позиции
    gp_Trsf scaleTransform;
    scaleTransform.SetScale(position_, sx, sy, sz);
    
    if (!shape_.IsNull()) {
        BRepBuilderAPI_Transform transform(shape_, scaleTransform, Standard_True);
        shape_ = transform.Shape();
    }
}

void Solution::addChild(std::shared_ptr<Solution> child) {
    if (child && child != shared_from_this()) {
        // Удаляем из предыдущего родителя
        if (child->getParent()) {
            child->getParent()->removeChild(child);
        }
        
        // Добавляем к текущему родителю
        children_.push_back(child);
        child->setParent(shared_from_this());
    }
}

void Solution::removeChild(std::shared_ptr<Solution> child) {
    auto it = std::find(children_.begin(), children_.end(), child);
    if (it != children_.end()) {
        (*it)->setParent(nullptr);
        children_.erase(it);
    }
}

void Solution::updateTransformation() {
    if (!shape_.IsNull()) {
        gp_Trsf transform = calculateTransformation();
        BRepBuilderAPI_Transform transformOp(shape_, transform, Standard_True);
        shape_ = transformOp.Shape();
    }
}

gp_Trsf Solution::calculateTransformation() const {
    gp_Trsf transform;
    
    // Позиция
    transform.SetTranslation(gp_Vec(position_.X(), position_.Y(), position_.Z()));
    
    // Ориентация (если отличается от стандартной)
    if (orientation_.Direction() != gp::DZ() || orientation_.XDirection() != gp::DX()) {
        gp_Trsf orientationTransform;
        orientationTransform.SetTransformation(orientation_, gp::XOY());
        transform.Multiply(orientationTransform);
    }
    
    return transform;
}

} // namespace TheSolution
