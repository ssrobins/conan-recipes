add_library(ErrorHandler STATIC
    ErrorHandler.cpp
    ErrorHandler.h
    Exceptions.h
)

target_include_directories(ErrorHandler
  PUBLIC
    .
  PRIVATE
    
)

target_link_libraries(ErrorHandler
    CONAN_PKG::sdl2
)
