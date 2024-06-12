from queue import Queue, Priority
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

def bfs(graph):
   state = bfs_init(graph)
   while state == MORE_STEPS_NEEDED:
      state = bfs_step(graph)
   return state

#def bredthfirstsearch(grpah,start,goal):
#  queue=[]
#  visited=[]
#  queue.append(start)
#  visited.append(start)
#  while queue:
#    current_node=queue.pop(0)
#    if current_node == goal:
#      return "SUCCESS"
#    for neighbour in grpah[current_node]:
#      if neighbour not in visited:
#        visited.append(neighbour)
#        queue.append(neighbour)
#  return "GOAL NOT FOUND"