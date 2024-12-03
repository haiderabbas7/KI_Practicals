from graph import *
from queues import *


class Node:
    def __init__(self, name, parent=None, cost=0):
        self.name = name
        self.parent = parent
        self.cost = cost

    def __repr__(self):
        return f"{self.name}"


def get_path(node):
    path = []
    while node is not None:
        path.append(node.name)
        node = node.parent
    return path[::-1]


def get_path_cost(graph, path):
    total_cost = 0
    for i in range(len(path) - 1):
        start_node = next((node for node in graph.nodes if node.name == path[i]), None)
        if start_node is not None:
            edge = next((edge for edge in start_node.edges if edge.end.name == path[i + 1]), None)
            if edge is not None:
                total_cost += edge.value
    return total_cost


def bfs(graph, start, goal):
    frontier = FifoQueue()
    start_node = Node(start)
    frontier.enqueue(start_node)
    explored = []
    goal_node = None

    while not frontier.is_empty():
        current_node = frontier.dequeue()
        explored.append(current_node)

        if current_node.name == goal:
            goal_node = current_node

        for neighbor in graph.get_neighbors(current_node.name):
            # falls der Knoten nicht in explored ist, also noch nicht relaxed wurde, und nicht in frontier ist
            if (not any(node.name == neighbor for node in explored)
                    and not any(node.name == neighbor for node in frontier.nodes)):
                new_node = Node(neighbor, current_node)
                frontier.enqueue(new_node)
    path_to_root = get_path(goal_node) if goal_node else None
    path_cost = get_path_cost(graph, path_to_root) if path_to_root else None
    return goal_node, explored, path_to_root, path_cost


def dfs(graph, start, goal):
    frontier = LifoQueue()
    start_node = Node(start)
    frontier.push(start_node)
    explored = []
    goal_node = None

    while not frontier.is_empty():
        current_node = frontier.pop()
        explored.append(current_node)

        if current_node.name == goal:
            goal_node = current_node

        for neighbor in graph.get_neighbors(current_node.name):
            # falls der Knoten nicht in explored ist, also noch nicht relaxed wurde, und nicht in frontier ist
            if (not any(node.name == neighbor for node in explored)
                    and not any(node.name == neighbor for node in frontier.nodes)):
                new_node = Node(neighbor, current_node)
                frontier.push(new_node)
    path_to_root = get_path(goal_node) if goal_node else None
    path_cost = get_path_cost(graph, path_to_root) if path_to_root else None
    return goal_node, explored, path_to_root, path_cost


def ucs(graph, start, target):
    frontier = PrioQueue()
    start_node = Node(start)
    frontier.enqueue(start_node, start_node.cost)
    explored = []
    goal_node = None

    while not frontier.is_empty():
        current_node = frontier.dequeue()
        explored.append(current_node.name)

        if current_node.name == target:
            goal_node = current_node

        for neighbor in graph.get_neighbors(current_node.name):
            # holt sich die Kante, über der dieser Nachbar erreicht wird
            edge = graph.find_edge(current_node.name, neighbor)
            child = Node(neighbor, current_node, current_node.cost + edge.value)

            # wenn der Nachbarknoten weder besucht noch in frontier ist, pack ihn in frontier rein
            if (child.name not in explored) and (child.name not in [node[1].name for node in frontier.nodes]):
                # Füge den Knoten zur Warteschlange hinzu
                frontier.enqueue(child, child.cost)
            # wenn der Knoten aber doch in frontier ist
            elif child.name in [node[1].name for node in frontier.nodes]:
                # fginde den Knoten in frontier
                existing_node = next((node for prio, node in frontier.nodes if node.name == child.name), None)
                # falls der pfad zu diesem nachbarknoten ÜBER current KÜRZER ist als der bisherige, in frontier
                # gefundene pfad, so lösche den bisherigen knoten aus der frontier
                # und pack den neuen auf die frontier prioqueue
                if existing_node and child.cost < existing_node.cost:
                    # Ersetze den Knoten in der Warteschlange durch den neuen Knoten
                    frontier.nodes.remove((existing_node.cost, existing_node))
                    frontier.enqueue(child, child.cost)
    path_to_root = get_path(goal_node) if goal_node else None
    path_cost = get_path_cost(graph, path_to_root) if path_to_root else None
    return goal_node, explored, path_to_root, path_cost


if __name__ == '__main__':
    romania = Graph(['Or', 'Ne', 'Ze', 'Ia', 'Ar', 'Si', 'Fa',
                     'Va', 'Ri', 'Ti', 'Lu', 'Pi', 'Ur', 'Hi',
                     'Me', 'Bu', 'Dr', 'Ef', 'Cr', 'Gi'],
                    [
                        ('Or', 'Ze', 71), ('Or', 'Si', 151),
                        ('Ne', 'Ia', 87), ('Ze', 'Ar', 75),
                        ('Ia', 'Va', 92), ('Ar', 'Si', 140),
                        ('Ar', 'Ti', 118), ('Si', 'Fa', 99),
                        ('Si', 'Ri', 80), ('Fa', 'Bu', 211),
                        ('Va', 'Ur', 142), ('Ri', 'Pi', 97),
                        ('Ri', 'Cr', 146), ('Ti', 'Lu', 111),
                        ('Lu', 'Me', 70), ('Me', 'Dr', 75),
                        ('Dr', 'Cr', 120), ('Cr', 'Pi', 138),
                        ('Pi', 'Bu', 101), ('Bu', 'Gi', 90),
                        ('Bu', 'Ur', 85), ('Ur', 'Hi', 98),
                        ('Hi', 'Ef', 86)
                    ])

    print(bfs(romania, "Bu", "Ti"))
    print(dfs(romania, "Bu", "Ti"))
    print(ucs(romania, "Bu", "Ti"))
