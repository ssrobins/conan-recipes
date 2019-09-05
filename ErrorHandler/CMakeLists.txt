add_library(ErrorHandler STATIC
    ErrorHandler.cpp
    ErrorHandler.h
    Exceptions.h
)

set_target_properties(ErrorHandler PROPERTIES DEBUG_POSTFIX d)

if(MSVC)
    target_compile_options(ErrorHandler
      PRIVATE
        /Fd$<TARGET_FILE_DIR:ErrorHandler>/ErrorHandler$<$<CONFIG:Debug>:d>.pdb
    )
endif()


target_include_directories(ErrorHandler
  PUBLIC
    .
  PRIVATE
    
)

target_link_libraries(ErrorHandler
    CONAN_PKG::sdl2
)
