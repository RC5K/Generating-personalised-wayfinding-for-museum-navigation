def find_path(road_network,current_vertex,target_vertex):
    sub_path =[]
    indexes = []
    #find all instances of current_vertex in the excel map
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

def path_filler(road_network,path):
    new_path = []
    #fills in the path with all the rooms it goes through
    for index in xrange(0,len(path)-1):
        current = path[index]
        next_room = path[index+1]
        sub_path = find_path(road_network,current,next_room)
        if index ==0:
            new_path.append(current)
        for room in sub_path:
            new_path.append(room)
    temp_new_path = new_path[:]
    safe_index = None
    # deletes the extra rooms for floors and stairs
    for room_index in xrange(0,len(temp_new_path)-2):
        if "floor" in temp_new_path[room_index] and room_index != safe_index:
            start_floor = temp_new_path[room_index]
            end_floor = temp_new_path[room_index+2]
            if start_floor[:start_floor.rindex(' ')] != end_floor[:end_floor.rindex(' ')] and "stairs" in temp_new_path[room_index+1]:
                new_path.remove(temp_new_path[room_index+1])
            else:
                safe_index = room_index +2
    return new_path

def main(road_network,ftsp_path):
    #turn number is just the length of the path since the rooms in the path are turning rooms
    turn_num = len(ftsp_path) -2
    new_path = path_filler(road_network,ftsp_path)
    room_num = len(new_path) - 1
    return room_num,turn_num,new_path
