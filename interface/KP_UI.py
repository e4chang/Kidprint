#
# KP_UI.py
# An attempt to improve the UI of Project KP.
# 
# Author: Albert Tang
#

# general purpose strings
REGISTRATION_OR_IDENTIFICATION = \
"To register a new infant, enter '%s'.\n" \
"To identify a registered infant, enter '%s'.\n" \
"To quit the program, enter '%s'."
EXIT_STATEMENT = "Exiting."
IDENTIFICATION_USAGE = "This is the identification usage."
INVALID_OPTION = "Invalid option."

# strings used for registration interface
REG_GEN_USAGE = \
"Enter nothing to skip any question.\n"\
"To quit registration at any time, enter '%s'."
REG_USAGE = [
"Enter the name of the infant.",
"Enter the sex of the infant.",
"Enter the age of the infant in months.",
"Enter the location of the infant.",
"Enter the name of the mother.",
"Enter the name of the father.",
]
REG_FAILURE = "Infant was not registered."
REG_SUCCESS = "Infant successfully registered!"

# strings used for identification interface
ID_GEN_USAGE =\
"To quit identification at any time, enter '%s'."
ID_NAME_PROMPT =\
"Enter the name or ID of the infant you want to identify."
ID_SUCCESS =\
"%s successfully found!"
ID_FAILURE =\
"%s returned no results."
INFO_DISPLAY =\
"1. Name: %s\n"\
"2. Sex: %s\n"\
"3. Age: %s\n"\
"4. Location: %s\n"\
"5. Mother: %s\n"\
"6. Father: %s"
INFO_CHANGE_PROMPT = "Enter number of information to change."
INFO_CURRENT_CHANGE =\
"Current: %s\n"\
"Enter value to change it to."
INFO_CHANGE_SUCCESS = "Information successfully changed!"

# configurable strings
DB_FILENAME = "kpdb.txt"
REGISTER_OPTION = "r"
IDENTIFY_OPTION = "i"
QUIT_OPTION = "q"
USER_PROMPT = "> "

Global_Database = None

# Runs the interface to register a new infant in the database
def Register():
	quit = False	# determins what gets printed on return
	infant_info = [None]*len(REG_USAGE)
	info_index = 0

	# runs through list of information prompts and saves user input
	print REG_GEN_USAGE % QUIT_OPTION
	for USAGE_STRING in REG_USAGE:
		print USAGE_STRING
		user_input = raw_input(USER_PROMPT)
		# breaks out of loop if user enters quit
		if user_input == QUIT_OPTION:
			quit = True
			break
		elif user_input:
			infant_info[info_index] = user_input
		info_index += 1

	if quit:
		print REG_FAILURE
	else:
		print REG_SUCCESS

# Runs the interface to find and change an infant's information
def Identify():
	print ID_GEN_USAGE % QUIT_OPTION
	current_infant = None	# currently selected infant
	# Loops until an infant is found and selected
	while True:
		print ID_NAME_PROMPT
		user_input = raw_input(USER_PROMPT)
		if user_input == QUIT_OPTION:
			return

		# Attempt to find the infant in the database
		current_infant = SearchDatabase(user_input)
		if current_infant:
			print ID_SUCCESS % current_infant[0]
			break
		else:
			print ID_FAILURE % user_input
	
	# Loops until user quits
	while True:
		print INFO_DISPLAY % tuple(current_infant)
		print INFO_CHANGE_PROMPT
		user_input = raw_input(USER_PROMPT)
		if user_input == QUIT_OPTION:
			return
		else:
			# Attempt to access index value and change it
			try:
				index = int(user_input)-1
				print INFO_CURRENT_CHANGE % current_infant[index]
				user_input = raw_input(USER_PROMPT)
				if user_input == QUIT_OPTION:
					return
				else:
					current_infant[index] = user_input
					print INFO_CHANGE_SUCCESS 
			except:
				print INVALID_OPTION

# TODO
# Loads a database of infants from a file
def BuildDatabase():
	# with open(DB_FILENAME) as db:
	#	infant_info = [None]*len(REG_USAGE)
	print "Building database!"

# TODO
# Searches the database given credentials and returns info array
def SearchDatabase(credentials):
	return ["Jack", "M", "6", "Earth", "Jane", "John"]

# Main method -program starts here
if __name__ == "__main__":
	while True:
		print REGISTRATION_OR_IDENTIFICATION %\
			(REGISTER_OPTION, IDENTIFY_OPTION, QUIT_OPTION)
		option = raw_input(USER_PROMPT)
		if option == REGISTER_OPTION:
			Register()
		elif option == IDENTIFY_OPTION:
			Identify()
		elif option == QUIT_OPTION:
			print EXIT_STATEMENT
			break
		else:
			print INVALID_OPTION

