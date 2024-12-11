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

def parseur(tokens, result=None):

    if result is None:
        result = [] 
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
                            result.append({"error": f"DRAW with {infos[1]} requires at least 4 parameters: cursor, form, size, and additional info."})
                            continue
                        if len(infos) < 3:
                            result.append({"error": "DRAW requires at least 3 parameters: cursor, form, size."})
                            continue
                        if infos[1] not in ["ARC_CIRCLE", "RECTANGLE", "CIRCLE", "LINE", "SQUARE"]:
                            result.append({"error": f"Unsupported shape '{infos[1]}' in DRAW."})
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
                    try:
                        infos = "".join(instr[instr.index("(")+1:instr.index(")")]).split(",")
                        if len(infos) != 2:
                            result.append({"error": "MOOV requires exactly 2 parameters: cursor_name and distance."})
                            continue
                        
                        result.append({
                            "ast": {
                                "instruction": "MOOV",
                                "distance": infos[1],
                                "cursor": infos[0]
                            }
                        })
                    except Exception as e:
                        result.append({"error": f"Unexpected error in MOOV: {str(e)}"})

                elif instr[0] == "CREATE_CURSOR":
                    #CREATE_CURSOR(name,x,y,color,épaisseur)
                    try:
                        infos = "".join(instr[instr.index("(")+1:instr.index(")")]).split(",")
                        if len(infos) != 5:
                            result.append({"error": "CREATE_CURSOR requires exactly 5 parameters: name, x, y, color, and thickness."})
                            continue
                        
                        result.append({
                            "ast": {
                                "instruction": "CREATE_CURSOR",
                                "name": infos[0],
                                "x": infos[1],
                                "y": infos[2],
                                "color": infos[3],
                                "epaisseur": infos[4],
                            }
                        })
                    except Exception as e:
                        result.append({"error": f"Unexpected error in CREATE_CURSOR: {str(e)}"})

                elif instr[0] == "ROTATE":
                    #ROTATE(cursor,angle)
                    try:
                        infos = "".join(instr[instr.index("(")+1:instr.index(")")]).split(",")
                        if len(infos) != 2:
                            result.append({"error": "ROTATE requires exactly 2 parameters: cursor and angle."})
                            continue
                        
                        result.append({
                            "ast": {
                                "instruction": "ROTATE",
                                "name_cursor": infos[0],
                                "angle": infos[1]
                            }
                        })
                    except Exception as e:
                        result.append({"error": f"Unexpected error in ROTATE: {str(e)}"})

                elif instr[0] == "SET":
                    #SET(cursor_name,x,y,color,epaisseur)
                    try:
                        infos = "".join(instr[instr.index("(")+1:instr.index(")")]).split(",")
                        if len(infos) != 5:
                            result.append({"error": "SET requires exactly 5 parameters: cursor_name, x, y, color, thickness."})
                            continue
                        result.append({
                            "ast": {
                                "instruction": "SET",
                                "name": infos[0],
                                "x": infos[1],
                                "y": infos[2],
                                "color": infos[3],
                                "epaisseur": infos[4],
                            }
                        })
                    except Exception as e:
                        result.append({"error": f"Unexpected error in SET: {str(e)}"})

                elif instr[0] == "if":
                    #if(condition){...}
                    try:
                        condition = "".join(instr[instr.index("(")+1:instr.index(")")])
                        bod = tokens[count + 1]
                        result.append({
                            "ast": {
                                "instruction": "if",
                                "condition": condition,
                                "body": parseur(bod),
                            }
                        })
                    except Exception as e:
                        result.append({"error": f"Unexpected error in IF statement: {str(e)}"})

                elif instr[0] == "for":
                    #for i in range(a,b){...}
                    try:
                        param = "".join(instr[instr.index("(")+1:instr.index(")")]).split(",")
                        if len(param) != 2:
                            result.append({"error": "FOR requires exactly 2 parameters: start and end range."})
                            continue
                        body = tokens[count + 1]
                        result.append({
                            "ast": {
                                "instruction": "for",
                                "variable": instr[1],
                                "range": (param[0], param[1]),
                                "body": parseur(body),
                            }
                        })
                    except Exception as e:
                        result.append({"error": f"Unexpected error in FOR loop: {str(e)}"})

                elif instr[1] == "=":
                    #nom_var = value_var
                    try:
                        nom_var = instr[0]
                        value_var = "".join(instr[2:])
                        result.append({
                            "ast": {
                                "instruction": "ASSIGN",
                                "variable": nom_var,
                                "value": value_var
                            }
                        })
                    except Exception as e:
                        result.append({"error": f"Unexpected error in ASSIGNMENT: {str(e)}"})

                else:
                    result.append({"error": f"Unknown instruction: {instr[0]}"})

        except Exception as e:
            result.append({"error": f"General parsing error: {str(e)}"})
        count += 1
    return result
    