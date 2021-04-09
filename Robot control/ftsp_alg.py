from __future__ import division
from __future__ import absolute_import

def find_path(road_network,current_vertex,target_vertex):
    sub_path =[]
    indexes = []
    #find indexes of current_vertex
    for row in xrange(0, len(road_network)):
        for col in xrange(0,len(road_network[row])):
            if road_network[row][col] == current_vertex:
                indexes.append([row,col])

    directions = [[0,-1],[-1,0],[0,1],[1,0]]#left up right down
    #for each instance of current_vertex go in all four directions to see if there is a path to the target vertex
    for index in indexes:
        for direction in directions:
            row = index[0]
            col = index[1]
            current_vertex = road_network[row][col]
            sub_path= [current_vertex]
            #checks if the current vertex is not a empty cell
            while current_vertex != "none":
                row += direction[0]
                col += direction[1]
                #checks if the coordinates are valid
                if row < len(road_network) and row>=0:
                    if col <len(road_network[0]) and col>=0:
                        current_vertex = road_network[row][col]
                        #if the current vertex is not an empty cell and isn't already the same as the starting room or in the path
                        #this removes duplicate instances of the same room name
                        if current_vertex != "none" and current_vertex != road_network[index[0]][index[1]] and not any(current_vertex == vertex1 for vertex1 in sub_path):
                            sub_path.append(current_vertex)
                        if current_vertex == target_vertex:
                            del sub_path[0]
                            return sub_path
                    else:
                        current_vertex = "none"
                else:
                    current_vertex = "none"

    return None
def find_zero_reachable(road_network,current_vertex):
    zero_reachable =[]
    indexes = []
    #find indexes of current_vertex
    for row in xrange(0, len(road_network)):
        for col in xrange(0,len(road_network[row])):
            if road_network[row][col] == current_vertex:
                indexes.append([row,col])

    directions = [[0,-1],[-1,0],[0,1],[1,0]]#left up right down
    #for each instance of current_vertex go in all four directions to see if there is a path to the target vertex
    for index in indexes:
        for direction in directions:
            row = index[0]
            col = index[1]
            current_vertex = road_network[row][col]
            while current_vertex != "none":
                row += direction[0]
                col += direction[1]
                #checks if the coordinates are valid
                if row < len(road_network) and row>=0:
                    if col <len(road_network[0]) and col>=0:
                        current_vertex = road_network[row][col]
                        #if the current vertex is not an empty cell and isn't already the same as the starting room or in the path
                        #this removes duplicate instances of the same room name
                        if current_vertex != "none" and current_vertex != road_network[index[0]][index[1]] and not any(current_vertex == vertex1 for vertex1 in zero_reachable):
                            zero_reachable.append(current_vertex)
                    else:
                        current_vertex = "none"
                else:
                    current_vertex = "none"
    return zero_reachable


def forward_search(road_network,start,target):
    HG = [] # ["H","J",["B","K"]]
    vertex_colour = {}

    #fills in vertex_colour with a vertex letter and a corresponding colour
    for road in road_network:
        for vertex in road:
            #check whether vertex is in vertex_colour
            if not any(vertex == vertex1 for vertex1 in vertex_colour):
                if vertex == start:
                    vertex_colour[vertex] ="gray"
                else:
                    vertex_colour[vertex] = "white"

    Q = [start]
    hf = start
    buffer_add = []
    first_loop = True
    while first_loop or not any(target ==index for index in HG[-1] ):
        try:
            current_vertex = Q.pop(0)
        except IndexError as error:
            return "path not possible"

        #find all the zero level reachable points for current_vertex
        zero_reachable = find_zero_reachable(road_network,current_vertex)
        # if vertex is white, add zero_reachable vertexes to Q and set to gray
        for vertex in zero_reachable:
            #find colour of vertex
            if vertex_colour[vertex] == "white":
                vertex_colour[vertex] = "gray"
                Q.append(vertex)

        #set current vertex to black and add to HG
        vertex_colour[current_vertex] = "black"
        buffer_add.append(current_vertex)


        if hf not in Q:
            HG.append(buffer_add)
            buffer_add = []
            if len(Q)>0:
                hf = Q[-1]
        if first_loop == True:
            first_loop = False
    return HG

def backward_cleaning(HG,target,road_network):
    # remove all vertexes that aren't the target in layer N
    n = len(HG)-1
    edges = []
    for element in HG[n]:
        if element != target:
            HG[-1].remove(element)
    #remove vertexes in layer n-1 if they aren't zero level reachable from layer n
    for layer in xrange(n-1,-1,-1):
        #find zero level reachable from layer n
        zero_reachable = []
        for vertex in HG[layer+1]:
            current_vertex_reachable = find_zero_reachable(road_network,vertex)
            for element in current_vertex_reachable:
                if current_vertex_reachable not in zero_reachable:
                    zero_reachable.append(element)
        #remove non zero level reachable from layer n-1
        temp = HG[layer][:]
        for vertex in temp:
            if vertex not in zero_reachable:
                HG[layer].remove(vertex)

        # add edge to link two zero level reachable vertexes between layer n and n-1
        for vertex in HG[layer]:
            current_vertex_reachable = find_zero_reachable(road_network,vertex)
            for element in current_vertex_reachable:
                 if element in HG[layer+1]:
                     edges.append([vertex, element])

        G_star = HG[:]
        #generate graph
        graph = {}
        for layer in G_star:
            for vertex in layer:
                graph[vertex] = {}

        for edge in edges:
            sub_path = find_path(road_network,edge[0],edge[1])
            temp_sub_path = sub_path[:]
            safe_index = None
            for room_index in xrange(0,len(temp_sub_path)-2):
                if "floor" in temp_sub_path[room_index] and room_index != safe_index:
                    start_floor = temp_sub_path[room_index]
                    end_floor = temp_sub_path[room_index+2]
                    if start_floor[:-1] != end_floor[:-1] and "stairs" in temp_sub_path[room_index+1]:
                        sub_path.remove(temp_sub_path[room_index+1])
                    else:
                        safe_index = room_index +2
            graph[edge[0]][edge[1]] = len(sub_path)
    return graph

def dijkstra(graph,start,target):
    unvisited = {}
    visited = {}

    #adds all the vertexes to the unvisited list
    for vertex in graph:
        unvisited[vertex] = [None,float(u'inf')]
    unvisited[start] = [None,0]

    # while rooms in unvisited
    while len(unvisited)>0:
        first = True
        #finds the next unvisited room based on lowest cost
        for vertex in unvisited:
            if first == True:
                lowest_cost = unvisited[vertex][1]
                lowest_vertex = vertex
                first = False
            else:
                if unvisited[vertex][1] < lowest_cost:
                    lowest_cost = unvisited[vertex][1]
                    lowest_vertex = vertex

        #moves the new room and adds vertex, previous vertex and cost to visited
        current_vertex = lowest_vertex
        for vertex in graph[current_vertex]:
            if vertex not in visited:
                cost = unvisited[current_vertex][1] + graph[current_vertex][vertex]
                if cost < unvisited[vertex][1]:
                    unvisited[vertex][0] = current_vertex
                    unvisited[vertex][1] = cost
        visited[current_vertex] = unvisited.pop(current_vertex)

    path = []

    # follows the previous verticess backwards from target to find path
    current_vertex = target
    path.append(target)
    while current_vertex != start:
        current_vertex = visited[current_vertex][0] # set previous target to current target
        path.append(current_vertex)
    path.reverse()
    return path


def main(road_network, start, target):
    HG = forward_search(road_network, start, target)
    # this is for when the target is not possible
    if HG == "path not possible":
        return "failed"
    else:
        graph = backward_cleaning(HG,target,road_network)
        path = dijkstra(graph,start,target)
        return path
