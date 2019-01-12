include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(BUILD_SHARED_LIBS OFF)

add_subdirectory(source/build/cmake)