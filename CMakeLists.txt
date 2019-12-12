cmake_minimum_required(VERSION 3.16)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include(${CONAN_CMAKE_UTILS_ROOT}/global_settings_thirdparty.cmake)

option(BOX2D_BUILD_EXAMPLES "Build Box2D examples" OFF)
option(BOX2D_INSTALL "Install Box2D libs, includes, and CMake scripts" ON)

add_subdirectory(source/Box2D)

set_target_properties(Box2D PROPERTIES DEBUG_POSTFIX d)

if(MSVC)
    target_compile_options(Box2D
      PRIVATE
        /Fd$<TARGET_FILE_DIR:Box2D>/Box2D$<$<CONFIG:Debug>:d>.pdb
    )
endif()
