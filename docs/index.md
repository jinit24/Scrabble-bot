This documentation explains the general idea behind the code and an explanation of it. If you're looking to play with the bot head over to <a href="https://github.com/jinit24/Scrabble-bot"> Bot </a>.

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


## Case 1 : End point
```
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   | N |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   | E |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   | W |   |   |   |   |   |   | 
------------------------------------------------------------
|   |   |   |   | e | x | i | s | t | i | n | g |   |   |   | 
------------------------------------------------------------
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 

```
So here exisiting is a word that was already on the board.   
We play a new word NEWt (End point 't' is already on the board)  

## Case 2 : Starting point
```
|   |   |   |   | e | x | i | s | t |   |   |  |   |   |   | 
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

```
exisit is a word that was already on the board.  
We play a new word sNEW (starting point 's' is already on the board)  


## Case 3 : Side-On
```
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

```
exist is a word that was already on the board. 
We play a new word NEST (letter 'S' is connected to a word on the board).  

## Case 4 : In Between
```
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
|   |   |   |   |   |   |   | S  |   | p |   |   |   |   |   | 

```
exists, exist and slip were already on the board.  
We play a new word HAsHeS. (letter 's' and 'e' were already on the board, we play a word that uses both of them)



