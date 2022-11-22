cmake_minimum_required(VERSION 3.17)

set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE false)
set(CMAKE_OPTIMIZE_DEPENDENCIES true)

project(Project)

option(BUILD_SHARED_LIBS "Build the library as a shared library" OFF)
option(SDL2TTF_SAMPLES "Build the SDL2_ttf sample program(s)" OFF)
option(SDL2TTF_VENDORED "Use vendored third-party libraries" OFF})

add_subdirectory(source)

set_target_properties(SDL2_ttf PROPERTIES DEBUG_POSTFIX d)
