cmake_minimum_required(VERSION 3.14)

include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

# Force find_package() to look in the Conan package directories first
set(CMAKE_FIND_ROOT_PATH ${CONAN_CMAKE_MODULE_PATH} ${CMAKE_FIND_ROOT_PATH})

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

    # Remove '_static' from the libpng name so that find_package(PNG) will work.
    # This pending merge request would fix it:
    # https://gitlab.kitware.com/cmake/cmake/merge_requests/3552
    get_target_property(png_filename png_static OUTPUT_NAME)
    string(REPLACE "_static" "" png_filename ${png_filename})
    set_target_properties(png_static PROPERTIES
        OUTPUT_NAME ${png_filename}
    )
endif()
