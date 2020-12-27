#include "ErrorHandler.h"
#include "Game.h"
#include "SDL_image.h"
#include "SDL_ttf.h"

Game::Game(const int numTilesWidth, const int numTilesHeight, const char* title, bool fullscreen)
    : screenScale(getScreenScale(fullscreen))
    , display(numTilesWidth, numTilesHeight)
{
    int flags = SDL_WINDOW_ALLOW_HIGHDPI;

    if (fullscreen)
    {
        flags = flags|SDL_WINDOW_FULLSCREEN;
    }

    if (SDL_Init(SDL_INIT_VIDEO) != 0)
    {
        throw Exception(SDL_GetError());
    }

    SDL_DisplayMode displayMode;
    if (SDL_GetCurrentDisplayMode(0, &displayMode) != 0)
    {
        throw Exception(SDL_GetError());
    }
    display.setDisplaySize(displayMode.w, displayMode.h, screenScale, false);

    window = SDL_CreateWindow(title,
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        display.getGameWidth(),
        display.getGameHeight(),
        flags);
    if (window == nullptr)
    {
        throw Exception(SDL_GetError());
    }

    std::string iconPath = basePath + "assets/Icon1024x1024.png";
    SDL_Surface* icon = IMG_Load(iconPath.c_str());
    if (icon == nullptr)
    {
        throw Exception(SDL_GetError());
    }
    SDL_SetWindowIcon(window, icon);
    SDL_FreeSurface(icon);

    renderer = SDL_CreateRenderer(window, -1, 0);
    if (renderer == nullptr)
    {
        throw Exception(SDL_GetError());
    }

    int pixelWidth;
    int pixelHeight;
    SDL_GetRendererOutputSize(renderer, &pixelWidth, &pixelHeight);
    display.setDisplaySize(pixelWidth, pixelHeight, 1.0f, true);
    renderRect.x = (display.getScreenWidth()-display.getGameWidth())/2;
    renderRect.y = (display.getScreenHeight()-display.getGameHeight())/2;
    renderRect.w = display.getGameWidth();
    renderRect.h = display.getGameHeight();

    if (TTF_Init() != 0)
    {
        throw Exception(SDL_GetError());
    }
}

Game::~Game()
{
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
}

const float Game::getScreenScale(bool fullscreen)
{
    if (fullscreen)
    {
        return 1.0f;
    }
    else
    {
        return 0.8f;
    }
}

float Game::getPixelsToPointsScaleFactor(std::string& fontPath)
{
    int fontSize = 100;
    TTF_Font* font = TTF_OpenFont(fontPath.c_str(), fontSize);
    if (font == nullptr)
    {
        throw Exception(SDL_GetError());
    }

    int height = TTF_FontHeight(font);
    if (height <= 0)
    {
        throw Exception("Font " + fontPath + " height is " + std::to_string(height));
    }

    TTF_CloseFont(font);

    return static_cast<float>(fontSize) / static_cast<float>(height);
}

void Game::text(const char * text, int fontSizeHeightPercent, SDL_Color& fontColor, int x, int y, bool centered)
{
    std::string fontPath = basePath + "assets/OpenSans-Regular.ttf";

    float scale = getPixelsToPointsScaleFactor(fontPath);
    int heightPixels = display.heightPercentToPixels(fontSizeHeightPercent);
    int fontSize = static_cast<int>(heightPixels * scale);

    TTF_Font* font = TTF_OpenFont(fontPath.c_str(), fontSize);
    if (font == nullptr)
    {
        throw Exception(SDL_GetError());
    }

    SDL_Surface* surf = TTF_RenderText_Blended(font, text, fontColor);

    TTF_CloseFont(font);
    SDL_Texture* labelTexture = SDL_CreateTextureFromSurface(renderer, surf);

    int textureWidth = surf->w;
    int textureHeight = surf->h;
    SDL_FreeSurface(surf);

    if (centered)
    {
        x = (display.getGameWidth() - textureWidth) / 2 - 3;
    }

    SDL_Rect renderQuad = { x, y, textureWidth, textureHeight };

    SDL_RenderCopyEx(renderer, labelTexture, nullptr, &renderQuad, 0.0, nullptr, SDL_FLIP_NONE);
    SDL_DestroyTexture(labelTexture);
}

void Game::renderSetViewport()
{
    if (SDL_RenderSetViewport(renderer, &renderRect) != 0)
    {
        throw Exception(SDL_GetError());
    }
}

void Game::setRenderDrawColor(const SDL_Color& color)
{
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);
}

void Game::renderClear()
{
    SDL_RenderClear(renderer);
}

void Game::renderPresent()
{
    SDL_RenderPresent(renderer);
}

void Game::renderFillRect(const SDL_Rect& rect, const SDL_Color& color)
{
    setRenderDrawColor(color);
    SDL_RenderFillRect(renderer, &rect);
}
