cmake_minimum_required(VERSION 3.17)

project(Project)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(zlib REQUIRED)
set(ZLIB_INCLUDE_DIR ${zlib_INCLUDE_DIRS_DEBUG}${zlib_INCLUDE_DIRS_RELEASE})

option(PNG_SHARED "Build shared lib" OFF)

# Workaround for this issue:
# https://sourceforge.net/p/libpng/bugs/281/
if(CMAKE_OSX_ARCHITECTURES MATCHES arm)
    set(PNG_ARM_NEON off CACHE STRING "")
endif()

add_subdirectory(source)

set_target_properties(png_static PROPERTIES DEBUG_POSTFIX d)
