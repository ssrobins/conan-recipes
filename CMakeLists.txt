cmake_minimum_required(VERSION 3.14)

include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(PNG_SHARED "Build shared lib" OFF)

# Set the location of the Conan-packaged zlib so libpng's find_package()
# function finds it instead of a system library
set(ZLIB_LIBRARY ${CONAN_LIB_DIRS_ZLIB}/${CONAN_LIBS_ZLIB})
set(ZLIB_ROOT ${CONAN_ZLIB_ROOT})

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
