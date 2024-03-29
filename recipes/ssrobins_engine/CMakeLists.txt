cmake_minimum_required(VERSION 3.17)

set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE false)
set(CMAKE_OPTIMIZE_DEPENDENCIES true)

project(Project)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(cmake_utils REQUIRED)
find_package(gtest REQUIRED)
find_package(SDL2 REQUIRED)
find_package(sdl_image REQUIRED)
find_package(sdl_mixer REQUIRED)
find_package(sdl_ttf REQUIRED)

include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/global_settings.cmake)

# Helper functions
include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/add_executable_custom.cmake)
include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/add_test_executable.cmake)

enable_testing()

add_subdirectory(Display)
add_subdirectory(DisplayTest)
add_subdirectory(ErrorHandler)
add_subdirectory(Game)
