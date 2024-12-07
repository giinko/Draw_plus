def tokenize(code):

    code = code.replace("(", " ( ").replace(")", " ) ").replace(",", " , ")

    tokens = code.split()

    return tokens


def parse(tokens):

    if not tokens:
        return {"error": "Empty instruction"}

    if tokens[0] == "CREATE_CURSOR":
        if len(tokens) != 8 or tokens[1] != "(" or tokens[7] != ")":
            return {"error": "Invalid syntax for CREATE_CURSOR"}
        try:
            x = int(tokens[2])
            y = int(tokens[4])
            visibility = tokens[6]
            if visibility not in ["visible", "invisible"]:
                return {"error": f"Invalid visibility value: {visibility}"}
        except ValueError:
            return {"error": "Invalid coordinate value for CREATE_CURSOR"}
        
        return {
            "instruction": "CREATE_CURSOR",
            "x": x,
            "y": y,
            "visibility": visibility,
        }

    elif tokens[0] == "SET":
        if len(tokens) != 6 or tokens[1] != "(" or tokens[5] != ")":
            return {"error": "Invalid syntax for SET"}
        color = tokens[2]
        try:
            epaisseur = int(tokens[4])
        except ValueError:
            return {"error": "Invalid thickness value for SET"}
        
        return {
            "ast": {
                "instruction": "SET",
                "color": color,
                "thickness": epaisseur,
            }
        }

    # MOOV
    elif tokens[0] == "MOOV":
        if len(tokens) != 4 or tokens[1] != "(" or tokens[3] != ")":
            return {"error": "Invalid syntax for MOOV"}
        try:
            distance = int(tokens[2])
        except ValueError:
            return {"error": "Invalid distance value for MOOV"}
        
        return {
            "ast": {
                "instruction": "MOOV",
                "distance": distance,
            }
        }

    # DRAW
    elif tokens[0] == "DRAW":
        if len(tokens) != 4 or tokens[1] != "(" or tokens[3] != ")":
            return {"error": "Invalid syntax for DRAW"}
        shape = tokens[2]
        if shape not in ["SEGMENT", "CIRCLE", "SQUARE", "RECTANGLE", "HALF_CIRCLE"]:
            return {"error": f"Invalid shape: {shape}"}
        
        return {
            "ast": {
                "instruction": "DRAW",
                "shape": shape,
            }
        }

    # IF
    elif tokens[0] == "if":
        if len(tokens) < 5 or tokens[1] != "(" or tokens[-1] != ")":
            return {"error": "Invalid syntax for if condition"}
        condition = " ".join(tokens[2:-1])  # Combine les tokens de la condition
        return {
            "ast": {
                "instruction": "if",
                "condition": condition,
            }
        }

    # FOR
    elif tokens[0] == "for":
        if len(tokens) < 6 or tokens[2] != "in" or tokens[3] != "range" or tokens[4] != "(" or tokens[-1] != ")":
            return {"error": "Invalid syntax for for loop"}
        try:
            range_start = int(tokens[5])
            range_end = int(tokens[7])
        except ValueError:
            return {"error": "Invalid range values for for loop"}
        
        return {
            "ast": {
                "instruction": "for",
                "variable": tokens[1],
                "range": (range_start, range_end),
            }
        }

    # Si l'instruction est inconnue
    return {"error": f"Unknown instruction: {tokens[0]}"}





code = "for i in range(1, 10)"
tokens = tokenize(code)
result = parse(tokens)
print(result)
# Résultat attendu :
# {'ast': {'instruction': 'for', 'variable': 'i', 'range': (1, 10)}}

