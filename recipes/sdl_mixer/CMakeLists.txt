cmake_minimum_required(VERSION 3.17)

project(Project)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(cmake_utils REQUIRED)

include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/global_settings_thirdparty.cmake)

option(BUILD_SHARED_LIBS "Build the library as a shared library" OFF)
option(SDL2MIXER_FLAC "Enable FLAC music" OFF)
option(SDL2MIXER_MIDI "Enable MIDI music" OFF)
option(SDL2MIXER_MOD "Support loading MOD music" OFF)
option(SDL2MIXER_OPUS "Enable Opus music" OFF)

add_subdirectory(source)

set_target_properties(SDL2_mixer PROPERTIES
    OUTPUT_NAME "SDL2_mixer"
)
