set(target_name ErrorHandler)

add_library(${target_name} STATIC
    ErrorHandler.cpp
    ErrorHandler.h
    Exceptions.h
)

target_include_directories(${target_name}
  PUBLIC
    .
  PRIVATE
    
)

target_link_libraries(${target_name}
)
