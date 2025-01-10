#include "draw_lib.h"
#include <stdio.h>
#include <math.h>

int main() {
    // Initialize the window
    if (!initialize_graphics(800, 600, "Drawing Window")) {
        fprintf(stderr, "Échec de l'initialisation graphique\n");
        return 1;
    }

    // Create a new cursor
    Cursor cur1 = create_cursor(100, 100, "black", 5);
    int x = 3;
    while (x<5) {
        move_cursor(&cur1, 100);
        // Draw a square
        draw_square(&cur1, 25);
        x = x+1;
    }

    // Update the window
    SDL_RenderPresent(renderer);
    SDL_Delay(5000);  // Wait 5 second before closing the window
    cleanup_graphics(); // Close the window

    return 0;
}
