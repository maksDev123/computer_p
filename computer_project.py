'''
Computer project
'''

import doctest
from typing import Dict, List
import copy

def task_1(path:str, directed:bool = False) -> dict[int, list[int]]:
    '''
    Function reads file by path
    If directed is True than graph will be read taking into account direction of edges.
    If directed is False than reading won't take into account direction of edges.

    Input:
    path - path to file,
    directed - whether graph is directed or not.

    Output:
    graph - dictionary of connectivity
    '''
    if directed is None:
        directed = False
    with open(path,'r',encoding='utf-8') as file: # open file
        lines = file.readlines() # return all lines in the file, as a list
        lst = [line.strip().split(',') for line in lines] # create list of edges
    new_lst = [[int(x) for x in inner] for inner in lst] # convert string numbers to int
    # following code converts a list of edges into a dictionary
    dicti={}
    if directed is False:
        for n_1,n_2 in new_lst:
            if n_1 not in dicti:
                dicti[n_1] = []
            dicti[n_1].append(n_2)
            if n_2 not in dicti:
                dicti[n_2] = []
            dicti[n_2].append(n_1)
    if directed is True:
        for n_1,n_2 in new_lst:
            if n_1 not in dicti:
                dicti[n_1] = []
            dicti[n_1].append(n_2)
    return dicti # return dictionary, that represents graph

def task_2(path:str, graph:dict[int, list[int]], directed:bool = False) -> None:
    '''
    Function writes the graph to a file given as dictionary of connectivity
    If directed is True than graph will be written taking into account direction of edges.
    If directed is False than writing won't take into account direction of edges.

    Input:
    path - path to file,
    graph - dictionary of connectivity,
    directed - whether graph is directed or not.

    Output:
    None
    '''
    edges = []
    with open(path,'w',encoding='utf-8') as file:

        for vertice_1 in graph:
            for vertice_2 in graph[vertice_1]:
                if directed is False and f"{vertice_2},{vertice_1}\n" not in edges:
                    edges.append(f'{vertice_1},{vertice_2}\n')
                elif directed is True:
                    edges.append(f'{vertice_1},{vertice_2}\n')

        file.write("".join(edges))
    return

def task_3(graph: dict[int, list[int]]) -> int:
    '''
    Functions finds connectivity components abd returns them as list, where each list
    represents connectivity component as list of it's nodes
    >>> task_3({1: [2, 4, 3], 2: [1, 3], 3: [2, 1], 4: [1],9:[10],10:[9],11:[]})
    [[1, 2, 3, 4], [9, 10], [11]]
    '''
    nodes=list(graph.keys()) #list of nodes
    visited = [] # visited nodes in DFS
    glob=[] # list to return
    def dfs(graph,node):
        '''
        DFS function that helps me find all nodes of connectivity node
        '''
        if node not in visited:
            visited.append(node)
            for new_node in graph[node]:
                dfs(graph,new_node)
        return visited
    while nodes: #while len(nodes) != 0
        temp=dfs(graph,nodes[0]) # list of nides in exact connectivity component
        glob.append(list(temp)) # Add connectivity node to list, that will be returned
        nodes=[i for i in nodes if i not in visited] # Delete all nodes of connectivity/
                                                     # component from list of all nodes
        visited.clear() # Clear list of visited nodes
                        # to prepare it for execution of the breadth-first search function
    return glob # return result

def task_4(n_vertices:int, graph: Dict[int, int]) -> List[int]:
    '''
    Finds and return strongly connected comnonents and returns
    list of integer that represent lowest of vertices for this component
    If data type is inappropriate than None will be returned.

    Input: vertices - number of vertices, graph - dictionary of connectivity
    Output: list of lowest id of every scc

    >>> task_4("a", {1: [2], 2: [1]})
    >>> task_4(2, [0, 1])
    >>> task_4(5 ,{1: [0], 0: [2, 3], 2: [1], 3: [4]})
    [4, 3, 0]
    >>> task_4(4 ,{0: [1], 1: [2], 2: [3]})
    [3, 2, 1, 0]
    >>> task_4(7 ,{0: [1], 1: [2, 3, 4, 6], 2: [0], 3: [5], 4: [5]})
    [5, 3, 4, 6, 0]
    >>> task_4(5 ,{0: [1], 1: [2], 2: [3, 4], 3: [0], 4: [2]})
    [0]
    >>> task_4(11,{0: [1, 3], 1: [2, 4], 2: [0, 6], 3: [2], 4: [5, 6],\
    5: [6, 7, 8, 9], 6: [4], 7: [9], 8: [9], 9: [8]})
    [8, 7, 4, 0, 10]
    >>> task_4(0, {})
    []
    >>> task_4(3, {1: [2], 2: [1]})
    [0, 1]

    This was made using tarjan algorithm for scc.
    '''
    # Initialize index (id)
    index = 0
    # Checks whether appropriate input data type
    if not isinstance(n_vertices, int) or not isinstance(graph, dict):
        return

    # result is list which contains minimum vertex id of scc
    result = []

    # traversal is list which contains position of vertex or -1 if vertex was not visited
    traversal = [-1] * n_vertices

    # low is a list, which contains low-link values of every verrtice
    # or -1 if this vertice was not discovered
    low_link = [-1] * n_vertices

    # Stack which maintains valid verices for scc
    stack = []


    for vertice in range(n_vertices):

        # If verices was not previously visited than run script recur_scc (dfs)
        if traversal[vertice] == -1:
            index = recur_scc(index, result, traversal, vertice, low_link, stack, graph)

    # If all verices are visited than return result
    return result

def recur_scc(index, result, traversal, vertice, low, stack, graph):
    '''
    Dfs based function for recursion to determine minimum vertex id of scc
    '''
    # Adding id to traversal
    traversal[vertice] = index

    # Initializing low-link value of vertice
    low[vertice] = index

    # Adding one to id
    index += 1

    # Adding vertice to stack of valid vertices
    stack.append(vertice)

    if vertice in graph:

        # Goes throught every adjacent vertice
        for adjacent in graph[vertice]:

            # If next vertice is not visited than we will visit
            # it and take minimum of low-link values
            if len(traversal) > adjacent and traversal[adjacent] == -1:
                index = recur_scc(index, result, traversal, adjacent, low, stack, graph)
                low[vertice] = min(low[vertice], low[adjacent])

            # If next vertice is in stack than we take minimum
            # of low link value of current vertice and id of adjacent vertice
            elif adjacent in stack:
                # Takes minimum of low link and id (not low-link and low-link)
                # because i
                low[vertice] = min(low[vertice], low[adjacent])

    # If vertice is head of subgraph we take all vertices
    # before it in stack and take minimum of them
    if low[vertice] == traversal[vertice]:

        ver = stack.pop()
        min_vertice = ver
        while ver != vertice:
            # Takes vertice from the top of the stack and deletes it
            ver = stack.pop()
            if min_vertice > ver:
                min_vertice = ver

        result.append(min_vertice)
    return index

def task_5(graph: Dict[int, int]) -> List[tuple]:
    """
    A function that finds the bridges in the graph and returns a list of them.
    If there are no bridges in the graph, then returns None.

    Input: graph - graph in the form of as dictionary
    Output: bridges - list of bridges in graph

    >>> task_5({1: [4, 3], 4: [1, 2, 3], 3: [1, 4], 2: [4]})
    [(4, 2)]
    >>> task_5({1: [2], 2: [1, 3, 5], 3: [2, 4, 6], 4: [3], 5:[2, 6], 6:[3, 5]})
    [(1, 2), (3, 4)]
    >>> task_5({1: [2, 3], 2: [1, 4], 3: [1, 4], 4: [2, 3]})
    >>> task_5({1: [2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4]})
    [(1, 2), (2, 3), (3, 4), (4, 5)]
    """
    # Creation the copy of given graph. And creating needed variables
    new_graph = copy.deepcopy(graph)
    bridges = []
    edges = []
    # For loop iteration for transorming given graph to tuple with edges.
    for key in graph.keys():
        for elem in graph[key]:
            edge = (key, elem)
    # A module to prevent circular dependency, like (2,3) and (3,2).
            if (elem, key) in edges:
                continue
            edges.append(edge)
    # A module to check whether the edge is a bridge or not.
    for edge in edges:
    # Removing each edge from graph
        new_graph[edge[0]].remove(edge[1])
        new_graph[edge[1]].remove(edge[0])
    # Checking whether without this component graph is connected.
        if len(task_3(new_graph)) != 1:
            bridges.append(edge)
    # Deepcopying new graph to try an algorithm with a different edge.
        new_graph = copy.deepcopy(graph)
    # When graph has no bridges you return None.
    if not bridges:
        return None
    # Returning the list with bridges.
    return bridges

def task_6(graph: Dict[int, int]) -> List[int]:
    """
    Finds connected vertices in a graph, and as a result returns their list
    If they are missing, then returns None
    Input: graph - graph in the form of as dictionary
    Output: conect_vertices - list of connection vertices
    >>> task_6({1: [4, 3], 4: [1, 2, 3], 3: [1, 4], 2: [4]})
    [4]
    >>> task_6({1: [2], 2: [1, 3, 5], 3: [2, 4, 6], 4: [3], 5:[2, 6], 6:[3, 5]})
    [2, 3]
    >>> task_6({1: [2, 3], 2: [1, 4], 3: [1, 4], 4: [2, 3]})
    >>> task_6({1: [2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4]})
    [2, 3, 4]
    """

    #Create a new dictionary in order to store the edited graphs in it
    new_graph = copy.deepcopy(graph)

    #Create a list in which we will store connection vertices
    conect_vertices = []

    #Create a variable that will store the number of graph components
    lentgh_of_graph = len(task_3(graph))

    #Cycle that iterates over dictionary keys (vertices)
    for key in graph.keys():
        #Cycle that iterates over key variables and removes a vertex from the graph
        for elem in graph[key]:
            new_graph[elem].remove(key)
        del new_graph[key]

        #If the number of components has changed after removing a vertex,
        #then we add this vertex to the list
        if len(task_3(new_graph)) != lentgh_of_graph:
            conect_vertices.append(key)

        #Return the graph to its former content
        new_graph = copy.deepcopy(graph)

    #Checks if the list is empty
    if not conect_vertices:
        return None

    #Return list of connection vertices
    return conect_vertices

doctest.testmod()
