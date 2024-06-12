from queue import Queue, PriorityQueue
from graph import Graph

GOAL_FOUND = 1
GOAL_NOT_REACHABLE = 2
MORE_STEPS_NEEDED = 3

def bfs_init(graph):
    graph.frontier = Queue()
    graph.frontier_set = {}
    graph.visited = {}
    graph.path_cost = {}
    graph.parent = {}
    graph.frontier.put(graph.initial)
    graph.frontier_set[graph.initial] = True
    graph.visited[graph.initial] = True
    graph.path_cost[graph.initial] = 0
    if graph.initial == graph.goal:
        # Return path to show we're done.
        return GOAL_FOUND
    return MORE_STEPS_NEEDED

def bfs_step(graph):
    if graph.frontier.empty():
        return GOAL_NOT_REACHABLE
    else:
       node = graph.frontier.get()
       del graph.frontier_set[node]
       if node == graph.goal:
          return GOAL_FOUND
       for edge in graph.edges_from(node):
          other = edge.other(node)
          path_cost = edge.weight + graph.path_cost[node]
          if other not in graph.visited:
            graph.visited[other] = True
            graph.frontier.put(other)
            graph.frontier_set[other] = True
            graph.parent[other] = node
            graph.path_cost[other] = path_cost
          elif path_cost < graph.path_cost[other]:
            graph.parent[other] = node
            graph.path_cost[other] = path_cost
       return MORE_STEPS_NEEDED

# Part 1:
# 1. Copy bfs_init and bfs_step, chaning bfs to dijkstra.
# 2. Change the line setting 'algorithm' to 'bfs' to say dijkstra instead.
# 3. Initialize frontier as a PriorityQueue.
# 4. Update the graph.frontier.put() lines to push the tuple (path_cost, node) instead of just node.
#      - This ensures that the order of path_cost is used as the priority.
# 5. Update the graph.frontier.get() line to take the second element of the tuple.
# 6. Test by running main.py and stepping through by pressing 's' to step forward.
#    '[' and  ']' cycles through previously defined graphs.
#
# Let me know if you have any problems running or debugging this, or get stuck at any point, and I'd be happy to help.
# Also If you find it too easy, I can set you something more challenging.
# I reccomend using print statements to see the path_costs, and which node it's considering.

# Part 2. Can you combine these two algorithms into a single 'bestfirstsearch'
# function that uses a priority queue to emulate both Dijkstra and
# breadth-first search?
#
# Hint: Pass in a function f that computes path cost and use that as the priority.

# Part 3.
# What would you need to change implement depth first search?
