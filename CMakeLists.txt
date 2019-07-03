cmake_minimum_required(VERSION 3.14)

include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

# Force find_package() to look in the Conan package directories first
set(CMAKE_FIND_ROOT_PATH ${CONAN_CMAKE_MODULE_PATH} ${CMAKE_FIND_ROOT_PATH})

add_subdirectory(source)

if(MSVC)
    target_compile_options(freetype
      PRIVATE
        /Fd$<TARGET_FILE_DIR:freetype>/freetype$<$<CONFIG:Debug>:d>.pdb
    )
endif()
