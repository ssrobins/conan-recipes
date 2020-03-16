cmake_minimum_required(VERSION 3.17)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include(${CONAN_CMAKE_UTILS_ROOT}/global_settings.cmake)

# Helper functions
include(${CONAN_CMAKE_UTILS_ROOT}/add_executable_custom.cmake)
include(${CONAN_CMAKE_UTILS_ROOT}/add_test_executable.cmake)

enable_testing()

add_subdirectory(Display)
add_subdirectory(DisplayTest)
add_subdirectory(ErrorHandler)
add_subdirectory(Game)
