#include "freetype/freetype.h"

int main(int argc, char *argv[])
{
    FT_Library library;
    FT_Init_FreeType(&library); 
    return 0;
}
