#include "../opencascade/visualization_3d.h"
#include <QMouseEvent>
#include <QWheelEvent>
#include <QPainter>
#include <QApplication>
#include <QScreen>
#include <opencascade/Graphic3d_GraphicDriver.hxx>
#include <opencascade/OpenGl_GraphicDriver.hxx>
#include <opencascade/Aspect_DisplayConnection.hxx>
#include <opencascade/OpenGl_Context.hxx>
#include <opencascade/AIS_InteractiveContext.hxx>
#include <opencascade/V3d_View.hxx>
#include <opencascade/AIS_Shape.hxx>
#include <opencascade/Prs3d_Drawer.hxx>
#include <opencascade/Graphic3d_MaterialAspect.hxx>
#include <opencascade/Graphic3d_Texture2Dmanual.hxx>
#include <opencascade/STEPControl_Writer.hxx>
#include <opencascade/Interface_Static.hxx>

namespace TheSolution {

Visualization3D::Visualization3D(QWidget* parent)
    : QOpenGLWidget(parent)
    , cameraPosition_(0, 0, 10)
    , cameraTarget_(0, 0, 0)
    , cameraUp_(0, 1, 0)
    , cameraDistance_(10.0)
    , mousePressed_(false)
    , wireframeMode_(false)
    , shadedMode_(true)
    , lightingEnabled_(true)
    , transparency_(0.0)
    , backgroundColor_(Qt::white)
{
    setFocusPolicy(Qt::StrongFocus);
    setMouseTracking(true);
}

Visualization3D::~Visualization3D() {
    makeCurrent();
    // Очистка OpenCASCADE ресурсов
    if (!context_.IsNull()) {
        context_->RemoveAll(false);
    }
    doneCurrent();
}

void Visualization3D::initializeGL() {
    initializeOpenGLFunctions();
    
    // Инициализация OpenCASCADE
    initializeOpenCASCADE();
    
    // Настройка OpenGL
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);
    glEnable(GL_COLOR_MATERIAL);
    
    // Настройка камеры и освещения
    setupCamera();
    setupLighting();
}

void Visualization3D::initializeOpenCASCADE() {
    try {
        // Создание дисплей соединения
        displayConnection_ = new Aspect_DisplayConnection();
        
        // Создание графического драйвера
        driver_ = new OpenGl_GraphicDriver(displayConnection_);
        
        // Создание интерактивного контекста
        context_ = new AIS_InteractiveContext(driver_);
        
        // Создание вида
        view_ = new V3d_View(context_);
        
        // Настройка вида
        view_->SetBackgroundColor(Quantity_Color(backgroundColor_.redF(), 
                                                backgroundColor_.greenF(), 
                                                backgroundColor_.blueF(), 
                                                Quantity_TOC_RGB));
        
        // Установка размера
        view_->SetWindow(new Aspect_Window(winId()));
        view_->MustBeResized();
        
    } catch (const Standard_Failure& e) {
        qWarning("OpenCASCADE initialization failed: %s", e.GetMessageString());
    }
}

void Visualization3D::setupCamera() {
    if (view_.IsNull()) return;
    
    // Установка позиции камеры
    view_->SetEye(cameraPosition_.x(), cameraPosition_.y(), cameraPosition_.z());
    view_->SetAt(cameraTarget_.x(), cameraTarget_.y(), cameraTarget_.z());
    view_->SetUp(cameraUp_.x(), cameraUp_.y(), cameraUp_.z());
    
    // Настройка проекции
    view_->SetProj(0, 0, 1);
    view_->SetDepth(1000);
    
    // Обновление вида
    view_->Redraw();
}

void Visualization3D::setupLighting() {
    if (view_.IsNull()) return;
    
    // Настройка освещения
    view_->SetLightOn();
    
    // Основной источник света
    Handle(V3d_DirectionalLight) light = new V3d_DirectionalLight(V3d_XnegYposZpos, Quantity_Color(Quantity_NOC_WHITE), 1);
    view_->SetLightOn(light);
}

void Visualization3D::paintGL() {
    if (view_.IsNull()) return;
    
    // Очистка буфера
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    
    // Рендеринг OpenCASCADE сцены
    view_->Redraw();
}

void Visualization3D::resizeGL(int width, int height) {
    if (view_.IsNull()) return;
    
    // Обновление размера вида
    view_->MustBeResized();
    view_->Redraw();
}

void Visualization3D::addShape(const TopoDS_Shape& shape, const QString& name) {
    if (context_.IsNull() || shape.IsNull()) return;
    
    try {
        // Создание AIS_Shape для отображения
        Handle(AIS_Shape) aisShape = new AIS_Shape(shape);
        
        // Настройка отображения
        if (wireframeMode_) {
            aisShape->SetDisplayMode(AIS_WireFrame);
        } else if (shadedMode_) {
            aisShape->SetDisplayMode(AIS_Shaded);
        }
        
        // Настройка прозрачности
        if (transparency_ > 0.0) {
            aisShape->SetTransparency(transparency_);
        }
        
        // Добавление в контекст
        context_->Display(aisShape, Standard_True);
        
        // Сохранение в списке
        shapes_.push_back(std::make_pair(aisShape, name));
        
        // Обновление вида
        view_->FitAll();
        view_->Redraw();
        
    } catch (const Standard_Failure& e) {
        qWarning("Failed to add shape: %s", e.GetMessageString());
    }
}

void Visualization3D::removeShape(const QString& name) {
    if (context_.IsNull()) return;
    
    // Поиск и удаление формы
    for (auto it = shapes_.begin(); it != shapes_.end(); ++it) {
        if (it->second == name) {
            context_->Erase(it->first, Standard_True);
            shapes_.erase(it);
            view_->Redraw();
            break;
        }
    }
}

void Visualization3D::clearShapes() {
    if (context_.IsNull()) return;
    
    context_->RemoveAll(Standard_True);
    shapes_.clear();
    view_->Redraw();
}

void Visualization3D::setViewFront() {
    if (view_.IsNull()) return;
    view_->SetProj(0, 0, -1);
    view_->Redraw();
}

void Visualization3D::setViewBack() {
    if (view_.IsNull()) return;
    view_->SetProj(0, 0, 1);
    view_->Redraw();
}

void Visualization3D::setViewLeft() {
    if (view_.IsNull()) return;
    view_->SetProj(-1, 0, 0);
    view_->Redraw();
}

void Visualization3D::setViewRight() {
    if (view_.IsNull()) return;
    view_->SetProj(1, 0, 0);
    view_->Redraw();
}

void Visualization3D::setViewTop() {
    if (view_.IsNull()) return;
    view_->SetProj(0, 1, 0);
    view_->Redraw();
}

void Visualization3D::setViewBottom() {
    if (view_.IsNull()) return;
    view_->SetProj(0, -1, 0);
    view_->Redraw();
}

void Visualization3D::setViewIsometric() {
    if (view_.IsNull()) return;
    view_->SetProj(1, 1, 1);
    view_->Redraw();
}

void Visualization3D::setWireframeMode(bool enabled) {
    wireframeMode_ = enabled;
    if (enabled) {
        shadedMode_ = false;
    }
    
    // Обновление всех форм
    for (auto& shape : shapes_) {
        if (wireframeMode_) {
            shape.first->SetDisplayMode(AIS_WireFrame);
        } else {
            shape.first->SetDisplayMode(AIS_Shaded);
        }
    }
    
    if (!view_.IsNull()) {
        view_->Redraw();
    }
}

void Visualization3D::setShadedMode(bool enabled) {
    shadedMode_ = enabled;
    if (enabled) {
        wireframeMode_ = false;
    }
    
    // Обновление всех форм
    for (auto& shape : shapes_) {
        if (shadedMode_) {
            shape.first->SetDisplayMode(AIS_Shaded);
        } else {
            shape.first->SetDisplayMode(AIS_WireFrame);
        }
    }
    
    if (!view_.IsNull()) {
        view_->Redraw();
    }
}

void Visualization3D::setTransparency(double transparency) {
    transparency_ = qBound(0.0, transparency, 1.0);
    
    // Обновление всех форм
    for (auto& shape : shapes_) {
        shape.first->SetTransparency(transparency_);
    }
    
    if (!view_.IsNull()) {
        view_->Redraw();
    }
}

void Visualization3D::setLighting(bool enabled) {
    lightingEnabled_ = enabled;
    
    if (!view_.IsNull()) {
        if (enabled) {
            view_->SetLightOn();
        } else {
            view_->SetLightOff();
        }
        view_->Redraw();
    }
}

void Visualization3D::setBackgroundColor(const QColor& color) {
    backgroundColor_ = color;
    
    if (!view_.IsNull()) {
        view_->SetBackgroundColor(Quantity_Color(color.redF(), 
                                                color.greenF(), 
                                                color.blueF(), 
                                                Quantity_TOC_RGB));
        view_->Redraw();
    }
}

void Visualization3D::mousePressEvent(QMouseEvent* event) {
    lastMousePos_ = event->pos();
    mousePressed_ = true;
    pressedButton_ = event->button();
    setFocus();
}

void Visualization3D::mouseMoveEvent(QMouseEvent* event) {
    if (!mousePressed_ || view_.IsNull()) return;
    
    QPoint delta = event->pos() - lastMousePos_;
    
    switch (pressedButton_) {
        case Qt::LeftButton:
            handleMouseRotation(delta);
            break;
        case Qt::MiddleButton:
            handleMousePan(delta);
            break;
        default:
            break;
    }
    
    lastMousePos_ = event->pos();
}

void Visualization3D::mouseReleaseEvent(QMouseEvent* event) {
    mousePressed_ = false;
}

void Visualization3D::wheelEvent(QWheelEvent* event) {
    if (view_.IsNull()) return;
    
    handleMouseZoom(event->angleDelta().y());
}

void Visualization3D::handleMouseRotation(const QPoint& delta) {
    if (view_.IsNull()) return;
    
    // Вращение камеры
    view_->Rotation(delta.x(), delta.y());
}

void Visualization3D::handleMousePan(const QPoint& delta) {
    if (view_.IsNull()) return;
    
    // Перемещение камеры
    view_->Pan(delta.x(), -delta.y());
}

void Visualization3D::handleMouseZoom(int delta) {
    if (view_.IsNull()) return;
    
    // Масштабирование
    if (delta > 0) {
        view_->SetZoom(1.2);
    } else {
        view_->SetZoom(0.8);
    }
}

void Visualization3D::exportToImage(const QString& filename) {
    if (view_.IsNull()) return;
    
    // Экспорт в изображение
    view_->Dump(filename.toStdString().c_str());
}

void Visualization3D::exportToSTEP(const QString& filename) {
    try {
        STEPControl_Writer writer;
        
        // Добавление всех форм
        for (const auto& shape : shapes_) {
            writer.Transfer(shape.first->Shape(), STEPControl_AsIs);
        }
        
        // Сохранение файла
        IFSelect_ReturnStatus status = writer.Write(filename.toStdString().c_str());
        
        if (status != IFSelect_RetDone) {
            qWarning("Failed to export STEP file");
        }
        
    } catch (const Standard_Failure& e) {
        qWarning("STEP export failed: %s", e.GetMessageString());
    }
}

// SceneManager реализация
SceneManager::SceneManager() {
}

SceneManager::~SceneManager() {
    clearObjects();
}

void SceneManager::addObject(const TopoDS_Shape& shape, const QString& name) {
    objects_.push_back(std::make_pair(shape, name));
}

void SceneManager::removeObject(const QString& name) {
    for (auto it = objects_.begin(); it != objects_.end(); ++it) {
        if (it->second == name) {
            objects_.erase(it);
            break;
        }
    }
}

void SceneManager::clearObjects() {
    objects_.clear();
}

std::vector<TopoDS_Shape> SceneManager::getObjects() const {
    std::vector<TopoDS_Shape> shapes;
    for (const auto& obj : objects_) {
        shapes.push_back(obj.first);
    }
    return shapes;
}

TopoDS_Shape SceneManager::getObject(const QString& name) const {
    for (const auto& obj : objects_) {
        if (obj.second == name) {
            return obj.first;
        }
    }
    return TopoDS_Shape();
}

void SceneManager::selectObject(const QString& name) {
    selectedObject_ = name;
}

void SceneManager::deselectObject(const QString& name) {
    if (selectedObject_ == name) {
        selectedObject_.clear();
    }
}

void SceneManager::highlightObject(const QString& name, bool highlight) {
    // Реализация подсветки объектов
}

void SceneManager::exportScene(const QString& filename) {
    try {
        STEPControl_Writer writer;
        
        // Добавление всех объектов
        for (const auto& obj : objects_) {
            writer.Transfer(obj.first, STEPControl_AsIs);
        }
        
        // Сохранение файла
        IFSelect_ReturnStatus status = writer.Write(filename.toStdString().c_str());
        
        if (status != IFSelect_RetDone) {
            qWarning("Failed to export scene");
        }
        
    } catch (const Standard_Failure& e) {
        qWarning("Scene export failed: %s", e.GetMessageString());
    }
}

} // namespace TheSolution
