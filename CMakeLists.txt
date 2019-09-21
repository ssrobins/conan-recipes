cmake_minimum_required(VERSION 3.14)

include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(BUILD_ZLIB_EXAMPLE "Build zlib example" OFF)
option(BUILD_ZLIB_MINIGZIP "Build zlib gzip example" OFF)
option(BUILD_ZLIB_SHARED "Build zlib shared library" OFF)

add_subdirectory(source)

set_target_properties(zlibstatic PROPERTIES DEBUG_POSTFIX d)

if(MSVC)
    target_compile_options(zlibstatic
      PRIVATE
        /Fd$<TARGET_FILE_DIR:zlibstatic>/zlibstatic$<$<CONFIG:Debug>:d>.pdb
    )
endif()
