# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
         (action, stepCost, successor), where 'action' is the action
         required to get there, 'stepCost' is the incremental
         cost of expanding to that successor and 'successor' is a
         successor to the current state.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    closed=[]  # closed = empty set
    fringe=util.Stack()
    fringe.push(([],problem.getStartState())) 
    # push item: (state, path)
    while (True):
        if fringe.isEmpty():
            util.raiseNotDefined()
        move,node=fringe.pop()
        if problem.isGoalState(node):
            return move
        if node not in closed:
            closed.append(node)
            for child_node in problem.getSuccessors(node):
                fringe.push((move+[child_node[0]],child_node[2]))
                # push state+[], successor
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # BFS: Queue
    closed=[]
    fringe=util.Queue()
    fringe.push(([],problem.getStartState()))
    # push item: (path,state)
    while(True):
        if fringe.isEmpty():
            util.raiseNotDefined()
        move,node=fringe.pop()
        if problem.isGoalState(node):
            return move
        if node not in closed:
            closed.append(node)
            for child_node in problem.getSuccessors(node):
                fringe.push((move+[child_node[0]],child_node[2]))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    closed=[]
    fringe=util.PriorityQueue()
    fringe.push(([],0,problem.getStartState()),0)
    # action, cost, successor
    # add cost to the item, and cost to be priority
    while (True):
        if fringe.isEmpty():
            util.raiseNotDefined()
        (move,cost,node)=fringe.pop()
        if problem.isGoalState(node):
            return move
        if node not in closed:
            closed.append(node)
            for child_node in problem.getSuccessors(node):
                # update the priority queue with pri: cost
                fringe.update((move+[child_node[0]],cost+child_node[1],child_node[2]),
                              cost+child_node[1])
    util.raiseNotDefined()
    
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    closed=[]
    fringe=util.PriorityQueue()
    fringe.push(([],0,problem.getStartState()),heuristic(problem.getStartState(),problem))
    # priority=cost+heuristic
    while(True):
        if fringe.isEmpty():
            util.raiseNotDefined()
        (move,cost,node)=fringe.pop()
        if problem.isGoalState(node):
            return move
        if node not in closed:
            closed.append(node)
            for child_node in problem.getSuccessors(node):
                fringe.update((move+[child_node[0]],cost+child_node[1],child_node[2]),
                              cost+child_node[1]+heuristic(child_node[2],problem))
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
