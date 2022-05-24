cmake_minimum_required(VERSION 3.17)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include(${CONAN_CMAKE_UTILS_ROOT}/global_settings_thirdparty.cmake)

find_package(ogg REQUIRED)

add_subdirectory(source)

set_target_properties(vorbisfile vorbisenc vorbis PROPERTIES DEBUG_POSTFIX d)
