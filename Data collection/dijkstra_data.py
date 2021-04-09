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

def main(road_network,path):
    #path length is length of path list
    room_num = len(path) - 1

    #finds the number of turns
    turn_num = 0
    prev_direction = None
    #keeps seeing if there is a path between the current room and the next room in the path
    #until it finds a room that is not reachable, there is a turn required
    for index in xrange(0,len(path)-1):
        if index == 0:
            current = path[index]
        next = path[index+1]
        sub_path = find_path(road_network,current,next)

        if sub_path == None:
            current = path[index]
            turn_num +=1

    return room_num,turn_num
