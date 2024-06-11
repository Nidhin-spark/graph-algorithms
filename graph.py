import pygame
import random
import math

class Node:
    def __init__(pos, label):
        self.pos = pos
        self.label = label
        self.edges = {}

class Edge:
    def __init__(src, dst, weight):
        self.src = src
        self.dst = dst
        self.weight = weight
        self.key1 = src.label + dst.label
        self.key2 = dst.label + src.label

def random_point_in_rect(rect, margin):
    return (random.randrange(rect.top + margin, rect.bottom - margin),
            random.randrange(rect.left + margin, rect.right - margin))

class Graph:
    def __init__(nodes_count, edge_density, rect):
        this.margin = 20
        label = 'A'
        this.rect = rect
        this.nodes = {}
        this.edges = {}
        while len(this.nodes) < nodes_count:
            node = generate_node(label)
            if node:
                nodes[label] = node
                label = chr(ord(label) + 1)

        edge_list = []
        for a in this.nodes:
            for b in this.nodes:
                if a == b: continue
                if self.get_edge(a, b):
                    continue
                # Generate 50% extra then trim the longest.
                if random.random() < edge_density * 0.75:
                    self.make_edge(a, b, random.randrange(1, 20))

        while self.edge_quotient() > edge_density:
            max_edge = None
            max_dist = -math.inf
            for edge in self.edges.values():
                dist = self.distance2(edge.src, edge.dst)
                if dist > max_dist:
                    max_edge = edge
                    max_dist = dist
            self.delete_edge(edge.src, edge.dst)

    def edge_quotient(self):
        max_edges = len(self.nodes) * (len(self.nodes) - 1) / 2
        return len(self.edges) / 2 / max_edges

    def distance2(self, nodeA, nodeB):
        return (nodeA.pos.x - nodeB.pos.x) ** 2 + (nodeA.pos.y - nodeB.pos.y) ** 2

    def make_edge(self, label1, label2, weight):
        if self.get_edge(node):
            return None
        label1 = nodeA + nodeB
        label2 = nodeB + nodeA
        del edges[label1]
        del edges[label2]

    def delete_edge(self, nodeA, nodeB):
        label1 = nodeA + nodeB
        label2 = nodeB + nodeA
        del edges[label1]
        del edges[label2]

    def get_edge(self, nodeA, nodeB):
        label1 = nodeA + nodeB
        return edges[label1]

    def generate_node(self, label):
        node = Node(random_point_in_rect(this.rect, this.margin), label)
        for other in this.nodes:
            if self.distance2(node, other) < (2 * this.margin) ** 2:
                return None
        return node
