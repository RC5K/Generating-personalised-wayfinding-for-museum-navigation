import openpyxl
def room_list_generator(road_network):
    room_list = []
    #for each cell in the excel map
    for row in xrange(0, len(road_network)):
        for col in xrange(0,len(road_network[row])):
            current_vertex = road_network[row][col]
            if current_vertex != "none":
                # checks if vertex is already in room_list. If it isn't, add the new entry
                if not any( current_vertex == vertex for vertex in room_list):
                    room_list.append(current_vertex)
    return room_list

def map_import():
    wb = openpyxl.load_workbook("road network map.xlsx")
    ws = wb["Map"]
    road_network = []
    #add every cell to the road_network
    for row in ws.iter_rows(min_row=1):
        temp = []
        for col in xrange(0,len(row)):
            temp.append(unicode(row[col].value).lower())
        road_network.append(temp)
    return road_network

def main():
    configuration_file = open("configuration.txt","r+")
    backup_file = open("configuration_backup.txt","w")

    #backup config file to backup file
    for line in configuration_file:
        backup_file.write(line)

    print "Enter host and port in format host:port"
    ip_and_port = raw_input()
    configuration_file.seek(0)
    configuration_file.write(ip_and_port+'\n')
    configuration_file.truncate()

    condition = True
    #keeps asking until a valid input is given
    while condition:
        print "Operating location of the robot"
        location = raw_input()
        road_network = map_import()
        room_list = room_list_generator(road_network)
        if any(location == room for room in room_list):
            configuration_file.write(location+'\n')
            configuration_file.truncate()
            condition = False
        else:
            print "Invalid room"
    configuration_file.close()
main()
