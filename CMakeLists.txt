include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(INSTALL_GMOCK OFF)
option(INSTALL_GTEST OFF)

add_subdirectory(source)