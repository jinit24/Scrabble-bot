# Scrabble-bot
A simple bot that plays scrabble. It predicts the best move for a given board position. 

# Playing the bot
```
git clone -b 'new-ui' https://github.com/jinit24/Scrabble-bot
cd Scrabble-bot
python3 game.py
````
I've made a UI using curses. The user is set up as the first player.
After the game is over, it'll show you stats of the game.  





# Targets
Right now the best move is chosen through brute force searching through all possible options.   
This causes issues when it opens up a triple word or triple letter for the opponent. So in the next version will try to quantify that.  
Also because the game has incomplete information, it will be difficult to use standard algorithms like Minimax.  
 
Rigorous testing of the algorithm is left. (If you have ideas on how do this open a pull request and we can discuss it)  

Incorporating the blank tile is left.
