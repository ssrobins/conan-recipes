cmake_minimum_required(VERSION 3.17)

project(Project)

set(CMAKE_FIND_ROOT_PATH ${CMAKE_BINARY_DIR})

find_package(cmake_utils REQUIRED)

include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/global_settings_thirdparty.cmake)

option(BUILD_ZLIB_EXAMPLE "Build zlib example" OFF)
option(BUILD_ZLIB_MINIGZIP "Build zlib gzip example" OFF)
option(BUILD_ZLIB_SHARED "Build zlib shared library" OFF)

add_subdirectory(source)

set_target_properties(zlibstatic PROPERTIES DEBUG_POSTFIX d)
