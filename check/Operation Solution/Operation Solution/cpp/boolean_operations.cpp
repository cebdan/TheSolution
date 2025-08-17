#include "../opencascade/boolean_operations.h"
#include <OpenCascade_7.8.1/opencascade/BRepAlgoAPI_Fuse.hxx>
#include <OpenCascade_7.8.1/opencascade/BRepAlgoAPI_Cut.hxx>
#include <OpenCascade_7.8.1/opencascade/BRepAlgoAPI_Common.hxx>
#include <OpenCascade_7.8.1/opencascade/BRepAlgoAPI_Section.hxx>
#include <OpenCascade_7.8.1/opencascade/BRepAlgoAPI_Splitter.hxx>
#include <OpenCascade_7.8.1/opencascade/BRepAlgoAPI_Defeaturing.hxx>

namespace TheSolution {

BooleanOperations::BooleanOperations() {
}

BooleanOperations::~BooleanOperations() {
}

TopoDS_Shape BooleanOperations::union_op(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2) {
    if (shape1.IsNull() || shape2.IsNull()) {
        return TopoDS_Shape();
    }
    
    BRepAlgoAPI_Fuse fuseOp(shape1, shape2);
    if (fuseOp.IsDone()) {
        return fuseOp.Shape();
    }
    return TopoDS_Shape();
}

TopoDS_Shape BooleanOperations::subtract(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2) {
    if (shape1.IsNull() || shape2.IsNull()) {
        return TopoDS_Shape();
    }
    
    BRepAlgoAPI_Cut cutOp(shape1, shape2);
    if (cutOp.IsDone()) {
        return cutOp.Shape();
    }
    return TopoDS_Shape();
}

TopoDS_Shape BooleanOperations::intersect(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2) {
    if (shape1.IsNull() || shape2.IsNull()) {
        return TopoDS_Shape();
    }
    
    BRepAlgoAPI_Common commonOp(shape1, shape2);
    if (commonOp.IsDone()) {
        return commonOp.Shape();
    }
    return TopoDS_Shape();
}

TopoDS_Shape BooleanOperations::section(const TopoDS_Shape& shape1, const TopoDS_Shape& shape2) {
    if (shape1.IsNull() || shape2.IsNull()) {
        return TopoDS_Shape();
    }
    
    BRepAlgoAPI_Section sectionOp(shape1, shape2);
    if (sectionOp.IsDone()) {
        return sectionOp.Shape();
    }
    return TopoDS_Shape();
}

TopoDS_Shape BooleanOperations::split(const TopoDS_Shape& shape, const TopoDS_Shape& tool) {
    if (shape.IsNull() || tool.IsNull()) {
        return TopoDS_Shape();
    }
    
    BRepAlgoAPI_Splitter splitterOp;
    splitterOp.AddArgument(shape);
    splitterOp.AddTool(tool);
    
    if (splitterOp.IsDone()) {
        return splitterOp.Shape();
    }
    return TopoDS_Shape();
}

TopoDS_Shape BooleanOperations::defeature(const TopoDS_Shape& shape, const std::vector<TopoDS_Shape>& features) {
    if (shape.IsNull() || features.empty()) {
        return TopoDS_Shape();
    }
    
    BRepAlgoAPI_Defeaturing defeatureOp(shape);
    
    for (const auto& feature : features) {
        if (!feature.IsNull()) {
            defeatureOp.AddFaceToRemove(feature);
        }
    }
    
    if (defeatureOp.IsDone()) {
        return defeatureOp.Shape();
    }
    return TopoDS_Shape();
}

} // namespace TheSolution
