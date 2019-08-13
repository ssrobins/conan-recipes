add_library(Display STATIC
    Display.cpp
    Display.h
)

target_include_directories(Display
  PUBLIC
    .
  PRIVATE
    
)

target_link_libraries(Display
)
