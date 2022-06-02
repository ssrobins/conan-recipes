#pragma once

#include <vector>

class Display
{
public:
    Display(const int numTilesWidth, const int numTilesHeight);
    void setDisplaySize(const int width, const int height, const float screenScale, const bool outline);
    int heightPercentToPixels(const int percent);
    int widthPercentToPixels(const int percent);
    int getScreenWidth() { return screenWidth; };
    int getScreenHeight() { return screenHeight; };
    int getTileSize() { return tileSize; };
    int getGameWidth() { return gameWidth; };
    int getGameHeight() { return gameHeight; };
    int getOutlineOffsetWidth() { return outlineOffsetWidth; };
    int getOutlineOffsetHeight() { return outlineOffsetHeight; };
private:
    const int numTilesWidth;
    const int numTilesHeight;
    int screenWidth;
    int screenHeight;
    int gameWidth;
    int gameHeight;
    int outlineOffsetWidth;
    int outlineOffsetHeight;
    int tileSize;
};
