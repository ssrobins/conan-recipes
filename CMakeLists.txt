cmake_minimum_required(VERSION 3.17)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include(${CONAN_CMAKE_UTILS_ROOT}/global_settings_thirdparty.cmake)

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
endif()
