cmake_minimum_required(VERSION 3.17)

set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE false)

project(Project)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(ogg REQUIRED)
set(OGG_INCLUDE_DIR ${ogg_INCLUDE_DIRS_DEBUG}${ogg_INCLUDE_DIRS_RELEASE})

add_subdirectory(source)

target_include_directories(vorbis PUBLIC
    ${OGG_INCLUDE_DIR}
)

set_target_properties(vorbisfile vorbisenc vorbis PROPERTIES DEBUG_POSTFIX d)
