#!/usr/bin/env python3

import os.path
import time
from conan_create import *

recipe_path = f"{os.path.dirname(os.path.realpath(__file__))}/../recipes"

sleep_length = 1

conan_create_single_platform(f"{recipe_path}/android_sdl")
time.sleep(sleep_length)
conan_create_single_platform(f"{recipe_path}/cmake_utils")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/box2d")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/bzip2")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/glew", desktop_only=True)
time.sleep(sleep_length)
conan_create(f"{recipe_path}/gtest")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/ogg")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/sdl")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/zlib")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/libpng")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/vorbis")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/freetype")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/sfml", desktop_only=True)
time.sleep(sleep_length)
conan_create(f"{recipe_path}/sdl_image")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/sdl_mixer")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/sdl_ttf")
time.sleep(sleep_length)
conan_create(f"{recipe_path}/ssrobins_engine", own_code=True)
