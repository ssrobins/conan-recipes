cmake_minimum_required(VERSION 3.17)

set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE false)

project(Project)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(freetype REQUIRED)
set(FREETYPE_INCLUDE_DIRS ${freetype_INCLUDE_DIRS_DEBUG}${freetype_INCLUDE_DIRS_RELEASE})

if(APPLE)
    set(SFML_DEPENDENCIES_INSTALL_PREFIX "Frameworks" CACHE PATH "External libraries (FLAC, Freetype, Vorbis, ...) installation directory")
endif()

option(BUILD_SHARED_LIBS OFF)
option(SFML_BUILD_EXAMPLES OFF)
option(SFML_GENERATE_PDB ON)
option(SFML_USE_STATIC_STD_LIBS ON)

add_subdirectory(source)
