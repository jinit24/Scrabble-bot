import time, itertools, random
from trie_node import *
from best_word import *
from user_moves import *

def initialise():
	
	start = time.time()
	board =  [[" " for x in range(15)] for y in range(15)]
	prefix_trie = node()

	insert_words("Collins Scrabble Words (2019).txt", prefix_trie)
	print("Time taken to insert words : ", time.time() - start)

	return [board, prefix_trie]

def get_best_word(board, tiles):

	best = get_down_all_words(prefix_trie, board, tiles)

	rotate_clockwise(board)
	flip_about_col(board)

	X = get_down_all_words(prefix_trie, board, tiles)

	flip_about_col(board)
	rotate_anti_clockwise(board)

	if(X[1] > best[1]):
		return [X[0],X[1],og_points(X[2]),og_points(X[3]), X[4]]

	return best


board, prefix_trie = initialise()
print("Scrabble-bot> Enter 1 to player 1 else enter 2 : ", end = "")


points = [0,0]
bingos = [0,0]
time_taken = [0,0]
moves_made = [0,0]

user = 0
bot  = 1

line = input().split()
if(line[0]=="2"):
	user = 1
	bot = 0

turn = 0
tiles_available = tiles_available_at_start
tiles = [[],[]]
first_move = 1

for i in range(2):

	s = random.sample(tiles_available, 7)
	tiles[i].extend(s)

	for char in s:
		tiles_available.remove(char)

print("Your tiles : ", tiles[user])

while(1):

	print("Scrabble-bot> ", end = "")
	line = input().split()

	if(len(line) == 0):
		print("Error : Please enter a command.")
	if(line[0].lower() =='show' or line[0].lower() =='print'):

		if(len(line)<2):
			print("Syntax error! Specify board or tiles.")
			continue

		if(line[1].lower() == 'board'):
			print_board(board)
		elif(line[1].lower() == 'tiles'):
			print(tiles[user])
		else:
			print("Syntax error! Specify board or tiles.")
			continue

	if(line[0].lower() == 'play'):

		if(len(line) != 5):
			print("Syntax error! Eg : play 'word' at 6,9 right")
			continue

		word            = line[1]
		start_position  = line[3].split(',')
		start_position  = int(start_position[0]),int(start_position[1])
		direction       = line[4]

		x = play_word(prefix_trie, board, tiles[user], word, start_position, direction, first_move)

		if(x == -1):
			continue

		for char in x[2]:
			tiles[user].remove(char)

		moves_made[user] = moves_made[user] + 1
		length = min(len(tiles_available), len(x[2]))
		if(length != 0):
			s = random.sample(tiles_available, length)
			tiles[user].extend(s)

			for char in s:
				tiles_available.remove(char)

		points[bot] = points[bot] + x[1]

		first_move = 0
		x = get_best_word(board, tiles[bot])
		print("Move made is : ", x[0], " starting at : ", x[2], " points gained : ", x[1])

		if(x[1] == -1):
			print("No word possible")
			break

		if(x[2][0] == x[3][0]):
			play_word(prefix_trie, board, tiles[bot], x[0][0], x[2], "right", first_move)
		else:
			play_word(prefix_trie, board, tiles[bot], x[0][0], x[2], "down", first_move)


		points[bot] = points[bot] + x[1]

		for char in x[4]:
			tiles[bot].remove(char)

		moves_made[bot] = moves_made[bot] + 1

		length = min(len(tiles_available), len(x[4]))

		if(length != 0):
			s = random.sample(tiles_available, length)
			tiles[bot].extend(s)

			for char in s:
				tiles_available.remove(char)




# points = [0,0]
# bingos = [0,0]
# time_taken = [0,0]
# moves_made = [0,0]

# limit = 1
# lists = []

# for j in range(limit):

# 	print(j)
# 	tiles_available = tiles_available_at_start
# 	tiles = [[],[]]

# 	for i in range(2):

# 		s = random.sample(tiles_available, 7)
# 		tiles[i].extend(s)

# 		for char in s:
# 			tiles_available.remove(char)

# 	board =  [[" " for x in range(15)] for y in range(15)]
# 	print_board(board)
# 	print(tiles)

# 	for i in range(1000):

# 		start = time.time()
# 		x = get_best_word(board, tiles[i%2])
# 		print("Move made is : ", x[0], " starting at : ", x[2], " points gained : ", x[1])

# 		if(x[1] == -1):
# 			print("No word possible")
# 			break

# 		if(x[2][0] == x[3][0]):
# 			play_word(board, x[0][0], x[2], direction = "Right")
# 		else:
# 			play_word(board, x[0][0], x[2], direction = "Down")

# 		points[i%2] = points[i%2] + x[1]
# 		if(len(x[4]) == 7):
# 			# bingos[i%2].append(x[0][0])
# 			bingos[i%2] = bingos[i%2] + 1

# 		time_taken[i%2] = time_taken[i%2] + (time.time() - start)

# 		for char in x[4]:
# 			tiles[i%2].remove(char)

# 		moves_made[i%2] = moves_made[i%2] + 1

# 		length = min(len(tiles_available), len(x[4]))

# 		if(length != 0):
# 			s = random.sample(tiles_available, length)
# 			tiles[i%2].extend(s)

# 			for char in s:
# 				tiles_available.remove(char)

# 		print("Player ", i%2)
# 		print_board(board)
# 		print(tiles[i%2])

# 		if(len(tiles[i%2]) == 0):
# 			print("Tiles are over.")
# 			break

# print("Average points per game : ", points[0]/limit, points[1]/limit)
# print("Average Bingos per game : ", bingos[0]/limit, bingos[1]/limit)
# print("Average time taken per move : ", time_taken[0]/(moves_made[0]), time_taken[1]/(moves_made[1]))
# print("Average moves per game : ", moves_made[0]/limit, moves_made[1]/limit)




