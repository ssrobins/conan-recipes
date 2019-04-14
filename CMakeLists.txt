include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

if(APPLE)
    set(SFML_DEPENDENCIES_INSTALL_PREFIX "Frameworks" CACHE PATH "External libraries (FLAC, Freetype, Vorbis, ...) installation directory")
endif()

option(BUILD_SHARED_LIBS OFF)
option(SFML_BUILD_EXAMPLES OFF)
option(SFML_GENERATE_PDB ON)
option(SFML_USE_STATIC_STD_LIBS ON)

add_subdirectory(source)

if(MSVC)
    target_compile_options(sfml-audio
      PRIVATE
        /Fd$<TARGET_FILE_DIR:sfml-audio>/sfml-audio$<$<CONFIG:Debug>:-d>.pdb
    )
    target_compile_options(sfml-graphics
      PRIVATE
        /Fd$<TARGET_FILE_DIR:sfml-graphics>/sfml-graphics$<$<CONFIG:Debug>:-d>.pdb
    )
    target_compile_options(sfml-main
      PRIVATE
        /Fd$<TARGET_FILE_DIR:sfml-main>/sfml-main$<$<CONFIG:Debug>:-d>.pdb
    )
    target_compile_options(sfml-network
      PRIVATE
        /Fd$<TARGET_FILE_DIR:sfml-network>/sfml-network$<$<CONFIG:Debug>:-d>.pdb
    )
    target_compile_options(sfml-system
      PRIVATE
        /Fd$<TARGET_FILE_DIR:sfml-system>/sfml-system$<$<CONFIG:Debug>:-d>.pdb
    )
    target_compile_options(sfml-window
      PRIVATE
        /Fd$<TARGET_FILE_DIR:sfml-window>/sfml-window$<$<CONFIG:Debug>:-d>.pdb
    )
endif()