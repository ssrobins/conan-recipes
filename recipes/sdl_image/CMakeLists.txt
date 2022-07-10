cmake_minimum_required(VERSION 3.17)

project(Project)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(cmake_utils REQUIRED)

include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/global_settings_thirdparty.cmake)

option(BUILD_SHARED_LIBS "Build the library as a shared library" OFF)
option(SDL2IMAGE_BMP "Support loading BMP images" OFF)
option(SDL2IMAGE_GIF "Support loading GIF images" OFF)
option(SDL2IMAGE_JPG "Support loading JPEG images" OFF)
option(SDL2IMAGE_LBM "Support loading LBM images" OFF)
option(SDL2IMAGE_PCX "Support loading PCX images" OFF)
option(SDL2IMAGE_PNG "Support loading PNG images" OFF)
option(SDL2IMAGE_PNM "Support loading PNM images" OFF)
option(SDL2IMAGE_QOI "Support loading QOI images" OFF)
option(SDL2IMAGE_SVG "Support loading SVG images" OFF)
option(SDL2IMAGE_TGA "Support loading TGA images" OFF)
option(SDL2IMAGE_XCF "Support loading XCF images" OFF)
option(SDL2IMAGE_XPM "Support loading XPM images" OFF)
option(SDL2IMAGE_XV "Support loading XV images" OFF)

if(APPLE)
    option(SDL2IMAGE_BACKEND_IMAGEIO "Use native Mac OS X frameworks for loading images" OFF)
endif()

add_subdirectory(source)

set_target_properties(SDL2_image PROPERTIES
    OUTPUT_NAME "SDL2_image"
)
