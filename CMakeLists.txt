include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(PNG_SHARED "Build shared lib" OFF)

# Set location of zlib so libpng's find_package(ZLIB REQUIRED) finds the Conan package library
set(ZLIB_LIBRARY ${CONAN_LIB_DIRS_ZLIB}/${CONAN_LIBS_ZLIB})

# Workaround for this issue:
# https://sourceforge.net/p/libpng/bugs/281/
if(IOS AND IOS_ARCH MATCHES arm)
    set(CMAKE_SYSTEM_PROCESSOR arm)
    set(PNG_ARM_NEON off CACHE STRING "")
endif()

add_subdirectory(source)
