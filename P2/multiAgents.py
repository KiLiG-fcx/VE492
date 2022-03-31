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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        # from the action, generate the next state
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        score=successorGameState.getScore() # get the initial score
        # state[0] is the configuration, including (pos,direction)
        food_dist=[] # the list for food distance to pacman, and calculate the min
        ghost_dist=manhattanDistance(newPos,newGhostStates[0].getPosition())
        for foods in newFood.asList():
            food_dist.append(manhattanDistance(foods,newPos))
        if (len(food_dist)>0):
            score=score + 2/min(food_dist)
        if ghost_dist!=0:
            score=score - 1/ghost_dist
        return score
        return successorGameState.getScore()


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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        def pac_helper(state, depth, agentIndex):
            agent_num = state.getNumAgents()
            if agentIndex==agent_num: # pacman
                if gameState.isWin() or gameState.isLose() or depth == self.depth:
                    # it has reaches the final state
                    return self.evaluationFunction(state)
                else:
                    return pac_helper(state, depth+1, 0)
            else:
                legal_action = state.getLegalActions(agentIndex)
                successor=[]
                if len(legal_action)==0:
                    # no legal action, return the eva. value
                    return self.evaluationFunction(state)
                for actions in legal_action:
                    # for each legal action, append the successor value
                    successor.append(pac_helper(state.generateSuccessor(agentIndex, actions)
                                                ,depth, agentIndex + 1))
                # choose max/min
                if(agentIndex==0):  # the pacman's move, choose the maxvalue
                    return max(successor)
                else: # else choose minvalue
                    return min(successor)
        pac_action=gameState.getLegalActions(0)
        return max(pac_action,
                   key=lambda k:pac_helper(gameState.generateSuccessor(0, k), 1, 1))
   
        
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # the initial alpha is -inf, and initial beta is inf
        result=self.ab_main(float('-inf'), float('inf'),gameState,0)
        # return the action result[0]
        return result[0]
    
    def max_value(self, alpha, beta, state, depth):
        legal_action = state.getLegalActions(0)
        # get the legal actions of pacman
        curr_v=-float('inf')
        action=None
        # record action & current value
        v=(action, curr_v)
        for actions in legal_action:
            # the max value considers pacman, so agentIndex=0
            successor = state.generateSuccessor(0, actions)
            # get success value
            suc_v = self.ab_main(alpha,beta,successor, depth+1)
            if v[1]<suc_v[1]:
                v = (actions,suc_v[1])
            if v[1]>beta:
                return v
            # do a-b pruning
            alpha = max(v[1],alpha) 
        return v
    
    def min_value(self, alpha, beta,state, depth):
        agent_num=state.getNumAgents()
        legal_action = state.getLegalActions(depth%agent_num)
        curr_v=float('inf')
        action=None
        # v contains required get_action, and compared v[1] in pseudo code
        v=(action,curr_v)
        for actions in legal_action:
            # in the min-value, consider the next agent index is pacman/ghost
            successor = state.generateSuccessor(depth%agent_num,actions)
            suc_v = self.ab_main(alpha,beta,successor,depth+1)
            if v[1]>suc_v[1]:
                v = (actions, suc_v[1])
            if v[1]<alpha:
                return v
            # do a-b pruning
            beta = min(v[1],beta)
        return v
    
    def ab_main(self,alpha, beta,state, depth):
        agent_num=state.getNumAgents()
        if state.isWin() or state.isLose() or depth == self.depth*agent_num:
            # reaches the end state
            return (None, self.evaluationFunction(state))
        if depth%agent_num != 0: 
            # the ghost step, do min-value
            return self.min_value(alpha, beta,state,depth)
        else: # the pacman step, do max-value
            return self.max_value(alpha,beta,state, depth)
        util.raiseNotDefined()

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
        agent_num=gameState.getNumAgents()
        v_tot=util.Counter()
        legal_action=gameState.getLegalActions(0)
        def expectimax(state,depth,agentIndex):   
            if state.isWin() or state.isLose() or depth==0: 
                # the end state, use evaluate func
                return self.evaluationFunction(state)
            v=-float('inf')
            s=0.00 # average value
            for actions in state.getLegalActions(agentIndex):
                if (agentIndex==0):
                    # pacman state, use max-value
                    v=max(v,expectimax(state.generateSuccessor(agentIndex,actions),
                                       depth,agentIndex+1))
                else:
                    # ghost state
                    ghost_num=len(state.getLegalActions(agentIndex))
                    if(agentIndex<agent_num-1):
                        # not the last ghost
                        s=s+expectimax(state.generateSuccessor(agentIndex,actions),
                                           depth,agentIndex+1)
                    else:
                        # end of ghost, agent Index go to pacman again
                        s=s+expectimax(state.generateSuccessor(agentIndex,actions),
                                           depth-1,0)
                    v=s/ghost_num # calculate avg
            return v
        for actions in legal_action:
            i=legal_action.index(actions)
            v_tot[i]=expectimax(gameState.generateSuccessor(0,actions),self.depth,1)
        return legal_action[v_tot.argMax()]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    consider the reciprocal of the nearest food in food_list (as food score)
    and the current position from pacman to all the ghosts
    if reaches the ghost, minus reciprocal with weight -1
    otherwise, add to the score with weight 10
    """
    "*** YOUR CODE HERE ***"
    score=currentGameState.getScore() # get current score in this game state
    pac_pos=currentGameState.getPacmanPosition() # get the pacman position
    ghost_states=currentGameState.getGhostStates() # find all the ghosts
    food_lst=currentGameState.getFood().asList() 
    # get all the foods, and turn into list of (x,y)
    curr_min=float('inf')
    #calculate food score
    if(len(food_lst)>0):
        for food in food_lst:
            curr_min=min(manhattanDistance(pac_pos,food),curr_min)
        score+=1/curr_min 
        # calculate ghost dist scores
    for ghost in ghost_states:
        dist=manhattanDistance(pac_pos,ghost.getPosition())
        #+scared_time[ghost_states.index(ghost)]
        if(dist!=0):
            # pacman not reach the ghost, add 10* reciprocal
            if(ghost.scaredTimer>0):
                score+=10/dist
            else:
                # reach the ghost
                score-=1/dist
    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
