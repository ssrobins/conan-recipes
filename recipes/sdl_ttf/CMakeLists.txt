cmake_minimum_required(VERSION 3.17)

project(Project)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(cmake_utils REQUIRED)

include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/global_settings_thirdparty.cmake)

option(BUILD_SHARED_LIBS "Build the library as a shared library" OFF)
option(SDL2TTF_VENDORED "Use vendored third-party libraries" OFF})

add_subdirectory(source)

set_target_properties(SDL2_ttf PROPERTIES DEBUG_POSTFIX d)
