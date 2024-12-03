from prettytable import PrettyTable
from utils import *


class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.edges = []
        self.value = 0


class Edge:
    # edge ist ein Tupel mit (start, ende, wert)
    def __init__(self, edge):
        self.start = edge[0]
        self.end = edge[1]
        self.value = edge[2]


class Graph:
    def __init__(self, node_list, edges):
        self.nodes = []

        for name in node_list:
            self.nodes.append(Node(name))

        for e in edges:
            e = (get_node(e[0], self.nodes), get_node(e[1], self.nodes), e[2])

            self.nodes[next((i for i, v in enumerate(self.nodes) if v.name == e[0].name), -1)].edges.append(Edge(e))
            self.nodes[next((i for i, v in enumerate(self.nodes) if v.name == e[1].name), -1)].edges.append(
                Edge((e[1], e[0], e[2])))

    def print(self):
        node_list = self.nodes

        t = PrettyTable(['  '] + [i.name for i in node_list])
        for node in node_list:
            edge_values = ['X'] * len(node_list)
            for edge in node.edges:
                edge_values[next((i for i, e in enumerate(node_list) if e.name == edge.end.name), -1)] = edge.value
            t.add_row([node.name] + edge_values)
        print(t)

    def get_neighbors(self, node_name):
        # sucht den Knoten mit node_name in der node-liste
        node = next((node for node in self.nodes if node.name == node_name), None)
        # returned alle namen der benachbarten knoten des gefundenen knotens
        if node is not None:
            return [edge.end.name for edge in node.edges]
        else:
            return []

    def find_edge(self, start_node_name, end_node_name):
        # sucht den Knoten mit start_node_name in der node-liste
        start_node = next((node for node in self.nodes if node.name == start_node_name), None)
        if start_node is not None:
            # sucht in den Kanten des gefundenen Knoten nach der Kante, die auf end_node_name endet
            edge = next((edge for edge in start_node.edges if edge.end.name == end_node_name), None)
            return edge
        return None
