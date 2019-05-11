cmake_minimum_required(VERSION 3.14)

include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(SDL_SHARED "Build a shared version of the library" OFF)

if(ANDROID)
    option(SDL_STATIC_PIC "Static version of the library should be built with Position Independent Code" ON)
elseif(IOS)
    set(CMAKE_XCODE_ATTRIBUTE_CLANG_ENABLE_OBJC_ARC YES)
endif()

add_subdirectory(source)

if(MSVC)
    target_compile_options(SDL2-static
      PRIVATE
        /Fd$<TARGET_FILE_DIR:SDL2-static>/SDL2-static$<$<CONFIG:Debug>:d>.pdb
    )
    target_compile_options(SDL2main
      PRIVATE
        /Fd$<TARGET_FILE_DIR:SDL2main>/SDL2main$<$<CONFIG:Debug>:d>.pdb
    )
endif()
