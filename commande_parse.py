def commande_parse(command, cursor):
	instruction = command.split()
	action = instruction[0]
	if(action == "MOOVE"):
		#On récupe les données selon la grammaire 
		print("On se déplace")