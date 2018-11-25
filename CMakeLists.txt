set(target_name Game)

add_library(${target_name} STATIC
    Game.cpp
    Game.h
)

target_include_directories(${target_name}
  PUBLIC
    .
  PRIVATE
    
)

target_link_libraries(${target_name}
    Display
    ErrorHandler
    CONAN_PKG::sdl2
    SDL2_image
    SDL2_ttf
)
