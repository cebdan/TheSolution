# Operation Solution C++ компоненты
cmake_minimum_required(VERSION 3.16)

# Создание библиотеки операционных компонентов
add_library(thesolution_operations STATIC
    geometry_operations.cpp
    visualization_3d.cpp
    boolean_operations.cpp
)

# Включение заголовочных файлов
target_include_directories(thesolution_operations PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/../opencascade
    ${CMAKE_CURRENT_SOURCE_DIR}/../../Base Solution/include
)

# Линковка библиотек
target_link_libraries(thesolution_operations PUBLIC
    thesolution_base
    ${OpenCASCADE_LIBRARIES}
    Qt6::Core
    Qt6::Widgets
    Qt6::OpenGL
)

# Установка заголовочных файлов
install(FILES 
    ../opencascade/geometry_operations.h
    ../opencascade/visualization_3d.h
    ../opencascade/boolean_operations.h
    DESTINATION include/thesolution/operations
)
