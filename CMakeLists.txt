include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

if(APPLE)
    set(SFML_DEPENDENCIES_INSTALL_PREFIX "Frameworks" CACHE PATH "External libraries (FLAC, Freetype, Vorbis, ...) installation directory")
endif()

option(BUILD_SHARED_LIBS OFF)
option(SFML_BUILD_EXAMPLES OFF)
option(SFML_USE_STATIC_STD_LIBS ON)

add_subdirectory(source)

target_compile_options(sfml-graphics PUBLIC
    -DSFML_STATIC
)
