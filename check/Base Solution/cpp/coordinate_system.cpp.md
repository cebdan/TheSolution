#include "../include/solution_coordinate.h"
#include <opencascade/gp_Pnt.hxx>
#include <opencascade/gp_Ax2.hxx>
#include <opencascade/gp_Dir.hxx>
#include <opencascade/gp_Vec.hxx>
#include <cmath>

namespace TheSolution {

SolutionCoordinate::SolutionCoordinate()
    : x_(0.0), y_(0.0), z_(0.0)
{
}

SolutionCoordinate::SolutionCoordinate(double x, double y, double z)
    : x_(x), y_(y), z_(z)
{
}

double SolutionCoordinate::getX() const { return x_; }
double SolutionCoordinate::getY() const { return y_; }
double SolutionCoordinate::getZ() const { return z_; }

void SolutionCoordinate::setX(double x) { x_ = x; }
void SolutionCoordinate::setY(double y) { y_ = y; }
void SolutionCoordinate::setZ(double z) { z_ = z; }

void SolutionCoordinate::set(double x, double y, double z) {
    x_ = x;
    y_ = y;
    z_ = z;
}

double SolutionCoordinate::distance(const SolutionCoordinate& other) const {
    double dx = x_ - other.x_;
    double dy = y_ - other.y_;
    double dz = z_ - other.z_;
    return sqrt(dx*dx + dy*dy + dz*dz);
}

void SolutionCoordinate::translate(double dx, double dy, double dz) {
    x_ += dx;
    y_ += dy;
    z_ += dz;
}

void SolutionCoordinate::rotate(double angle, double ax, double ay, double az) {
    // Простое вращение вокруг оси
    double cos_a = cos(angle);
    double sin_a = sin(angle);
    
    // Нормализация оси вращения
    double len = sqrt(ax*ax + ay*ay + az*az);
    if (len > 0) {
        ax /= len;
        ay /= len;
        az /= len;
    }
    
    // Матрица вращения
    double x_new = x_ * (cos_a + ax*ax*(1-cos_a)) + 
                   y_ * (ax*ay*(1-cos_a) - az*sin_a) + 
                   z_ * (ax*az*(1-cos_a) + ay*sin_a);
    
    double y_new = x_ * (ay*ax*(1-cos_a) + az*sin_a) + 
                   y_ * (cos_a + ay*ay*(1-cos_a)) + 
                   z_ * (ay*az*(1-cos_a) - ax*sin_a);
    
    double z_new = x_ * (az*ax*(1-cos_a) - ay*sin_a) + 
                   y_ * (az*ay*(1-cos_a) + ax*sin_a) + 
                   z_ * (cos_a + az*az*(1-cos_a));
    
    x_ = x_new;
    y_ = y_new;
    z_ = z_new;
}

gp_Pnt SolutionCoordinate::toGpPnt() const {
    return gp_Pnt(x_, y_, z_);
}

gp_Ax2 SolutionCoordinate::toGpAx2() const {
    return gp_Ax2(toGpPnt(), gp::DZ());
}

} // namespace TheSolution
