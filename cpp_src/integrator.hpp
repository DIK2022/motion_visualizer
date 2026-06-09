#pragma once

class Integrator
{
public:
    Integrator();
    void setSpeed(double vx, double vy);
    void update(double dt);
    double getX() const;
    double getY() const;
    void reset();

private:
    double x, y;
    double vx, vy;
};