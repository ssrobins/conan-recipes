set(target_name SDL2_ttf)

include(${CMAKE_BINARY_DIR}/global_settings.cmake)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_library(${target_name} STATIC
    SDL_ttf.c
)

target_include_directories(${target_name} PUBLIC
    .
)
