cmake_minimum_required(VERSION 3.17)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include(${CONAN_CMAKE_UTILS_ROOT}/global_settings_thirdparty.cmake)

if(APPLE)
    set(SFML_DEPENDENCIES_INSTALL_PREFIX "Frameworks" CACHE PATH "External libraries (FLAC, Freetype, Vorbis, ...) installation directory")
endif()

option(BUILD_SHARED_LIBS OFF)
option(SFML_BUILD_EXAMPLES OFF)
option(SFML_GENERATE_PDB ON)
option(SFML_USE_STATIC_STD_LIBS ON)

add_subdirectory(source)
