#include <pybind11/pybind11.h>
#include "integrator.hpp"

namespace py = pybind11;

PYBIND11_MODULE(motion_core, m)
{
    py::class_<Integrator>(m, "Integrator")
        .def(py::init<>())
        .def("set_speed", &Integrator::setSpeed)
        .def("update", &Integrator::update)
        .def("get_x", &Integrator::getX)
        .def("get_y", &Integrator::getY)
        .def("reset", &Integrator::reset);
}