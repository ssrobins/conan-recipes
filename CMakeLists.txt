cmake_minimum_required(VERSION 2.8.12)

include(global_settings.cmake)
include(conanbuildinfo.cmake)
conan_basic_setup()

# Set the location of the Conan-packaged libraries so freetype's find_package()
# functions finds them instead of system libraries
set(BZIP2_LIBRARIES ${CONAN_LIB_DIRS_BZIP2}/${CONAN_LIBS_BZIP2})
set(PNG_LIBRARY ${CONAN_LIB_DIRS_LIBPNG}/${CONAN_LIBS_LIBPNG})
set(PNG_PNG_INCLUDE_DIR ${CONAN_INCLUDE_DIRS_LIBPNG})
set(ZLIB_LIBRARY ${CONAN_LIB_DIRS_ZLIB}/${CONAN_LIBS_ZLIB})
set(ZLIB_ROOT ${CONAN_ZLIB_ROOT})

add_subdirectory(source)
