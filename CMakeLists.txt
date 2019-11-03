cmake_minimum_required(VERSION 3.14)

include(conanbuildinfo.cmake)
conan_basic_setup()

include(${CONAN_CMAKE_UTILS_ROOT}/global_settings_thirdparty.cmake)

add_subdirectory(source)

if(MSVC)
    target_compile_options(bzip2
      PRIVATE
        /Fd$<TARGET_FILE_DIR:bzip2>/bzip2$<$<CONFIG:Debug>:d>.pdb
    )
endif()
