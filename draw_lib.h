#ifndef DRAW_LIB_H
#define DRAW_LIB_H

#include <SDL2/SDL.h>

typedef struct {
    int x, y;       // Position actuelle
    int angle;      // Orientation (en degrés)
    SDL_Color color; // Couleur (SDL_Color contient r, g, b, a)
    int thickness;  // Épaisseur des traits
} Cursor;

// Initialisation et nettoyage
int initialize_graphics(int width, int height, const char* title);
void cleanup_graphics();

// Gestion des curseurs
Cursor create_cursor(int x, int y, const char* color_name, int thickness);
void move_cursor(Cursor* cursor, int distance);
void rotate_cursor(Cursor* cursor, int angle);
SDL_Color get_color(const char* color_name);



// Dessin de formes
void draw_circle(Cursor cursor, int radius);
void draw_rectangle(Cursor cursor, int width, int height);
void draw_line(Cursor* cursor, int length);
void draw_arc(Cursor cursor, int radius, int start_angle, int extent);
void draw_polygon(Cursor cursor, const int* points, int num_points);
void draw_text(Cursor cursor, const char* text);

// Autres fonctionnalités
void update_screen();
void clear_screen(SDL_Color background_color);

#endif
