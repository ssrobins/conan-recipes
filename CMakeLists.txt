cmake_minimum_required(VERSION 3.14)

include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_FIND_ROOT_PATH ${CONAN_ZLIB_ROOT} ${CMAKE_FIND_ROOT_PATH})

option(PNG_SHARED "Build shared lib" OFF)

# Workaround for this issue:
# https://sourceforge.net/p/libpng/bugs/281/
if(IOS AND CMAKE_OSX_ARCHITECTURES MATCHES arm)
    set(CMAKE_SYSTEM_PROCESSOR arm)
    set(PNG_ARM_NEON off CACHE STRING "")
endif()

add_subdirectory(source)

set_target_properties(png_static PROPERTIES DEBUG_POSTFIX d)

if(MSVC)
    target_compile_options(png_static
      PRIVATE
        /Fd$<TARGET_FILE_DIR:png_static>/png_static$<$<CONFIG:Debug>:d>.pdb
    )
endif()
