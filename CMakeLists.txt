cmake_minimum_required(VERSION 3.17)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include(${CONAN_CMAKE_UTILS_ROOT}/global_settings_thirdparty.cmake)

# Force find_package() to look in the Conan package directories first
set(CMAKE_FIND_ROOT_PATH ${CONAN_CMAKE_MODULE_PATH} ${CMAKE_FIND_ROOT_PATH})

option(FT_WITH_BZIP2 "Support bzip2 compressed fonts." ON)
option(FT_WITH_PNG "Support PNG compressed OpenType embedded bitmaps." ON)
option(FT_WITH_ZLIB "Use system zlib instead of internal library." ON)
set(CMAKE_DISABLE_FIND_PACKAGE_BrotliDec true)

add_subdirectory(source)

if(MSVC)
    target_compile_options(freetype
      PRIVATE
        /Fd$<TARGET_FILE_DIR:freetype>/freetype$<$<CONFIG:Debug>:d>.pdb
    )
endif()
