#pragma once

#include <OpenCascade_7.8.1/opencascade/TopoDS_Shape.hxx>
#include <vector>

namespace TheSolution {

class GeometryOperations {
public:
    GeometryOperations();
    ~GeometryOperations();
    
    // Булевы операции
    TopoDS_Shape fuse(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2);
    TopoDS_Shape cut(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2);
    TopoDS_Shape intersect(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2);
    
    // Операции с формами
    TopoDS_Shape fillet(const TopoDS_Shape& shape, double radius);
    
    // Трансформации
    TopoDS_Shape translate(const TopoDS_Shape& shape, double dx, double dy, double dz);
    TopoDS_Shape rotate(const TopoDS_Shape& shape, double angle, double ax, double ay, double az);
    TopoDS_Shape scale(const TopoDS_Shape& shape, double sx, double sy, double sz);
};

} // namespace TheSolution
