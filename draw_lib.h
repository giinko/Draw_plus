#ifndef INSTRUCTION_H
#define INSTRUCTION_H

#include <SDL2/SDL.h>
#include <SDL2/SDL2_gfxPrimitives.h>
#include <math.h>

// Déclaration des variables externes
extern SDL_Window* window;
extern SDL_Renderer* renderer;

// Déclaration des fonctions de gestion graphique
int initialize_graphics(int width, int height, const char* title);
void cleanup_graphics();

// Gestion des couleurs
uint32_t get_color(const char* color_name);
SDL_Color get_color_SDL(const char* color_name);

// Définition de la structure Cursor
typedef struct {
    int x, y;         // Position actuelle
    char* color_name; // Nom de la couleur
    int thickness;    // Épaisseur des traits
    int angle;        // Orientation (en degrés)
} Cursor;

// Fonctions associées au curseur
Cursor create_cursor(int x, int y, char* color_name, int thickness);
void move_cursor(Cursor* cursor, int distance);
void rotate_cursor(Cursor* cursor, int angle);

// Fonctions de dessin
void draw_circle(Cursor* cursor, int radius);
void draw_rectangle(Cursor* cursor, int width, int height);
void draw_square(Cursor* cursor, int width);
void draw_arc(Cursor* cursor, int radius, int start_angle, int end_angle);
void draw_point(Cursor* cursor);
void draw_line(Cursor* cursor, int distance);

#endif // INSTRUCTION_H
