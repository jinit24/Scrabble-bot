import curses, time, itertools, random
from trie_node import *
from best_word import *
from user_moves import *

CH_P1 = 'X'
CH_P2 = 'O'
X_STEP = 4
Y_STEP = 2
X_OFFSET = 1
Y_OFFSET = 5
tiles_available = tiles_available_at_start
points = [0,0]
bingos = [0,0]
time_taken = [0,0]
moves_made = [0,0]


def initialise():
	
	print("You'll be playing as player 1. Please wait while the bot initializes.")

	prefix_trie = node()
	insert_words("Collins Scrabble Words (2019).txt", prefix_trie)

	tiles = [[],[]]
	board =  [[" " for x in range(15)] for y in range(15)]

	for i in range(2):

		s = random.sample(tiles_available  , 7)
		tiles[i].extend(s)

		for char in s:
			tiles_available.remove(char)


	return [board, prefix_trie, tiles]


def update_tiles(tiles, turn, new_chars, points_made):

	for char in new_chars:
		tiles[turn].remove(char)

	moves_made[turn] = moves_made[turn] + 1
	points[turn]     = points[turn]     + points_made

	if(len(new_chars) == 7):
		bingos[turn] = bingos[turn] + 1

	length = min(len(tiles_available), len(new_chars))

	if(length != 0):

		s = random.sample(tiles_available, length)
		tiles[turn].extend(s)

		for char in s:
			tiles_available.remove(char)

	if(length == 0):
		return -1

	return 1



def print_board(stdscr, board):

	stdscr.addstr(0, 0, 'Scrabble')
	stdscr.hline(1, 0, '-', 50)
	stdscr.addstr(2, 0, 'Use arrows to move, [ESC] Quit, [a-z] enter at position, [BACKSPACE] to remove character, [ENTER] play move, [SPACE] Skip turn')

	curses.use_default_colors()

	try:

		for j in range(15):
			stdscr.addstr(Y_OFFSET-1, X_OFFSET + j*X_STEP, "-----")

		for i in range(15):
			
			stdscr.addstr(Y_OFFSET + i*2, X_OFFSET, "| ")

			for j in range(15):
				stdscr.addstr(Y_OFFSET + 2*i+1, X_OFFSET + j*X_STEP, "-----")


			for j in range(15):

				if(board[i][j] == " " and position_points[i][j] == "T"):

					curses.init_pair(1, curses.COLOR_RED, -1)
					stdscr.addstr(Y_OFFSET + Y_STEP*i, X_OFFSET + j*X_STEP + 2, position_points[i][j], curses.color_pair(1))
					stdscr.addstr(Y_OFFSET + Y_STEP*i, X_OFFSET + j*X_STEP + 2 + 1, " | ")

				elif(board[i][j] == " " and position_points[i][j] == "t"):

					curses.init_pair(2, curses.COLOR_BLUE, -1)
					stdscr.addstr(Y_OFFSET + Y_STEP*i, X_OFFSET + j*X_STEP + 2, position_points[i][j], curses.color_pair(2))
					stdscr.addstr(Y_OFFSET + Y_STEP*i, X_OFFSET + j*X_STEP + 2 + 1, " | ")

				elif(board[i][j] == " " and position_points[i][j] == "d"):

					curses.init_pair(3, curses.COLOR_CYAN, -1)
					stdscr.addstr(Y_OFFSET + Y_STEP*i, X_OFFSET + j*X_STEP + 2, position_points[i][j], curses.color_pair(3))
					stdscr.addstr(Y_OFFSET + Y_STEP*i, X_OFFSET + j*X_STEP + 2 + 1, " | ")

				elif(board[i][j] == " " and (position_points[i][j] == "D" or position_points[i][j] == "X")  ):

					curses.init_pair(4, curses.COLOR_MAGENTA, -1)
					stdscr.addstr(Y_OFFSET + Y_STEP*i, X_OFFSET + j*X_STEP + 2, position_points[i][j], curses.color_pair(4))
					stdscr.addstr(Y_OFFSET + Y_STEP*i, X_OFFSET + j*X_STEP + 2 + 1, " | ")

				else:
					stdscr.addstr(Y_OFFSET + Y_STEP*i, X_OFFSET + j*X_STEP + 2, str(board[i][j] + " |"))

	except Exception as e:
		raise Exception("Please use the terminal in full screen.") 


def print_tiles(stdscr, tiles, user):

	stdscr.addstr(Y_OFFSET, X_OFFSET + 65, "Your Tiles : ")
	stdscr.addstr(Y_OFFSET, X_OFFSET + 80, "[")

	for j in range(len(tiles[user])):
		stdscr.addstr(Y_OFFSET, X_OFFSET + (j+1)*X_STEP + 80, tiles[user][j])
	
	stdscr.addstr(Y_OFFSET, X_OFFSET + 8*X_STEP + 80, "]")

	stdscr.addstr(Y_OFFSET+2, X_OFFSET + 80, "     Your Scrore     |     Computer's Score     ")
	stdscr.addstr(Y_OFFSET+3, X_OFFSET + 80, "       " + str(points[user])     + "            ")
	stdscr.addstr(Y_OFFSET+3, X_OFFSET + 102,"       " + str(points[1 - user]) + "            ")


def user_move(stdscr, prefix_trie, board, new_char_pos, first_move, user, tiles):

	new_char_pos = list(set(new_char_pos))
	x = check_word_new_pos(prefix_trie, board, tiles[user], new_char_pos, first_move)

	stdscr.addstr(Y_OFFSET + 6, X_OFFSET + 70, " "*55)

	if(x[0] == -1):
		
		for i in new_char_pos:
			board[i[0]][i[1]] = " "

		print_board(stdscr, board)
		print_tiles(stdscr, tiles, user)

		stdscr.addstr(Y_OFFSET + 6, X_OFFSET + 70, x[1][:55])

		return -1

	stdscr.addstr(Y_OFFSET + 5, X_OFFSET + 70, "Points added : " + str(x[1]))
	update_tiles(tiles, user, x[2], x[1])

	return 1


def bot_move(stdscr, prefix_trie, board, first_move, bot, tiles):

	x = get_best_word(prefix_trie, board, tiles[bot])
	stdscr.addstr(Y_OFFSET + 5, X_OFFSET + 70, " "*50)

	if(x[1] == -1):
		return -1

	stdscr.addstr(Y_OFFSET + 5, X_OFFSET + 70, "Move made by computer : " + str(x[0][0]) + " for " + str(x[1]) + " points")

	if(x[2][0] == x[3][0]):
		play_word(prefix_trie, board, tiles[bot], x[0][0], x[2], "right", first_move)
	else:
		play_word(prefix_trie, board, tiles[bot], x[0][0], x[2], "down", first_move)

	
	update_tiles(tiles, bot, x[4], x[1])

	print_board(stdscr, board)
	print_tiles(stdscr, tiles, 1 - bot)



def main(stdscr):

	user = 0
	bot  = 1
	turn = 0

	board, prefix_trie, tiles = initialise()
	print_board(stdscr, board)
	print_tiles(stdscr, tiles, user)

	x_pos = 0
	y_pos = 0
	new_char_pos = []
	first_move = 1

	while True:

		stdscr.move(Y_OFFSET + y_pos * Y_STEP, X_OFFSET + x_pos * X_STEP + 2)

		c = stdscr.getch()
		if c == curses.KEY_UP:
			y_pos = max(0, y_pos - 1)
		elif c == curses.KEY_DOWN:
			y_pos = min(14, y_pos + 1)
		elif c == curses.KEY_LEFT:
			x_pos = max(0, x_pos - 1)
		elif c == curses.KEY_RIGHT:
			x_pos = min(14, x_pos + 1)

		elif c == ord(' ') and len(new_char_pos) == 0:
			y = bot_move(stdscr, prefix_trie, board, first_move, bot, tiles)

			if(y == -1):
				break

			new_char_pos = []

		elif c == 27:
			break
		elif c == curses.KEY_BACKSPACE and ((y_pos, x_pos, board[y_pos][x_pos]) in new_char_pos):

			new_char_pos.remove( (y_pos, x_pos, board[y_pos][x_pos]) )
			board[y_pos][x_pos] = " "
			y, x = stdscr.getyx()
			stdscr.addstr(y,x, " ")

		elif c >= ord('a') and c <= ord('z') and board[y_pos][x_pos] == " ":

			y, x = stdscr.getyx()
			stdscr.addstr(y,x, chr(c))
			# stdscr.addstr(Y_OFFSET + 14, X_OFFSET + 93, str(first_move))
			# stdscr.addstr(Y_OFFSET + 14, X_OFFSET + 93, str(y_pos))
			# stdscr.addstr(Y_OFFSET + 14, X_OFFSET + 96, str(x_pos))
			# stdscr.addstr(Y_OFFSET + 14, X_OFFSET + 99, chr(c))

			board[y_pos][x_pos] = chr(c)
			new_char_pos.append( (y_pos, x_pos, chr(c)) )

		elif c == curses.KEY_ENTER or c == 10 or c == 13:

			x = user_move(stdscr, prefix_trie, board, new_char_pos, first_move, user, tiles)

			if(x == -1):
				new_char_pos = []
				continue

			first_move = 0

			if(len(tiles[user]) == 0):
				break

			y = bot_move(stdscr, prefix_trie, board, first_move, bot, tiles)

			if(y == -1):
				break

			new_char_pos = []



	stdscr.erase()
	stdscr.addstr(Y_OFFSET + 9, X_OFFSET + 50,"                            User            Bot              ")
	stdscr.addstr(Y_OFFSET + 10, X_OFFSET + 50," Points                      " + str(points[0]) +  "               "+ str(points[1]) +"           ")
	stdscr.addstr(Y_OFFSET + 11, X_OFFSET + 50," Bingos                      " + str(bingos[0]) +  "               "+ str(bingos[1]) +"           ")
	stdscr.addstr(Y_OFFSET + 12, X_OFFSET + 50," Moves                       " + str(moves_made[0]) +  "               "+ str(moves_made[1]) +"           ")
	stdscr.addstr(Y_OFFSET + 20, X_OFFSET + 50," Press any key to exit.")
	c = stdscr.getch()

if __name__ == '__main__':
	curses.wrapper(main)
