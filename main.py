from collections import deque
from heapq import heappush, heappop 
import math

def shortest_shortest_path(graph, source):
    """
    Params: 
      graph.....a graph represented as a dict where each key is a vertex
                and the value is a set of (vertex, weight) tuples (as in the test case)
      source....the source node
      
    Returns:
      a dict where each key is a vertex and the value is a tuple of
      (shortest path weight, shortest path number of edges). See test case for example.
    """
    dist_lst = {node: math.inf for node in graph}
    weight_lst = {node: math.inf for node in graph}

    dist_lst[source] = 0
    weight_lst[source] = 0
    frontier = [(0, source)]
    while frontier:
        dist, top = heappop(frontier)
        for neighbor, weight in graph[top]:
            if dist_lst[neighbor] == math.inf or dist_lst[neighbor] > dist + 1:
                dist_lst[neighbor] = dist + 1
                weight_lst[neighbor] = weight_lst[top] + weight
                heappush(frontier, (dist+1, neighbor))
    result = {}
    for node in graph:
        result[node] = (weight_lst[node], dist_lst[node])
    return result
                

    
def test_shortest_shortest_path():

    graph = {
                's': {('a', 1), ('c', 4)},
                'a': {('b', 2)}, # 'a': {'b'},
                'b': {('c', 1), ('d', 4)}, 
                'c': {('d', 3)},
                'd': {},
                'e': {('d', 0)}
            }
    result = shortest_shortest_path(graph, 's')
    # result has both the weight and number of edges in the shortest shortest path
    assert result['s'] == (0,0)
    assert result['a'] == (1,1)
    assert result['b'] == (3,2)
    assert result['c'] == (4,1)
    assert result['d'] == (7,2)
    
    
def bfs_path(graph, source):
    """
    Returns:
      a dict where each key is a vertex and the value is the parent of 
      that vertex in the shortest path tree.
    """
    queue = deque()
    queue.append(source)
    parent = {source: None}
    while queue:
        first = queue.popleft()
        for node in graph[first]:
            if node not in parent:
                parent[node] = first
                queue.append(node)
    del parent[source]
    return parent

def get_sample_graph():
     return {'s': {'a', 'b'},
            'a': {'b'},
            'b': {'c'},
            'c': {'a', 'd'},
            'd': {}
            }

def test_bfs_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert parents['a'] == 's'
    assert parents['b'] == 's'    
    assert parents['c'] == 'b'
    assert parents['d'] == 'c'
    
def get_path(parents, destination):
    """
    Returns:
      The shortest path from the source node to this destination node 
      (excluding the destination node itself). See test_get_path for an example.
    """
    paths = []
    while destination in parents:
        paths.append(parents[destination])
        destination = parents[destination]
    paths = paths[::-1]
    return "".join(paths)

def test_get_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert get_path(parents, 'd') == 'sbc'

test_shortest_shortest_path()
test_bfs_path()
test_get_path()