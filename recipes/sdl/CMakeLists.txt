cmake_minimum_required(VERSION 3.17)

project(Project)

list(INSERT CMAKE_FIND_ROOT_PATH 0 ${CMAKE_BINARY_DIR})

find_package(cmake_utils REQUIRED)

include(${cmake_utils_PACKAGE_FOLDER_DEBUG}${cmake_utils_PACKAGE_FOLDER_RELEASE}/global_settings_thirdparty.cmake)

option(SDL_SHARED "Build a shared version of the library" OFF)

if(ANDROID)
    option(SDL_STATIC_PIC "Static version of the library should be built with Position Independent Code" ON)
elseif(IOS)
    set(CMAKE_XCODE_ATTRIBUTE_CLANG_ENABLE_OBJC_ARC YES)
endif()

add_subdirectory(source)

set_target_properties(SDL2-static PROPERTIES DEBUG_POSTFIX "d")
set_target_properties(SDL2main PROPERTIES DEBUG_POSTFIX "d")

if(MSVC)
    target_compile_definitions(SDL2-static
      PRIVATE
        # Work around error LNK2005: __ftol2_sse already defined in SDL2.lib(SDL_stdlib.obj)
        HAVE_LIBC
    )
endif()
