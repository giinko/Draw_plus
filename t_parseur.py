def tokenize(code):

    instructions = code.split(";")
    tokens = []

    for instruction in instructions :
        chaine = instruction.replace("(", " ( ").replace(")", " ) ").replace(",", " , ").replace("="," = ").replace("{"," { ").replace("}"," } ")
        
        if ("+" and "=") in instruction and "if" not in instruction:
            chaine = chaine.replace(" ","").replace("="," = ")

        ch = chaine.split()
        if ch:
            tokens.append(ch)

    return tokens


def parse(tokens):
    if not tokens:
        return {"error": "Empty instruction"}

    if tokens[0] == "if":
        if len(tokens) < 5 or tokens[1] != "(" or  ")" not in tokens:
            return {"error": "Invalid syntax for if condition"}

        condition = "".join(tokens[2])  # Get the condition
        body = parse_block(tokens)  # Analyze the associated block

        return {
            "ast": {
                "instruction": "if",
                "condition": condition,
                "body": body,
            }
        }

    elif tokens[0] == "for":
        if len(tokens) < 9 or tokens[2] != "in" or tokens[3] != "range" or tokens[4] != "(" or ")" not in tokens:
            return {"error": "Invalid syntax for for loop"}
        try:
            range_start = tokens[5]
            range_end = tokens[7]
        except ValueError:
            return {"error": "Invalid range values for for loop"}
        
        body = parse_block(tokens) 

        return {
            "ast": {
                "instruction": "for",
                "variable": tokens[1],
                "range": (range_start, range_end),
                "body": body,
            }
        }

    # Other instructions
    elif tokens[0] in ["DRAW", "MOOV", "SET", "CREATE_CURSOR"]:
        # Existing code to analyze easy instructions

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
                "ast" : {
                    "instruction": "CREATE_CURSOR",
                    "x": x,
                    "y": y,
                    "visibility": visibility,
                    }
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


    elif "=" in tokens:
        var_name = tokens[0]  # Name of the variable
        try:
            value = tokens[2].replace(" ","")
        except ValueError:
            return {"error": "Invalid value for assignment"}
        
        return {
            "ast": {
                "instruction": "ASSIGN",
                "variable": var_name,
                "value": value
            }
        }

    return {"error": f"Unknown instruction in parseur: {tokens}"}


def parse_block(tokens):
    """
    Analyse un bloc d'instructions entre { et }
    """
    if "{" not in tokens or "}" not in tokens:
        return {"error": "Missing block delimiters { or }"}

    start = tokens.index("{") + 1
    end = tokens.index("}")
    block_tokens = tokens[start:end]  # Contains all the instructions of the block
    
    body = []
    while block_tokens:
        # Get each instruction (supposing ; as separator)
        try:
            semicolon = block_tokens.index(",")
            instruction_tokens = block_tokens[:semicolon]
            block_tokens = block_tokens[semicolon + 1:]  # Rest of the tokens
            result = parse(instruction_tokens)  # Recursive analysis
            if "error" not in result:
                body.append(result["ast"])
        except ValueError:
            break  # No semicolons, block finished

    return body


#Séparer les ; ( comme de base ) mais d'abord sep tout les { } 
#ensuite des que {} s'ouvre et se ferme on met dans une liste si y'a plus de {}
#on sep tout par ; et on fait truc normal [draw, ... , if, condition, [body], draw, ...]
#et dans le body on peut mettre encore des listes et des conditions.
