#include "vorbis/vorbisenc.h"

int main(int argc, char* argv[])
{
    vorbis_info vi;
    vorbis_info_init(&vi);
    vorbis_encode_init(&vi, 0.0l, 0.0l, 0.0l, 0.0l, 0.0l);
    return 0;
}
