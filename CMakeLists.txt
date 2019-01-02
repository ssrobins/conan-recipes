include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

option(BOX2D_BUILD_EXAMPLES "Build Box2D examples" OFF)

add_subdirectory(source/Box2D)

set_target_properties(Box2D PROPERTIES DEBUG_POSTFIX d)
