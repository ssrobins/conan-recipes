cmake_minimum_required(VERSION 3.14)

include(conanbuildinfo.cmake)
conan_basic_setup()

include(${CONAN_CMAKE_UTILS_ROOT}/global_settings_thirdparty.cmake)

add_subdirectory(source)
