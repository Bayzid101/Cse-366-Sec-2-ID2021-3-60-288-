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
from util import*
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
    """
    from util import Stack
    import time

    # Initialize timer
    start_time = time.time()

    # Initialize the frontier with the start state
    start_state = problem.getStartState()
    if problem.isGoalState(start_state):  # Check if the start state is the goal
        return []

    frontier = Stack()  # Use a stack for DFS
    frontier.push((start_state, []))  # (state, path)

    explored = set()  # A set to track explored states
    nodes_explored = 0

    while not frontier.isEmpty():
        # Pop the most recently added state and path
        state, path = frontier.pop()

        nodes_explored += 1  # Increment node counter

        if state in explored:  # Skip states we've already explored
            continue

        # Mark the state as explored
        explored.add(state)

        # Check if the current state is a goal state
        if problem.isGoalState(state):
            end_time = time.time()
            time_taken_ms = (end_time - start_time) * 1000
            print(f"Time taken: {time_taken_ms:.2f} ms")
            print(f"Nodes explored: {nodes_explored}")
            return path  # Return the path that leads to the goal

        # Get successors of the current state
        for successor, action, step_cost in problem.getSuccessors(state):
            if successor not in explored:
                # Push the successor to the frontier with the updated path
                frontier.push((successor, path + [action]))

    # No solution found
    end_time = time.time()
    time_taken_ms = (end_time - start_time) * 1000
    print(f"Time taken: {time_taken_ms:.2f} ms")
    print(f"Nodes explored: {nodes_explored}")
    return []



def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    from util import Queue
    import time

    # Initialize timer
    start_time = time.time()

    # Initialize the frontier with the start state
    start_state = problem.getStartState()
    if problem.isGoalState(start_state):  # Check if the start state is the goal
        return []

    frontier = Queue()
    frontier.push((start_state, []))  # (state, path)

    explored = set()  # A set to track explored states
    nodes_explored = 0

    while not frontier.isEmpty():
        # Pop the shallowest state and path
        state, path = frontier.pop()

        nodes_explored += 1  # Increment node counter

        if state in explored:  # Skip states we've already explored
            continue

        # Mark the state as explored
        explored.add(state)

        # Check if the current state is a goal state
        if problem.isGoalState(state):
            end_time = time.time()
            time_taken_ms = (end_time - start_time) * 1000
            print(f"Time taken: {time_taken_ms:.2f} ms")
            print(f"Nodes explored: {nodes_explored}")
            return path  # Return the path that leads to the goal

        # Get successors of the current state
        for successor, action, step_cost in problem.getSuccessors(state):
            if successor not in explored:
                # Push the successor to the frontier with the updated path
                frontier.push((successor, path + [action]))

    # No solution found
    end_time = time.time()
    time_taken_ms = (end_time - start_time) * 1000
    print(f"Time taken: {time_taken_ms:.2f} ms")
    print(f"Nodes explored: {nodes_explored}")
    return []


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    from util import PriorityQueue
    import time

    # Initialize timer
    start_time = time.time()

    # Initialize the frontier with the start state
    start_state = problem.getStartState()
    if problem.isGoalState(start_state):  # If the start state is the goal
        return []

    frontier = PriorityQueue()  # Priority queue for UCS
    frontier.push((start_state, []), 0)  # Push (state, path) with priority = 0
    explored = set()  # Track explored states
    nodes_explored = 0

    while not frontier.isEmpty():
        # Pop the state with the lowest cost
        state, path = frontier.pop()

        nodes_explored += 1  # Increment node counter

        if state in explored:
            continue

        explored.add(state)  # Mark as explored

        # Check if it's the goal state
        if problem.isGoalState(state):
            end_time = time.time()
            time_taken_ms = (end_time - start_time) * 1000
            print(f"Time taken: {time_taken_ms:.2f} ms")
            print(f"Nodes explored: {nodes_explored}")
            return path

        # Add successors to the frontier
        for successor, action, step_cost in problem.getSuccessors(state):
            if successor not in explored:
                new_path = path + [action]
                total_cost = problem.getCostOfActions(new_path)
                frontier.push((successor, new_path), total_cost)

    # No solution found
    end_time = time.time()
    time_taken_ms = (end_time - start_time) * 1000
    print(f"Time taken: {time_taken_ms:.2f} ms")
    print(f"Nodes explored: {nodes_explored}")
    return []



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
# astar = aStarSearch
ucs = uniformCostSearch
