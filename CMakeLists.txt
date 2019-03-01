cmake_minimum_required(VERSION 2.8.11)

include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(SDL_SHARED "Build a shared version of the library" OFF)

if(ANDROID)
    option(SDL_STATIC_PIC "Static version of the library should be built with Position Independent Code" ON)
endif()

add_subdirectory(source)
