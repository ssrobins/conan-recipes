#!/usr/bin/env python3

import os.path
from conan_create import *

recipe_path = f"{os.path.dirname(os.path.realpath(__file__))}/../recipes"

conan_create_single_platform(f"{recipe_path}/android_sdl")
conan_create_single_platform(f"{recipe_path}/cmake_utils")
conan_create(f"{recipe_path}/box2d")
conan_create(f"{recipe_path}/bzip2")
conan_create(f"{recipe_path}/glew", desktop_only=True)
conan_create(f"{recipe_path}/gtest")
conan_create(f"{recipe_path}/ogg")
conan_create(f"{recipe_path}/sdl")
conan_create(f"{recipe_path}/zlib")
conan_create(f"{recipe_path}/libpng")
conan_create(f"{recipe_path}/vorbis")
conan_create(f"{recipe_path}/freetype")
conan_create(f"{recipe_path}/sfml", desktop_only=True)
conan_create(f"{recipe_path}/sdl_image")
conan_create(f"{recipe_path}/sdl_mixer")
conan_create(f"{recipe_path}/sdl_ttf")
conan_create(f"{recipe_path}/ssrobins_engine")
