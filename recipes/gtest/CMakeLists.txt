cmake_minimum_required(VERSION 3.17)

project(Project)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(cmake_utils REQUIRED)

include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/global_settings_thirdparty.cmake)

option(INSTALL_GMOCK OFF)
option(INSTALL_GTEST OFF)

add_subdirectory(source)

set_target_properties(gmock_main gmock gtest_main gtest PROPERTIES DEBUG_POSTFIX d)
