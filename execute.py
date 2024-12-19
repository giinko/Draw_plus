import re
from instruction import Cursor
import time

def execute(ast, context=None,timer=None):

    if context is None:
        context = {"errors": []}  

    canvas = context.get("canvas")


    try:
        if ast["instruction"] == "if":
            condition = ast["condition"]
            try:
                if eval(condition, {}, context):  # Évaluer la condition dans le contexte donné
                    for instruction in ast["body"]:  # Exécuter les instructions dans le corps du if
                        result = execute(instruction['ast'], context, timer)
                else:
                    if "else" in ast:  # Vérifier si un bloc else existe
                        for instruction in ast["else"]:  # Exécuter les instructions dans le bloc else
                            result = execute(instruction['ast'], context, timer)

            except Exception as e:
                return {"error": f"Invalid condition for if: {e}"}

        elif ast["instruction"] == "for":
            variable = ast["variable"]
            range_start, range_end = ast["range"]

            try:
                range_start = eval(range_start, {}, context)
                range_end = eval(range_end, {}, context)
            except Exception as e:
                return {"error": f"Invalid range values in for loop: {e}"}

            for i in range(range_start, range_end):
                context[variable] = i
                for instruction in ast["body"]:
                    result = execute(instruction["ast"], context,timer)
                    if "error" in result:
                        return result

        elif ast["instruction"] == "while":
            condition_expr = ast["condition"]  
            
            try:
                while eval(condition_expr, {}, context):  
                    for instruction in ast["body"]:
                        result = execute(instruction["ast"], context, timer)
                        if "error" in result:
                            return result  
            except Exception as e:
                return {"error": f"Invalid values in condition for while loop: {e}"}


        elif ast["instruction"] == "ASSIGN":
            var_name = ast["variable"]
            expression = ast["value"]

            try:
                value = eval(expression, {}, context)
                context[var_name] = value
            except Exception as e:
                return {"error": f"Failed to assign value to variable '{var_name}': {e}"}

        elif ast["instruction"] == "DRAW":
            shape = ast['FORM']
            try:
                taille = eval(ast["TAILLE"], {}, context)
            except Exception as e:
                return {"error": f"Invalid size value in DRAW: {e}"}

            name_curs = ast["cursor"]
            if name_curs not in context:
                return {"error": f"Cursor '{name_curs}' is not defined in context."}

            cursor = context[name_curs]
            if canvas:
                try:
                    if shape == "CIRCLE":
                        cursor.draw_circle(taille)
                    elif shape == "SQUARE":
                        cursor.draw_rectangle(taille, taille)
                    elif shape == "RECTANGLE":
                        supp = eval(ast["Info_supp"], {}, context)
                        cursor.draw_rectangle(taille, supp)
                    elif shape == "ARC_CIRCLE":
                        supp = eval(ast["Info_supp"], {}, context)
                        cursor.draw_arc(taille, 0, supp)
                    elif shape == "LINE":
                        cursor.draw_line(taille)
                    else:
                        return {"error": f"Shape '{shape}' is not recognized."}
                    if timer :
                        time.sleep(timer)
                        canvas.update()
                except Exception as e:
                    return {"error": f"Failed to draw shape '{shape}': {e}"}

        elif ast["instruction"] == "MOOV":
            try:
                dis = eval(ast["distance"], {}, context)
                name_cursor = ast["cursor"]
                if name_cursor not in context:
                    return {"error": f"Cursor '{name_cursor}' is not defined in context."}
                cursor = context[name_cursor]
                cursor.move_forward(dis)
            except Exception as e:
                return {"error": f"Failed to move cursor: {e}"}

        elif ast["instruction"] == "ROTATE":
            try:
                name_curs = ast["name_cursor"]
                try:
                    angle = eval(ast["angle"], {}, context)
                except Exception as e:
                    return {"error": f"Invalid angle value in ROTATE: {e}"}
                
                if name_curs not in context:
                    return {"error": f"Cursor '{name_curs}' is not defined in context."}
                cursor = context[name_curs]
                cursor.rotate(angle)
            except Exception as e:
                return {"error": f"Failed to rotate cursor: {e}"}

        elif ast["instruction"] == "SET":
            try:
                name = ast["name"]
                x = eval(ast["x"], {}, context)
                y = eval(ast["y"], {}, context)
                color = ast["color"]
                epaisseur = eval(ast["epaisseur"], {}, context)
                curs = Cursor(canvas, x, y, color, epaisseur)
                context[name] = curs
            except Exception as e:
                return {"error": f"Failed to set cursor properties: {e}"}

        elif ast["instruction"] == "CREATE_CURSOR":
            try:
                name = ast["name"]
                x = eval(ast["x"], {}, context)
                y = eval(ast["y"], {}, context)
                color = ast["color"]
                epaisseur = eval(ast["epaisseur"], {}, context)
                curs = Cursor(canvas, x, y, color, epaisseur)
                context[name] = curs
            except Exception as e:
                return {"error": f"Failed to create cursor: {e}"}

        else:
            return {"error": f"Unknown instruction: {ast['instruction']}"}

    except Exception as general_error:
        return {"error": f"Unexpected error: {str(general_error)}"}

    return context  
