# The following code is a workaround for this issue:
# https://gitlab.kitware.com/cmake/cmake/issues/20160
if(CMAKE_GENERATOR STREQUAL Xcode)
    configure_file(
        ${CMAKE_CURRENT_LIST_DIR}/WorkspaceSettings.xcsettings
        ${CMAKE_BINARY_DIR}/${PROJECT_NAME}.xcodeproj/project.xcworkspace/xcuserdata/$ENV{USER}.xcuserdatad/WorkspaceSettings.xcsettings
        COPYONLY
    )
endif()

if(MSVC)
    add_compile_options(
        $<$<CONFIG:Release>:/Gy> # Enable function-level linking
        /MP # Multi-processor compilation
        $<$<CONFIG:>:/MT> #---------|
        $<$<CONFIG:Debug>:/MTd> #---|-- Statically link the runtime libraries
        $<$<CONFIG:Release>:/MT> #--|
        $<$<CONFIG:Release>:/Oi> # Generate intrinsic functions
        /permissive- # Standard C++ conformance
        $<$<CONFIG:Debug>:/ZI> # Produces a program database (PDB) that supports edit and continue
        $<$<CONFIG:Release>:/Zi> # Produces a program database (PDB)
    )

    add_link_options(
        $<$<CONFIG:Release>:/DEBUG> # Generate debug information
        $<$<CONFIG:Release>:/LTCG:incremental> # Link-time code generation
        $<$<CONFIG:Release>:/OPT:ICF> # Perform identical COMDAT folding
        $<$<CONFIG:Release>:/OPT:REF> # Eliminates functions and/or data that are never referenced
        /SAFESEH:NO # Don't produce an image with a table of safe exceptions handlers
    )
endif()

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
    # CMAKE_POSITION_INDEPENDENT_CODE isn't setting -fPIC on gcc, find out why.
    # Until it's fixed, set it manually.
    add_compile_options(
        -fPIC
    )

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
