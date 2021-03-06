# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        curFood = currentGameState.getFood()
        curFoodList = curFood.asList()
        posInf = float("inf")        # Positive infinity
        negInf = float("-inf")       # Negative infinity
        score = 0
        foodDis = posInf        # Distance to food, initialize as positive infinity

        # Prevent pacman stay at same spot
        if action == Directions.STOP:
            score = negInf
            return score

        # Check if collision with ghost when they not scared
        for ghostState in newGhostStates:
            if ghostState.getPosition() == newPos:
                if ghostState.scaredTimer == 0:
                    score = negInf
                    return score

        # Return the closest food pellet distance
        for food in curFoodList:
            temp = manhattanDistance(food, newPos)
            if temp < foodDis:
                foodDis = temp

        # The closer the food gets higher score
        score = 1/(foodDis + 0.0001)        # 0.0001 is in case of foodDis equal to 0
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.plyIndex = 0   # initial ply index

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, self.index, self.plyIndex)
        util.raiseNotDefined()

    def minimax(self, gs, agentIndex, plyIndex):      # gs game state

        if gs.isWin() or gs.isLose():
            return self.evaluationFunction(gs)

        # Next ply or return evaluation score
        if agentIndex == gs.getNumAgents():
            agentIndex = self.index
            plyIndex += 1
            if plyIndex == self.depth:
                return self.evaluationFunction(gs)

        if agentIndex == self.index:
            return self.maxValue(gs, agentIndex, plyIndex)
        else:
            return self.minValue(gs, agentIndex, plyIndex)

    def maxValue(self, pgs, agentIndex, plyIndex):        # pgs pacman game state
        value = float("-inf")
        actionList = pgs.getLegalActions(agentIndex)
        maxValueAction = ''

        for action in actionList:
            successor = pgs.generateSuccessor(agentIndex, action)
            # get value from ghost's turn
            tempValue = self.minimax(successor, agentIndex + 1, plyIndex)
            if tempValue > value:
                value = tempValue
                maxValueAction = action

        # return action if at the end of the recursive(agentIndex 0, plyIndex 0)
        if plyIndex == 0:
            return maxValueAction
        return value

    def minValue(self, ggs, agentIndex, plyIndex):        # ggs ghost game state
        value = float("inf")
        actionList = ggs.getLegalActions(agentIndex)

        for action in actionList:
            successor = ggs.generateSuccessor(agentIndex, action)
            # Increase agent index, call next ghost agent
            tempValue = self.minimax(successor, agentIndex + 1, plyIndex)
            value = min(tempValue, value)

        return value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBeta(gameState, self.index, self.plyIndex, float("-inf"), float("inf"))
        #util.raiseNotDefined()

    def alphaBeta(self, gs, agentIndex, plyIndex, alpha, beta):      # gs game state

        if gs.isWin() or gs.isLose():
            return self.evaluationFunction(gs)

        # Next ply or return evaluation score
        if agentIndex == gs.getNumAgents():
            agentIndex = self.index
            plyIndex += 1
            if plyIndex == self.depth:
                return self.evaluationFunction(gs)

        if agentIndex == self.index:
            return self.maxValue(gs, agentIndex, plyIndex, alpha, beta)
        else:
            return self.minValue(gs, agentIndex, plyIndex, alpha, beta)

    def maxValue(self, pgs, agentIndex, plyIndex, alpha, beta):        # pgs pacman game state
        value = float("-inf")
        actionList = pgs.getLegalActions(agentIndex)
        maxValueAction = ''

        for action in actionList:
            successor = pgs.generateSuccessor(agentIndex, action)
            # get value from ghost's turn
            tempValue = self.alphaBeta(successor, agentIndex + 1, plyIndex, alpha, beta)
            if tempValue > value:
                value = tempValue
                maxValueAction = action
            # check if pruning
            if value > beta:
                return value

            alpha = max(alpha, value)
        # return action if at the end of the recursive(agentIndex 0, plyIndex 0)
        if plyIndex == 0:
            return maxValueAction
        return value

    def minValue(self, ggs, agentIndex, plyIndex, alpha, beta):        # ggs ghost game state
        value = float("inf")
        actionList = ggs.getLegalActions(agentIndex)

        for action in actionList:
            successor = ggs.generateSuccessor(agentIndex, action)
            # Increase agent index, call next ghost agent
            tempValue = self.alphaBeta(successor, agentIndex + 1, plyIndex, alpha, beta)
            value = min(tempValue, value)
            # check if pruning
            if value < alpha:
                return value

            beta = min(beta, value)

        return value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(gameState, self.index, self.plyIndex)
        util.raiseNotDefined()

    def expectimax(self, gs, agentIndex, plyIndex):      # gs game state

        if gs.isWin() or gs.isLose():
            return self.evaluationFunction(gs)

        # Next ply or return evaluation score
        if agentIndex == gs.getNumAgents():
            agentIndex = self.index
            plyIndex += 1
            if plyIndex == self.depth:
                return self.evaluationFunction(gs)

        if agentIndex == self.index:
            return self.maxValue(gs, agentIndex, plyIndex)
        else:
            return self.expectValue(gs, agentIndex, plyIndex)

    def maxValue(self, pgs, agentIndex, plyIndex):        # pgs pacman game state
        value = float("-inf")
        actionList = pgs.getLegalActions(agentIndex)
        maxValueAction = ''

        for action in actionList:
            successor = pgs.generateSuccessor(agentIndex, action)
            # get value from ghost's turn
            tempValue = self.expectimax(successor, agentIndex + 1, plyIndex)
            if tempValue > value:
                value = tempValue
                maxValueAction = action

        # return action if at the end of the recursive(agentIndex 0, plyIndex 0)
        if plyIndex == 0:
            return maxValueAction
        return value

    def expectValue(self, ggs, agentIndex, plyIndex):        # ggs ghost game state
        value = 0       # set initial value to 0
        actionList = ggs.getLegalActions(agentIndex)
        probability = 1.0/len(actionList)       # probability of each value

        for action in actionList:
            successor = ggs.generateSuccessor(agentIndex, action)
            # Increase agent index, call next ghost agent
            curValue = self.expectimax(successor, agentIndex + 1, plyIndex)    # current ghost picked value
            value += probability * curValue

        return value

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      I found when I only consider the distance to food and penalty for stop, pacman gives the maximum average score.(
      not really make sense)
      When I try to weight number of food left or distance to ghost, etc. The average score goes down a bit, so I just 
      leave it with food distance and not stop.
    """
    "*** YOUR CODE HERE ***"
    curPos = currentGameState.getPacmanPosition()
    curFood = currentGameState.getFood()
    curFoodList = curFood.asList()
    # curFoodNum = len(curFoodList)
    curScore = currentGameState.getScore()
    ghostStates = currentGameState.getGhostStates()
    posInf = float("inf")  # Positive infinity
    negInf = float("-inf")  # Negative infinity
    foodDis = posInf  # Distance to food, initialize as positive infinity
    # ghostSumDis = 0
    score = 0

    # Check if collision with ghost when they not scared
    for ghostState in ghostStates:
        if ghostState.getPosition() == curPos:
            if ghostState.scaredTimer == 0:
                score = negInf
                return score
        # ghostSumDis += manhattanDistance(ghostState.getPosition(), curPos)

    # Return the closest food pellet distance
    for food in curFoodList:
        temp = manhattanDistance(food, curPos)
        if temp < foodDis:
            foodDis = temp

    # give some weight to food to distance and huge weight on not stopping
    score = 10 * 1 / (foodDis + 0.0001) + curScore * 5
    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

