set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(ANDROID)
    set(android_min_sdk_version 15)
endif()

if(APPLE AND NOT IOS)
    set(CMAKE_OSX_DEPLOYMENT_TARGET "10.9" CACHE STRING "Minimum OS X deployment version" FORCE)
endif()

if(IOS)
    set(xcode_code_sign_identity "iPhone Developer")
elseif(APPLE)
    set(xcode_code_sign_identity "Developer ID Application")
endif()
if(APPLE)
    set(xcode_dev_team MLPC343Q5F)
    set(MACOSX_BUNDLE_GUI_IDENTIFIER "com.${company}.\${PRODUCT_NAME:identifier}")
endif()

set(version_major 0)
set(version_minor 1)
set(version_patch 0)

if(MSVC)
    add_compile_options(
        $<$<CONFIG:Release>:/GL> # Whole program optimization
        $<$<CONFIG:Release>:/Gy> # Enable function-level linking
        /MP # Multi-processor compilation
        $<$<CONFIG:>:/MT> #---------|
        $<$<CONFIG:Debug>:/MTd> #---|-- Statically link the runtime libraries
        $<$<CONFIG:Release>:/MT> #--|
        $<$<CONFIG:Release>:/Oi> # Generate intrinsic functions
        /permissive- # Standard C++ conformance
        /sdl # Enable additional security checks
        /WX # Warning as error
        $<$<CONFIG:Debug>:/ZI> # Produces a program database (PDB) that supports edit and continue
        $<$<CONFIG:Release>:/Zi> # Produces a program database (PDB)
    )

    add_link_options(
        $<$<CONFIG:Release>:/DEBUG> # Generate debug information
        $<$<CONFIG:Release>:/LTCG:incremental> # Link-time code generation
        $<$<CONFIG:Release>:/OPT:ICF> # Perform identical COMDAT folding
        $<$<CONFIG:Release>:/OPT:REF> # Eliminates functions and/or data that are never referenced
        /SAFESEH:NO # Don't produce an image with a table of safe exceptions handlers
        /WX # Warning as error
    )
elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
    add_link_options(
        -static-libgcc
        -static-libstdc++
    )
elseif(IOS)
    add_link_options(
        "${XCODE_IOS_PLATFORM_VERSION_FLAGS}"
    )
else()
    add_compile_options(
        -Werror # Warning as error
    )
endif()

# Allow organizing source files into subdirectories
set_property(GLOBAL PROPERTY USE_FOLDERS ON)
define_property(
    TARGET
    PROPERTY FOLDER
    INHERITED
    BRIEF_DOCS "Set the folder name."
    FULL_DOCS  "Use to organize targets in an IDE."
)

set(company dnqpy)

if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(bitness 64)
else()
    set(bitness 32)
endif()

if(WIN32)
    set(CPACK_GENERATOR ZIP)
    set(platform Windows)
elseif(APPLE)
    set(CPACK_GENERATOR ZIP)
    set(platform Mac)
else()
    set(CPACK_GENERATOR TGZ)
    set(platform Linux${bitness})
endif()

# Settings for install and packaging
set(CMAKE_INSTALL_PREFIX ${PROJECT_BINARY_DIR}/_install)
set(CPACK_PACKAGE_DIRECTORY ${PROJECT_BINARY_DIR}/_package)
set(CPACK_ARCHIVE_COMPONENT_INSTALL ON)
set(CPACK_COMPONENTS_GROUPING IGNORE)
set(CPACK_PACKAGE_VERSION_MAJOR ${version_major})
set(CPACK_PACKAGE_VERSION_MINOR ${version_minor})
set(CPACK_PACKAGE_VERSION_PATCH ${version_patch})
set(CPACK_INCLUDE_TOPLEVEL_DIRECTORY 0)
set(CPACK_PACKAGE_FILE_NAME ${CMAKE_PROJECT_NAME})
