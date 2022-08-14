if(MSVC)
    add_compile_options(
        $<$<CONFIG:Release>:/Gy> # Enable function-level linking
        /MP # Multi-processor compilation
        $<$<CONFIG:Release>:/Oi> # Generate intrinsic functions
        /permissive- # Standard C++ conformance
        $<$<CONFIG:Debug>:/ZI> # Produces a program database (PDB) that supports edit and continue
        $<$<CONFIG:Release>:/Zi> # Produces a program database (PDB)
    )
endif()

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
    add_link_options(
        -static-libgcc
        -static-libstdc++
    )
endif()

if(ANDROID)
    add_compile_options(
        $<$<CONFIG:Release>:-g0> # Don’t generate any debug info
    )
    add_link_options(
        $<$<CONFIG:Release>:-g0> # Don’t generate any debug info
    )
endif()
