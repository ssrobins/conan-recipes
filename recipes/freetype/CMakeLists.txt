cmake_minimum_required(VERSION 3.17)

project(Project)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(zlib REQUIRED)
set(ZLIB_INCLUDE_DIR ${zlib_INCLUDE_DIRS_DEBUG}${zlib_INCLUDE_DIRS_RELEASE})

option(FT_REQUIRE_BZIP2
    "Require support of bzip2 compressed fonts." ON)
option(FT_REQUIRE_PNG
    "Require support of PNG compressed OpenType embedded bitmaps." ON)
option(FT_REQUIRE_ZLIB
    "Require system zlib instead of internal zlib library." ON)
option(FT_DISABLE_BROTLI
    "Disable support of compressed WOFF2 fonts." ON)
option(FT_DISABLE_HARFBUZZ
    "Disable HarfBuzz (used for improving auto-hinting of OpenType fonts)." ON)

add_subdirectory(source)
