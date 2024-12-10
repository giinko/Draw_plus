import re
from instruction import Cursor

def execute(ast, context=None):

    if context is None:
        context = {}

    canvas = context.get("canvas")
    cursor = context.get("cursor")


    if ast["instruction"] == "if":
        condition = ast["condition"]
        print(ast)
        if eval(condition, {}, context):  
            for instruction in ast["body"]:

                execute(instruction['ast'], context) #Vérifier que pas d'erreur faire un check

    elif ast["instruction"] == "for":
        
        print("for")

        variable = ast["variable"]
        print("for")
        range_start, range_end = ast["range"]

        try:
            range_start = int(range_start)
            range_end = int(range_end)
        except ValueError:
            if isinstance(range_start, str) and range_start in context:
                range_start = context[range_start]
            if isinstance(range_end, str) and range_end in context:
                range_end = context[range_end]

        for i in range(range_start, range_end):
            context[variable] = i
            for instruction in ast["body"]:
                execute(instruction["ast"], context)

    elif ast["instruction"] == "ASSIGN":
        var_name = ast["variable"]
        expression = ast["value"]

        try:

            if not isinstance(expression, int):
                value = eval(expression, {}, context)
                context[var_name] = value 
            else:
                context[var_name] = expression
                value = expression

            print(f"Variable {var_name} set to {value}")
        except Exception as e:
            print(f"Erreur lors de l'évaluation de l'expression '{expression}': {e}")


    elif ast["instruction"] == "DRAW":
        print(f"Drawing shape: {ast['FORM']}")  # Exemple of actions to perform
        shape = ast['FORM']
        taille = int(ast["TAILLE"])
        name_curs = ast["cursor"]
        cursor = context[name_curs]
        print(cursor)
        if canvas:
            if shape == "CIRCLE":
                cursor.draw_circle(taille)

            elif shape == "SQUARE":
                cursor.draw_rectangle(taille,taille)

            elif shape == "RECTANGLE":
                supp = int(ast["Info_supp"])
                cursor.draw_rectangle(taille,supp)

            elif shape == "ARC_CIRCLE":
                supp = int(ast["Info_supp"])
                cursor.draw_arc(taille,0,supp)

            elif shape == "LINE":
                cursor.draw_line(taille)

            else:
                print(f"Shape '{shape}' is not recognized.")

    elif ast["instruction"] == "MOOV":
        print(f"Moving cursor by {ast['distance']} units") 

        dis = int(ast["distance"])
        name_cursor = ast["cursor"]
        cursor = context[name_cursor]

        cursor.move_forward(dis)

    elif ast["instruction"] == "ROTATE":
        name_curs = ast["name_cursor"]
        angle = ast["angle"]
        cursor = context[name_curs]

        cursor.rotate(angle)

    elif ast["instruction"] == "SET":
        print(f"Setting color to {ast['color']} and thickness to {ast['epaisseur']}")
        curs = Cursor(canvas,int(ast["x"]),int(ast["y"]),ast["color"],int(ast["epaisseur"]))
        name = ast["name"]
        context[name] = curs
    

    elif ast["instruction"] == "CREATE_CURSOR":
        print(f"Creating cursor at ({ast['x']}, {ast['y']})")
        curs = Cursor(canvas,int(ast["x"]),int(ast["y"]),ast["color"],int(ast["epaisseur"]))
        name = ast["name"]
        context[name] = curs
    

    else:
        print(f"Unknown instruction in execute : {ast['instruction']}")

    return context


#Finaliser toutes les instructions (Rajouter MOOV, SET, CREATE ...)

#Faire en sorte que toute le code fonctionne bien ( focntion tokenize a revoir )

#Rajouter des parametres pour chaque truc ( taille , ...)
