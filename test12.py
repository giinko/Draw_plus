import re

def parse_instructions(code):

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

def parse(tokens, result=None):
    if result is None:
        result = []  # Initialisation de la liste au premier appel
    count = 0
    for instruction in tokens:
        if isinstance(instruction, str):

            instr = re.findall(r'\w+|\d+|[^\w\s]', instruction)

            if instr[0] == "DRAW":
                
                try :
                    forme = instr[2]
                    taille = instr[4]
                
                    result.append({
                        "ast" : {
                            "instruction" : "DRAW",
                            "FORM" : forme,
                            "TAILLE" : taille
                            }
                        })
                except:
                    print("erreur on verra apres")

            elif instr[0] == "MOOV":
                #Faire les checks d'erreur
                distance = "".join(instr[instr.index("(")+1:instr.index(")")])
                result.append({
                    "ast": {
                    "instruction": "MOOV",
                    "distance": distance,
                    }
                })

            elif instr[0] == "if":
                condition = "".join(instr[instr.index("(")+1:instr.index(")")])
                bod = tokens[count+1]
                result.append({
                    "ast": {
                        "instruction": "if",
                        "condition": condition,
                        "body": parse(bod),
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
                        "body": parse(bod),
                    }
                })

            elif instr[1] == "=":
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
    
        count += 1
    return result
    

tt = parse(["for i in range(2,4)",["if(5>4)",["DRAW(CIRCLE)"],"DRAW(CIRCLE)"],'DRAW(CIRCLE)', 'if(3>4)',['DRAW(CIRCLE)',"DRAW(CIRCLE)"]])


yes= parse(["DRAW(CIRCLE,50)"])

print(yes)

# Exemple d'utilisation avec la chaîne donnée
code = "DRAW(CIRCLE);DRAW(CIRCLE);if(3>4){if(5>4){DRAW(CIRCLE);} } DRAW(CIRCLE);for i in range(1,2){DRAW(CIRCLE);}"
parsed = parse_instructions(code)

ttt = parse(parsed)
#print(ttt)


