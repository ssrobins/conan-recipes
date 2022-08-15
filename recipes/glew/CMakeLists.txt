cmake_minimum_required(VERSION 3.17)

project(Project)

option(BUILD_SHARED_LIBS "install/link shared instead of static libs" OFF)
option(BUILD_UTILS "utilities" OFF)

add_subdirectory(source/build/cmake)
