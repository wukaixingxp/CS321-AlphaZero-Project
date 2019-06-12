"""
MCTS starter code. This is the only file you'll need to modify, although
you can take a look at game1.py to get a sense of how the game is structured.
Created on June  10  2019
@author Bryce Wiedenbeck
@author Anna Rafferty (adapted from original)
@author Kaixing Wu and James Yang (adapted from original)
"""

# These imports are used by the starter code.
import random
import argparse
import game1
# You will want to use this import in your code
import math
import numpy as np

# since we use both random and np.random for random generation, we set both seeds to 123
random.seed(123)
np.random.seed(123)

# Whether to display the UCB rankings at each turn.
DISPLAY_BOARDS = False 

# UCB_CONST value - you should experiment with different values
UCB_CONST = .5

class Node(object):
    """Node used in MCTS"""
    
    def __init__(self, state, parent_node):
        """Constructor for a new node representing game state
        state. parent_node is the Node that is the parent of this
        one in the MCTS tree. """
        self.state = state
        self.parent = parent_node
        self.children = {} # maps moves (keys) to Nodes (values); if you use it differently, you must also change addMove
        self.visits = 0
        self.value = 0
        # self.prior = prior
        # Note: you may add additional fields if needed
        
    def addMove(self, move):
        """
        Adds a new node for the child resulting from move if one doesn't already exist.
        Returns true if a new node was added, false otherwise.
        """
        if move not in self.children:
            state = self.state.nextState(move)
            self.children[move] = Node(state, self)
            return True
        return False
    
    def getValue(self):
        """
        Gets the value estimate for the current node. Value estimates should correspond
        to the win percentage for the player at this node (accounting for draws as in 
        the project description).
        """
        return self.value

    def updateValue(self, outcome):
        """Updates the value estimate for the node's state.
        outcome: +1 for 1st player win, -1 for 2nd player win, 0 for draw."""
        # NOTE: which outcome is preferred depends on self.state.turn()

        # do not bother with values for the root node
        if self.parent:
            turn = self.parent.state.getTurn()
            turn2 = self.state.getTurn()
            assert(turn == -1 * turn2)
            if math.isnan(self.value):
                self.value = (outcome+1) / 2.0
            elif outcome == 0:
                self.value = (self.value * self.visits + 0.5) /float(self.visits+1)
            elif outcome == turn:
                self.value = (self.value * self.visits + 1) /float(self.visits+1)
            else: 
                self.value = max((self.value * self.visits - 0.5) /float(self.visits+1),0)

        self.visits += 1

    def UCBWeight(self):
        """Weight from the UCB formula used by parent to select a child.
        This node will be selected by parent with probability proportional
        to its weight."""
        return self.value + UCB_CONST * (math.log(self.parent.visits)/float(self.visits))**0.5

def mctsPlay(root, rollouts):
    """Select a move by Monte Carlo tree search.
    Plays rollouts random games from the root node to a terminal state.
    In each rollout, play proceeds according to UCB while all children have
    been expanded. The first node with unexpanded children has a random child
    expanded. After expansion, play proceeds by selecting uniform random moves.
    Upon reaching a terminal state, values are propagated back along the
    expanded portion of the path. After all rollouts are completed, the move
    generating the highest value child of root is returned.
    Inputs:
        node: the node for which we want to find the optimal move
        rollouts: the number of root-leaf traversals to run
    Return:
        The legal move from node.state with the highest value estimate
    """

    for i in range(rollouts): 
        # selecting a node with unexpanded children
        selectedNode = bestUCB(root)
        state = selectedNode.state
        #print(state.xMin,state.xMax,state.yMin,state.yMax)
        if selectedNode.state.isTerminal():
            expandNode = selectedNode
            outcome = selectedNode.state.value
        # if chosen node is not terminal, expand a random child on that node
        else:
            moves = selectedNode.state.getMoves()
            nextMove = None

            # select children that have not been expanded
            for move in moves:
                if selectedNode.addMove(move):
                    nextMove = move
                    break
            expandNode = selectedNode.children[nextMove]
            # roll out
            outcome = rollout(expandNode.state)
        # propagate values back to the root node
        curNode = expandNode
        while(curNode):
            curNode.updateValue(outcome)
            curNode = curNode.parent

    # find the best move from root node
    bestMove = None
    bestVal = 0
    for move in root.children:
        if root.children[move].value >= bestVal:
            bestMove = move
            bestVal = root.children[move].value
    root.addMove(bestMove)
    root = root.children[bestMove]
    return bestMove

# performs rollout on a state by randomly choosing moves until reaches terminal state
def rollout(state):
    if state.isTerminal():
        return state.value()
    else:
        done = False
        while not done:
            move = random.choice(state.getMoves())
            # print(12345,move,len(state._board))
            i = move// len(state._board)
            j = move % len(state._board)
            # print(state.xMin,state.xMax,state.yMin,state.yMax)

            if state.xMin <= i <= state.xMax and state.yMin <= j <= state.yMax:
                done = True
        return rollout(state.nextState(move))

# this function, given a node, uses UCB to keep traversing levels of nodes until reaches a node
# such that not all children have been expanded
def bestUCB(node):
    # if node is a terminal node, or if there are still children to expand from the node
    if node.state.isTerminal() or len(node.children.values()) < len(node.state.getMoves()):
        #print(node.state.isTerminal(),len(node.children.values()),len(node.state.getMoves()))
        #print("ending",node.state)
        return node
    nodes = []
    probs = []
    state = node.state
    for key, value in node.children.items():
        i = key//len(state._board)
        j = key % len(state._board)
        if state.xMin <= i <= state.xMax and state.yMin <= j <= state.yMax:
            nodes.append(value)
            probs.append(value.UCBWeight())
    # if total sum is 0, that is, all nodes have 0 UCB weight
    # then we find a node uniformly
    if sum(probs) == 0:
        probs = [1 / float(len(probs)) for _ in probs]
    # otherwise, normalize
    probs = [p / float(sum(probs)) for p in probs]
    best = np.argmax(probs)
    possibleNode = np.random.choice(nodes, 1, p = probs)
    nextNode = nodes[best]
    return bestUCB(nextNode)

def chooseUCB(node):
    # if node is a terminal node, or if there are still children to expand from the node
    if node.state.isTerminal() or len(node.children.values()) < len(node.state.getMoves()):
        #print(node.state.isTerminal(),len(node.children.values()),len(node.state.getMoves()))
        #print("ending",node.state)
        return node
    nodes = []
    probs = []
    for key, value in node.children.items():
        nodes.append(value)
        probs.append(value.UCBWeight())
    # if total sum is 0, that is, all nodes have 0 UCB weight
    # then we find a node uniformly
    if sum(probs) == 0:
        probs = [1 / float(len(probs)) for _ in probs]
    # otherwise, normalize
    probs = [p / float(sum(probs)) for p in probs]
    nextNode = np.random.choice(nodes, 1, p = probs)
    return chooseUCB(nextNode[0])




def random_move(node):
    """
    Choose a valid move uniformly at random.
    """
    move = random.choice(node.state.getMoves())
    node.addMove(move)
    return move

