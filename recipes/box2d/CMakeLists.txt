cmake_minimum_required(VERSION 3.17)

project(Project)

option(BOX2D_BUILD_EXAMPLES "Build Box2D examples" OFF)
option(BOX2D_INSTALL "Install Box2D libs, includes, and CMake scripts" ON)

add_subdirectory(source/Box2D)

set_target_properties(Box2D PROPERTIES DEBUG_POSTFIX d)
