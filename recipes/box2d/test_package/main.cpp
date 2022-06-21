#include "Box2d/Box2D.h"

int main(int argc, char *argv[])
{
    b2Vec2 gravity(0.0f, -10.0f);
    b2World world(gravity);
    return 0;
}
