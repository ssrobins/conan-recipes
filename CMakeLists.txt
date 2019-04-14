cmake_minimum_required(VERSION 3.13)

include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

add_subdirectory(source)

if(MSVC)
    target_compile_options(bzip2
      PRIVATE
        /Fd$<TARGET_FILE_DIR:bzip2>/bzip2$<$<CONFIG:Debug>:d>.pdb
    )
endif()