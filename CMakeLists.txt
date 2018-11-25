set(target_name SDL2_mixer)

include(${CMAKE_BINARY_DIR}/global_settings.cmake)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_library(${target_name} STATIC
    effect_position.c
    effect_stereoreverse.c
    effects_internal.c
    effects_internal.h
    load_aiff.c
    load_aiff.h
    load_voc.c
    load_voc.h
    mixer.c
    mixer.h
    music.c
    music.h
    music_cmd.c
    music_cmd.h
    music_flac.c
    music_flac.h
    music_fluidsynth.c
    music_fluidsynth.h
    music_mad.c
    music_mad.h
    music_mikmod.c
    music_mikmod.h
    music_modplug.c
    music_modplug.h
    music_mpg123.c
    music_mpg123.h
    music_nativemidi.c
    music_nativemidi.h
    music_ogg.c
    music_ogg.h
    music_opus.c
    music_opus.h
    music_timidity.c
    music_timidity.h
    music_wav.c
    music_wav.h
    SDL_mixer.h
)

target_compile_definitions(${target_name} PRIVATE
    -DMUSIC_WAV
)

target_include_directories(${target_name} PUBLIC
    .
)