# Scrabble-bot
A simple bot that plays scrabble. It predicts the best move for a given board position.  
If you're looking to play with the bot head over to : <a href = "https://github.com/jinit24/Scrabble-bot"> New-ui </a>

# Playing the bot
```
git clone -b 'opponent_modelling' https://github.com/jinit24/Scrabble-bot
cd Scrabble-bot
python3 bot.py
````
I've set it up to play against itself, so it'll keep making moves. Both the players here are the bot itself.  
Player 0 is playing greedily and player 1 is using opponent modelling.
After the game is over, it'll show you stats of the game.  

# Goals
1. Right now the best move is chosen through brute force searching through all possible options.   
This causes issues when it opens up a triple word or triple letter for the opponent. So in the next version will try to quantify that.  
Also because the game has incomplete information, it will be difficult to use standard algorithms like Minimax.  
 
2. Adding an UI would be helpful, if the user wants to play against the bot.

3. Rigorous testing of the algorithm is left. (If you have ideas on how do this open a pull request and we can discuss it)  

4. Incorporating the blank tile is left.

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
