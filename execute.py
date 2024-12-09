import re

def execute(ast, context=None):

    if context is None:
        context = {}

    canvas = context.get("canvas")



    if ast["instruction"] == "if":
        condition = ast["condition"]
        if eval(condition, {}, context):  
            for instruction in ast["body"]:
                execute(instruction, context)

    elif ast["instruction"] == "for":

        variable = ast["variable"]
        range_start, range_end = ast["range"]

        if not isinstance(range_start,int):
            range_start = context[range_start]
        if not isinstance(range_end,int):
            range_end = context[range_end]

        for i in range(range_start, range_end):
            context[variable] = i
            for instruction in ast["body"]:
                execute(instruction, context)

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
        print(f"Drawing shape: {ast['shape']}")  # Exemple of actions to perform
        shape = ast['shape']
        if canvas:
            if shape == "CIRCLE":
                # Draw a circle : arbitrary coordinates
                canvas.create_oval(150, 150, 250, 250, outline="black", width=2)
            elif shape == "SQUARE":
                # Draw a square : arbitrary coordinates
                canvas.create_rectangle(150, 150, 250, 250, outline="black", width=2)
            elif shape == "RECTANGLE":
                # Draw a rectangle : arbitrary coordinates
                canvas.create_rectangle(150, 150, 300, 200, outline="black", width=2)
            elif shape == "HALF_CIRCLE":
                # Draw a semi-circle : arbitrary position and size
                canvas.create_arc(150, 150, 250, 250, start=0, extent=180, outline="black", width=2)
            else:
                print(f"Shape '{shape}' is not recognized.")

    elif ast["instruction"] == "MOOV":
        print(f"Moving cursor by {ast['distance']} units") 

    elif ast["instruction"] == "SET":
        print(f"Setting color to {ast['color']} and thickness to {ast['thickness']}")

    elif ast["instruction"] == "CREATE_CURSOR":
        print(f"Creating cursor at ({ast['x']}, {ast['y']}) with visibility {ast['visibility']}")

    else:
        print(f"Unknown instruction in execute : {ast['instruction']}")

    return context


#Finaliser toutes les instructions (Rajouter MOOV, SET, CREATE ...)

#Faire en sorte que toute le code fonctionne bien ( focntion tokenize a revoir )

#Rajouter des parametres pour chaque truc ( taille , ...)
