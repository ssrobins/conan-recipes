set(target_name SDL2_image)

include(${CMAKE_BINARY_DIR}/global_settings.cmake)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_library(${target_name} STATIC
    IMG.c
    IMG_bmp.c
    IMG_gif.c
    IMG_jpg.c
    IMG_lbm.c
    IMG_pcx.c
    IMG_png.c
    IMG_pnm.c
    IMG_svg.c
    IMG_tga.c
    IMG_tif.c
    IMG_webp.c
    IMG_xcf.c
    IMG_xpm.c
    IMG_xv.c
    IMG_xxx.c
)

target_compile_options(${target_name} PRIVATE
    -DLOAD_BMP
    -DLOAD_PNG
    -DSDL_IMAGE_USE_COMMON_BACKEND
)

target_include_directories(${target_name} PUBLIC
    .
)
