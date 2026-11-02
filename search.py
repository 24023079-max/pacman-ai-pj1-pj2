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
    # Store one predecessor per expanded state, rather than copying full paths.
    # Recording states when popped preserves the usual DFS/LIFO expansion order.
    start = problem.getStartState()
    frontier = util.Stack()
    frontier.push((start, None, None))
    parents = {}

    while not frontier.isEmpty():
        state, previous, action = frontier.pop()
        if state in parents:
            continue
        parents[state] = (previous, action)

        if problem.isGoalState(state):
            return _reconstruct_path(parents, state)

        for successor, move, _ in problem.getSuccessors(state):
            if successor not in parents:
                frontier.push((successor, state, move))
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    start = problem.getStartState()
    frontier = util.Queue()
    frontier.push(start)
    parents = {start: (None, None)}  # vừa truy vết vừa đóng vai trò tập đã duyệt

    while not frontier.isEmpty():
        state = frontier.pop()
        if problem.isGoalState(state):
            return _reconstruct_path(parents, state)

        for successor, action, _ in problem.getSuccessors(state):
            if successor not in parents:
                parents[successor] = (state, action)
                frontier.push(successor)

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
    """Dijkstra/A* with a binary heap, best-g updates and lazy stale removal.

    The single records table holds both g costs and predecessor links.  A
    cheaper path re-opens a state, so A* also supports inconsistent heuristics.
    Step costs must be non-negative, as required by UCS/A*.
    """
    start = problem.getStartState()
    tie_breaker = count()
    heappush_fn, heappop_fn = heappush, heappop
    frontier = [(heuristic(start, problem), next(tie_breaker), 0, start)]
    records = {start: (0, None, None)}  # state -> (best_g, parent, action)

    while frontier:
        _, _, g, state = heappop_fn(frontier)
        if g != records[state][0]:  # Old heap entry, superseded by better g.
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
                heappush_fn(frontier, (priority, next(tie_breaker), new_g, successor))

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
