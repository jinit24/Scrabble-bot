# Scrabble-bot
Scrabble-bot predicts the best move for a given board position. 

# Playing the bot
```
git clone https://github.com/jinit24/Scrabble-bot
cd Scrabble-bot
python3 bot.py
````
I've set it up to play against itself, so it'll keep making moves. Both the players here are the bot itself.   
After the game is over, it'll show you stats of the game.  
Setting up of the UI is left, so its a little tedious to let the user make moves.

# Targets
Right now the best move is chosen through brute force searching through all possible options.   
This causes issues when it opens up a triple word or triple letter for the opponent. So in the next version will try to quantify that.  
Also because the game has incomplete information, it will be difficult to use standard algorithms like Minimax.  
 
Adding an UI would be helpful, if the user wants to play against the bot.

Rigorous testing of the algorithm is left. (If you have ideas on how do this open a pull request and we can discuss it)  

Incorporating the blank tile is left.

# Game 
![sample_game](https://user-images.githubusercontent.com/45783917/116738002-83f47700-aa0f-11eb-9a29-e02a8e5f8b96.png)  
This is a snapshot when the game is midway. You can see the available tiles, move made, its position and points for it.

# Random Stats 

| Bot vs Bot                 |Bot as Player 1  | Bot as Player 2  |
| :-----:                    | :-:             | :-:              |
|Average points per game     | 410.11          | 392.88           |
|Average Bingos per game     | 0.6             | 0.63             |
|Average time taken per move | 1.45s           | 1.52s            |
|Average moves per game      |  13.08          | 12.63            |
|Average points per move     | 31.35           | 31.10            |

I played the bot against itself for 100 games and above are the results.
