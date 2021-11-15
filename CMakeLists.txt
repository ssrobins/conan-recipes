cmake_minimum_required(VERSION 3.17)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include(${CONAN_CMAKE_UTILS_ROOT}/global_settings_thirdparty.cmake)

option(BUILD_UTILS OFF)

add_subdirectory(source/build/cmake)
