add_library(Game STATIC
    Game.cpp
    Game.h
)

set_target_properties(Game PROPERTIES DEBUG_POSTFIX d)

target_include_directories(Game
  PUBLIC
    .
  PRIVATE
    
)

target_link_libraries(Game
    Display
    ErrorHandler
    sdl2::sdl2
    sdl2_image::sdl2_image
    sdl2_mixer::sdl2_mixer
    sdl2_ttf::sdl2_ttf
)
