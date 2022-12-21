'''
Computer project
'''
import doctest
from typing import Dict, List


def task_1():
    pass

def task_2():
    pass

def task_3():
    pass

def task_4(vertices:int, graph: Dict[int, int]) -> List[int]:
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
    # Checks whether appropriate input data type
    if not isinstance(vertices, int) or not isinstance(graph, dict):
        return

    # result is list which contains minimum vertex id of scc
    result = []

    # obhid is list which contains position of vertex or -1 if vertex was not visited
    obhid = [-1] * vertices

    # low is a list, which contains low-link values of every verrtice
    # or -1 if this vertice was not discovered
    low = [-1] * vertices

    # Stack which maintains valid verices for scc
    stack = []


    for vertice in range(vertices):

        # If verices was not previously visited than run script recur_scc (dfs)
        if obhid[vertice] == -1:
            recur_scc(result, obhid, vertice, low, stack, graph)

    # If all verices are visited than return result
    return result

def recur_scc(result, obhid, vertice, low, stack, graph):
    '''
    Dfs based function for recursion to determine minimum vertex id of scc
    '''
    # Adding id to obhid
    obhid[vertice] =  len(stack)
    # Initializing low-link value of vertice
    low[vertice] = len(stack)
    # Adding vertice to stack of valid vertices
    stack.append(vertice)

    if vertice in graph:

        # Goes throught every adjacent vertice
        for adjacent in graph[vertice]:

            # If next vertice is not visited than we will visit
            # it and take minimum of low-link values
            if len(obhid) > adjacent and obhid[adjacent] == -1:
                recur_scc(result, obhid, adjacent, low, stack, graph)
                low[vertice] = min(low[vertice], low[adjacent])

            # If next vertice is in stack than we take minimum
            # of low link value of current vertice and id of adjacent vertice
            elif adjacent in stack:
                # Takes minimum of low link and id (not low-link and low-link)
                # because i
                low[vertice] = min(low[vertice], low[adjacent])

    # If vertice is head of subgraph we take all vertices
    # before it in stack and take minimum of them
    if low[vertice] == obhid[vertice]:

        ver = stack.pop()
        min_vertice = ver
        while ver != vertice:
            # Takes vertice from the top of the stack and deletes it
            ver = stack.pop()
            if min_vertice > ver:
                min_vertice = ver

        result.append(min_vertice)

def task_5():
    pass

def task_6():
    pass
