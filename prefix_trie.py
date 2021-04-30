from trie_node import node
import time

prefix_trie = node()
suffix_trie = node()

def insert_words(file_name, trie):

	with open(file_name,'r') as file:
	   
		for line in file:
			for word in line.split():
				trie.insert(word)
				# suffix_trie.insert(word[::-1])


# start = time.time()
# print("Time taken to insert words : ", time.time() - start)


# start = time.time()
# for i in range(1000):
# 	(prefix_trie.check_word("arrivancies"))

# print("Time taken to find words : ", time.time() - start)

# print(prefix_trie.max_prefix_match("zakaria"))
