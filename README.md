# Scrabble-bot
Scrabble-bot predicts the best move for a given board position. 

# Playing the bot
```
https://github.com/jinit24/Scrabble-bot
cd Scrabble-bot
python3 bot.py
````
I've set it up to play against itself, so it'll keep making moves.Both the players here are the bot itself.   
After the game is over, it'll show you stats of the game.  
Setting up of the UI is left, so its a little tedious to let the user make moves one by one.

# Targets
Right now the best move is chosen through brute force searching through all possible options.   
This causes issues when it opens up a triple word or triple letter for the oponent. So in the next version will try to quantify that.  
Also because the game has incomplete information, it will be difficult to use standard algorithms like Minimax.  
 
Adding an UI would be helpful, if the user wants to play against the bot.

Rigorous testing of the algorithm is left. (If you have ideas on how do this open a pull request and we can discuss it)


# Game 
![alt text](https://github.com/jinit24/Scrabble-bot/blob/main/sample_game.png?raw=true)
