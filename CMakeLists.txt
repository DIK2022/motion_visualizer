cmake_minimum_required(VERSION 3.15)
project(motion_visualizer_core)

set(CMAKE_CXX_STANDARD 17)

# Находим Python и pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(motion_core
    cpp_src/integrator.cpp
    cpp_src/bindings.cpp
)

target_include_directories(motion_core PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/cpp_src)

# Устанавливаем модуль в папку src/motion_visualizer/cpp_bridge
install(TARGETS motion_core DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/src/motion_visualizer/cpp_bridge)
