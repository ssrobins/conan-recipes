cmake_minimum_required(VERSION 3.16)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include(${CONAN_CMAKE_UTILS_ROOT}/global_settings_thirdparty.cmake)

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
