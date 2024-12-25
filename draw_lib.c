#include <math.h>
#include <stdio.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL2_gfxPrimitives.h>
#include "draw_lib.h"


// Variables globales pour SDL
SDL_Window* window = NULL;
SDL_Renderer* renderer = NULL;


// Initialisation de SDL et de la fenêtre
int initialize_graphics(int width, int height, const char* title) {
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        fprintf(stderr, "Erreur SDL: %s\n", SDL_GetError());
        return 0;
    }

    window = SDL_CreateWindow(title, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, width, height, SDL_WINDOW_SHOWN);
    if (!window) {
        fprintf(stderr, "Erreur création fenêtre: %s\n", SDL_GetError());
        SDL_Quit();
        return 0;
    }

    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        fprintf(stderr, "Erreur création renderer: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 0;
    }

    // Couleur d'arrière-plan (blanc)
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    SDL_RenderClear(renderer); 

    return 1; // Succès
}

// Nettoyage des ressources SDL
void cleanup_graphics() {
    if (renderer) SDL_DestroyRenderer(renderer);
    if (window) SDL_DestroyWindow(window);
    SDL_Quit();
}

uint32_t get_color(const char* color_name) {
    uint32_t color;

    if (strcmp(color_name, "red") == 0) {
        color = 0xFF0000FF;
    } else if (strcmp(color_name, "green") == 0) {
        color = 0xFF00FF00;
    } else if (strcmp(color_name, "blue") == 0) {
        color = 0xFFFF0000;
    } else if (strcmp(color_name, "black") == 0) {
        color = 0xFF000000;
    } else if (strcmp(color_name, "white") == 0) {
        color = 0xFFFFFFFF;
    } else {
        // Couleur par défaut : noir
        fprintf(stderr, "Couleur non reconnue : %s. Utilisation du noir par défaut.\n", color_name);
        color = 0xFF000000;
    }

    return color;
}

SDL_Color get_color_SDL(const char* color_name) {
    SDL_Color color;

    if (strcmp(color_name, "red") == 0) {
        color = (SDL_Color){255, 0, 0, 255};
    } else if (strcmp(color_name, "green") == 0) {
        color = (SDL_Color){0, 255, 0, 255};
    } else if (strcmp(color_name, "blue") == 0) {
        color = (SDL_Color){0, 0, 255, 255};
    } else if (strcmp(color_name, "black") == 0) {
        color = (SDL_Color){0, 0, 0, 255};
    } else if (strcmp(color_name, "white") == 0) {
        color = (SDL_Color){255, 255, 255, 255};
    } else {
        // Couleur par défaut : noir
        fprintf(stderr, "Couleur non reconnue : %s. Utilisation du noir par défaut.\n", color_name);
        color = (SDL_Color){0, 0, 0, 255};
    }

    return color;
}

// Creates a new cursor
Cursor create_cursor(int x, int y, char* color_name, int thickness) {
    SDL_Color color = get_color_SDL(color_name);
    SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);
    Cursor cursor = {x, y, color_name, thickness};
    return cursor;
}

// Moves the cursor to a new position
void move_cursor(Cursor* cursor, int distance) {
    cursor->x = round(cursor->x + distance * cos(cursor->angle * M_PI / 180.0));
    cursor->y = round(cursor->y + distance * sin(cursor->angle * M_PI / 180.0));
}

// Rotates the cursor
void rotate_cursor(Cursor* cursor, int angle) {
    cursor->angle = (cursor->angle + angle) % 360;
}

// Draws a circle with adjustable thickness
void draw_circle(Cursor* cursor, int radius) {
    uint32_t color = get_color(cursor->color_name);
    for (int i = 0; i < cursor->thickness; i++) {
        circleColor(renderer, cursor->x, cursor->y, radius + i, color);
    }
}

// Draws a rectangle with adjustable thickness
void draw_rectangle(Cursor* cursor, int width, int height) {
    for (int i = 0; i < cursor->thickness; i++) {
        SDL_Rect rect = {cursor->x - i, cursor->y - i, width + 2 * i, height + 2 * i};
        SDL_RenderDrawRect(renderer, &rect);
    }
}

// Draws an arc with adjustable thickness
void draw_arc(Cursor* cursor, int radius, int start_angle, int end_angle) {
    uint32_t color = get_color(cursor->color_name);
    for (int i = 0; i < cursor->thickness; i++) {
        arcColor(renderer, cursor->x, cursor->y, radius + i, start_angle, end_angle, color);
    }
}

// Draws a point with adjustable thickness
void draw_point(Cursor* cursor) {
    for (int dx = -cursor->thickness / 2; dx <= cursor->thickness / 2; dx++) {
        for (int dy = -cursor->thickness / 2; dy <= cursor->thickness / 2; dy++) {
            SDL_RenderDrawPoint(renderer, cursor->x + dx, cursor->y + dy);
        }
    }
}

// Draws a line with adjustable thickness
void draw_line(Cursor* cursor, int distance) {
    int new_x = round(cursor->x + distance * cos(cursor->angle * M_PI / 180.0));
    int new_y = round(cursor->y + distance * sin(cursor->angle * M_PI / 180.0));

    // Calcul d'un vecteur perpendiculaire à la ligne
    double perp_dx = -sin(cursor->angle * M_PI / 180.0);
    double perp_dy = cos(cursor->angle * M_PI / 180.0);

    // Tracer les lignes parallèles pour l'épaisseur
    for (int i = -cursor->thickness / 2; i <= cursor->thickness / 2; i++) {
        int offset_x = round(i * perp_dx);
        int offset_y = round(i * perp_dy);

        SDL_RenderDrawLine(renderer, cursor->x + offset_x, cursor->y + offset_y, new_x + offset_x, new_y + offset_y);
    }

    cursor->x = new_x;
    cursor->y = new_y;
}
