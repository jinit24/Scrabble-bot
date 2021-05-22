# Scrabble-bot
A simple bot that plays scrabble. It predicts the best move for a given board position.  
If you're looking to play with the bot head over to : <a href = "https://github.com/jinit24/Scrabble-bot"> New-ui </a>
<a href="https://jinit24.github.io/Scrabble-bot/">Documentation</a> : this discusses the idea behind the bot and explanation of the code.

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
1. The opponent modelling right now uses sampling. So from the tiles left it samples tiles possible for the opponent. Based on the possible move for me, it checks whether the opponent is able to make a better move. Its difficult to make sure if this is working because you don't know the opponent's tiles and sometimes you might end up aiding the opponent. Incomplete information is the issue.
 
2. Incorporating the blank tile is left.

# Game 
![Screenshot from 2021-05-17 19-25-02](https://user-images.githubusercontent.com/45783917/118500836-c1fad600-b745-11eb-8085-daef71a57777.png)
This is a snapshot when the game is midway. You can see the moves made, and final score.

# Random Stats 

### Bot with Opp Modelling  
Average Points Lost    	    :  -13.16  
Average Potential upside    :  5.64   

| Bot vs Bot                 |Greedy Bot       | Bot with Opp Modelling  |
| :-----:                    | :-:             | :-:              |
|Total Wins                  | 12              | 13               |
|Average points per game     | 419.56          | 412.16           |
|Average Bingos per game     | 1.4             | 1.2              |
|Average time taken per move | 0.18s           | 9.72s            |
|Average moves per game      | 12.6            | 12.6             |
|Average points per move     | 33.29           | 32.71            |


I played the two bots against each other for 25 games.
