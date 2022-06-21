#include "bzlib.h"

int main(int argc, char *argv[])
{
    bz_stream bz;
    BZ2_bzCompressEnd(&bz);
    return 0;
}
