include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

# Set the location of the Conan-packaged libraries so freetype's find_package()
# functions finds them instead of system libraries
set(PNG_LIBRARY ${CONAN_LIB_DIRS_LIBPNG}/${CONAN_LIBS_LIBPNG})
set(ZLIB_LIBRARY ${CONAN_LIB_DIRS_ZLIB}/${CONAN_LIBS_ZLIB})

add_subdirectory(source)