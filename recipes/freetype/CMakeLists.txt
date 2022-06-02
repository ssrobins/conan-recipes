cmake_minimum_required(VERSION 3.17)

project(Project)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(cmake_utils REQUIRED)

find_package(zlib REQUIRED)
set(ZLIB_INCLUDE_DIR ${zlib_INCLUDE_DIRS_DEBUG}${zlib_INCLUDE_DIRS_RELEASE})

include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/global_settings_thirdparty.cmake)

option(FT_WITH_BZIP2 "Support bzip2 compressed fonts." ON)
option(FT_WITH_PNG "Support PNG compressed OpenType embedded bitmaps." ON)
option(FT_WITH_ZLIB "Use system zlib instead of internal library." ON)
set(CMAKE_DISABLE_FIND_PACKAGE_BrotliDec true)

add_subdirectory(source)
