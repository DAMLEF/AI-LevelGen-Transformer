# This module is a special implementation (adapted to our map format) or A* algorithm
import numpy as np

import heapq

from game.map import *


class Node:
    def __init__(self, x: int, y: int, cost, heuristic):
        self.x = x
        self.y = y

        self.c = cost
        self.h = heuristic

    def get_heuristic(self):
        return self.h

    def get_cost(self):
        return self.c

    def get_value(self):
        return self.h + self.c

    def __eq__(self, other):
        return isinstance(other, Node) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return self.get_value() < other.get_value()


class StartNode(Node):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 0, 0)


class Queue:
    def __init__(self):
        self.c: list[Node] = []

    def empty(self):
        return self.c == []

    def enqueue(self, value: Node):
        self.c.append(value)

    def dequeue(self):
        if not self.empty():
            result = self.c[0]

            self.c = self.c[1:]

            return result

    def __contains__(self, item):
        return item in self.c


# Tas pour gérer les nœuds


class Heap:
    def __init__(self):
        self.c = []

    def enqueue(self, node):
        heapq.heappush(self.c, node)

    def dequeue(self):
        return heapq.heappop(self.c)

    def empty(self):
        return len(self.c) == 0

    def __contains__(self, item):
        return any(n == item for _, n in self.c)



def compare_heuristic(n1: Node, n2: Node):
    a = n1.get_heuristic()
    b = n2.get_heuristic()

    if a < b:
        return 1
    elif a == b:
        return 0
    else:
        return -1


def get_element(tab: list[Node], element):
    alternate_in = None
    for e in tab:
        if e.x == element.x and e.y == element.y:
            alternate_in = e
            break

    return alternate_in


def condition_node_validate(tab: list[Node], element: Node):
    if get_element(tab, element) is not None:
        return False
    return True


def reconstruct_path(path_map, end):
    total_path = [end]
    current = end
    while current in path_map:
        current = path_map[current]
        total_path.append(current)

    return total_path
    # return total_path[::-1]


def a_star(world: Map, end: tuple[float, float], start: tuple[float, float], neighbour_all_access: bool = False):
    closedQ = Queue()
    openQ = Heap()

    path = {}

    if not world.in_map(get_cell_pos(end)):
        return []

    node_start = Node(int(start[0]), int(start[1]), 0, distance2(start[0], start[1], end[0], end[1]))
    node_end = Node(int(end[0]), int(end[1]), 0, 0)

    openQ.enqueue(node_start)

    while not openQ.empty():
        e = openQ.dequeue()

        if e.x == node_end.x and e.y == node_end.y:
            return reconstruct_path(path, e)

        if not neighbour_all_access:
            neighbour = world.get_neighbour_walkable(e.x, e.y)
        else:
            neighbour = world.get_neighbour(e.x, e.y)

        for i, n in enumerate(neighbour):
            n_x, n_y = n[0], n[1]

            node = Node(n[0], n[1], e.c + distance2(e.x, e.y, n_x, n_y), distance2(n_x, n_y, node_end.x, node_end.y))

            if node not in closedQ:
                existing_node = get_element(openQ.c, node)

                if existing_node is None:
                    path[node] = e
                    openQ.enqueue(node)
                elif node.get_cost() < existing_node.get_cost():
                    # Chemin plus court trouvé, on remplace
                    openQ.c.remove(existing_node)
                    path[node] = e
                    openQ.enqueue(node)

        closedQ.enqueue(e)

    return []
