cmake_minimum_required(VERSION 3.14)

include(conanbuildinfo.cmake)
conan_basic_setup()

include(${CONAN_CMAKE_UTILS_ROOT}/global_settings_thirdparty.cmake)

option(BUILD_UTILS OFF)

add_subdirectory(source/build/cmake)

if(MSVC)
    target_compile_options(glew_s
      PRIVATE
        /Fd$<TARGET_FILE_DIR:glew_s>/glew_s$<$<CONFIG:Debug>:d>.pdb
    )
endif()
