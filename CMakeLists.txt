include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(PNG_SHARED "Build shared lib" OFF)
option(PNG_BUILD_ZLIB "Custom zlib Location, else find_package is used" ON)

# Workaround for this issue:
# https://sourceforge.net/p/libpng/bugs/281/
if(IOS AND IOS_ARCH MATCHES arm)
    set(CMAKE_SYSTEM_PROCESSOR arm)
    set(PNG_ARM_NEON off CACHE STRING "")
endif()

add_subdirectory(source)