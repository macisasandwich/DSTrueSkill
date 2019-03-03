debug = False 
dataFile = None

def print_debug(msg):
	if debug:
		print(msg)

def require_input(msg):
	ans = None 

	while not ans:
		ans = input(msg)

		if not ans:
			print("Invalid input. Try again.")

	return ans
