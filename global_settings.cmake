include(${CMAKE_CURRENT_LIST_DIR}/global_settings_common.cmake)

if(ANDROID)
    set(android_sdk_version 29)
endif()

set(company dnqpy)

if(IOS)
    set(xcode_code_sign_identity "iPhone Developer")
elseif(APPLE)
    set(xcode_code_sign_identity "Developer ID Application")
endif()
if(APPLE)
    set(xcode_dev_team MLPC343Q5F)
    set(MACOSX_BUNDLE_GUI_IDENTIFIER "com.${company}.\${PRODUCT_NAME:identifier}")
endif()

if(MSVC)
    add_compile_options(
        $<$<CONFIG:Release>:/GL> # Whole program optimization
        /sdl # Enable additional security checks
        /WX # Warning as error
    )

    add_link_options(
        /WX # Warning as error
    )
else()
    add_compile_options(
        # CMAKE_POSITION_INDEPENDENT_CODE isn't setting -fPIC on gcc, find out why.
        # Until it's fixed, set it manually.
        -fPIC

        -Werror # Warning as error
    )
    add_link_options(
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

if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(bitness 64)
else()
    set(bitness 32)
endif()

if(ANDROID)
    set(CPACK_GENERATOR External)
    set(CPACK_EXTERNAL_PACKAGE_SCRIPT ${CMAKE_CURRENT_LIST_DIR}/package_android_apk.cmake)
    set(CPACK_EXTERNAL_ENABLE_STAGING true)
    set(CPACK_BUILD_CONFIG ${CMAKE_BUILD_TYPE})
    set(platform Android)
elseif(IOS)
    set(CPACK_GENERATOR External)
    set(CPACK_EXTERNAL_PACKAGE_SCRIPT ${CMAKE_CURRENT_LIST_DIR}/package_ios_ipa.cmake)
    set(CPACK_EXTERNAL_ENABLE_STAGING true)
    set(platform iOS)
elseif(APPLE)
    set(CPACK_GENERATOR ZIP)
    set(platform Mac)
elseif(WIN32)
    set(CPACK_GENERATOR ZIP)
    set(platform Windows)
else()
    set(CPACK_GENERATOR TGZ)
    set(platform Linux${bitness})
endif()

# Settings for install and packaging
set(CMAKE_INSTALL_PREFIX ${PROJECT_BINARY_DIR}/_install)
set(CPACK_PACKAGE_DIRECTORY ${PROJECT_BINARY_DIR}/_package)
set(CPACK_COMPONENTS_GROUPING IGNORE)
set(CPACK_INCLUDE_TOPLEVEL_DIRECTORY 0)
