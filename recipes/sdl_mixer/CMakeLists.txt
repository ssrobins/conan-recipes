cmake_minimum_required(VERSION 3.17)

set(ANDROID_USE_LEGACY_TOOLCHAIN_FILE false)

project(Project)

option(BUILD_SHARED_LIBS "Build the library as a shared library" OFF)
option(SDL2MIXER_FLAC "Enable FLAC music" OFF)
option(SDL2MIXER_MIDI "Enable MIDI music" OFF)
option(SDL2MIXER_MOD "Support loading MOD music" OFF)
option(SDL2MIXER_OPUS "Enable Opus music" OFF)
option(SDL2MIXER_SAMPLES "Build the SDL2_mixer sample program(s)" OFF)

add_subdirectory(source)

set_target_properties(SDL2_mixer PROPERTIES
    DEBUG_POSTFIX d
    OUTPUT_NAME "SDL2_mixer"
)
