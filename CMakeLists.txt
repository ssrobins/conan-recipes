set(target_name DisplayTest)

include(${CMAKE_SOURCE_DIR}/add_executable.cmake)

target_sources(${target_name} PRIVATE
    DisplayTest.cpp
)

target_include_directories(${target_name} PRIVATE
)

target_link_libraries(${target_name}
    Display
    CONAN_PKG::libpng
    CONAN_PKG::bzip2
    CONAN_PKG::freetype
    CONAN_PKG::sdl2_image
)

include(${CMAKE_SOURCE_DIR}/testing.cmake)
