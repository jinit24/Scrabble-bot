import time, itertools, random
from trie_node import *
from best_word import *

def initialise():
	
	start = time.time()
	insert_words("Collins Scrabble Words (2019).txt", prefix_trie)
	print("Time taken to insert words : ", time.time() - start)
	board =  [[" " for x in range(15)] for y in range(15)]
	prefix_trie = node()
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

 
board, prefix_tree = initialise()

points = [0,0]
bingos = [0,0]
time_taken = [0,0]
moves_made = [0,0]

limit = 1
lists = []

for j in range(limit):

	print(j)
	tiles_available = tiles_available_at_start
	tiles = [[],[]]

	for i in range(2):

		s = random.sample(tiles_available, 7)
		tiles[i].extend(s)

		for char in s:
			tiles_available.remove(char)

	board =  [[" " for x in range(15)] for y in range(15)]
	print_board(board)
	print(tiles)

	for i in range(1000):

		start = time.time()
		x = get_best_word(board, tiles[i%2])
		print("Move made is : ", x[0], " starting at : ", x[2], " points gained : ", x[1])

		if(x[1] == -1):
			print("No word possible")
			break

		if(x[2][0] == x[3][0]):
			play_word(board, x[0][0], x[2], direction = "Right")
		else:
			play_word(board, x[0][0], x[2], direction = "Down")

		points[i%2] = points[i%2] + x[1]
		if(len(x[4]) == 7):
			# bingos[i%2].append(x[0][0])
			bingos[i%2] = bingos[i%2] + 1

		time_taken[i%2] = time_taken[i%2] + (time.time() - start)

		for char in x[4]:
			tiles[i%2].remove(char)

		moves_made[i%2] = moves_made[i%2] + 1

		length = min(len(tiles_available), len(x[4]))

		if(length != 0):
			s = random.sample(tiles_available, length)
			tiles[i%2].extend(s)

			for char in s:
				tiles_available.remove(char)

		print("Player ", i%2)
		print_board(board)
		print(tiles[i%2])

		if(len(tiles[i%2]) == 0):
			print("Tiles are over.")
			break

print("Average points per game : ", points[0]/limit, points[1]/limit)
print("Average Bingos per game : ", bingos[0]/limit, bingos[1]/limit)
print("Average time taken per move : ", time_taken[0]/(moves_made[0]), time_taken[1]/(moves_made[1]))
print("Average moves per game : ", moves_made[0]/limit, moves_made[1]/limit)




