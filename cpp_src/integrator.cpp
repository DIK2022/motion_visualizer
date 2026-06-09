#include "integrator.hpp"

Integrator::Integrator() : x(0.0), y(0.0), vx(10.0), vy(10.0) {}

void Integrator::setSpeed(double vx, double vy)
{
    this->vx = vx;
    this->vy = vy;
}

void Integrator::update(double dt)
{
    x += vx * dt;
    y += vy * dt;
}

double Integrator::getX() const { return x; }
double Integrator::getY() const { return y; }

void Integrator::reset()
{
    x = 0.0;
    y = 0.0;
}