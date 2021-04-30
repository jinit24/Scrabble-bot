from collections import defaultdict
import copy

class node():

	def __init__(self):

		self.children = [None]*26
		self.word_ends = 0
		self.depth = 0

	def insert(self, word):

		for char in word:

			index = ord(char) - ord('a')
			if(self.children[index] == None):
				self.children[index] = node()

			self.children[index].depth = self.depth + 1
			self = self.children[index]

		self.word_ends = self.word_ends + 1
		return


	def check_word(self, word):

		for char in word:

			index = ord(char) - ord('a')
			if(self.children[index] == None):
				return False

			self = self.children[index]

		return self.word_ends > 0 

	def max_prefix_match(self, word):

		for i in range(len(word)):

			index = ord(word[i]) - ord('a')
			if(self.children[index] == None):
				return word[:i]

			self = self.children[index]

		return word 


def traverse_word(current_node, word, tiles, intial_word = ""):
	
	word_list = []
	word_formed = intial_word

	if(len(word) == 0):
		return []

	char = word[0]

	if(char == "*"):

		for key in tiles:

			if(tiles[key] > 0):

				index = ord(key) - ord('a')
				if(current_node.children[index] == None):
					continue

				# current_node = current_node.children[index]
				tiles[key] = tiles[key] - 1
				word_list.extend(traverse_word(current_node.children[index], word[1:], tiles, word_formed + key))	
				tiles[key] = tiles[key] + 1

	else:


		i = 0
		while( i < len(word) and word[i] != "*" ):

			char = word[i]
			index = ord(char) - ord('a')
			if(current_node.children[index] == None):
				return  word_list
			word_formed = word_formed + char
			current_node = current_node.children[index]
			i = i + 1

		word_list.extend(traverse_word(current_node, word[i:], tiles, word_formed))	


	if(current_node.word_ends > 0):
		word_list.append(word_formed)


	return  word_list
