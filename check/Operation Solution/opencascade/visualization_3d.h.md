#pragma once

#include <QOpenGLWidget>
#include <QOpenGLFunctions>
#include <QOpenGLShaderProgram>
#include <QOpenGLBuffer>
#include <QOpenGLVertexArrayObject>
#include <QMatrix4x4>
#include <QVector3D>
#include <memory>
#include <vector>
#include <opencascade/TopoDS_Shape.hxx>
#include <opencascade/AIS_InteractiveContext.hxx>
#include <opencascade/V3d_View.hxx>
#include <opencascade/AIS_Shape.hxx>
#include <opencascade/Graphic3d_GraphicDriver.hxx>
#include <opencascade/OpenGl_GraphicDriver.hxx>
#include <opencascade/Aspect_DisplayConnection.hxx>
#include <opencascade/OpenGl_Context.hxx>

namespace TheSolution {

// Класс для 3D визуализации с OpenCASCADE
class Visualization3D : public QOpenGLWidget, protected QOpenGLFunctions {
    Q_OBJECT

public:
    explicit Visualization3D(QWidget* parent = nullptr);
    ~Visualization3D();

    // Основные методы
    void addShape(const TopoDS_Shape& shape, const QString& name = "");
    void removeShape(const QString& name);
    void clearShapes();
    
    // Управление камерой
    void setViewFront();
    void setViewBack();
    void setViewLeft();
    void setViewRight();
    void setViewTop();
    void setViewBottom();
    void setViewIsometric();
    
    // Управление отображением
    void setWireframeMode(bool enabled);
    void setShadedMode(bool enabled);
    void setTransparency(double transparency);
    
    // Управление освещением
    void setLighting(bool enabled);
    void setBackgroundColor(const QColor& color);
    
    // Экспорт
    void exportToImage(const QString& filename);
    void exportToSTEP(const QString& filename);

protected:
    // QOpenGLWidget переопределения
    void initializeGL() override;
    void paintGL() override;
    void resizeGL(int width, int height) override;
    
    // Обработка событий мыши
    void mousePressEvent(QMouseEvent* event) override;
    void mouseMoveEvent(QMouseEvent* event) override;
    void mouseReleaseEvent(QMouseEvent* event) override;
    void wheelEvent(QWheelEvent* event) override;

private:
    // OpenCASCADE компоненты
    Handle(AIS_InteractiveContext) context_;
    Handle(V3d_View) view_;
    Handle(Graphic3d_GraphicDriver) driver_;
    Handle(Aspect_DisplayConnection) displayConnection_;
    
    // Список отображаемых объектов
    std::vector<std::pair<Handle(AIS_Shape), QString>> shapes_;
    
    // Состояние камеры
    QVector3D cameraPosition_;
    QVector3D cameraTarget_;
    QVector3D cameraUp_;
    double cameraDistance_;
    
    // Состояние мыши
    QPoint lastMousePos_;
    bool mousePressed_;
    Qt::MouseButton pressedButton_;
    
    // Настройки отображения
    bool wireframeMode_;
    bool shadedMode_;
    bool lightingEnabled_;
    double transparency_;
    QColor backgroundColor_;
    
    // Внутренние методы
    void initializeOpenCASCADE();
    void setupCamera();
    void setupLighting();
    void updateView();
    void handleMouseRotation(const QPoint& delta);
    void handleMousePan(const QPoint& delta);
    void handleMouseZoom(int delta);
    
    // Утилиты
    QVector3D screenToWorld(const QPoint& screenPos);
    QPoint worldToScreen(const QVector3D& worldPos);
};

// Класс для управления сценой
class SceneManager {
public:
    SceneManager();
    ~SceneManager();
    
    // Управление объектами
    void addObject(const TopoDS_Shape& shape, const QString& name);
    void removeObject(const QString& name);
    void clearObjects();
    
    // Получение объектов
    std::vector<TopoDS_Shape> getObjects() const;
    TopoDS_Shape getObject(const QString& name) const;
    
    // Операции с объектами
    void selectObject(const QString& name);
    void deselectObject(const QString& name);
    void highlightObject(const QString& name, bool highlight);
    
    // Экспорт сцены
    void exportScene(const QString& filename);

private:
    std::vector<std::pair<TopoDS_Shape, QString>> objects_;
    QString selectedObject_;
};

} // namespace TheSolution
