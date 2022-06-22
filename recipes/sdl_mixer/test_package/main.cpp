#include "SDL_mixer.h"

int main(int argc, char *argv[])
{
    Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 2048);
    return 0;
}
