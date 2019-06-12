import graphics
from MCTS_Gomoku import *
from game1 import *
from mcts_alphaZero import *
from game import *
import os
from os import path
from policy_value_net_tensorlayer import PolicyValueNet

#Global variables for MCTS
start_state = game1.new_game()
curNode = Node(start_state, None)
ROLLOUT = 400
#Global variables for AlphaZero
alphaBoard = AlphaBoard(width=15, height=15, n_in_row=5)
alphaBoard.init_board(0)
p = os.getcwd()
model_file = path.join(p, 'model_15_15_5/best_policy.model')
policy = None
# Introduction Class Runs Introduction Program to GoMoku.
class IntroScreen(object):

    def __init__(self):

        self.win = graphics.GraphWin("Gomoku Start", 300, 300)
        self.win.setCoords(0, 0, 300, 300)

    def intro(self):

        '''
        Main intro page function. Runs generateIntro. "Searches" for a click on either the "play" or "instructions" button
        using a while loop set to true. When one button is clicked the intro page is undrawn and the appropriate function
        is run. When the self.chooseOpponent function and all of its subsidiaries are run, the values chosen in them are returned
        via this function to the main function.
        '''

        self.generateIntro()
        while True:
            click = self.win.getMouse()
            X = click.getX()
            Y = click.getY()
            if 70 < Y < 120:
                if 20 < X < 140:
                    self.unDrawObjects()
                    return self.chooseOpponent()

                if 160 < X < 280:
                    self.unDrawObjects()
                    self.instruct()
                    self.generateIntro()

    def instruct(self):

        '''
        Instructions page function. Displays instructions. Returns to intro page when "back" button is clicked (uses
        a while loop set to true).
        '''

        Title = graphics.Text(graphics.Point(150, 275), "Instructions")
        Title.setSize(24)
        Title.draw(self.win)
        instructions = graphics.Text(graphics.Point(150, 185),
                                     "GoMoku or GoBang is an oriental\n board-game, similar to the game" +
                                     " Go. Players \n alternate placing black and white stones \n on the vertices of the board. The game is \n won when a player manages" +
                                     " to place five \n stones of the same color in a row (horizontally, \n diagonally, or vertically). Try it out for yourself!")
        instructions.setSize(14)
        instructions.draw(self.win)

        backButton = graphics.Rectangle(graphics.Point(110, 100), graphics.Point(190, 40))
        backButton.setFill("red")
        backButtonText = graphics.Text(graphics.Point(150, 70), "Back")
        backButtonText.setSize(16)
        backButtonText.setStyle("bold")
        backButtonText.setTextColor("white")
        backButton.draw(self.win)
        backButtonText.draw(self.win)

        while True:
            click = self.win.getMouse()
            X = click.getX()
            Y = click.getY()
            if 110 < X < 190:
                if 40 < Y < 100:
                    instructions.undraw()
                    backButton.undraw()
                    backButtonText.undraw()
                    Title.undraw()
                    return

    def chooseOpponent(self):

        '''
        Another game-set-up page. User is presented with two options (computer or human opponent) and chooseColor
        function runs when one is clicked (methodology is the same as intro page). Additionally the difficulty
        funciton runs if computer is selected.
        '''

        typeText = graphics.Text(graphics.Point(150, 250), "Choose an opponent!")
        typeText.setSize(24)
        typeText.draw(self.win)

        self.playButton.setFill("Blue")
        self.playButton.draw(self.win)
        self.humanButtonText = graphics.Text(graphics.Point(80, 95), "Human")
        self.humanButtonText.setSize(20)
        self.humanButtonText.setTextColor("white")
        self.humanButtonText.draw(self.win)

        self.instructButton.setFill("Orange")
        self.instructButton.draw(self.win)
        self.computerButtonText = graphics.Text(graphics.Point(220, 95), "Computer")
        self.computerButtonText.setSize(20)
        self.computerButtonText.draw(self.win)

        while True:
            click = self.win.getMouse()
            X = click.getX()
            Y = click.getY()
            if 70 < Y < 120:
                if 20 < X < 140:
                    typeText.undraw()
                    self.playButton.undraw()
                    self.humanButtonText.undraw()
                    self.instructButton.undraw()
                    self.computerButtonText.undraw()
                    return self.chooseColor("Human", 0)

                if 160 < X < 280:
                    typeText.undraw()
                    self.playButton.undraw()
                    self.humanButtonText.undraw()
                    self.instructButton.undraw()
                    self.computerButtonText.undraw()
                    difficulty = self.difficulty()
                    return self.chooseColor("Computer", difficulty)

    def difficulty(self):

        '''
        Another game-set-up page. User is presented with two difficulty options (easy or hard) and chooseColor
        function runs when one is clicked (methodology is the same as intro page).
        '''

        difficultyText = graphics.Text(graphics.Point(150, 250), "Choose a difficulty!")
        difficultyText.setSize(24)
        difficultyText.draw(self.win)

        self.playButton.setFill("Purple")
        self.playButton.draw(self.win)
        self.easyButtonText = graphics.Text(graphics.Point(80, 95), "Easy")
        self.easyButtonText.setSize(20)
        self.easyButtonText.setTextColor("white")
        self.easyButtonText.draw(self.win)

        self.instructButton.setFill("Yellow")
        self.instructButton.draw(self.win)
        self.hardButtonText = graphics.Text(graphics.Point(220, 95), "Hard")
        self.hardButtonText.setSize(20)
        self.hardButtonText.draw(self.win)

        while True:
            click = self.win.getMouse()
            X = click.getX()
            Y = click.getY()
            if 70 < Y < 120:
                if 20 < X < 140:
                    difficultyText.undraw()
                    self.playButton.undraw()
                    self.humanButtonText.undraw()
                    self.instructButton.undraw()
                    self.computerButtonText.undraw()
                    return "Easy"

                if 160 < X < 280:
                    difficultyText.undraw()
                    self.playButton.undraw()
                    self.easyButtonText.undraw()
                    self.instructButton.undraw()
                    self.hardButtonText.undraw()
                    return "Hard"

    def chooseColor(self, opponent, difficulty):

        '''
        Another game-set-up page. User is presented with two options (black or white, black plays first) and both the opponent
        and the color are returned when one is clicked (methods used are same as the intro page function).
        '''

        typeText = graphics.Text(graphics.Point(150, 250), "Choose a team color! \n Black moves first.")
        typeText.setSize(24)
        typeText.draw(self.win)

        self.playButton.setFill("Black")
        self.playButton.draw(self.win)

        self.instructButton.setFill("white")
        self.instructButton.draw(self.win)

        while True:
            click = self.win.getMouse()
            X = click.getX()
            Y = click.getY()
            if 70 < Y < 120:
                if 20 < X < 140:
                    return [opponent, difficulty, "Black"]

                if 160 < X < 280:
                    return [opponent, difficulty, "White"]

    def generateIntro(self):

        # Generates a number of graphics objects for intro page

        self.introText = graphics.Text(graphics.Point(150, 250), "Welcome to Gomoku!")
        self.introText.setSize(30)
        self.introText.draw(self.win)

        self.playButton = graphics.Rectangle(graphics.Point(20, 120), graphics.Point(140, 70))
        self.playButton.setFill("Green")
        self.playButton.draw(self.win)
        self.playButtonText = graphics.Text(graphics.Point(80, 95), "Play Game!")
        self.playButtonText.setSize(20)
        self.playButtonText.draw(self.win)

        self.instructButton = graphics.Rectangle(graphics.Point(160, 120), graphics.Point(280, 70))
        self.instructButton.setFill("Purple")
        self.instructButton.draw(self.win)
        self.instructButtonText = graphics.Text(graphics.Point(220, 95), "Instructions")
        self.instructButtonText.setSize(20)
        self.instructButtonText.setTextColor("white")
        self.instructButtonText.draw(self.win)

    def unDrawObjects(self):

        # Undraws objects for the intro screen.

        self.introText.undraw()
        self.playButtonText.undraw()
        self.instructButtonText.undraw()
        self.playButton.undraw()
        self.instructButton.undraw()


# ____________________________________________________________________________

'''
This is the board class. Its purpose is to generate a graphical interface players can use to interact
with the program. Size is a parameter because some variations of GoMoku call for a larger board (and different
winning conditions, but we use the standard 15X15 here for AI consistency.
'''


class Board(object):

    def __init__(self, size):

        # Board generation instance variables

        self.win = graphics.GraphWin("Gomoku", 600, 600)
        self.win.setCoords(-50, -50, 550, 550)

        self.size = size

        # Generates stones objects. Detailed below and in readme.
        self.generateStones()
        self.stonesGraphic = []

        # Generates graphical board objects

        self.background()
        self.lines()
        self.generateButtons()

    # Board generation methods

    '''
    Stone generation function. Using lists we generate 15 lists, each with 15 integer inside of them. 0 is empty, 1 is black stone 
    and 2 is white stone
    '''

    def generateStones(self):

        self.stones = []
        for i in range(16):
            l = []
            for j in range(16):
                l.append(0)
            self.stones.append(l)

    # Generates 16 vertical and horizontal lines and appends them to a list of lines. Lines are spaced
    # 30 pixels apart using "for" loops. Lines are then drawn on board.

    def lines(self):

        lines = []
        for i in range(self.size):
            vertLine = graphics.Line(graphics.Point(30 * i, 0), graphics.Point(30 * i, 420))
            lines.append(vertLine)
        for i in range(self.size):
            horizLine = graphics.Line(graphics.Point(0, 30 * i), graphics.Point(420, 30 * i))
            lines.append(horizLine)
        for item in lines:
            item.draw(self.win)

    def background(self):

        self.board = graphics.Image(graphics.Point(100, 200), "wood.ppm")
        self.board.draw(self.win)

    # Generates the game title and "newgame, and resign" buttons respectively.

    def generateButtons(self):

        self.gomokuText = graphics.Text(graphics.Point(230, 495), "G o m o k u")
        self.gomokuText.setStyle("bold")
        self.gomokuText.setSize(36)
        self.gomokuText.setFace("helvetica")
        self.gomokuText.draw(self.win)


        self.newGame = graphics.Rectangle(graphics.Point(465, 200), graphics.Point(545, 250))
        self.newGameText = graphics.Text(graphics.Point(505, 225), "New Game")
        self.newGame.setFill("blue")
        self.newGameText.setSize(14)
        self.newGameText.setTextColor("white")
        self.newGame.draw(self.win)
        self.newGameText.draw(self.win)

        self.resign = graphics.Rectangle(graphics.Point(465, 100), graphics.Point(545, 150))
        self.resign.setFill("black")
        self.resign.draw(self.win)
        self.resignText = graphics.Text(graphics.Point(505, 125), "Resign")
        self.resignText.setSize(14)
        self.resignText.setTextColor("white")
        self.resignText.draw(self.win)

        self.quit = graphics.Rectangle(graphics.Point(465, 0), graphics.Point(545, 50))
        self.quit.setFill(graphics.color_rgb(100, 200, 100))
        self.quit.draw(self.win)
        self.quitText = graphics.Text(graphics.Point(505, 25), "Quit")
        self.quitText.setSize(14)
        self.quitText.setTextColor("white")
        self.quitText.draw(self.win)

    '''
    This function allows us to analyze user clicks on the board. It takes the x and y pixel of the click as inputs
    and outputs that click to the nearest "30" (the board's vertices are located at intervals of 30 pixels on the 
    screen. This way, if a player clicks near a vertex, but not directly on it, the program still recognizes the 
    click as a valid move. The modified point is returned.
    '''

    def findPoint(self, X, Y):

        divideX = X // 30
        remainderX = X % 30
        divideY = Y // 30
        remainderY = Y % 30

        if remainderX > 14:
            divideX = divideX + 1
        if remainderY > 14:
            divideY = divideY + 1
        point = (divideX * 30, divideY * 30)

        return point
    '''This function place a stone on the board and draw it out on UI.
    '''
    def placeStone(self, xPos, yPos, team):
        self.stones[xPos][yPos] = team
        Stone = graphics.Circle(graphics.Point(30 * xPos, 30 * yPos), 10)
        if team == 1:
            color = "Black"
        else:
            color = "White"
        Stone.setFill(color)
        self.stonesGraphic.append([xPos, yPos, Stone])
        Stone.draw(self.win)


class HumanPlayer:

    def __init__(self, teamColor, board):

        self.color = teamColor
        self.board = board

    '''
    The turn method allows the player to go about their turn. We first print some text on the board that denotes whose turn
    it is. Next, using a while loop set to true, we let the user click on the board to determine their move. Once a click
    is clicked (we get the click by running the getClick method), we look at its value. If it is a string with a command,
    we do that command (using if statements). If it is a point, we turn the point from "pixel" form to "vertex" form (so 
    we divide it by thirty) and search the stone list to determine if the vertex is open. If it is, we run the addStone and
    placeStone functions, placing that stone on the board, and end the turn. If it is not, the while loop repeats.
    '''

    def turn(self):
        if self.color == 1:
            color = "Black"
        else:
            color = "White"
        # Text changes for new turn
        self.turnText = graphics.Text(graphics.Point(230, -27), color + "'s Turn!")
        self.turnText.setTextColor(color)
        self.turnText.setSize(20)
        self.turnText.draw(self.board.win)

        # Getting a click and determining what to do
        while True:
            point = self.getClick()
            if point == "done":
                return "done", "done"

            elif type(point) != type("string"):
                i = int(point[0] / 30)
                j = int(point[1] / 30)
                stone = self.board.stones[i][j]
                if stone == 0:
                    self.board.placeStone(i, j, self.color)
                    self.turnText.undraw()
                    return i + list(range(14, -1, -1))[j] * self.board.size, i * 15 + j

    '''
    This is the getClick method. Using a while loop we "force" the user to click the board. We first run otherClick to check
    if the click was for any of the buttons on the board. If it was, we return the value of the otherClick method.
    If not, we modify the click using the findPoint method, check to see whether the point is within the board, and then 
    return the point.
    '''

    def getClick(self):

        while True:

            click = self.board.win.getMouse()
            X = click.getX()
            Y = click.getY()

            value = self.otherClick(X, Y)
            if value != 0:
                return value

            point = self.board.findPoint(X, Y)
            if (-10 < point[0] < 430) and (-10 < point[1] < 430):
                return point

    # Using code similar to the intro page, we check to see if the click was within the buttons on the board. If so, we run
    # those functions. If not, we return 0.

    def otherClick(self, X, Y):

        if 465 < X < 545:
            if 200 < Y < 250:
                return self.makeNewGame()
            elif 100 < Y < 150:
                return self.resigning()
            elif 0 < Y < 50:
                return self.quit()

        return 0

    '''
    This function "undos" the last two turns on the board. First it uses the remove stone function to remove the stone from
    the directory of stones and to undo any priority modifications that occurred when the stone was placed. Then we identify
    the stones in the stoneGraphic list, undraw it, and remove them from the list as well.
    '''

    def undo(self):
        return "not done"

    # This function makes a new game when the New Game button is clicked. It also returns done, which prompts the program
    # to end in a series of return sequences.

    def makeNewGame(self):
        global curNode
        global alphaBoard
        self.board.win.close()
        start_state = game1.new_game()
        curNode = Node(start_state, None)
        alphaBoard.init_board(0)
        main()
        return "done"

    # This functions prints resign text when the resign button is clicked. It also returns done, which prompts the program to
    # end in a series of return sequences.

    def resigning(self):
        global curNode
        global alphaBoard
        self.turnText.undraw()
        start_state = game1.new_game()
        curNode = Node(start_state, None)
        alphaBoard.init_board(0)
        if self.color == 1:
            color = "Black"
        else:
            color = "White"
        resignText = graphics.Text(graphics.Point(230, -10), color + " Resigned :( \n" + "Better Luck Next Time!")
        resignText.setSize(36)
        resignText.setTextColor(color)
        resignText.setFace("helvetica")
        resignText.draw(self.board.win)
        click = self.board.win.getMouse()
        self.board.win.close()
        main()
        return "done"

    # Returns "done", which prompts a series of return sequences that end the program.

    def quit(self):
        return "done"


class mctsPlayer:

    def __init__(self, teamColor, rollout, board):
        self.color = teamColor
        self.board = board
        self.rollout = rollout
        # If the computer is going first, we have mandated it's first move so that it doesn't get confused (there are
        # no other stones to based it's move off of on the first move).

        if self.color == 1:
            self.start = 1
        else:
            self.start = 0

    def turn(self):
        global curNode
        if self.start == 1:
            self.start = 0
            self.board.placeStone(7, 7, self.color)
            return 7 * self.board.size + 7, 7 * self.board.size + 7
        else:
            # Use MCTS to play num of rollout games and find the best move.
            move = mctsPlay(curNode, self.rollout)
            i = move % self.board.size
            j = 14 - move // self.board.size
            stone = self.board.stones[i][j]

            if stone == 0:
                self.board.placeStone(i, j, self.color)
                return move, None
            else:
                print("warning: add stone failed")


class alphaPlayer:

    def __init__(self, teamColor, model_file, board):
        global policy
        self.color = teamColor
        self.board = board
        self.rollout = rollout
        # If the computer is going first, we have mandated it's first move so that it doesn't get confused (there are
        # no other stones to based it's move off of on the first move).
        if policy == None:
            policy = PolicyValueNet(board_width=15, board_height=15, block=19, init_model=model_file, cuda=False)
        self.policy = policy.policy_value_fn
        self._action_fc = policy.action_fc_test
        self._evaluation_fc = policy.evaluation_fc2_test
        if self.color == 1:
            self.start = 1
        else:
            self.start = 0

    def turn(self):
        global alphaBoard
        if self.start == 1:
            alphaBoard.init_board(0)
            alphaBoard.availables = list(range(15 * 15))
            self.start = 0
            self.board.placeStone(7, 7, self.color)
            return None, 7 * self.board.size + 7
        else:
            # Use the network to predict the move distribution
            act_probs, value = self.policy(alphaBoard, self._action_fc, self._evaluation_fc)
            temp = 0
            move = None
            #Find the best move
            for act in act_probs:
                if act[1] >= temp:
                    temp = act[1]
                    move = act[0]
            assert (move in alphaBoard.availables)
            loc = alphaBoard.move_to_location(move)
            i = loc[0]
            j = loc[1]
            stone = self.board.stones[i][j]
            if stone == 0:
                self.board.placeStone(i, j, self.color)
                return None, i * 15 + j
            else:
                print("warning: add stone failed")


class GoMoku:

    # Initializer. We set the player instance variables according to which player is which color.

    def __init__(self, player1, player2, board):

        if player1.color == 1:
            self.player1 = player1
            self.player2 = player2
        else:
            self.player2 = player1
            self.player1 = player2

        self.p1Color = "Black"
        self.p2Color = "White"
        self.board = board

    # This method checks for a winning position after every turn. It looks at every stone that has a team (so is actualized)
    # on the board. It calls the list of priorities for this stone and assesses whether any of them is over 9 (since 10+ is
    # a winning priority). If so it returns the string "win"; if not "no winner".

    def checkWinning(self):
        if self._wins(1) or self._wins(2):
            return "Win"
        return "no winner"

    def _wins(self, player):
        """
        Returns True if this state is a win for the given player (1 = player 1, -1 = player 2) and False otherwise.
        """
        board = self.board.stones
        for j in range(WIDTH):  # start from left
            for i in range(HEIGHT - 1, -1, -1):  # start from bottom
                if board[i][j] == player:
                    for k in range(1, CONNECT):  # go up
                        if (i - k < 0) or (board[i - k][j] != player):
                            break
                        if k == CONNECT - 1:
                            return True
                    for k in range(1, CONNECT):  # go right
                        if (j + k >= WIDTH) or (board[i][j + k] != player):
                            break
                        if k == CONNECT - 1:
                            return True
                    for k in range(1, CONNECT):  # go up-right
                        if (i - k < 0) or (j + k >= WIDTH) or (board[i - k][j + k] != player):
                            break
                        if k == CONNECT - 1:
                            return True
            for i in range(HEIGHT - 1, -1, -1):
                if board[i][j] == player:
                    for k in range(1, CONNECT):  # go down-right
                        if (i + k >= HEIGHT) or (j + k >= WIDTH) or (board[i + k][j + k] != player):
                            break
                        if k == CONNECT - 1:
                            return True
        return False

    '''
    This is the runGame function. Using a while loop, it infinitely runs, letting players alternate their turns and 
    checking for a winning board after every turn. When someone has won, it prints winning text on the board, waits for 
    a click, and then runs the game again.
    '''

    def runGame(self):
        global curNode
        win = "no winner"

        while win == "no winner":

            # The player turns return a value depending on what they did during their turn. If during their turn they
            # chose to end the game or start a new one, "done" is returned and the program ends. Thus, the variable "a"
            # acts as a dummy variable.

            mcts, alpha = self.player1.turn()
            if mcts == "done":
                return
            alphaBoard.do_move(alpha)
            curNode.addMove(mcts)
            curNode = curNode.children[mcts]
            win = self.checkWinning()
            if win == "Win":
                alphaBoard.init_board(0)
                curNode = Node(start_state, None)
                winText = graphics.Text(graphics.Point(230, -20), self.p1Color + " Wins!")
                winText.setSize(36)
                winText.setTextColor(self.p1Color)
                winText.setFace("helvetica")
                winText.draw(self.board.win)
                self.board.win.getMouse()
                self.board.win.close()
                main()
                return

            mcts, alpha = self.player2.turn()
            if mcts == "done":
                return
            alphaBoard.do_move(alpha)
            curNode.addMove(mcts)
            curNode = curNode.children[mcts]
            win = self.checkWinning()
            if win == "Win":
                alphaBoard.init_board(0)
                curNode = Node(start_state, None)
                winText = graphics.Text(graphics.Point(230, -20), self.p2Color + " Wins!")
                winText.setSize(36)
                winText.setTextColor(self.p2Color)
                winText.setFace("helvetica")
                winText.draw(self.board.win)
                self.board.win.getMouse()
                self.board.win.close()
                main()
                return


# _______________________________________________________________________

'''
Method that runs GoMoku game. First we determine the colors of the players depending on the color parameter.
A board class is generated (with the number of squares being fifteen). Then a human player (P1) class and an
opponent class (either a human or computer, depending on user choice in chooseOpponent) is generated.Finally, a game class
is generated and the runGame method is run.
'''


def play(opponent, difficulty, color):
    if color == "White":
        myTeam = 2
        opTeam = 1
    elif color == "Black":
        myTeam = 1
        opTeam = 2
    theBoard = Board(15)
    P1 = HumanPlayer(myTeam, theBoard)

    if opponent == "Computer":
        if difficulty == "Hard":
            P2 = alphaPlayer(opTeam, model_file, theBoard)
        else:
            P2 = mctsPlayer(opTeam, ROLLOUT, theBoard)

    else:
        P2 = HumanPlayer(opTeam, theBoard)

    game = GoMoku(P1, P2, theBoard)
    game.runGame()


'''
The main function of the program. First we run the intro screen to introduce the game and determine what type of game
the player would like to play. This class returns the parameters of the game. The intro screen is then closed and 
the play function is run with the chosen parameters.
'''


def main():
    intro = IntroScreen()
    parameters = intro.intro()
    intro.win.close()
    play(parameters[0], parameters[1], parameters[2])


if __name__ == '__main__':
    main()
