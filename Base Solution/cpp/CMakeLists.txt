# Base Solution C++ компоненты
cmake_minimum_required(VERSION 3.16)

# Создание библиотеки базовых компонентов
add_library(thesolution_base STATIC
    coordinate_system.cpp
    solution_base.cpp
    geometry_primitives.cpp
)

# Включение заголовочных файлов
target_include_directories(thesolution_base PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/../include
)

# Линковка OpenCASCADE
target_link_libraries(thesolution_base PUBLIC
    ${OpenCASCADE_LIBRARIES}
)

# Установка заголовочных файлов
install(FILES 
    ../include/solution_coordinate.h
    ../include/solution_base.h
    ../include/geometry_primitives.h
    DESTINATION include/thesolution
)
