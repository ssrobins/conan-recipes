include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(BUILD_SHARED_LIBS OFF)

add_subdirectory(source/build/cmake)

if(MSVC)
    target_compile_options(glew_s
      PRIVATE
        /Fd$<TARGET_FILE_DIR:glew_s>/glew_s$<$<CONFIG:Debug>:d>.pdb
    )
endif()