cmake_minimum_required(VERSION 3.17)

project(Project)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(cmake_utils REQUIRED)

find_package(ogg REQUIRED)
set(OGG_INCLUDE_DIR ${ogg_INCLUDE_DIRS_DEBUG}${ogg_INCLUDE_DIRS_RELEASE})

include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/global_settings_thirdparty.cmake)

add_subdirectory(source)

target_include_directories(vorbis PUBLIC
    ${OGG_INCLUDE_DIR}
)

set_target_properties(vorbisfile vorbisenc vorbis PROPERTIES DEBUG_POSTFIX d)
