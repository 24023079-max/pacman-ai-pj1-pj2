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
from collections import deque
from heapq import heappop, heappush
from itertools import count

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

def depthFirstSearch(problem: SearchProblem):
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
    
    visited = set()
    stack = util.Stack()
    stack.push((problem.getStartState(), []))

    while not stack.isEmpty():
        state, action = stack.pop()
        if state in visited:
            continue
        visited.add(state)

        if problem.isGoalState(state):
            return action

        for successor, move, stepcost in problem.getSuccessors(state):
            if successor not in visited:
                stack.push((successor, action + [move]))
    return []


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    start = problem.getStartState()

    visited = {start}
    queue = util.Queue()
    queue.push((start, []))

    while not queue.isEmpty():
        state, actions = queue.pop()

        if problem.isGoalState(state):
            return actions

        for successor, move, stepcost in problem.getSuccessors(state):
            if successor not in visited:
                visited.add(successor)
                queue.push((successor, actions + [move]))

    return []



def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    return _best_first_search(problem, nullHeuristic)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    return _best_first_search(problem, heuristic)


def _reconstruct_path(parents, goal):
    """Reconstruct once, after the search reaches a goal (O(path length))."""
    actions = []
    while True:
        previous, action = parents[goal]
        if previous is None:
            actions.reverse()
            return actions
        actions.append(action)
        goal = previous


def _best_first_search(problem, heuristic):
    """UCS/A* graph search with best-g updates and stale-entry removal."""
    start = problem.getStartState()

    frontier = util.PriorityQueue()
    frontier.push((start, 0), heuristic(start, problem))

    # state -> (best_g, parent, action)
    records = {start: (0, None, None)}

    while not frontier.isEmpty():
        state, g = frontier.pop()

        # Skip outdated entries.
        if g != records[state][0]:
            continue

        if problem.isGoalState(state):
            actions = []
            while True:
                _, previous, action = records[state]
                if previous is None:
                    actions.reverse()
                    return actions
                actions.append(action)
                state = previous

        for successor, action, step_cost in problem.getSuccessors(state):
            new_g = g + step_cost
            old_record = records.get(successor)

            if old_record is None or new_g < old_record[0]:
                records[successor] = (new_g, state, action)
                priority = new_g + heuristic(successor, problem)
                frontier.push((successor, new_g), priority)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
