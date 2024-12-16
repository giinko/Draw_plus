from parseur import instrctions_listed,parseur


def generate_c_code(ast_list, output_file="output.c"):
    """
    Génère le code C à partir de l'AST (liste des instructions).
    """
    # Début du code C
    code = [
        '#include "draw_lib.h"',
        "",
        "int main() {",
        '    // Initialisation de la fenêtre graphique',
        '    if (!initialize_graphics(800, 600, "Draw++ Output")) {',
        "        return -1;",
        "    }",
        "",
        "    // Nettoyage de l'écran avec une couleur blanche",
        "    clear_screen((SDL_Color){255, 255, 255, 255});",
        ""
    ]

    # Dictionnaire des curseurs créés
    cursors = {}

    # Parcourir les instructions de l'AST
    for ast in ast_list:
        ast = ast["ast"]
        if ast["instruction"] == "CREATE_CURSOR":
            # Créer un curseur
            name = ast["name"]
            x = ast["x"]
            y = ast["y"]
            color = ast["color"]
            thickness = ast["epaisseur"]
            cursors[name] = True
            code.append(f'    Cursor {name} = create_cursor({x}, {y}, "{color}", {thickness});')

        elif ast["instruction"] == "DRAW":
            # Dessiner une forme
            cursor = ast["cursor"]
            if cursor not in cursors:
                raise ValueError(f"Cursor '{cursor}' n'a pas été créé avant son utilisation.")
            shape = ast["FORM"]
            size = ast["TAILLE"]
            if shape == "CIRCLE":
                code.append(f'    draw_circle({cursor}, {size});')
            elif shape == "RECTANGLE":
                additional = ast["Info_supp"]
                code.append(f'    draw_rectangle({cursor}, {size}, {additional});')
            elif shape == "ARC_CIRCLE":
                additional = ast["Info_supp"]
                code.append(f'    draw_arc({cursor}, {size}, 0, {additional});')
            elif shape == "LINE":
                code.append(f'    draw_line({cursor}, {size});')
            else:
                raise ValueError(f"Forme non supportée : {shape}")

        elif ast["instruction"] == "MOOV":
            # Déplacer un curseur
            cursor = ast["cursor"]
            distance = ast["distance"]
            if cursor not in cursors:
                raise ValueError(f"Cursor '{cursor}' n'a pas été créé avant son utilisation.")
            code.append(f'    move_cursor(&{cursor}, {distance});')

        elif ast["instruction"] == "ROTATE":
            # Tourner un curseur
            cursor = ast["name_cursor"]
            angle = ast["angle"]
            if cursor not in cursors:
                raise ValueError(f"Cursor '{cursor}' n'a pas été créé avant son utilisation.")
            code.append(f'    rotate_cursor(&{cursor}, {angle});')

        else:
            raise ValueError(f"Instruction non supportée : {ast['instruction']}")

    # Ajouter la mise à jour de l'écran et le nettoyage des ressources
    code.append("")
    code.append("    // Mettre à jour l'écran et attendre 5 secondes")
    code.append("    update_screen();")
    code.append("    SDL_Delay(5000);")
    code.append("")
    code.append("    // Nettoyage des ressources graphiques")
    code.append("    cleanup_graphics();")
    code.append("")
    code.append("    return 0;")
    code.append("}")

    # Écrire dans un fichier
    with open(output_file, "w") as f:
        f.write("\n".join(code))

    print(f"Code C généré avec succès dans {output_file}.")


# Exemple d'utilisation
if __name__ == "__main__":

    code = "CREATE_CURSOR(cur1,100,100,red,4);DRAW(cur1,RECTANGLE,50,100);MOOV(cur1,100);DRAW(cur1,RECTANGLE,50,100);"
    t = instrctions_listed(code)

    tt= parseur(t)

    # Génération du code C

    generate_c_code(tt)

# cree if else et for !! ouin ouin 