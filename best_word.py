import time, itertools, random
from game_info import *
from trie_node import *

def rotate_clockwise(mat):
 
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

def rotate_anti_clockwise(mat):
	 
	N = 15
	for x in range(0, int(N / 2)):
		 
		for y in range(x, N-x-1):
			 
			temp = mat[x][y]
			mat[x][y] = mat[y][N-1-x]
			mat[y][N-1-x] = mat[N-1-x][N-1-y]
			mat[N-1-x][N-1-y] = mat[N-1-y][x]
			mat[N-1-y][x] = temp

def flip_about_col(arr):
 
	N = 15

	for i in range(N):
		arr[i] = arr[i][::-1]


def og_points(point):

	x,y = point
	return (y, x)


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

def get_points(start_position, end_position, word, new_char_pos = None, direction = 'down'):

	letter_value = letter_values

	points = 0
	new_chars = []

	for char in word:
		points = points + letter_value[char]

	k = 0
	if(direction == "right"):
		k = 1

	for pos in new_char_pos:

		val = position_points[pos[0]][pos[1]]
		new_char = word[pos[k] - start_position[k]]
		new_chars.append(new_char)

		if(val == 'd'):
			points = points + letter_value[new_char]

		elif(val == 't'):
			points = points +  2 * letter_value[new_char]

		elif(val == 'D' or val == 'X'):
			points = 2 * points

		elif(val == 'T'):
			points = 3 * points


	if(len(new_char_pos) == 7):
		points = points + 50

	return [points, new_chars]

def get_other_words(prefix_trie, board, word, start_position, end_position, old_character_pos = [], direction = 'down'):

	length = end_position[0] - start_position[0] + 1

	if(start_position[1] != end_position[1]):
		print("Please give correct positions, ie in same col")
		return []

	arr = []
	points = 0
	for l in range(length):

		if(l in old_character_pos):
			continue

		current_row = start_position[0] + l
		current_col = start_position[1]

		word_on_left = get_word_on_left(board, (current_row, current_col - 1))
		word_on_right = get_word_on_right(board, (current_row, current_col + 1))

		if(len(word_on_left) == 0 and len(word_on_right) == 0):
			continue

		word_formed = word_on_left + word[l] + word_on_right

		if(prefix_trie.check_word(word_formed)):

			s_position = (current_row, current_col - len(word_on_left))
			e_position = (current_row , current_col + len(word_on_right))

			p = get_points(s_position, e_position, word_formed, new_char_pos = [(current_row, current_col)], direction = "right")
			arr.append(word_formed)
			points = points + p[0]
			
		else:
			return -1

	if(len(arr) == 0):
		return 0

	return [arr, points]

def get_separated_words(prefix_trie, board, tiles):

	occupied_positions = get_occupied_positions(board)
	best_word = ["", -1, (-1,-1), (-1,-1),-1]

	for pos in occupied_positions:

		if(board[pos[0]-1][pos[1]] != " "):
			# print("Already covered", pos)
			continue

		col = pos[1]
		word_on_top = get_word_on_top(board, (pos[0]-1, col))
		word_on_bottom = get_word_on_bottom(board, (pos[0]+1, col))

		word_on_board = word_on_top + board[pos[0]][pos[1]] + word_on_bottom

		free_distance_on_top = 0
		row = pos[0] - len(word_on_top) - 1

		while(row >= 0 and board[row][col] == " "):
			free_distance_on_top = free_distance_on_top + 1
			row = row - 1

		free_distance_on_bottom = 0
		row = pos[0] + len(word_on_bottom) + 1

		while(row < 15 and board[row][col] == " "):
			free_distance_on_bottom = free_distance_on_bottom + 1
			row = row + 1

		free_distance_on_top = min(free_distance_on_top, 7)
		free_distance_on_bottom = min(free_distance_on_bottom, 7)

		# print(word_on_board, free_distance_on_top, free_distance_on_bottom, pos)


		for len_top in range(1, free_distance_on_top + 1):

			cx, cy = pos[0]-len_top, col
			word_on_top = get_word_on_top(board, (cx-1,cy))

			new_letters_added = 0
			word_formed = ""

			while(new_letters_added < len(tiles) and cx < 15):
				
				if(board[cx][cy] == " "):
					word_formed = word_formed + "*"
					new_letters_added = new_letters_added + 1
				else:
					word_formed = word_formed + board[cx][cy]

				cx = cx + 1


			dicts = {}
			for x in tiles:
				dicts[x] = 0

			for x in tiles:
				dicts[x] = dicts[x] + 1

			final_word  = word_on_top + word_formed
			words_possible = traverse_word(prefix_trie, final_word, dicts)
			words_possible = [item for item in words_possible if len(item) >= len_top]

			for w in words_possible:

				new_char_pos = []
				old_character_pos = []

				for i in range(len(w)):
					if(final_word[i] == "*"):
						new_char_pos.append((pos[0] - len_top - len(word_on_top) + i,cy))
					else:
						old_character_pos.append(i)

				if(len(new_char_pos) == 0):
					continue

				s_position = (pos[0]- len_top - len(word_on_top),cy)
				e_position = (s_position[0] + len(w) - 1,cy)

				main_points = get_points(s_position, e_position, w, new_char_pos = new_char_pos)

				extra = get_other_words(prefix_trie, board, w, s_position, e_position, old_character_pos = old_character_pos)

				if(extra == -1):
					continue

				elif(extra == 0):
					if(main_points[0] > best_word[1]):
						# best_word = [[w], main_points, (pos[0] - len_top,pos[1]), (e_position)]
						best_word = [[w], main_points[0], s_position, (e_position), main_points[1]]


				elif(main_points[0] + extra[1] > best_word[1]):
					# best_word = [[w,extra[0]], main_points + extra[1], (pos[0] - len_top,pos[1]), (e_position)]
					best_word = [[w,extra[0]], main_points[0] + extra[1], s_position, (e_position), main_points[1]]

				# print(main_points, final_word, w, s_position, e_position, extra, new_char_pos)

	return best_word

def get_words(prefix_trie, board, position, tiles, min_length = 1, direction = 'down'):

	occupied_positions = get_occupied_positions(board)
	x,y = position
	best_word = ["", -1, (-1,-1), (-1,-1),-1]
	
	if(min_length == 0):
		return best_word

	# Checking if minimum possible length possible
	for length in range(min_length - 1):
		if(board[x + length][y] != " "):
			return best_word

	arr = []

	# first character at (x,y) and last character  at (x + l,y)
	# So total length is l + 1

	for length in range(min_length - 1, 7):

		if(x+length == 15 or board[x + length][y] != " "):
			return best_word

		word_on_top    = get_word_on_top(board, (x - 1,y))
		word_on_bottom = get_word_on_bottom(board, (x + length + 1,y))
		permutations   = itertools.permutations(tiles, length + 1)

		for p in permutations:

			words_formed = []
			word = ""
			for char in p:
				word = word + char

			word_formed = word_on_top + word + word_on_bottom

			if(prefix_trie.check_word(word_formed)):

				start_position = (x - len(word_on_top), y)
				end_position   = (x + length + len(word_on_bottom), y)

				new_char_start = (x, y)
				new_char_end = (x + length, y)

				new_char_pos = []
				for a in range(length+1):
					new_char_pos.append((x+a,y))

				main_points = get_points(start_position, end_position, word_formed, new_char_pos = new_char_pos)
				# words_formed.append([word_formed, (x - len(word_on_top), y), (x + length + len(word_on_bottom), y), p])
			else:
				continue

			# other_words = get_other_words(board, word, (x, y), (x + length, y))
			extra = get_other_words(prefix_trie, board, word, (x, y), (x + length, y))

			if(extra == -1):
				continue

			elif(extra == 0):
				if(main_points [0]> best_word[1]):
					# best_word = [[word_formed], main_points, new_char_start, new_char_end]
					best_word = [[word_formed], main_points[0], start_position, end_position, main_points[1]]

			elif(main_points[0] + extra[1] > best_word[1]):
				# best_word = [[word_formed,extra[0]], main_points + extra[1], new_char_start, new_char_end]
				best_word = [[word_formed,extra[0]], main_points[0] + extra[1], start_position, end_position, main_points[1]]


			# words_formed.append(other_words)
			# arr.append([words_formed])

	# return arr
	return best_word

def get_down_all_words(prefix_trie, board, tiles):

	occupied_positions = get_occupied_positions(board)

	words = []
	best_word = ["", -1, (-1,-1), (-1,-1),-1]

	if(len(occupied_positions) == 0):

		length = 1
		while( 7-length > 0 and board[7-length][7] == " "):
			length = length + 1
			# words.append(get_words(board, (x-length, y), length))
			word = get_words(prefix_trie, board,  (8-length, 7), tiles,length)
			if(word[1] > best_word[1]):
				best_word = word

		return best_word

	for x,y in occupied_positions:

		if( x < 14 and board[x+1][y] == " "):
			# words.append(get_words(board, (x+1,y)))
			word = get_words(prefix_trie, board, (x+1,y), tiles)
			if(word[1] > best_word[1]):
				best_word = word

		length = 1
		while( x-length > 0 and board[x-length][y] == " "):
			length = length + 1
			# words.append(get_words(board, (x-length, y), length))
			word = get_words(prefix_trie, board, (x-length, y), tiles, length)
			if(word[1] > best_word[1]):
				best_word = word

		for k in [1,-1]:

			new_col = y + k
			if(new_col == 15 or new_col == -1):
				continue

			length = 0

			while( x-length > 0 and board[x-length][new_col] == " " and length < 7):
				length = length + 1
				# words.append(get_words(board, (x-length, new_col), length + 1))
				word = get_words(prefix_trie, board, (x-length, new_col), tiles, length + 1)
				if(word[1] > best_word[1]):
					best_word = word


	word = get_separated_words(prefix_trie, board, tiles)
	if(word[1] > best_word[1]):
		best_word = word

	# return words
	return best_word


def get_best_word(prefix_trie, board, tiles):

	best = get_down_all_words(prefix_trie, board, tiles)

	rotate_clockwise(board)
	flip_about_col(board)

	X = get_down_all_words(prefix_trie, board, tiles)

	flip_about_col(board)
	rotate_anti_clockwise(board)

	if(X[1] > best[1]):
		return [X[0],X[1],og_points(X[2]),og_points(X[3]), X[4]]

	return best
