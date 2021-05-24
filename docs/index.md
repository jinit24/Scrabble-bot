This documentation explains the general idea behind the code and an explanation of it. I'll be explaining the greedy version of the bot - picking the best word from all possible words based on their points.

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>


If you're looking to play with the bot head over to <a href="https://github.com/jinit24/Scrabble-bot"> Bot </a>.  
# Checking Words
{:toc}
We need a dictionary to check whether the words formed are valid or not.  

1. I could do store all the possible words as an array. Then binary search through it. Both space and time complexity are an issue here.
2. I could also store all the possible words in a dictionary (Hash map). In the worst case the complexity could be O(Size of Dictionary) which is an issue.
3. I decided to use a trie. Its basically a tree which letters as nodes. Searching is O(length of word) which is very fast. Some data compression does happen. (Insertion is slow, it takes up 3 seconds at the start)
 
I could improve this by using <a href="https://en.wikipedia.org/wiki/Deterministic_acyclic_finite_state_automaton"> DAFSA</a> as data is static. I haven't implemented it though. 

# Placing Words
I'll be only considering words than are made in the up-down direction because I can flip the board and use the same algorithm to get words made from left-right.   
(You'll have to see why flipping is necessary that is (x,y) => (y,x) and rotating the board 90 degrees will give you incorrect answers)   

The word you place on the board has to be connected to some word on the board unless its the first turn.  
So there are 4 basic cases : 
1. End point of new word is on the board
2. Starting point of new word is on the board
3. One or more letters of the new word is connected side-on to an exisiting word on the board
4. New word uses one or more tiles of existing word on the board. (But not case 1 or case 2)

For the examples - <strong> New letters placed are shown in uppercase. </strong>


## Case 1 : End Point
```js
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   | N |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   | E |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   | W |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   | e | x | i | s | t |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 
------------------------------------------------------------
```
exist is a word that was already on the board.   
We play a new word NEWt (End point 't' is already on the board)  

## Case 2 : Starting Point
```js
------------------------------------------------------------
|   |   |   |   | e | x | i | s | t |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   | N |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   | E |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   | W |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 
------------------------------------------------------------
```
exist is a word that was already on the board.   
We play a new word sNEW (starting point 's' is already on the board)   


## Case 3 : Side-On
```js
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   | N |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   | E |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   | e | x | i | s | t | S |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   | T |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
------------------------------------------------------------
```
exist is a word that was already on the board.  
We play a new word NEST (letter 'S' is connected to a word on the board).    
Here NEST could also be played in front forming Sexist and NEST. Both of which are acceptable words.  

## Case 4 : In Between
```js
------------------------------------------------------------
|   |   |   |   |   |   |   | H |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   | A |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   | e | x | i | s | t | s |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   | H |   | l |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   | e | x | i | s | t |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   | S  |   | p |  |   |   |   |   | 
------------------------------------------------------------
```
exists, exist and slip were already on the board.  
We play a new word HAsHeS. (letter 's' and 'e' were already on the board, we play a word that uses both of them)

# Making words
For a given set of letters we now want to make words. Based on the above 4 cases, we have some extra information to accomodate.
Importantly for each word once we place it we have to check if extra words are formed in the left to right direction.
```js
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   | N |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   | r | a | t | s | E |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   | y |   |   |   | W |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   | e | x | i | s | t |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 
------------------------------------------------------------
```
rats, rye and exist were already on the board. Now suppose I want to play NEWt, but a new word is form ratsE. This is not a word.
Hence, extra words can be formed which need to be checked if they are valid.


## Initial Idea - Permutations

Once you fix a length you can find all the permutations possible.    
In the worst case there are 7!(5040) permutations. This is managable and not really an issue.  
This is a one-liner in python : 
```py
import itertools
permutations   = itertools.permutations(tiles, length)
```
The main branch uses this idea.  
It's a bigger issue implementing this for case 4. You have to iterate over possible lengths on top and below, which worsens the complexity.  

## Improved Idea - Travesring the trie
This is almost 10x faster than the above idea. Instead we traverse through the trie.   
So an argument 'word' here is kind of regex.   
For example, here * can represent any character present in the tiles. In case 4 it can represent an empty tile.      
  Case 1 : word = "\*\*\*\*t"   
  Case 2 : word = "st\*\*"   
  Case 3 : word = "\*\*\*\*\*\*"   
  Case 4 : word = "\*\*t\*e\*"   
You can check the function "traverse_word" in trie_node.py

# Putting it together
First we need to find out all the positions where a letter already exists.   
All its neighbouring positions are our matter of concern. Let's say (x,y) is one of positions  
 
## Step 1 
{: .no_toc }
Case 1:   
We iterate from (x-1,y) to (x-7,y) or till we hit an existing tile. Make sure the minimum length of word formed is such that it ends at (x,y)

Case 2:    
We iterate from (x+1,y) to (x+7,y) or till we hit an existing tile.

Case 3:   
Our starting positon will be (x+1,y) or (x - length of word, y). I'm assuming x,y is the rightmost end of the word. Here regex can be of the form "\*\*\*\*\*".

Case 4:   
We fix a starting position here (x - l, y) and the end is where I've kept all 7 tiles. Here is where the regex comes in handy, you don't need to place all 7 tiles but still the function will find all words which use \[l,7\] number of new tiles. We need to iterate l from 1 to 7 or till we hit a tile.

The above case handling is done in  **get_down_all_words** function in **best_word.py** in opponnent_modelling branch. 
A separate case needs to be made when there are no tiles on the board (first turn of the game). You have to make sure to use (7,7) accordingly fix x = 7 and y = 7 in the case 1 and case 2.

## Step 2 
{: .no_toc }
For each case, find out word on top and word on bottom. 
```js
------------------------------------------------------------
|   |   |   |   |   |   |   | C |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   | A |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   | e | x | i | s | t |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   | t | a | r | t |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 
------------------------------------------------------------
```
exist and tart were previously on the board. We play CAst. 
Notice that there is more than 1 tile at the bottom of the word - 'st'.   
Similarly it is possible to have more than 1 tile at the top as well. Hence, word on top and word on bottom is the terminology.   

## Step 3
{: .no_toc }
Form the regex pattern. (You could also use the permutations idea check the get_words function in best_word.py in 'main' branch)   

Case 1,2,3:

```py
word_form_regex  = word_on_top + "*"*(length+1) + word_on_bottom
```

Case 4:

```py
new_letters_added = 0
word_formed = ""

# Making sure you have placed all tiles on the board
while(new_letters_added < len(tiles) and cx < 15):

 if(board[cx][cy] == " "):
   word_formed = word_formed + "*"
   new_letters_added = new_letters_added + 1
 else:
   word_formed = word_formed + board[cx][cy]

 cx = cx + 1
word_form_regex  = word_on_top + word_formed
```

## Step 4 
{: .no_toc }
Find all possible words. The traverse_word function is in the trie_node.py.
This is where most of the magic happens. Based on the regex passed it returns a list of words possible.

```py
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
```

## Step 5
{: .no_toc }
For each find out other words formed on left to right and check its validity. If all words formed are valid then return words formed and their points.    
This is done in **get_other_words** function in **best_word.py** in opponnent_modelling branch.    
word on right and word on left have the same idea as word on top and word on bottom.     

## Step 6
{: .no_toc }
Calculating the points is a little tricky. You have to only consider words that contain at least one new letter.   
Based on the position of the tiles placed you might get a double letter or double word or triple letter or triple word.    
All this is taken into account in **get_points** function in **best_word.py** in opponnent_modelling branch.    
Return the word which has the highest points.    

## Step 7
{: .no_toc }
To finally get the best word you'll have to find the best word in up-down direction then flip the board, repeat the same procedure, compare the best words and flip the board back again.


# Function Description
**best_word.py** in opponnent_modelling branch

* The separation of cases is done in  **get_down_all_words**, which calls get_words internally.
* The rest of heavylifting of finding words on top, words on bottom, regex formation, calling traverse_word, calling get_points and getting extra words formed is done  in **get_words**.
* **get_separated_words** separately handles Case 4.
* **get_other_words** finds the extra word formed in the left to right direcition. Called by get_words.   
 

I really enjoyed doing this project. I have only described the greedy bot here. I'm working on one that has opponent modelling, interesting stuff.   
If you wish to discuss any ideas please feel free to mail me at : dornumofficial@gmail.com
