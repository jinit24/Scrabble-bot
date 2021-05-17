from collections import defaultdict
from string import ascii_lowercase
import copy

dicts = dict(zip(ascii_lowercase, range(0,26)))

class node():

	def __init__(self):

		self.children = [None]*26
		self.word_ends = 0

	def insert(self, word):

		for char in word:
			index = dicts[char]
			if(self.children[index] == None):
				self.children[index] = node()

			self = self.children[index]

		self.word_ends = 1
		return


	def check_word(self, word):

		for char in word:

			index = dicts[char]
			if(self.children[index] == None):
				return False

			self = self.children[index]

		return self.word_ends > 0 

	def max_prefix_match(self, word):

		for i in range(len(word)):

			index = dicts[word[i]]
			if(self.children[index] == None):
				return i

			self = self.children[index]

		return len(word) 


def traverse_word(current_node, word, tiles, intial_word = ""):
	
	word_list = []
	word_formed = intial_word

	if(len(word) == 0):
		if(len(word_formed)>0 and current_node.word_ends > 0):
			return [word_formed]

		return []

	char = word[0]

	if(char == "*"):

		for key in tiles:

			if(tiles[key] > 0):

				index = dicts[key]
				if(current_node.children[index] == None):
					continue

				tiles[key] = tiles[key] - 1
				word_list.extend(traverse_word(current_node.children[index], word[1:], tiles, word_formed + key))	
				tiles[key] = tiles[key] + 1

	else:


		i = 0
		while( i < len(word) and word[i] != "*" ):

			char = word[i]
			index = dicts[char]
			if(current_node.children[index] == None):
				return  word_list
			word_formed = word_formed + char
			current_node = current_node.children[index]
			i = i + 1

		word_list.extend(traverse_word(current_node, word[i:], tiles, word_formed))	


	if(current_node.word_ends > 0):
		word_list.append(word_formed)

	return  word_list
