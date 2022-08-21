#include "Display.h"
#include "ErrorHandler.h"
#include "Game.h"

int main(int argc, char* argv[])
{
    Display display(12, 20);
    ErrorHandler errorHandler("error.log");
    return 0;
}
