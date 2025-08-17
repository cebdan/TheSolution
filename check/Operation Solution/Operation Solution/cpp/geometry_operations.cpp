#include "../opencascade/geometry_operations.h"
#include <OpenCascade_7.8.1/opencascade/BRepAlgoAPI_Fuse.hxx>
#include <OpenCascade_7.8.1/opencascade/BRepAlgoAPI_Cut.hxx>
#include <OpenCascade_7.8.1/opencascade/BRepAlgoAPI_Common.hxx>
#include <OpenCascade_7.8.1/opencascade/BRepFilletAPI_MakeFillet.hxx>
#include <OpenCascade_7.8.1/opencascade/BRepBuilderAPI_Transform.hxx>
#include <OpenCascade_7.8.1/opencascade/gp_Trsf.hxx>
#include <OpenCascade_7.8.1/opencascade/gp_Vec.hxx>
#include <OpenCascade_7.8.1/opencascade/gp_Ax1.hxx>
#include <OpenCascade_7.8.1/opencascade/gp_Dir.hxx>

namespace TheSolution {

GeometryOperations::GeometryOperations() {
}

GeometryOperations::~GeometryOperations() {
}

TopoDS_Shape GeometryOperations::fuse(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2) {
    if (shape1.IsNull() || shape2.IsNull()) {
        return TopoDS_Shape();
    }
    
    BRepAlgoAPI_Fuse fuseOp(shape1, shape2);
    if (fuseOp.IsDone()) {
        return fuseOp.Shape();
    }
    return TopoDS_Shape();
}

TopoDS_Shape GeometryOperations::cut(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2) {
    if (shape1.IsNull() || shape2.IsNull()) {
        return TopoDS_Shape();
    }
    
    BRepAlgoAPI_Cut cutOp(shape1, shape2);
    if (cutOp.IsDone()) {
        return cutOp.Shape();
    }
    return TopoDS_Shape();
}

TopoDS_Shape GeometryOperations::intersect(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2) {
    if (shape1.IsNull() || shape2.IsNull()) {
        return TopoDS_Shape();
    }
    
    BRepAlgoAPI_Common commonOp(shape1, shape2);
    if (commonOp.IsDone()) {
        return commonOp.Shape();
    }
    return TopoDS_Shape();
}

TopoDS_Shape GeometryOperations::fillet(const TopoDS_Shape& shape, double radius) {
    if (shape.IsNull() || radius <= 0) {
        return TopoDS_Shape();
    }
    
    BRepFilletAPI_MakeFillet filletOp(shape);
    
    // Добавляем все ребра для скругления
    TopExp_Explorer explorer(shape, TopAbs_EDGE);
    while (explorer.More()) {
        TopoDS_Edge edge = TopoDS::Edge(explorer.Current());
        filletOp.Add(radius, edge);
        explorer.Next();
    }
    
    if (filletOp.IsDone()) {
        return filletOp.Shape();
    }
    return TopoDS_Shape();
}

TopoDS_Shape GeometryOperations::translate(const TopoDS_Shape& shape, double dx, double dy, double dz) {
    if (shape.IsNull()) {
        return TopoDS_Shape();
    }
    
    gp_Trsf transform;
    transform.SetTranslation(gp_Vec(dx, dy, dz));
    
    BRepBuilderAPI_Transform transformOp(shape, transform, Standard_True);
    if (transformOp.IsDone()) {
        return transformOp.Shape();
    }
    return TopoDS_Shape();
}

TopoDS_Shape GeometryOperations::rotate(const TopoDS_Shape& shape, double angle, double ax, double ay, double az) {
    if (shape.IsNull()) {
        return TopoDS_Shape();
    }
    
    gp_Dir axis(ax, ay, az);
    gp_Ax1 rotationAxis(gp::Origin(), axis);
    
    gp_Trsf transform;
    transform.SetRotation(rotationAxis, angle);
    
    BRepBuilderAPI_Transform transformOp(shape, transform, Standard_True);
    if (transformOp.IsDone()) {
        return transformOp.Shape();
    }
    return TopoDS_Shape();
}

TopoDS_Shape GeometryOperations::scale(const TopoDS_Shape& shape, double sx, double sy, double sz) {
    if (shape.IsNull()) {
        return TopoDS_Shape();
    }
    
    gp_Trsf transform;
    transform.SetScale(gp::Origin(), sx, sy, sz);
    
    BRepBuilderAPI_Transform transformOp(shape, transform, Standard_True);
    if (transformOp.IsDone()) {
        return transformOp.Shape();
    }
    return TopoDS_Shape();
}

} // namespace TheSolution
