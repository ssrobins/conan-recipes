cmake_minimum_required(VERSION 2.8.8)

include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(INSTALL_GMOCK OFF)
option(INSTALL_GTEST OFF)

add_subdirectory(source)
