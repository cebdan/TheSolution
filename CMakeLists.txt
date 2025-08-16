cmake_minimum_required(VERSION 3.16)
project(TheSolution VERSION 1.0.0 LANGUAGES CXX)

# Настройки C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Настройки сборки
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Поиск Python
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Поиск pybind11
find_package(pybind11 REQUIRED)

# Поиск Qt6
find_package(Qt6 COMPONENTS Core Widgets OpenGL REQUIRED)

# Поиск OpenCASCADE
find_package(OpenCASCADE REQUIRED)

# Включение директорий
include_directories(${CMAKE_SOURCE_DIR}/Base Solution/include)
include_directories(${CMAKE_SOURCE_DIR}/Operation Solution/opencascade)

# Сборка базовых компонентов
add_subdirectory("Base Solution/cpp")
add_subdirectory("Operation Solution/cpp")

# Создание Python модуля
pybind11_add_module(thesolution_core 
    "Base Solution/python/coordinate_bindings.cpp"
    "Operation Solution/python/operation_bindings.cpp"
)

# Линковка библиотек
target_link_libraries(thesolution_core 
    PRIVATE 
    thesolution_base
    thesolution_operations
    ${OpenCASCADE_LIBRARIES}
    Qt6::Core
    Qt6::Widgets
    Qt6::OpenGL
)

# Установка
install(TARGETS thesolution_core
    LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/python${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR}/site-packages
)

# Копирование Python файлов
install(DIRECTORY "Base Solution/python/"
    DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/python${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR}/site-packages/thesolution
    FILES_MATCHING PATTERN "*.py"
)

install(DIRECTORY "Operation Solution/python/"
    DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/python${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR}/site-packages/thesolution
    FILES_MATCHING PATTERN "*.py"
)
