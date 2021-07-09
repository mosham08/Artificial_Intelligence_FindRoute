# Mohammad Abdellatif 
# 1001534657
# CSE 4308
import sys
from queue import PriorityQueue


def input_file(filename): # Reads file
    graph = {}
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()
    for line in lines[:-1]:
        data = line.split()
        if data == 'END OF INPUT':
            return graph
        else:
            if data[0] in graph:
                graph[data[0]][data[1]] = float(data[2])
            else:
                if data[2] == 'INPUT':
                    break
                graph[data[0]] = {data[1]: float(data[2])}
            if data[1] in graph:
                graph[data[1]][data[0]] = float(data[2])
            else:
                graph[data[1]] = {data[0]: float(data[2])}
    return graph


def input_file_heuristic(filename): # Reads the heuristic file
    val = {}
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()
    for line in lines[:-1]:
        data = line.split()
        if data == 'END OF INPUT':
            return val
        else:
            if data[1] == 'OF':
                break
            val[data[0]] = float(data[1])
    return val


def uninformed_search(node, graphnode, graph): # Uninformed search
    generated = 0
    expanded = 0
    fringe = PriorityQueue()
    fringe.put((0, node))
    visited = {}
    visited[node] = ("", 0)
    parsed = []
    max_node = 0
    while not fringe.empty():
        if len(fringe.queue) > max_node:
            max_node = len(fringe.queue)
        _, node_count = fringe.get()
        expanded += 1
        if node_count == graphnode:
            break
        if node_count in parsed:
            continue
        parsed.append(node_count)
        for i in graph[node_count]:
            generated += 1
            fringe.put((graph[node_count][i]+visited[node_count][1], i))
            if i not in visited:
                visited[i] = (node_count, graph[node_count][i]+visited[node_count][1])
    route = []
    distance = "infinity"
    if graphnode in visited:
        distance = 0.0
        node_count = graphnode
        while node_count != node:
            distance += graph[visited[node_count][0]][node_count]
            route.append(node_count)
            node_count = visited[node_count][0]
    return route, expanded, generated, distance, max_node


def informed_search(snode, gnode, graph, val): # Informed search
    generated = 0
    expanded = 0
    fringe = PriorityQueue()
    fringe.put((0, snode))
    visited = {}
    visited[snode] = ("", 0)
    explored = []
    mnode = 0
    while not fringe.empty():
        if len(fringe.queue) > mnode:
            mnode = len(fringe.queue)
        _, countnode = fringe.get()
        expanded += 1
        if countnode == gnode:
            break
        if countnode in explored:
            continue
        explored.append(countnode)
        for i in graph[countnode]:
            generated += 1
            if i not in visited:
                visited[i] = (countnode, graph[countnode][i] + visited[countnode][1])
            fringe.put((graph[countnode][i] + visited[countnode][1] + val[i], i))
    route = []
    dist = "infinity"
    if gnode in visited:
        dist = 0.0
        countnode = gnode
        while countnode != snode:
            dist += graph[visited[countnode][0]][countnode]
            route.append(countnode)
            countnode = visited[countnode][0]
    return route, expanded, generated, dist, mnode


# Creating output
if len(sys.argv) == 4:
    file_name = sys.argv[1]
    src = sys.argv[2]
    dest = sys.argv[3]
    graph = input_file(file_name)
    route, expanded, generated, distance, max_node = uninformed_search(src, dest, graph)
    print("nodes expanded: {}".format(expanded))
    print("nodes generated: {}".format(generated))
    print("distance: {} km".format(distance))
    print("route:")
    node_count = src
    if len(route) == 0:
        print("none")
    else:
        for path in route[::-1]:
            print("{} to {}, {} km".format(node_count, path, graph[node_count][path]))
            node_count = path

elif len(sys.argv) == 5:
    file_name = sys.argv[1]
    src = sys.argv[2]
    dest = sys.argv[3]
    fname_h = sys.argv[4]
    graph = input_file(file_name)
    val = input_file_heuristic(fname_h)
    route, expanded, generated, distance, max_node = informed_search(src, dest, graph, val)
    print("nodes expanded: {}".format(expanded))
    print("nodes generated: {}".format(generated))
    print("distance: {} km".format(distance))
    print("route:")
    node_count = src
    if len(route) == 0:
        print("none")
    else:
        for path in route[::-1]:
            print("{} to {}, {} km".format(node_count, path, graph[node_count][path]))
            node_count = path