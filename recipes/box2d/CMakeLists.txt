cmake_minimum_required(VERSION 3.17)

set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE false)
set(CMAKE_OPTIMIZE_DEPENDENCIES true)

project(Project)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

option(BOX2D_BUILD_EXAMPLES "Build Box2D examples" OFF)
option(BOX2D_INSTALL "Install Box2D libs, includes, and CMake scripts" ON)

add_subdirectory(source)

set_target_properties(box2d PROPERTIES DEBUG_POSTFIX d)
