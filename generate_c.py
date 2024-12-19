from parseur import instrctions_listed,parseur


def generate_c_code(ast, window_width=800, window_height=600, window_title="Drawing Window"):
    """
    Générateur de code C complet à partir de l'AST.
    :param ast: L'AST généré par le parseur.
    :param window_width: Largeur de la fenêtre SDL.
    :param window_height: Hauteur de la fenêtre SDL.
    :param window_title: Titre de la fenêtre SDL.
    :return: Le code C sous forme de chaîne.
    """
    c_code = f"""#include "draw_lib.h"
#include <stdio.h>
#include <math.h>

int main() {{
    // Initialisation de la fenêtre
    if (!initialize_graphics({window_width}, {window_height}, "{window_title}")) {{
        fprintf(stderr, "Échec de l'initialisation graphique\\n");
        return 1;
    }}

    SDL_Color background_color = get_color("white");  // Fond blanc par défaut
    clear_screen(background_color);

    // Déclaration des curseurs
"""
    indentation = "    "  # Indentation pour les blocs internes

    def generate_block(ast_block, indent_level=1):
        block_code = ""
        current_indent = indentation * indent_level

        for instruction in ast_block:
            if "error" in instruction:
                block_code += f"{current_indent}// ERROR: {instruction['error']}\n"
                continue

            node = instruction["ast"]
            instr_type = node["instruction"]

            if instr_type == "CREATE_CURSOR":
                block_code += f'{current_indent}Cursor {node["name"]} = create_cursor({node["x"]}, {node["y"]}, "{node["color"]}", {node["epaisseur"]});\n'

            elif instr_type == "DRAW":
                shape = node["FORM"].upper()
                if shape == "CIRCLE":
                    block_code += f'{current_indent}draw_circle({node["cursor"]}, {node["TAILLE"]});\n'
                elif shape == "RECTANGLE":
                    block_code += f'{current_indent}draw_rectangle({node["cursor"]}, {node["TAILLE"]}, {node["Info_supp"]});\n'
                elif shape == "LINE":
                    block_code += f'{current_indent}draw_line(&{node["cursor"]}, {node["TAILLE"]});\n'
                else:
                    block_code += f"{current_indent}// Shape '{shape}' non supportée\n"

            elif instr_type == "MOOV":
                block_code += f'{current_indent}move_cursor(&{node["cursor"]}, {node["distance"]});\n'

            elif instr_type == "ROTATE":
                block_code += f'{current_indent}rotate_cursor(&{node["name_cursor"]}, {node["angle"]});\n'

            elif instr_type == "ASSIGN":
                block_code += f'{current_indent}int {node["variable"]} = {node["value"]};\n'

            elif instr_type == "if":
                block_code += f'{current_indent}if ({node["condition"]}) {{\n'
                block_code += generate_block(node["body"], indent_level + 1)
                block_code += f'{current_indent}}}\n'
                if "else" in node:
                    block_code += f'{current_indent}else {{\n'
                    block_code += generate_block(node["else"], indent_level + 1)
                    block_code += f'{current_indent}}}\n'

            elif instr_type == "for":
                block_code += f'{current_indent}for (int {node["variable"]} = {node["range"][0]}; {node["variable"]} < {node["range"][1]}; ++{node["variable"]}) {{\n'
                block_code += generate_block(node["body"], indent_level + 1)
                block_code += f'{current_indent}}}\n'

            elif instr_type == "while":
                block_code += f'{current_indent}while ({node["condition"]}) {{\n'
                block_code += generate_block(node["body"], indent_level + 1)
                block_code += f'{current_indent}}}\n'

        return block_code

    # Générer le bloc principal du programme
    c_code += generate_block(ast)

    # Finalisation
    c_code += f"""
    update_screen();
    SDL_Delay(5000);  // Attendre 5 secondes avant de quitter
    cleanup_graphics();
    return 0;
}}
"""
    return c_code


def write_c_file(code_c, file_name="output.c"):
    """
    Écrit le code C dans un fichier spécifié.
    :param code_c: Le code C sous forme de chaîne.
    :param file_name: Le nom du fichier où écrire le code.
    """
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(code_c)
        print(f"Le code a été sauvegardé dans le fichier '{file_name}'.")
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier: {str(e)}")