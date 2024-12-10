import re

def instrctions_listed(code):

    stack = [[]]  
    current_instruction = ""  
    
    for char in code:
        if char == ";":  # End of an instruction
            if current_instruction.strip():  # Add the instruction if it's not empty
                stack[-1].append(current_instruction.strip())
                current_instruction = ""
        elif char == "{":  # Start of a new block
            if current_instruction.strip():  # Add the instruction preceding the block
                stack[-1].append(current_instruction.strip())
                current_instruction = ""
            new_block = []  # Create a new list for the block
            stack[-1].append(new_block)  # Add it to the current context
            stack.append(new_block)  # Push it onto the stack
        elif char == "}":  # End of the current block
            if current_instruction.strip():  # Add any instruction before closing the block
                stack[-1].append(current_instruction.strip())
                current_instruction = ""
            stack.pop()  # Pop the current block off the stack
        else:  # Part of an instruction
            current_instruction += char
    
    # Add the last instruction if the code doesn't end with a semicolon
    if current_instruction.strip():
        stack[-1].append(current_instruction.strip())
    
    return stack[0]  # The result is the top-level list

def parseur_2(tokens, result=None):

    if result is None:
        result = []  # Initialisation of the list at first call
    count = 0

    for instruction in tokens:

        try :
            if isinstance(instruction, str):

                instr = re.findall(r'\w+|\d+|[^\w\s]', instruction)

                if instr[0] == "DRAW":
                    #DRAW(cursor,form,taille,supp(taille,angle))
                    try:
                        infos = "".join(instr[instr.index("(")+1:instr.index(")")]).split(",")
                        if (len(infos) < 4) & (infos[1] in ["ARC_CIRCLE", "RECTANGLE"]):
                            result.append({"error": "DRAW requires at least 4 parameters: cursor, form, size, and additional info."})
                            continue
                        if len(infos) < 3:
                            result.append({"error": "DRAW requires at least 3 parameters: cursor, form, size."})
                            continue
                        if infos[1] not in ["ARC_CIRCLE", "RECTANGLE", "CIRCLE", "LINE", "SQUARE"]:
                            result.append({"error": f"Unsupported shape '{infos[1]}' in DRAW."})
                            continue
                        if not infos[2].isdigit():
                            #Pas forcément ca peut aussi etre une variable on va voir ca apres
                            result.append({"error": f"The size parameter '{infos[2]}' in DRAW must be a positive integer."})
                            continue
                        result.append({
                            "ast": {
                                "instruction": "DRAW",
                                "FORM": infos[1],
                                "TAILLE": infos[2],
                                'cursor': infos[0],
                                "Info_supp": infos[3] if infos[1] in ["ARC_CIRCLE", "RECTANGLE"] else "50"
                            }
                        })
                    except Exception as e:
                        result.append({"error": f"Unexpected error in DRAW: {str(e)}"})
                
                elif instr[0] == "MOOV":
                    #MOOV(cursor,distance)
                    #Faire les checks d'erreur
                    infos = "".join(instr[instr.index("(")+1:instr.index(")")]).split(",")
                    result.append({
                        "ast": {
                        "instruction": "MOOV",
                        "distance": infos[1],
                        "cursor" : infos[0]
                        }
                    })

                elif instr[0] == "CREATE_CURSOR":
                    #CREATE_CURSOR(name,x,y,color,épaisseur)
                    #Faire les checks d'erreur
                    prop = "".join(instr[instr.index("(")+1:instr.index(")")]).split(",")

                    result.append({
                        "ast": {
                        "instruction": "CREATE_CURSOR",
                        "name" : prop[0],
                        "x" : prop[1],
                        "y" : prop[2],
                        "color" : prop[3],
                        "epaisseur": prop[4],
                        }
                    })

                elif instr[0] == "ROTATE":
                    #ROTATE(cursor,angle)
                    infos = "".join(instr[instr.index("(")+1:instr.index(")")]).split(",")
                    result.append({
                        "ast": {
                            "instruction": "ROTATE",
                            "name_cursor": infos[0],
                            "angle": infos[1]
                        }
                    })

                elif instr[0] == "SET":
                    #SET(cursor_name,x,y,color,epaisseur)
                    infos = "".join(instr[instr.index("(")+1:instr.index(")")]).split(",")
                    
                    result.append({
                        "ast": {
                        "instruction": "SET",
                        "name" : infos[0],
                        "x" : infos[1],
                        "y" : infos[2],
                        "color" : infos[3],
                        "epaisseur": infos[4],
                        }
                    })

                elif instr[0] == "if":
                    condition = "".join(instr[instr.index("(")+1:instr.index(")")])
                    bod = tokens[count+1]
                    result.append({
                        "ast": {
                            "instruction": "if",
                            "condition": condition,
                            "body": parseur_2(bod),
                        }
                    })

                elif instr[0] == "for":
                    in_par = "".join(instr[instr.index("(")+1:instr.index(")")]).split(",")
                    range_start = in_par[0]
                    range_end = in_par[1]
                    bod = tokens[count+1]

                    result.append({
                        "ast": {
                            "instruction": "for",
                            "variable": instr[1],
                            "range": (range_start, range_end),
                            "body": parseur_2(bod),
                        }
                    })

                elif instr[1] == "=":
                    #nom_var = value_var
                    nom_var = instr[0]
                    value_var = "".join(instr[2:])

                    result.append({
                        "ast": {
                            "instruction": "ASSIGN",
                            "variable": nom_var,
                            "value": value_var
                        }
                    })



                #Coder SET, MOOV, ...
                #Coder ASSIGN, ...
                #Faire en sorte de rajouter une taille  pour les formes

                else:
                    print("Cet instruction n'existe pas")

        except Exception as e:
            result.append({"error": f"General parsing error: {str(e)}"})
        count += 1
    return result
    

#tt = parse(["for i in range(2,4)",["if(5>4)",["DRAW(CIRCLE)"],"DRAW(CIRCLE)"],'DRAW(CIRCLE)', 'if(3>4)',['DRAW(CIRCLE)',"DRAW(CIRCLE)"]])


#yes= parse(["DRAW(CIRCLE,50)"])

#print(yes)

# Exemple of use with a given chain
#code = "DRAW(CIRCLE);DRAW(CIRCLE);if(3>4){if(5>4){DRAW(CIRCLE);} } DRAW(CIRCLE);for i in range(1,2){DRAW(CIRCLE);}"
#parsed = parse_instructions(code)

#ttt = parse(parsed)
#print(ttt)


