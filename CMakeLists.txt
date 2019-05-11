cmake_minimum_required(VERSION 3.14)

include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(INSTALL_GMOCK OFF)
option(INSTALL_GTEST OFF)

add_subdirectory(source)

if(MSVC)
    target_compile_options(gmock
      PRIVATE
        /Fd$<TARGET_FILE_DIR:gmock>/gmock$<$<CONFIG:Debug>:d>.pdb
    )
    target_compile_options(gmock_main
      PRIVATE
        /Fd$<TARGET_FILE_DIR:gmock_main>/gmock_main$<$<CONFIG:Debug>:d>.pdb
    )
    target_compile_options(gtest
      PRIVATE
        /Fd$<TARGET_FILE_DIR:gtest>/gtest$<$<CONFIG:Debug>:d>.pdb
    )
    target_compile_options(gtest_main
      PRIVATE
        /Fd$<TARGET_FILE_DIR:gtest_main>/gtest_main$<$<CONFIG:Debug>:d>.pdb
    )
endif()
