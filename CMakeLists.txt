set(target_name Display)

add_library(${target_name} STATIC
    Display.cpp
    Display.h
)

target_include_directories(${target_name}
  PUBLIC
    .
  PRIVATE
    
)

target_link_libraries(${target_name}
)
