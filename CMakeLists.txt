cmake_minimum_required(VERSION 3.14)

include(cmake/global_settings.cmake)

# Helper functions
include(cmake/add_executable_custom.cmake)
include(cmake/add_test_executable.cmake)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

enable_testing()

add_subdirectory(Display)
add_subdirectory(DisplayTest)
add_subdirectory(ErrorHandler)
add_subdirectory(Game)
