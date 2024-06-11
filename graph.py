from pygame import draw, Color, Rect
import random
import math

class Node:
    def __init__(self, pos, label):
        self.pos = pos
        self.label = label
        self.edges = {}

class Edge:
    def __init__(self, src, dst, weight):
        self.src = src
        self.dst = dst
        self.weight = weight
        self.key1 = src.label + dst.label
        self.key2 = dst.label + src.label

def random_point_in_rect(rect, margin):
    return (random.randrange(rect.left + margin, rect.right - margin),
            random.randrange(rect.top + margin, rect.bottom - margin))

class Graph:
    def __init__(self, nodes_count, edge_density, rect):
        self.margin = 50
        label = 'A'
        self.rect = rect
        self.nodes = {}
        self.edges = {}
        while len(self.nodes) < nodes_count:
            node = self.generate_node(label)
            if node:
                self.nodes[label] = node
                label = chr(ord(label) + 1)

        edge_list = []
        for a in self.nodes:
            for b in self.nodes:
                if a == b: continue
                if self.has_edge(a, b):
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
            self.delete_edge(edge.src.label, edge.dst.label)

    def edge_quotient(self):
        max_edges = len(self.nodes) * (len(self.nodes) - 1) / 2
        return len(self.edges) / 2 / max_edges

    def distance2(self, nodeA, nodeB):
        posA = nodeA.pos
        posB = nodeB.pos
        return (posA[0] - posB[0]) ** 2 + (posA[1] - posB[1]) ** 2

    def make_edge(self, nodeA, nodeB, weight):
        edge = Edge(self.nodes[nodeA], self.nodes[nodeB], weight)
        label1 = nodeA + nodeB
        label2 = nodeB + nodeA
        self.edges[label1] = edge
        self.edges[label2] = edge

    def delete_edge(self, nodeA, nodeB):
        label1 = nodeA + nodeB
        label2 = nodeB + nodeA
        del self.edges[label1]
        del self.edges[label2]

    def has_edge(self, nodeA, nodeB):
        return ((nodeA + nodeB) in self.edges)

    def get_edge(self, nodeA, nodeB):
        label1 = nodeA + nodeB
        return self.edges[label1]

    def generate_node(self, label):
        node = Node(random_point_in_rect(self.rect, self.margin), label)
        for other in self.nodes:
            if self.distance2(node, self.nodes[other]) < (2 * self.margin) ** 2:
                return None
        return node

    def draw(self, screen):
        radius = 50
        screen.fill("white")
        for n in self.nodes:
            draw.circle(screen, Color(0,0,0), self.nodes[n].pos, radius, 5)
        for e in self.edges:
            # Only draw edges once.
            if ord(e[0]) >= ord(e[1]):
                continue
            edge = self.edges[e]
            draw.line(screen, Color(0,0,0), edge.src.pos, edge.dst.pos, 5)
