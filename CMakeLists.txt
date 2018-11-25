include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(SDL_SHARED "Build a shared version of the library" OFF)

add_subdirectory(source)