cmake_minimum_required(VERSION 3.17)

set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE false)
set(CMAKE_OPTIMIZE_DEPENDENCIES true)

project(Project)

option(SDL_SHARED "Build a shared version of the library" OFF)
option(SDL_TEST "Build the SDL2_test library" OFF)
option(SDL_STATIC_PIC "Static version of the library should be built with Position Independent Code" ON)
option(SDL2_DISABLE_INSTALL "Disable installation of SDL2" OFF)

if(IOS)
    set(CMAKE_XCODE_ATTRIBUTE_CLANG_ENABLE_OBJC_ARC YES)
endif()

add_subdirectory(source)

set_target_properties(SDL2-static SDL2main PROPERTIES DEBUG_POSTFIX "d")

if(MSVC)
    target_compile_definitions(SDL2-static
      PRIVATE
        # Work around error LNK2005: __ftol2_sse already defined in SDL2.lib(SDL_stdlib.obj)
        HAVE_LIBC
    )
endif()
