#include "bzlib.h"

int main(int argc, char* argv[])
{
    BZFILE* b = nullptr;
    BZ2_bzclose(b);
    return 0;
}
