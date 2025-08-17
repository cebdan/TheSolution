#pragma once

#include <pybind11/pybind11.h>
#include <TopoDS_Shape.hxx>
#include <gp_Trsf.hxx>
#include <string>
#include <memory>

namespace py = pybind11;

/**
 * @brief Структура координат для Solution объектов
 * 
 * Содержит позиционные (x, y, z) и ориентационные (a, b, c) координаты
 * Все значения являются управляемыми параметрическими величинами
 */
struct SolutionCoordinate {
    // Позиционные координаты
    double x = 0.0;  // Координата X (смещение по оси X)
    double y = 0.0;  // Координата Y (смещение по оси Y) 
    double z = 0.0;  // Координата Z (смещение по оси Z)
    
    // Ориентационные координаты (векторы направления/поворота)
    double a = 1.0;  // Вектор направления по оси X
    double b = 1.0;  // Вектор направления по оси Y
    double c = 1.0;  // Вектор направления по оси Z
    
    // Конструкторы
    SolutionCoordinate() = default;
    SolutionCoordinate(double x, double y, double z, double a = 1.0, double b = 1.0, double c = 1.0);
    
    // Методы
    std::tuple<double, double, double> GetPosition() const;
    std::tuple<double, double, double> GetOrientation() const;
    gp_Trsf GetTransformation() const;
    
    // Операторы
    SolutionCoordinate operator+(const SolutionCoordinate& other) const;
    SolutionCoordinate operator-(const SolutionCoordinate& other) const;
    bool operator==(const SolutionCoordinate& other) const;
};

/**
 * @brief Базовый класс для всех объектов в CAD системе
 * 
 * Каждый объект в системе наследуется от этого класса
 * Содержит координаты, иерархическую структуру и базовый функционал
 */
class CSolution {
protected:
    std::string name_;
    SolutionCoordinate coordinate_;
    std::vector<std::shared_ptr<CSolution>> children_;
    std::weak_ptr<CSolution> parent_;
    std::string id_;
    bool visible_ = true;
    bool locked_ = false;

public:
    // Конструкторы
    CSolution(const std::string& name = "Solution", const SolutionCoordinate& coordinate = SolutionCoordinate());
    virtual ~CSolution() = default;
    
    // Основные методы
    void SetName(const std::string& name) { name_ = name; }
    std::string GetName() const { return name_; }
    
    void SetCoordinate(const SolutionCoordinate& coord) { coordinate_ = coord; }
    SolutionCoordinate GetCoordinate() const { return coordinate_; }
    
    // Иерархические методы
    void AddChild(std::shared_ptr<CSolution> child);
    void RemoveChild(const std::string& child_id);
    std::vector<std::shared_ptr<CSolution>> GetChildren() const { return children_; }
    std::shared_ptr<CSolution> GetParent() const { return parent_.lock(); }
    
    // Координатные методы
    void MoveTo(double x, double y, double z);
    void Translate(double dx, double dy, double dz);
    void SetOrientation(double a, double b, double c);
    SolutionCoordinate GetAbsoluteCoordinate() const;
    
    // Управление видимостью и блокировкой
    void SetVisible(bool visible) { visible_ = visible; }
    bool IsVisible() const { return visible_; }
    void SetLocked(bool locked) { locked_ = locked; }
    bool IsLocked() const { return locked_; }
    
    // Уникальный идентификатор
    std::string GetId() const { return id_; }
    
    // Виртуальные методы для переопределения
    virtual std::string GetType() const { return "Solution"; }
    virtual bool IsValid() const { return true; }
    
protected:
    std::string GenerateId() const;
    SolutionCoordinate CombineCoordinates(const SolutionCoordinate& parent, const SolutionCoordinate& child) const;
};
