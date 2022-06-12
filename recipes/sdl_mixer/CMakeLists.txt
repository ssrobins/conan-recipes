cmake_minimum_required(VERSION 3.17)

project(Project)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(cmake_utils REQUIRED)
find_package(sdl REQUIRED)
find_package(vorbis REQUIRED)

include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/global_settings_thirdparty.cmake)

add_subdirectory(source)
