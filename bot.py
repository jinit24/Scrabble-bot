import time, itertools, random, copy
from trie_node import *
from best_word import *
from user_moves import *
from string import ascii_lowercase

import cProfile, re

def initialise():
	
	start = time.time()
	board =  [[" " for x in range(15)] for y in range(15)]
	prefix_trie = node()
	insert_words("Collins Scrabble Words (2019).txt", prefix_trie)
	print("Time taken to insert words : ", time.time() - start)

	return [board, prefix_trie]



board, prefix_trie = initialise()

wins   = [0,0]
points = [0,0]
bingos = [0,0]
time_taken = [0,0]
moves_made = [0,0]

limit = 25
lists = []
up = 0
tp = 0

for j in range(limit):

	print(j)
	tiles_available = copy.deepcopy(tiles_available_at_start)
	tiles = [[],[]]

	for i in range(j,j+2):

		s = random.sample(tiles_available, 7)
		tiles[i%2].extend(s)

		for char in s:
			tiles_available.remove(char)

	board =  [[" " for x in range(15)] for y in range(15)]
	# print_board(board)
	# print(tiles)

	game_points = [0,0]
	upside = 0
	total_points_lost = 0
	# cProfile.run("get_best_word(prefix_trie, board, tiles[i%2], tiles_available, False)")
	# get_best_word(prefix_trie, board, tiles[i%2], tiles_available, False)
	for i in range(j%2, 1000):

		start = time.time()
		if(i%2 == 0):
			x = get_best_word(prefix_trie, board, tiles[i%2], tiles_available, True)
		else:
			x = get_best_word(prefix_trie, board, tiles[i%2], tiles_available, False)


		if(isinstance(x,int) or x[1] == -1):
			print("No word possible", x)
			break

		print("Player ", i%2,"'s turn : ")
		print("Move made is : ", x[0], " starting at : ", x[2], " ending at : ", x[3]," points gained : ", x[1])


		if(i%2 == 1):
			
			greedy_best = get_best_word(prefix_trie, board, tiles[i%2], tiles_available, True)
			move_up, points_lost  =  calc_potential_upside(prefix_trie, board, tiles[0], greedy_best, x)
			# print(move_up, points_lost)
			upside = upside + move_up
			total_points_lost = total_points_lost + points_lost

		if(x[2][0] == x[3][0]):
			play_word_without_check(board, x[0][0], x[2], direction = "right")
		else:
			play_word_without_check(board, x[0][0], x[2], direction = "down")

		game_points[i%2] = game_points[i%2] + x[1]
		if(len(x[4]) == 7):
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

		# print("Player ", i%2)
		# print_board(board)
		# print(tiles[i%2])
		# prin
		if(len(tiles[i%2]) == 0):
			print("Tiles are over.")
			break

	if(game_points[0] > game_points[1]):
		wins[0] = wins[0] + 1
	else:
		wins[1] = wins[1] + 1

	print("Final Points 		   : ", game_points[0], game_points[1])
	print("Potential upside        : ", upside)
	print("Points Lost 		       : ", total_points_lost)
	print()


	points[0] = points[0] + game_points[0]
	points[1] = points[1] + game_points[1]
	up = upside + up
	tp = tp + total_points_lost

print("Average Points Lost    	   : ", tp/limit)
print("Average Potential upside    : ", up/limit)
print("Total wins              	   : ", wins[0], wins[1])
print("Average points per game 	   : ", points[0]/limit, points[1]/limit)
print("Average Bingos per game 	   : ", bingos[0]/limit, bingos[1]/limit)
print("Average time taken per move : ", time_taken[0]/(moves_made[0]), time_taken[1]/(moves_made[1]))
print("Average moves per game 	   : ", moves_made[0]/limit, moves_made[1]/limit)