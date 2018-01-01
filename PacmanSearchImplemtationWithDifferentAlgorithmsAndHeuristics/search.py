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

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    state = problem.getStartState()
    # Set the start state to be visited
    visited = set([state])
    # Add the start state to the path
    path = [0]
    # Run dfs
    result,path = doDfs(problem,state,visited,path)
    return path[1:]

def doDfs(problem, state, visited, path):
    if(problem.isGoalState(state)):
        # if goal state is found
        return (True,path)
    for (nextState,dir,cost) in problem.getSuccessors(state)[::-1]:
        # for all the successors which are not visited
        if nextState not in visited:
            # visit them and add to path
            visited.add(nextState)
            path.append(dir)
            result,path = doDfs(problem,nextState,visited,path)
            # if found a path, then return it else undo the changes
            if result:
                return True,path
            path = path[:len(path) - 1]
    return (False,path)



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    startState = problem.getStartState()
    # Set the start state to be visited (node: (direction,prev state))
    visited = {startState:(0,0)}

    now = Queue()
    now.push(startState)
    state = startState
    while not now.isEmpty():
        # consider the top element
        state = now.pop()
        if problem.isGoalState(state):
            break;
        for (nextState, dir, cost) in problem.getSuccessors(state):
            if nextState not in visited:
                # for all the successors which are not visited, add them to the queue
                # and mark them visited
                # also store the current parent node, to trace back the path
                now.push(nextState)
                visited[nextState] = (dir,state)
    path = []
    # trace back the path
    while state is not startState:
        path.append(visited[state][0])
        state = visited[state][1]
    return path[::-1]

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    from util import PriorityQueue
    # use priorityqueue for considering the  states on the basis of
    # least total cost first
    now = PriorityQueue()
    # push start state's ((state,path,totalcost),totalcost)
    now.push((problem.getStartState(),[0],0),0)
    done = set([0])
    while not now.isEmpty():
        # the  state, the path and the total cost
        state,path,pcost = now.pop();

        if problem.isGoalState(state):
            # if goal state, then break
            break;
        if state not in done:
            # for the ones to the least cost path haven't been found
            # add them to done to signify that the least cost path to
            # them have been found
            done.add(state)
            for (nextState, dir, cost) in problem.getSuccessors(state):
                if nextState not in done:
                    # for the remaining nodes, push the updated path and costs
                    path.append(dir)
                    now.push((nextState,path,pcost+cost),pcost+cost)
                    path = path[:len(path)-1]
    # return paths
    return path[1:]
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
    import sys
    state = problem.getStartState()
    startState = state
    done = {}
    # format: state: (costToTheState + hueristic, costToTheState, prevState, direction)
    now = {startState:(0,0,0,0)}

    while True:
        # pop the one with least path cost
        state = min(now,key=now.get)
        totalCost,pcost,prevstate,di = now[state]
        # remove it from the list
        del now[state]
        if problem.isGoalState(state):
            # if found, then break
            done[state] = (prevstate, di)
            break;
        if state not in done:
            # if least cost path to the state hasn't been found, add to done
            done[state]=(prevstate,di)
            for (nextState, dir, cost) in problem.getSuccessors(state):
                if nextState not in done:
                    # for all the successor nodes, put nodes in the
                    # priority queue with totalcosts and paths
                    total = pcost + cost + heuristic(nextState, problem)
                    if nextState in now:
                        # if already present, then update
                        pre = now[nextState]
                        pre = (pre[0],pre[1])
                        if pre > (total,pcost+cost):
                            now[nextState] = (total,pcost+cost,state,dir)
                    else:
                        # else insert new entry
                        now[nextState] = (total, pcost + cost, state, dir)
    # trace back the path, and return
    path = []
    while state is not startState:
        path.append(done[state][1])
        state = done[state][0]
    return path[::-1]


    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
