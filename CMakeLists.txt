cmake_minimum_required(VERSION 3.17)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include(${CONAN_CMAKE_UTILS_ROOT}/global_settings_thirdparty.cmake)

option(INSTALL_GMOCK OFF)
option(INSTALL_GTEST OFF)

add_subdirectory(source)
