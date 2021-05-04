from best_word import *
from collections import defaultdict

def check_word(prefix_trie, board, tiles, word, start_position, direction, first_move):

	row,col = start_position[0], start_position[1]

	direction = direction.lower()
	new_char_pos = []
	old_character_pos = []

	if(direction != 'down' and direction != 'right'):
		print("Specify correct direction. ")
		return - 1

	dicts = defaultdict(lambda: 0)
	for i in  tiles:
		dicts[i] = dicts[i] + 1

	words = defaultdict(lambda: 0)
	for i in  word:
		words[i] = words[i] + 1

	attached = 0
	i = 0 
	for char in word:

		if(board[row][col] !=  " " and board[row][col] !=  char):
			print(word, "cannot be placed on the board")
			return -1

		elif(board[row][col] !=  " " and board[row][col] ==  char):
			attached = 1
			old_character_pos.append(i)

			# NEW CHANGE
			words[char] = words[char] - 1


		if(direction == 'down'):
			row = row + 1
		else:
			col = col + 1

		i = i + 1


	row,col = start_position[0], start_position[1]
	i = 0 

	for char in word:

		if(board[row][col] == " " ):

			if(dicts[char] < words[char] or dicts[char] == 0):
				print( "is used more than the times present in tiles", char)
				return -1
			
			new_char_pos.append((i + start_position[0], start_position[1]))

		if(direction == 'down'):
			row = row + 1
		else:
			col = col + 1
			
		i = i + 1

	if(not prefix_trie.check_word(word)):
		print(word, "is not a valid scrabble word. ")
		return -1


	end_position = (start_position[0] + len(word) - 1, start_position[1])

	other_words = get_other_words(prefix_trie, board, word, start_position, end_position, old_character_pos, direction)

	if(other_words == 0 and attached == 0 and first_move != 1):
		print("Not connected to any word present on board")
		return -1

	if(other_words == -1):
		print("Invalid word formed other than ", word)
		return -1

	[p, chars] = get_points(start_position, None, word, new_char_pos, direction)

	# print("New char", new_char_pos)

	if(other_words == 0):
		return [word, p, chars]

	p = p + other_words[1]

	return [[word, other_words[0]], p, chars]



def undo_rotation(board, new_char_pos, direction):

	if(direction == 'right'):
		flip_about_col(board)
		rotate_anti_clockwise(board)

		for i in range(len(new_char_pos)):
			(x,y,a) = new_char_pos[i]
			new_char_pos[i] = (y,x,a)

	return board, new_char_pos

def check_word_new_pos(prefix_trie, board, tiles, new_char_pos,first_move):

	if(len(new_char_pos) == 0):
		return [-1, "Error! No word entered!"]

	old_character_pos = []

	new_char_pos.sort()
	cx,cy = 0,0
	for i in new_char_pos:
		if(i[0] == new_char_pos[0][0]):
			cx = cx + 1
		if(i[1] == new_char_pos[0][1]):
			cy = cy + 1

	rows, cols = (new_char_pos[0][0], new_char_pos[0][1])
	rowe, cole = (new_char_pos[len(new_char_pos)-1][0], new_char_pos[len(new_char_pos)-1][1])

	if( cx != len(new_char_pos) and cy != len(new_char_pos)):
		return [-1, "Error! Please place all the tiles in one line. "]

	direction = 'down'
	if(cx == len(new_char_pos) and len(new_char_pos) != 1):

		direction = 'right'
		rotate_clockwise(board)
		flip_about_col(board)

		for i in range(len(new_char_pos)):
			(x,y,a) = new_char_pos[i]
			new_char_pos[i] = (y,x,a)
	
		new_char_pos.sort()
		rows, cols = (new_char_pos[0][0], new_char_pos[0][1])
		rowe, cole = (new_char_pos[len(new_char_pos)-1][0], new_char_pos[len(new_char_pos)-1][1])


	word = ""
	x,y = rows, cols

	i = 0
	while(x != rowe+1):
		word = word + (board[x][y])
		x = x + 1
		i = i + 1

	dicts = defaultdict(lambda: 0)
	for i in  tiles:
		dicts[i] = dicts[i] + 1

	words = defaultdict(lambda: 0)
	for i in  word:
		words[i] = words[i] + 1


	row, col = rows, cols
	attached = 0


	word_on_top    = get_word_on_top(board, (rows-1, cols))
	word_on_bottom = get_word_on_bottom(board, (rowe+1, cole))
	word_formed = word_on_top + word + word_on_bottom


	x,y = rows - len(word_on_top), cols
	for i in range(len(word_formed)):

		char = board[x][y]

		if((x, y,char) not in new_char_pos):
			old_character_pos.append(i)

		elif(dicts[char] < words[char] or dicts[char] == 0):
			board, new_char_pos = undo_rotation(board, new_char_pos, direction)
			return [-1, "Error! Please use the letters given on your tiles : " + char]

		x = x + 1

	if(len(old_character_pos)>0):
		attached = 1


	if(not prefix_trie.check_word(word_formed) and len(word_formed) > 1):
		board, new_char_pos = undo_rotation(board, new_char_pos, direction)
		return [-1, ("Error! " + word_formed + " is not a valid scrabble word. "), rows,cols, rowe, cole, word_on_top, word_on_bottom]

	end_position = (rows + len(word) + len(word_on_bottom) - 1, cols)
	other_words = get_other_words(prefix_trie, board, word_formed, (rows - len(word_on_top), cols), end_position, old_character_pos, direction = "down")



	if(len(word_on_top) > 0 or len(word_on_bottom) > 0):
		attached = 1

	if(other_words == 0 and attached == 0 and first_move != 1):
		board, new_char_pos = undo_rotation(board, new_char_pos, direction)
		return [-1, ("Error! Not connected to any word present on board")]

	if(other_words == -1):
		board, new_char_pos = undo_rotation(board, new_char_pos, direction)
		return [-1, "Error! Invalid word formed"]

	new_char = []
	for x,y,a in new_char_pos:
		new_char.append((x,y))

	[p, chars] = get_points((rows - len(word_on_top), cols), None, word_formed, new_char, direction = "down")

	if(other_words == 0):
		undo_rotation(board, new_char_pos, direction)
		return [word_formed, p, chars]

	p = p + other_words[1]

	board, new_char_pos = undo_rotation(board, new_char_pos, direction)
	return [[word_formed, other_words[0]], p, chars]

# def play_word_new_pos(prefix_trie, board, tiles, new_char_pos,first_move):


# def check_word_curses(prefix_trie, board, tiles, new_char_pos, old_character_pos, first_move):
# 



def play_word(prefix_trie, board, tiles, word, start_position, direction, first_move):
	
	row = start_position[0]
	col = start_position[1]

	direction = direction.lower()

	if(direction == "right"):
		rotate_clockwise(board)
		flip_about_col(board)
		row, col = col ,row

	info = check_word(prefix_trie, board, tiles, word, (row, col), 'down', first_move)

	if(direction == "right"):

		flip_about_col(board)
		rotate_anti_clockwise(board)
		row, col = col ,row

		# print(info)
		# for x,y in info[2]:
		# 	x,y = y,x


	if(info == -1):
		return -1


	for char in word:

		board[row][col] = char
		if(direction == 'down'):
			row = row + 1
		else:
			col = col + 1

	return info