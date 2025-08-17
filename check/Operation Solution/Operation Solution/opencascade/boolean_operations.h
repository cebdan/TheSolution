#pragma once

#include <OpenCascade_7.8.1/opencascade/TopoDS_Shape.hxx>
#include <vector>

namespace TheSolution {

class BooleanOperations {
public:
    BooleanOperations();
    ~BooleanOperations();
    
    // Основные булевы операции
    TopoDS_Shape union_op(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2);
    TopoDS_Shape subtract(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2);
    TopoDS_Shape intersect(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2);
    
    // Дополнительные операции
    TopoDS_Shape section(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2);
    TopoDS_Shape split(const TopoDS_Shape& shape, const TopoDS_Shape& tool);
    TopoDS_Shape defeature(const TopoDS_Shape& shape, const std::vector<TopoDS_Shape>& features);
};

} // namespace TheSolution
