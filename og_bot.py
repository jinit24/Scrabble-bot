import time, itertools, copy
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


# The end point of 'main' word made is already on the board
def down(board, occupied_positions = None):

	if(occupied_positions == None):

		occupied_positions = []
		for i in range(15):
			for j in range(15):
				if(board[i][j] != " "):
					occupied_positions.append((i, j))



	for position in occupied_positions:

		word_on_bottom = ""
		for i in range(position[0]+1,15):
			if(board[i][position[1]] == " "):
				break
			else:
				word_on_bottom  = word_on_bottom + board[i][position[1]]


		topmost_starting = position[0]
		for i in range(1,8):
			if(board[position[0] - i][position[1]] != " "):
				break
			topmost_starting = position[0] - i


		temp = board[position[0]][position[1]] + word_on_bottom

		for i in range(position[0]-1, topmost_starting -1 , -1):

			if(board[i][position[1]] != " "):
				print("Already coverred case.")
				break

			word_on_top = ""
			s = copy.deepcopy(i-1)	
			while( s>=0 and board[s][position[1]] != " "):
				word_on_top =  board[s][position[1]] + word_on_top
				s = s - 1


			start_point = (s + 1, position[1])
			end_point = (position[0] + len(word_on_bottom), position[1])
			new_letters_add = (position[0] - i)
			total_word_len = len(word_on_top) + new_letters_add + len(word_on_bottom) + 1
			
			total_permutations = (itertools.permutations(tiles, position[0] - i))
			for perm in total_permutations:

				words_formed = []
				word = ""
				for char in perm:
					word = word + char

				if(prefix_trie.check_word(word_on_top + word + temp)):
					# print(word_on_top + word + temp, end = " ")
					words_formed.append(word_on_top + word + temp)
				else:
					continue

				# Checking for other words formed from left to right

				for pos in range(len(word_on_top) + start_point[0], position[0]):

					word_on_left = ""
					ind = position[1] - 1
					while(ind > 0 and board[pos][ind] != " "):
						word_on_left = word_on_left + board[pos][ind]
						ind = ind - 1

					word_on_right = ""
					ind = position[1] + 1
					while(ind < 15 and board[pos][ind] != " "):
						word_on_right = board[pos][ind] + word_on_right
						ind = ind + 1

					if(len(word_on_left) == 0 and len(word_on_right) == 0):
						continue

					word_formed = word_on_left + word[pos - (len(word_on_top) + start_point[0])] + word_on_right
					# if(prefix_trie.check_word(word_formed)):
						# print(word_formed, end = " ")
					words_formed.append(word_formed)

				if(len(words_formed) > 0):
					print("Starting point : ", start_point, " Ending point : ", end_point," New letters added : " ,new_letters_add, "Total word length : ",total_word_len)
					print(words_formed)


def up(board, occupied_positions = None):


	if(occupied_positions == None):

		occupied_positions = []
		for i in range(15):
			for j in range(15):
				if(board[i][j] != " "):
					occupied_positions.append((i, j))



	for position in occupied_positions:

		new_col = position[1]
		first_letter_pos = (position[0]+1, position[1])

		word_on_top = ""
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

		occupied_positions = []
		for i in range(15):
			for j in range(15):
				if(board[i][j] != " "):
					occupied_positions.append((i, j))


	# Putting new letter to the right
	for position in occupied_positions:

		cols = [position[1] + 1, position[1] - 1]
		for new_col in cols:

			for first_letter_position in range(0,7):

				first_letter_pos = (position[0] - first_letter_position , new_col)

				word_on_top = ""
				s = first_letter_pos[0] - 1
				while( s >= 0 and board[s][new_col] != " "):
					word_on_top =  board[s][new_col] + word_on_top
					s = s - 1

				start_point = (s + 1, new_col)
				if(start_point[0] < 0):
					break

				max_length = 7
				for length in range(8):
					if( first_letter_pos[0] + length < 15 and board[first_letter_pos[0] + length][new_col] != " "):
						max_length = length
						break

				for length in range(position[0] - first_letter_pos[0] + 1, max_length + 1, 1):

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




prefix_trie = node()

initialize()
board =  [[" " for x in range(15)] for y in range(15)]
tiles = ['g','r','a','o','m','o','r']

board[3][7]  = 'a'
board[4][7]  = 's'
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
down_nep(board)
# down(board)
# rotate(board)
# print_board(board)			
# down(board)