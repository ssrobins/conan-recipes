set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(ANDROID)
    add_compile_options(
        $<$<CONFIG:Release>:-g0> # Don’t generate any debug info
    )
    add_link_options(
        $<$<CONFIG:Release>:-g0> # Don’t generate any debug info
    )
endif()
