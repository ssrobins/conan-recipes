#pragma once

#include "Display.h"
#include "SDL.h"
#include "SDL_mixer.h"
#include <chrono>
#include <string>

class Game
{
public:
    Game(const int numTilesWidth, const int numTilesHeight, const char* title, bool fullscreen);
    ~Game();
    const float getScreenScale(bool fullscreen);

    float getPixelsToPointsScaleFactor(std::string& fontPath);
    void text(const char * text, int fontSizeHeightPercent, SDL_Color& fontColor, int x = 0, int y = 0, bool centered = false);
    void renderSetViewport();
    void setRenderDrawColor(const SDL_Color& color);
    void renderClear();
    void renderPresent();
    void renderFillRect(const SDL_Rect& rect, const SDL_Color& color);
    void playMusic(const std::string& musicPath);
    void stopMusic();
    int getScreenWidth() { return display.getScreenWidth(); }
    int getScreenHeight() { return display.getScreenHeight(); }
    int getGameWidth() { return display.getGameWidth(); }
    int getGameHeight() { return display.getGameHeight(); }
    int getTileSize() { return display.getTileSize(); }
    int getOutlineOffsetWidth() { return display.getOutlineOffsetWidth(); };
    int getOutlineOffsetHeight() { return display.getOutlineOffsetHeight(); };
    int widthPercentToPixels(int percent) { return display.widthPercentToPixels(percent); }
    int heightPercentToPixels(int percent) { return display.heightPercentToPixels(percent); }

private:
    const float screenScale;

    Display display;

    SDL_Window *window;
    SDL_Renderer* renderer;
    SDL_Rect renderRect;
    Mix_Music* music;

    std::string basePath = 
    #if __ANDROID__
        "";
    #else
        SDL_GetBasePath();
    #endif
};
