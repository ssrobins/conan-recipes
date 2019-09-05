add_library(Display STATIC
    Display.cpp
    Display.h
)

set_target_properties(Display PROPERTIES DEBUG_POSTFIX d)

if(MSVC)
    target_compile_options(Display
      PRIVATE
        /Fd$<TARGET_FILE_DIR:Display>/Display$<$<CONFIG:Debug>:d>.pdb
    )
endif()


target_include_directories(Display
  PUBLIC
    .
  PRIVATE
    
)

target_link_libraries(Display
)
