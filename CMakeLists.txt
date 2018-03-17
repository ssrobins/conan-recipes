set(target_name ErrorHandler)

add_library(${target_name} STATIC
    ErrorLogger.cpp
    ErrorLogger.h
    Exceptions.h
)

target_include_directories(${target_name}
  PUBLIC
    .
  PRIVATE
    
)

target_link_libraries(${target_name}
)
