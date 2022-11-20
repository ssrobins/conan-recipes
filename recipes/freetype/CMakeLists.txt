cmake_minimum_required(VERSION 3.17)

set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE false)
set(CMAKE_OPTIMIZE_DEPENDENCIES true)

project(Project)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

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
