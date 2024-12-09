def commande_parse(command, cursor):
	instruction = command.split()
	action = instruction[0]
	if(action == "MOOVE"):
		#Get data based on grammar
		print("On se déplace")