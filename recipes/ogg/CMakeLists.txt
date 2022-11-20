cmake_minimum_required(VERSION 3.17)

set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE false)
set(CMAKE_OPTIMIZE_DEPENDENCIES true)

project(Project)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

add_subdirectory(source)

set_target_properties(ogg PROPERTIES DEBUG_POSTFIX d)
