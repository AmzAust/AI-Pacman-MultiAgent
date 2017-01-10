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
import sys

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
    remaining food (currentFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    currentFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    def manhattanDistance( xy1, xy2 ):
        "Returns the Manhattan distance between points xy1 and xy2"
        return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

    if successorGameState.isWin():
        return float("infinity") # If we win, we return infinity
    else:
        pass
    
    if successorGameState.isLose():
        pass
    
    foodProximity = 50 # Find our proximity to nearest food
    ghostposition = currentGameState.getGhostPosition(1) # Get ghost position
    ghostDistance = manhattanDistance(ghostposition, newPos) # Find distance from ghost
    totalScore = max(ghostDistance, 5) + successorGameState.getScore() # Get max score
    myList = currentFood.asList() # Create list of food
    
    for food in myList:
        currentDistance = manhattanDistance(food, newPos)
        if (foodProximity > currentDistance):
            foodProximity = currentDistance # Find distance from food
        else:
            pass
        
    if action == Directions.STOP:
        totalScore -= 2 # Lose points for stopping
    else:
        pass
    
    if (successorGameState.getNumFood() < currentGameState.getNumFood()):
        totalScore += 50 # Give more score for getting food
    else:
        pass
    
    penalty = 2 * foodProximity
    totalScore -= penalty # Penalize for having lots of food in proximity
    currentCapsules = currentGameState.getCapsules()
    
    if successorGameState.getPacmanPosition() in currentCapsules:
        totalScore += 60 # If pacmans position is in the capsules we add points
    else:
        pass
    
    return totalScore


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

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """
  def determineAction(self, gameState, depth, agentIndex=0):
  
    # Return score if we meet any of these conditions
    if gameState.isWin():
        return ( self.evaluationFunction(gameState), )
    else:
        pass
    
    if gameState.isLose():
        return ( self.evaluationFunction(gameState), )
    else:
        pass
    
    if depth == 0:
        return ( self.evaluationFunction(gameState), )
    else:
        pass
        

    numberOfGhosts = gameState.getNumAgents()

    if agentIndex == numberOfGhosts - 1: # If this is the last agent we decrease depth
        currentDepth = depth - 1
    else:
        currentDepth = depth # If its not the last agent, the depth stays the same
    calcOfIndex = (agentIndex + 1) % numberOfGhosts
    myIndex = calcOfIndex
    
    # Create a list of the possible actions we can take
    possibleActions = [(self.determineAction(gameState.generateSuccessor(agentIndex, i), currentDepth, myIndex)[0], i) for i in gameState.getLegalActions(agentIndex)]
    
    if(agentIndex != 0): # If the index isnt zero, its a minimum node
        minOfList = min(possibleActions)
        return minOfList
    else:
        maxOfList = max(possibleActions)
        return maxOfList # If the index is zero, its a maximum node

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
    resultMinMax = self.determineAction(gameState, self.depth)[1]
    # Return the result of our function
    return resultMinMax
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
  
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

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
    def valueExpected(gameState, agentIndex, depth):
        
        # Return score if we meet any of these conditions
        if gameState.isWin():
            return self.evaluationFunction(gameState)
        else:
            pass
        
        if gameState.isLose():
            return self.evaluationFunction(gameState)
        else:
            pass
        
        if depth == 0:
            return self.evaluationFunction(gameState)
        else:
            pass
        
        value = 0
        sum = 0
        numberOfGhosts = gameState.getNumAgents() - 1
        legalActions = gameState.getLegalActions(agentIndex) # Find legal actions
        countActions = len(legalActions) # Count number of actions we have
        
        for action in legalActions:
            nextState = gameState.generateSuccessor(agentIndex, action)
            if (agentIndex != numberOfGhosts): # Use expected value if index isnt equal to ghosts
                sum += valueExpected(nextState, agentIndex + 1, depth)
                value = sum
            else:
                sum += maxFunction(nextState, depth - 1)
                value = sum      
                # Use max if index is equal to ghosts
        result = value / countActions
        # Return our result
        return result 
    
    def maxFunction(gameState, depth):
        
        # Return score if we meet these conditions
        if gameState.isWin():
            return self.evaluationFunction(gameState)
        else:
            pass
        
        if gameState.isLose():
            return self.evaluationFunction(gameState)
        else:
            pass
        
        if depth == 0:
            return self.evaluationFunction(gameState)
        else:
            pass
        
        totalScore = - float("infinity")
        legalActions = gameState.getLegalActions(0)
        
        for action in legalActions:
            currentGameState = gameState.generateSuccessor(0, action)
            totalScore = max(valueExpected(currentGameState, 1, depth), totalScore)
        return totalScore # Return max for the total score
    
    # Return score if we meet these conditions
    if gameState.isWin():
        return self.evaluationFunction(gameState)
    else:
        pass
    
    if gameState.isLose():
        return self.evaluationFunction(gameState)
    else:
        pass
    
    # Initialize actions and score
    legalActions = gameState.getLegalActions(0)
    totalScore = - float("infinity")
    optimalAction = Directions.STOP
    
    for action in legalActions:
        currentGameState = gameState.generateSuccessor(0, action)
        lastScore = totalScore # Find max value for score
        totalScore = max(valueExpected(currentGameState, 1, self.depth), totalScore)
        if lastScore < totalScore: # If this score is better than the last, take the action
            optimalAction = action
        else:
            pass
    # Return the optimal move for pacman
    return optimalAction

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    
    DESCRIPTION: <write something here so we know what you did>
    
    We want to return positive values for winning and negative values for losing so that pacman
    will try not to die. If a ghost is within a certain distance pacman should run away, but we
    dont want him to always run away from the ghost no matter how far away the ghost is. To make
    pacman eat more food we subtract values for the food left and also subtract for the capsules
    that are left so that pacman will eat them if he is close to them.
    
  """
  "*** YOUR CODE HERE ***"
  def manhattanDistance( xy1, xy2 ):
        "Returns the Manhattan distance between points xy1 and xy2"
        return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )
    
  if currentGameState.isWin():
      return float("infinity") # Return positive float for winning
  else:
      pass
  
  if currentGameState.isLose():
      return - float("infinity") # Return negative float for losing
  else:
      pass
  
  foodProximity = float("infinity")
  totalScore = scoreEvaluationFunction(currentGameState) # Evaluate score
  currentFood = currentGameState.getFood()
  myList = currentFood.asList() # Make list of food
  
  for xy in myList: # Find distance from food in list for pacman
      currentDistance = manhattanDistance(currentGameState.getPacmanPosition(), xy)
      if (foodProximity > currentDistance):
          foodProximity = currentDistance
      else:
          pass
  
  # Initialize ghosts and thier distance
  numberOfGhosts = currentGameState.getNumAgents()
  i = 1
  ghostDistance = float("infinity")
  
  while i < numberOfGhosts: # Find pacman and ghost current position
      calculateDistance = manhattanDistance(currentGameState.getGhostPosition(i), currentGameState.getPacmanPosition())
      ghostDistance = min(calculateDistance, ghostDistance) # Return minimum ghost distance
      i += 1
  
  maxScore = max(4, ghostDistance) * 3 # Run away from ghosts within the max distance
  foodCalculation = foodProximity * 3
  foodInList = len(myList) * 4
  totalScore += maxScore
  totalScore -= foodCalculation
  capsulelocations = currentGameState.getCapsules()
  capsuleCalculation = len(capsulelocations) * 4
  totalScore -= foodInList # Lose points for not eating food
  totalScore -= capsuleCalculation # Subtract for existing capsules
  
  return totalScore

# Abbreviation
better = betterEvaluationFunction

