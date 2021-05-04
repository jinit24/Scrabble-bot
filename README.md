# Scrabble-bot
A simple bot that plays scrabble. It predicts the best move for a given board position. 

# Playing with the bot
```
git clone -b 'new-ui' https://github.com/jinit24/Scrabble-bot
cd Scrabble-bot
python3 game.py
````
I've made a UI using curses. The user is set up as the first player.  
After the game is over, it'll show you stats of the game.   

![Screenshot from 2021-05-04 17-00-24](https://user-images.githubusercontent.com/45783917/116997660-b5fd2600-acfa-11eb-81fb-4d5f4d13ad7c.png)

1. To play a word, use the arrows to go to the desired place.   
2. Then type the letter. If the word is invalid according to the rules, it'll show you the word.  
3. Press enter the play your word.  
4. Press space too skip your turn and ESC to quit the game.  


# Goals
Right now the best move is chosen through brute force searching through all possible options.   
This causes issues when it opens up a triple word or triple letter for the opponent. So in the next version will try to quantify that.  
Also because the game has incomplete information, it will be difficult to use standard algorithms like Minimax.  
 
Rigorous testing of the algorithm is left. (If you have ideas on how do this open a pull request and we can discuss it)  

Incorporating the blank tile is left.

Any suggestions on the game or the UI is welcome. 
