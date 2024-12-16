#include "draw_lib.h"
#include <math.h>
#include <stdio.h>

// Variables globales pour SDL
static SDL_Window* window = NULL;
static SDL_Renderer* renderer = NULL;

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

    return 1; // Succès
}

// Nettoyage des ressources SDL
void cleanup_graphics() {
    if (renderer) SDL_DestroyRenderer(renderer);
    if (window) SDL_DestroyWindow(window);
    SDL_Quit();
}

// Création d'un curseur
Cursor create_cursor(int x, int y, const char* color_name, int thickness) {
    SDL_Color color = get_color(color_name);
    Cursor cursor = {x, y, 0, color, thickness};
    return cursor;
}


// Mouvement d'un curseur
void move_cursor(Cursor* cursor, int distance) {
    cursor->x += distance * cos(cursor->angle * M_PI / 180.0);
    cursor->y += distance * sin(cursor->angle * M_PI / 180.0);
}

// Rotation d'un curseur
void rotate_cursor(Cursor* cursor, int angle) {
    cursor->angle = (cursor->angle + angle) % 360;
}

// Dessin d'un cercle
void draw_circle(Cursor cursor, int radius) {
    SDL_SetRenderDrawColor(renderer, cursor.color.r, cursor.color.g, cursor.color.b, cursor.color.a);
    for (int w = 0; w < radius * 2; w++) {
        for (int h = 0; h < radius * 2; h++) {
            int dx = radius - w; 
            int dy = radius - h; 
            if ((dx * dx + dy * dy) <= (radius * radius)) {
                SDL_RenderDrawPoint(renderer, cursor.x + dx, cursor.y + dy);
            }
        }
    }
}

// Dessin d'un rectangle
void draw_rectangle(Cursor cursor, int width, int height) {
    SDL_SetRenderDrawColor(renderer, cursor.color.r, cursor.color.g, cursor.color.b, cursor.color.a);
    SDL_Rect rect = {cursor.x, cursor.y, width, height};
    SDL_RenderDrawRect(renderer, &rect);
}

// Dessin d'une ligne
void draw_line(Cursor cursor, int length) {
    int x2 = cursor.x + length * cos(cursor.angle * M_PI / 180.0);
    int y2 = cursor.y + length * sin(cursor.angle * M_PI / 180.0);
    SDL_SetRenderDrawColor(renderer, cursor.color.r, cursor.color.g, cursor.color.b, cursor.color.a);
    SDL_RenderDrawLine(renderer, cursor.x, cursor.y, x2, y2);
}

// Dessin d'un arc
void draw_arc(Cursor cursor, int radius, int start_angle, int extent) {
    SDL_SetRenderDrawColor(renderer, cursor.color.r, cursor.color.g, cursor.color.b, cursor.color.a);
    for (int angle = start_angle; angle < start_angle + extent; angle++) {
        int x = cursor.x + radius * cos(angle * M_PI / 180.0);
        int y = cursor.y + radius * sin(angle * M_PI / 180.0);
        SDL_RenderDrawPoint(renderer, x, y);
    }
}

// Dessin d'un polygone
void draw_polygon(Cursor cursor, const int* points, int num_points) {
    SDL_SetRenderDrawColor(renderer, cursor.color.r, cursor.color.g, cursor.color.b, cursor.color.a);
    for (int i = 0; i < num_points - 1; i++) {
        SDL_RenderDrawLine(renderer, points[i * 2], points[i * 2 + 1], points[(i + 1) * 2], points[(i + 1) * 2 + 1]);
    }
    SDL_RenderDrawLine(renderer, points[0], points[1], points[(num_points - 1) * 2], points[(num_points - 1) * 2 + 1]);
}

// Dessin de texte
void draw_text(Cursor cursor, const char* text) {
    // Pour dessiner du texte, une bibliothèque comme SDL_ttf est nécessaire.
    fprintf(stderr, "Dessin de texte non implémenté. Utilisez SDL_ttf pour cette fonctionnalité.\n");
}

// Mise à jour de l'écran
void update_screen() {
    SDL_RenderPresent(renderer);
}

// Effacer l'écran
void clear_screen(SDL_Color background_color) {
    SDL_SetRenderDrawColor(renderer, background_color.r, background_color.g, background_color.b, background_color.a);
    SDL_RenderClear(renderer);
}

SDL_Color get_color(const char* color_name) {
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
