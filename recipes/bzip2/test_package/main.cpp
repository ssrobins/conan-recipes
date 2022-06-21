#include "bzlib.h"

int main(int argc, char *argv[])
{
    bz_stream bz = nullptr;
    BZ2_bzCompressEnd(&bz);
    return 0;
}
