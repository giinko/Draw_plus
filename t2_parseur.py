import re

def tokenize(code):

    

    tokens = re.findall(r'\w+|\d+|[^\w\s]', code) 

    return tokens


def parse(tokens):
    result = []
    while tokens:

        token = tokens.pop(0)

        if token == "DRAW":
            par1 = tokens.pop(0)
            forme = tokens.pop(0)
            par2 = tokens.pop(0)

            result.append({"ast": {
                    "instruction": "DRAW",
                    "shape": forme,
                }})

        elif token == "if":
            par1 = tokens.index"("
            par2 = tokens.index")"
            condition = "".join(tokens[par1+1:par2])
            guil1


    return result

code="DRAW(CIRCLE)"

tok = tokenize(code)

pars = parse(tok)

print(pars)

code = "if(x+2>4){DRAW (CIRCLE)}"

tok1 = tokenize(code)
print(tok1)