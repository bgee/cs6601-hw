from osm2networkx import *
import random
from operator import attrgetter
from math import sqrt

"""
Searching a street network using Breadth First Search

REQUIREMENTS:

  networkx: http://networkx.github.io/

REFERENCES:

  [1] Russel, Norvig: "Artificial Intelligene A Modern Approach", 3rd ed, Prentice Hall, 2010

ASSIGNMENT:

  Extend this program to Tridirectional Search.
  Find a path between three starting points.

author: Daniel Kohlsdorf and Thad Starner
"""

"""
The state space in our problem hold:

   1) A node in the street graph
   2) A parent node

"""
def find(state, state_list):
    for n in state_list:
        if state.node['data'].id == n.node['data'].id:
            return n

    return None

class State:

    def __init__(self, node, parent):
        self.node   = node
        self.parent = parent

    def __eq__(self, other):
        if isinstance(other, State):
            return self.node['data'].id == other.node['data'].id
        return NotImplemented

class CostState(State):

    def __init__(self, node, parent, cost):
        self.node = node
        self.parent = parent
        self.cost = cost

    def __eq__(self, other):
        if isinstance(other, State):
            return self.node['data'].id == other.node['data'].id
        return NotImplemented

    #def __getitem__(self)

"""
Implements BFS on our GPS data

see [1] Figure 3.11
"""
def bfs(graph, start, goal):
    if start == goal:
        print "START === GOAL"
        return None
    
    frontier = [start]
    explored = []
    num_explored = 0
    while len(frontier) > 0:
       node = frontier.pop(0)

       explored.append(node)
       for edge in networkx.edges(graph, node.node['data'].id):
           child = State(graph.node[edge[1]], node) 
           if (child not in explored) and (child not in frontier):
               # HINT: Goal - Check
               if child == goal:
                   print "Goal found, explored: ", num_explored, "\n\n"
                   return child
               else:
                   frontier.append(child)
               num_explored = num_explored + 1
    print "No path found, explored: ", num_explored

    return None


def ucs(graph, start, goal_state):
    frontier = [CostState(start.node, None, 0)]
    goal = CostState(goal_state.node, None, 0)
    explored = []
    num_explored = 0
    while len(frontier) > 0:
        frontier.sort(key = attrgetter('cost'))
        node = frontier.pop(0)

        if node == goal:
            print "Goal found, explored: ", num_explored, "\n\n"
            return node
        explored.append(node)
        for edge in networkx.edges(graph, node.node['data'].id):
            lat = graph.node[edge[1]]['data'].lat
            lon = graph.node[edge[1]]['data'].lon
            distance = sqrt((lat-node.node['data'].lat)**2 + (lon-node.node['data'].lon)**2)
            child = CostState(graph.node[edge[1]], node, node.cost+distance)
            found_in_frontier = find(child, frontier)
            found_in_explored = find(child, explored)
            if (found_in_frontier == None) and (found_in_explored == None):
                frontier.append(child)
                num_explored = num_explored + 1
            elif (found_in_frontier != None) and (found_in_frontier.cost>child.cost):
                frontier.remove(found_in_frontier)
                frontier.append(child)
    
    print "No path found, explored: ", num_explored

    return None

def a_star(graph, start, goal_state):
    frontier = [CostState(start.node, None, 0)]
    goal = CostState(goal_state.node, None, 0)
    explored = []
    num_explored = 0
    while len(frontier) > 0:
        frontier.sort(key = attrgetter('cost'))
        node = frontier.pop(0)

        if node == goal:
            print "Goal found, explored: ", num_explored, "\n\n"
            return node
        explored.append(node)
        for edge in networkx.edges(graph, node.node['data'].id):
            lat = graph.node[edge[1]]['data'].lat
            lon = graph.node[edge[1]]['data'].lon
            distance = sqrt((lat-node.node['data'].lat)**2 + (lon-node.node['data'].lon)**2)
            distance = distance + sqrt((lat-goal.node['data'].lat)**2 + (lon-goal.node['data'].lat)**2)
            child = CostState(graph.node[edge[1]], node, node.cost+distance)
            found_in_frontier = find(child, frontier)
            found_in_explored = find(child, explored)
            if (found_in_frontier == None) and (found_in_explored == None):
                frontier.append(child)
                num_explored = num_explored + 1
            elif (found_in_frontier != None) and (found_in_frontier.cost>child.cost):
                frontier.remove(found_in_frontier)
                frontier.append(child)
    
    print "No path found, explored: ", num_explored

    return None
def goal_check(start_list, stop_list):
    for item1 in start_list:
        for item2 in stop_list:
            if item1.node['data'].id == item2.node['data'].id:
                #print "equal node = ", item1.node['data'].id
                return True

    return False
def reverse_path(start_list, stop_list):
    reversed_stop_list = []
    last_stop = stop_list[len(stop_list)-1]
    last_start = start_list[len(start_list)-1]
    for item in stop_list:
        reversed = State(item.parent, item.node)
        reversed_stop_list.append(reversed)
    reversed_stop_list.pop(len(reversed_stop_list)-1)
    start_list.append(State(last_stop.node, last_start.node))
    start_list.append(reversed_stop_list)
    return reversed_stop_list[0]

def print_list(list):
    for item in list:
        if item.parent != None and item.node != None:
            print item.node['data'].id, " ", item.parent['data'].id
        else:
            print item.node['data']

#def find_node(start_list, stop_list):

def bi(graph, start, goal):
    if start == goal:
        print "START === GOAL"
        return None

    frontier_start = [start]
    frontier_goal = [goal]
    explored_start = []
    explored_goal = []
    num_start = 0
    num_goal = 0
    while (len(frontier_start)>0) and (len(frontier_goal) > 0):
        
        start_node = frontier_start.pop(0)
        explored_start.append(start_node)
        for edge in networkx.edges(graph, start_node.node['data'].id):
            child = State(graph.node[edge[1]], start_node)
            if (child not in explored_start) and (child not in frontier_start): #and (child not in explored_goal) and (child not in frontier_goal):
                # Goal check
                if goal_check(frontier_start, frontier_goal):
                    print "Goal found, explored: ", num_start+num_goal, "\n\n"
                    # reverse child and parent
                    
                    #print_list(frontier_start)
                    return reverse_path(frontier_start, frontier_goal)
                else:
                    frontier_start.append(child)
                num_start = num_start + 1

        goal_node = frontier_goal.pop(0)
        explored_goal.append(goal_node)
        for edge in networkx.edges(graph, goal_node.node['data'].id):
            child = State(graph.node[edge[1]], goal_node)
            if (child not in explored_goal) and (child not in frontier_goal):
                #and (child not in explored_start) and (child not in frontier_start):
                # Goal check
                if goal_check(frontier_start, frontier_goal):
                    print "Goal found, explored: ", num_start+num_goal, "\n\n"
                    # reverse child and parent
                    
                    #print_list(frontier_start)
                    return reverse_path(frontier_start, frontier_goal)
                else:
                    frontier_goal.append(child)
                num_goal = num_goal + 1

    print "No path found, explored: ", num_start+num_goal

    return None

def tri(graph, state_1, state_2, state_3):
    if state_1 == state_2 and state2 == state_3:
        print "3 CITIES EQUAL"
        return None
    frontier_1 = [state_1]
    frontier_2 = [state_2]
    frontier_3 = [state_3]
    explored_1 = []
    explored_2 = []
    explored_3 = []
    num_1 = 0
    num_2 = 0
    num_3 = 0
    while (len(frontier_1)>0) and (len(frontier_2)>0) and (len(frontier_3)>0):
        node_1 = frontier_1.pop(0)
        explored_1.append(node_1)
        for edge in networkx.edges(graph, node_1.node['data'].id):
            child = State(graph.node[edge[1]], node_1)
            if (child not in explored_1) and (child not in frontier_1):
                # Goal check
                if goal_check(frontier_1, frontier_2) and goal_check(frontier_2, frontier_3):
                    print "Goal found, explored: ", num_1+num_2+num_3, "\n\n"

                    #return value
                    return child
                else:
                    frontier_1.append(child)
                num_1 = num_1 + 1

        node_2 = frontier_2.pop(0)
        explored_2.append(node_2)
        for edge in networkx.edges(graph, node_2.node['data'].id):
            child = State(graph.node[edge[1]], node_2)
            if (child not in explored_2) and (child not in frontier_2):
                if goal_check(frontier_1, frontier_2) and goal_check(frontier_2, frontier_3):
                    print "Goal found, explored: ", num_1+num_2+num_3, "\n\n"

                    #return value
                    return child
                else:
                    frontier_2.append(child)
                num_2 = num_2 + 1

        node_3 = frontier_3.pop(0)
        explored_3.append(node_3)
        for edge in networkx.edges(graph, node_3.node['data'].id):
            child = State(graph.node[edge[1]], node_3)
            if (child not in explored_3) and (child not in frontier_3):
                if goal_check(frontier_1, frontier_2) and goal_check(frontier_2, frontier_3):
                    print "Goal found, explored: ", num_1+num_2+num_3, "\n\n"
                    return child
                else: frontier_3.append(child)
                num_3 = num_3 + 1
    print "No path found, explored: ", num_1+num_2+num_3
    return None


"""
Backtrack and output your solution
"""
def backtrack(state, graph):
    if state.parent != None:
        print "Node: ", state.node['data'].id
        if len(state.node['data'].tags) > 0:            
            for key in state.node['data'].tags.keys():
                print "       N: ", key, " ", state.node['data'].tags[key]        
              
        for edge in networkx.edges(graph, state.node['data'].id):
            if len(graph.node[edge[1]]['data'].tags) > 0:
                for key in graph.node[edge[1]]['data'].tags:
                    print "       E: ", graph.node[edge[1]]['data'].tags[key]
        backtrack(state.parent, graph)


"""
The setup
"""

print "\n\n----- 6601 Grad AI: Seaching ATLANTA ------\n\n"
only_roads = True
graph = read_osm('atlanta.osm', only_roads)

start_num = random.randint(0, len(graph.nodes()))
stop_num = random.randint(0, len(graph.nodes()))
inter_num = random.randint(0, len(graph.nodes()))

start     = graph.node[graph.nodes()[start_num]]
stop      = graph.node[graph.nodes()[stop_num]]
inter     = graph.node[graph.nodes()[inter_num]]

print "NUMBER OF NODES: ", len(graph.nodes())
print "NUMBER OF EDGES: ", len(graph.edges())
print "START:           ", start['data'].id
print "STOP :           ", stop['data'].id
print "INTER:           ", inter['data'].id

state = bfs(graph, State(start, None), State(stop, None))
state = bfs(graph, State(stop, None), State(inter, None))
#state = ucs(graph, State(start, None), State(stop, None))
#state = None
#if state != None:
#    backtrack(state, graph)

print "\n\n"
#state = bfs(graph, State(start, None), State(stop, None))
state = ucs(graph, State(start, None), State(stop, None))
state = ucs(graph, State(stop, None), State(inter, None))
#state = None
#if state != None:
#    backtrack(state, graph)

print "\n\n"

state = a_star(graph, State(start, None), State(stop, None))
state = a_star(graph, State(stop, None), State(inter, None))
#state = None
#if state != None:
#    backtrack(state, graph)

print "\n\n"

state = bi(graph, State(start, None), State(stop, None))
state = bi(graph, State(stop, None), State(inter, None))

'''if state != None:
    backtrack(state, graph)'''
print "\n\n"
state = tri(graph, State(start, None), State(inter, None), State(stop, None))