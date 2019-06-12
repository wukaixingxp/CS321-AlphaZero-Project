# CS321-AlphaZero-Project
AlphaZero Research on Gomoku and a Game with AlphaZero AI
James Yang and Kaixing Wu
Computer Science 321
Anna Rafferty
(Thanks for the work of Jonathan Gillespie)

For research details, please read our paper.

Gomoku Read-Me

Requirements:
pip3 install tensorflow
pip3 install tensorlayer==1.9.1

To run:
python3 Gomoku.py

Code modified from:
MCTS Player -- Connect four by @author Bryce Wiedenbeck
AlphaZero Player -- https://github.com/initial-h/AlphaZero_Gomoku_MPI, we also used the 15X15
model weights from here


This program runs a game of Gomoku with AI and human opponent options. It utilizes the 
graphics.py module to support a graphical interface. The program can be run from the command
line with the commands "python3 gomoku.py".

The game is briefly described in our intro page, but here we will describe it as well.
Gomoku is actually a "watered" down version of the popular game "Go". A possibly bad but not
entirely misplaced analogy could be made as follows: Go is to chess as Gomoku is to checkers.  
Players play on a gridded board, taking turns placing "stones", or black and white dots,
on vertices. The board can be various sizes, but the game is commonly played on 15x15, 
17x17, 19x19, and 21x21 boards. The goal of the game is to place five stones of the same
color in a row. Stones cannot be removed. So essentially tic-tac-toe with a lot more room
and five instead of three pieces in a row.

The first window that appears is the intro page. The user can move through these windows 
by clicking buttons that are displayed. When the color is picked, this window closes and
the main game window opens--it displays a board, a title, four "option" buttons, and the 
player whose turn it is. The user can play the game by clicking anywhere on the board. A
click places a stone at the nearest vertex, or, if the click is not near the board, does
nothing. Additionally, if an "option" button is clicked, the function associated with this 
option will be run--undo will undo the last two turns, new game starts a new game, resign 
ends the game, and quit quits the game. The game continues until one of the ending option
buttons is chosen or until five stones are placed in a row on the board. When this occurs
a winning message is displayed, and on the next click the game starts over from the intro
page.

The program utilizes a number of classes. The first class, the Intro class, serves to introduce
the game Gomoku and allows the user to choose what type of game they would like to play
(human or computer opponent, color of pieces, difficulty). 

The board class acts as the data storage and graphics class for the program; it stores game
data in the form of integer 0 -- empty,1 -- Black,2 -- White and generates
a window with the board and the option buttons. The stones themselves are a class. When a 
board class is generated, 225 0 are generated inside it.

The Gomoku class acts as an overarching game class that allows interaction between the two
players and the board. It alternates the players' turns and checks to see if a player has
won after every turn. 

The human class acts as the class for a human; it's methods allow a human player to interact
with the board. By clicking on the board the human can place a stone on the nearest vertex,
and by clicking on the option buttons the player can choose to enact one of the options.

Finally, the computer class has a MCTS player and a AlphaZero player. 

Easy level is the MCTS Player, which has a default of 400 rollouts. During the selectNode process, 
both ChooseUCB and BestUCB are avalible options -- ChooseUCB choose a node based on the weights while 
BestUCB choose the node greedily. After some tests, we set BestUCB as the default option. As the search space
is too big, we constrained the scope of random rollout to be the smaller window by find the xMin,xMax,Ymin and Ymax 
on the board. We notice a speed improvement but the MCTS player is still not so good with only 400 rollouts,  
A global MCTS tree is built to record each move and we reuse this tree during the searching process.
Restarting the game will reset the tree.

Hard level is the AlphaZero Player. It will first load the model weights using Tensorflow to build a global 
policy. A global alphaBoard is also used to track each move as the Tensorflow model requires the recent 8 moves
as inputs. The policy will return a move distributions given a state, and we act the move with highest possibility
Restarting the game will reset the alphaBoard, but the policy will still retained.








