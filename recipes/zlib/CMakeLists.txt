cmake_minimum_required(VERSION 3.17)

set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE false)

project(Project)

option(BUILD_ZLIB_EXAMPLE "Build zlib example" OFF)
option(BUILD_ZLIB_MINIGZIP "Build zlib gzip example" OFF)
option(BUILD_ZLIB_SHARED "Build zlib shared library" OFF)

add_subdirectory(source)

set_target_properties(zlibstatic PROPERTIES DEBUG_POSTFIX d)
