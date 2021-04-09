from __future__ import division
from __future__ import absolute_import
def graph_prep(road_network):
    graph = {}
    for row in xrange(0, len(road_network)):
        for col in xrange(0,len(road_network[row])):
            current_vertex =road_network[row][col].lower()
            if current_vertex != "none":
                # checks if vertex is already in graph. If it isn't, add the new entry
                if not any( current_vertex == vertex for vertex in graph):
                    graph[current_vertex] = {}

                # find the adjacent rooms and add any new adjacent rooms to the entry
                directions = [[0,-1],[-1,0],[0,1],[1,0]]#left up right down
                for direction in directions:
                    #calculates row and col position for adjacent vertexes
                    temp_row = row + direction[0]
                    temp_col = col + direction[1]

                    #checks that the row and col position is valid
                    if temp_row < len(road_network) and temp_row>=0:
                        if temp_col <len(road_network[0]) and temp_col>=0:
                            # finds name of adjacent room
                            temp_vertex = road_network[temp_row][temp_col].lower()
                            # if the adjacent room isn't labelled None or the same name as the temp room or isn't already in the adjacent room dictionary
                            if temp_vertex != "none" and temp_vertex != current_vertex and not any(temp_vertex == vertex for vertex in graph[current_vertex]):
                                #adds adjacent room with a cost of 1
                                graph[current_vertex][temp_vertex] = 1

    return graph

def dijkstra(graph,start,target):
    unvisited = {}
    visited = {}

    for vertex in graph:
        unvisited[vertex] = [None,float(u'inf')]
    unvisited[start] = [None,0]

    while len(unvisited)>0:
        first = True
        for vertex in unvisited:
            if first == True:
                lowest_cost = unvisited[vertex][1]
                lowest_vertex = vertex
                first = False
            else:
                if unvisited[vertex][1] < lowest_cost:
                    lowest_cost = unvisited[vertex][1]
                    lowest_vertex = vertex

        current_vertex = lowest_vertex
        for vertex in graph[current_vertex]:
            if vertex not in visited:
                cost = unvisited[current_vertex][1] + graph[current_vertex][vertex]
                if cost < unvisited[vertex][1]:
                    unvisited[vertex][0] = current_vertex
                    unvisited[vertex][1] = cost
        visited[current_vertex] = unvisited.pop(current_vertex)

    path = []

    current_vertex = target
    path.append(target)
    while current_vertex != start:
        current_vertex = visited[current_vertex][0] # set previous target to current target
        path.append(current_vertex)

    path.reverse()
    return path


def main(road_network, start, target):
    graph = graph_prep(road_network)
    path = dijkstra(graph,start,target)

    return path
