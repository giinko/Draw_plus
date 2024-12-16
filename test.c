#include "draw_lib.h"

int main() {
    // Initialiser la fenêtre graphique
    if (!initialize_graphics(800, 600, "Test Draw++")) {
        return -1;
    }

    // Définir les couleurs
    SDL_Color red = {255, 0, 0, 255};
    SDL_Color blue = {0, 0, 255, 255};

    // Créer un curseur
    Cursor c1 = create_cursor(400, 300, "red", 3);

    // Test 1 : Dessiner un cercle
    draw_circle(c1, 50);

    // Test 2 : Déplacer le curseur et dessiner un rectangle
    move_cursor(&c1, 100);
    draw_rectangle(c1, 100, 50);

    // Test 3 : Rotation et ligne
    rotate_cursor(&c1, 45);
    draw_line(c1, 150);

    // Test 4 : Dessiner un arc
    draw_arc(c1, 100, 0, 180);

    // Mise à jour de l'écran pour afficher les dessins
    update_screen();

    // Attendre 5 secondes
    SDL_Delay(5000);

    // Nettoyer les ressources
    cleanup_graphics();
    return 0;
}
