add_library(Game STATIC
    Game.cpp
    Game.h
)

set_target_properties(Game PROPERTIES DEBUG_POSTFIX d)

if(MSVC)
    target_compile_options(Game
      PRIVATE
        /Fd$<TARGET_FILE_DIR:Game>/Game$<$<CONFIG:Debug>:d>.pdb
    )
endif()

target_include_directories(Game
  PUBLIC
    .
  PRIVATE
    
)

target_link_libraries(Game
    Display
    ErrorHandler
    CONAN_PKG::sdl2
    CONAN_PKG::sdl2_image
    CONAN_PKG::sdl2_ttf
)
