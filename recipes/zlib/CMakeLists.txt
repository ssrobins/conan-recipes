cmake_minimum_required(VERSION 3.17)

set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE false)
set(CMAKE_OPTIMIZE_DEPENDENCIES true)

project(Project)

add_subdirectory(source)

set_target_properties(zlibstatic PROPERTIES DEBUG_POSTFIX d)
