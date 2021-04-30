import time, itertools, copy, pprint
from trie_node import node
from prefix_trie import *

def print_board(board):

	for j in range(15):
		print('----', end = "")
	print()

	for i in range(15):
		print('|', end = "")
		for j in range(15):
			print(board[i][j], end = " | ")
		print()
		for j in range(15):
			print('----', end = "")
		print()


def initialize():
	start = time.time()
	insert_words("Collins Scrabble Words (2019).txt", prefix_trie)
	print("Time taken to insert words : ", time.time() - start)

def rotate(mat):
 
	N = 15
	# Transpose the matrix
	for i in range(N):
		for j in range(i):
			temp = mat[i][j]
			mat[i][j] = mat[j][i]
			mat[j][i] = temp
 
	# swap columns
	for i in range(N):
		for j in range(int(N/2)):
			temp = mat[i][j]
			mat[i][j] = mat[i][N - j - 1]
			mat[i][N - j - 1] = temp



def get_occupied_positions(board):

	arr = []
	for i in range(15):
		for j in range(15):
			if(board[i][j] != " "):
				arr.append((i, j))

	return arr


def get_word_on_top(board, start_point):

	x,y = start_point
	s = ""

	for i in range(x, -1, -1):
		if(board[i][y] == " "):
			break
		else:
			s  = board[i][y] + s

	return s

def get_word_on_bottom(board, start_point):

	x,y = start_point
	s = ""

	for i in range(x, 15):
		if(board[i][y] == " "):
			break
		else:
			s  = s + board[i][y]

	return s

def get_word_on_left(board, start_point):

	x,y = start_point
	s = ""

	for i in range(y, -1, -1):
		if(board[x][i] == " "):
			break
		else:
			s  = board[x][i] + s

	return s

def get_word_on_right(board, start_point):

	x,y = start_point
	s = ""

	for i in range(y, 15):
		if(board[x][i] == " "):
			break
		else:
			s  = s + board[x][i]

	return s


# The end point of 'main' word made is already on the board
def down(board, occupied_positions = None):

	if(occupied_positions == None):
		occupied_positions = get_occupied_positions(board)

	for position in occupied_positions:

		print(position)
		word_on_bottom = get_word_on_bottom( board, (position[0] + 1, position[1]) )

		temp = board[position[0]][position[1]] + word_on_bottom

		i = position[0]
		while( i >= 0 ):
		# for i in range(position[0]-1, max(topmost_starting - 1, -1) , -1):

			i = i - 1
			if(board[i][position[1]] != " "):
				break

			word_on_top = get_word_on_top(board, (i-1, position[1]))

			start_point = (i - len(word_on_top) , position[1])
			end_point = (position[0] + len(word_on_bottom), position[1])
			new_letters_add = (position[0] - i)
			total_word_len = len(word_on_top) + new_letters_add + len(word_on_bottom) + 1
			
			total_permutations = (itertools.permutations(tiles, position[0] - i))
			for perm in total_permutations:

				words_formed = []

				word = ""
				for char in perm:
					word = word + char

				word_formed = word_on_top + word + temp

				if(prefix_trie.check_word(word_formed)):
					words_formed.append(word_formed)
				else:
					continue

				# Checking for other words formed from left to right
				for pos in range(len(word_on_top) + start_point[0], position[0]):

					word_on_left =  get_word_on_left(board, (pos, position[1] - 1))
					word_on_right = get_word_on_right(board, (pos, position[1] + 1))

					if(len(word_on_left) == 0 and len(word_on_right) == 0):
						continue

					word_formed = word_on_left + word[pos - (len(word_on_top) + start_point[0])] + word_on_right
					if(prefix_trie.check_word(word_formed)):
						words_formed.append(word_formed)
					else:
						words_formed = []
						break

				if(len(words_formed) > 0):
					print("Starting point : ", start_point, " Ending point : ", end_point," New letters added : " ,new_letters_add, "Total word length : ",total_word_len)
					print(words_formed)


def up(board, occupied_positions = None):


	if(occupied_positions == None):
		occupied_positions = get_occupied_positions(board)

	for position in occupied_positions:

		new_col = position[1]
		first_letter_pos = (position[0]+1, position[1])

		word_on_top = get_word_on_top(board, (first_letter_pos[0] - 1, new_col))
		s = first_letter_pos[0] - 1
		while( s >= 0 and board[s][new_col] != " "):
			word_on_top =  board[s][new_col] + word_on_top
			s = s - 1

		start_point = (s + 1, new_col)

		max_length = 7
		for length in range(8):
			if( first_letter_pos[0] + length < 15 and board[first_letter_pos[0] + length][position[1]] != " "):
				max_length = length
				break

		for length in range(1, max_length + 1):

			word_on_bottom = ""
			s = first_letter_pos[0] + length
			while( s < 15 and board[s][new_col] != " "):
				word_on_bottom =  word_on_bottom + board[s][new_col]
				s = s + 1
			

			new_letters_add = length
			end_point = (s -1, new_col)
			total_word_len = len(word_on_top) + length + len(word_on_bottom)

			total_permutations = (itertools.permutations(tiles, length))
			for perm in total_permutations:

				words_formed = []
				word = ""
				for char in perm:
					word = word + char

				word_formed = word_on_top + word + word_on_bottom
				if(prefix_trie.check_word(word_formed)):
					words_formed.append(word_formed)
				else:
					continue


				for l in range(length):
					
					pos = first_letter_pos[0] + l 

					word_on_left = ""
					ind = new_col - 1
					while(ind > 0 and board[pos][ind] != " "):
						word_on_left = word_on_left + board[pos][ind]
						ind = ind - 1

					word_on_right = ""
					ind = new_col + 1
					while(ind < 15 and board[pos][ind] != " "):
						word_on_right = board[pos][ind] + word_on_right
						ind = ind + 1

					if(len(word_on_left) == 0 and len(word_on_right) == 0):
						continue

					word_formed = word_on_left + word[l] + word_on_right

					if(prefix_trie.check_word(word_formed)):
						words_formed.append(word_formed)
					else:
						words_formed = []
						break

				if(len(words_formed) > 0):
					print("Starting point : ", start_point, " Ending point : ", end_point," New letters added : " ,new_letters_add, "Total word length : ",total_word_len, max_length)
					print(words_formed)


# new end point of main word
def down_nep(board, occupied_positions = None):


	if(occupied_positions == None):
		occupied_positions = get_occupied_positions(board)


	# Putting new letter to the right
	for position in occupied_positions:

		cols = [position[1] + 1, position[1] - 1]
		for new_col in cols:

			for first_letter_row in range(0,7):

				first_letter_pos = (position[0] - first_letter_row , new_col)
				if(first_letter_pos[0] < 0):
					break

				word_on_top = get_word_on_top(board, (first_letter_pos[0] - 1 , new_col))
				s = first_letter_pos[0] - 1 -len(word_on_top)
				start_point = (s + 1, new_col)

				length = position[0] - first_letter_pos[0]
				while(length <= 7):

				# for length in range(, max_length + 1, 1):
					length = length + 1

					if( board[first_letter_pos[0] + length][new_col] != " "):
						break

					word_on_bottom = get_word_on_bottom(board, (first_letter_pos[0]+length, new_col))
					s = first_letter_pos[0] + length + len(word_on_bottom)
					new_letters_add = length
					end_point = (s - 1, new_col)
					total_word_len = len(word_on_top) + length + len(word_on_bottom)


					total_permutations = (itertools.permutations(tiles, length))
					for perm in total_permutations:

						words_formed = []
						word = ""
						for char in perm:
							word = word + char

						word_formed = word_on_top + word + word_on_bottom
						if(prefix_trie.check_word(word_formed)):
							words_formed.append(word_formed)
						else:
							continue


						for l in range(length):
							
							pos = first_letter_pos[0] + l 

							word_on_left = get_word_on_left(board, (pos, new_col - 1))
							word_on_right = get_word_on_right(board, (pos, new_col + 1))

							if(len(word_on_left) == 0 and len(word_on_right) == 0):
								continue

							word_formed = word_on_left + word[l] + word_on_right

							if(prefix_trie.check_word(word_formed)):
								words_formed.append(word_formed)
							else:
								words_formed = []
								break

						if(len(words_formed) > 0):
							print("Starting point : ", start_point, " Ending point : ", end_point," New letters added : " ,new_letters_add, "Total word length : ",total_word_len)
							print(words_formed)


def get_other_words(board, word, start_position, end_position, direction = 'Down'):

	length = end_position[0] - start_position[0] + 1

	if(start_position[1] != end_position[1]):
		print("Please give correct positions, ie in same col")
		return []

	arr = []
	for l in range(length):

		current_row = start_position[0] + l
		current_col = start_position[1]

		word_on_left = get_word_on_left(board, (current_row, current_col - 1))
		word_on_right = get_word_on_right(board, (current_row, current_col + 1))

		if(len(word_on_left) == 0 and len(word_on_right) == 0):
			continue

		word_formed = word_on_left + word[l] + word_on_right

		if(prefix_trie.check_word(word_formed)):
			arr.append([word_formed,(current_row, current_col - len(word_on_left)), (current_row , current_col + len(word_on_right))])
		else:
			return -1

	return arr


def get_words(board, position, min_length = 1, direction = 'Down'):

	occupied_positions = get_occupied_positions(board)
	x,y = position
	
	if(min_length == 0):
		return []

	# Checking if minimum possible length possible
	for length in range(min_length - 1):
		if(board[x + length][y] != " "):
			return 

	arr = []

	# first character at (x,y) and last character  at (x + l,y)
	# So total length is l + 1

	# Now minimum length possible, so generating till possible
	for length in range(min_length - 1, 7):

		if(board[x + length][y] != " "):
			return arr

		word_on_top    = get_word_on_top(board, (x - 1,y))
		word_on_bottom = get_word_on_bottom(board, (x + length + 1,y))

		permutations = (itertools.permutations(tiles, length + 1))

		for p in permutations:

			words_formed = []
			word = ""
			for char in p:
				word = word + char

			word_formed = word_on_top + word + word_on_bottom

			if(prefix_trie.check_word(word_formed)):
				words_formed.append([word_formed, (x, y), (x + length, y)])
			else:
				continue

			other_words = get_other_words(board, word, (x, y), (x + length, y))

			if(other_words == -1):
				continue

			words_formed.append(other_words)
			arr.append([words_formed])

	return arr

def get_down_all_words(board):

	occupied_positions = get_occupied_positions(board)

	words = []
	for x,y in occupied_positions:

		if(board[x+1][y] == " "):
			words.append(get_words(board, (x+1,y)))

		length = 1
		while( x-length > 0 and board[x-length][y] == " "):
			length = length + 1
			words.append(get_words(board, (x-length, y), length))

		for k in [1,-1]:

			new_col = y + k
			length = 0

			while( x-length > 0 and board[x-length][new_col] == " " and length < 7):
				length = length + 1
				words.append(get_words(board, (x-length, new_col), length + 1))


	return words

prefix_trie = node()

initialize()
board =  [[" " for x in range(15)] for y in range(15)]
tiles = ['g','r','a','o','n','o','r']

# board[3][7]  = 'a'

# board[2][7]  = 'a'
# board[4][7]  = 's'
# board[4][8]  = 'e'
# board[4][9]  = 't'


board[5][6]  = 't'
# board[6][6]  = 'e'
# board[6][8]  = 'n'
# board[5][8]  = 'x'
# board[14][8]  = 'y'
# board[7][7]  = 't' 
# board[7][8]  = 'b'
# board[8][7]  = 'f'
# board[11][7] = 't'
# board[11][8] = 'e'

position_points = [
		'T..d...T...d..T',
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
		'T..d...T...d..T'
	]

print_board(board)
# up(board)
# down_nep(board)
pprint.pprint(get_down_all_words(board))
# rotate(board)
# print_board(board)			
# down(board)