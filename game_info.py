
position_points = ['T..d...T...d..T',
					'.D...t...t...D.',
					'..D...d.d...D..',
					'd..D...d...D..d',
					'....D.....D....',
					'.t...t...t...t.',
					'..d...d.d...d..',
					'T..d...X...d..T',
					'..d...d.d...d..',
					'.t...t...t...t.',
					'....D.....D....',
					'd..D...d...D..d',
					'..D...d.d...D..',
					'.D...t...t...D.',
					'T..d...T...d..T']

tiles_available_at_start = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'd', 'd', 'd', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'f', 'f', 'g', 'g', 'g', 'h', 'h', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'j', 'k', 'l', 'l', 'l', 'l', 'm', 'm', 'n', 'n', 'n', 'n', 'n', 'n', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'p', 'p', 'q', 'r', 'r', 'r', 'r', 'r', 'r', 's', 's', 's', 's', 't', 't', 't', 't', 't', 't', 'u', 'u', 'u', 'u', 'v', 'v', 'w', 'w', 'x', 'y', 'y', 'z']
letter_values = {'a':1 , 'b':3, 'c':3, 'd':2, 'e':1, 'f':4, 'g':2, 'h':4, 'i':1, 'j':8, 'k':5, 'l':1, 'm':3, 'n':1, 'o':1, 'p':3, 'q':10, 'r':1, 's':1, 't':1, 'u':1, 'v':4, 'w':4, 'x':8, 'y':4, 'z':10}


ENDC = '\033[m' # reset to the defaults
RED  =  '\033[31m' # RED Text
BLUE =  '\033[34m' # BLUE Text
PURPLE  =  '\033[35m' # PURPLE Text
CYAN  =  '\033[36m' # CYAN Text
WHITE  =  '\033[47m' # WHITE Background



def print_board(board):

	for j in range(15):
		print('----', end = "")
	print()

	for i in range(15):

		print('| ', end = "")
		for j in range(15):

			if(board[i][j] == " " and position_points[i][j] == "T"):
				print(RED  + position_points[i][j], ENDC, end = "| ")
			elif(board[i][j] == " " and position_points[i][j] == "t"):
				print(BLUE  + position_points[i][j], ENDC, end = "| ")
			elif(board[i][j] == " " and position_points[i][j] == "d"):
				print(CYAN  + position_points[i][j], ENDC, end = "| ")
			elif(board[i][j] == " " and (position_points[i][j] == "D" or position_points[i][j] == "X")  ):
				print(PURPLE  + position_points[i][j], ENDC, end = "| ")
			else:
				
				print(board[i][j], end = " | ")

		print()
		for j in range(15):
			print('----', end = "")
		print()

def insert_words(file_name, trie, trie2 = None):

	with open(file_name,'r') as file:
	   
		for line in file:
			for word in line.split():
				trie.insert(word)


	if(trie2 != None):
		
		with open(file_name,'r') as file:
		   
			for line in file:
				for word in line.split():
					trie2.insert(word[::-1])


