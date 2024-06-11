from pygame import draw, Color, Rect
from pygame.math import Vector2
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
    return Vector2(random.randrange(rect.left + margin, rect.right - margin),
                   random.randrange(rect.top + margin, rect.bottom - margin))

class Graph:
    def __init__(self, nodes_count, edge_density, rect, typeface):
        self.margin = 50
        self.radius = 50
        self.typeface = typeface
        self.rect = rect
        self.nodes = {}
        self.edges = {}
        label = 'A'
        while len(self.nodes) < nodes_count:
            node = self.generate_node(label)
            if node:
                self.nodes[label] = node
                label = chr(ord(label) + 1)

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
                dist = edge.src.pos.distance_to(edge.dst.pos)
                if dist > max_dist:
                    max_edge = edge
                    max_dist = dist
            self.delete_edge(edge.src.label, edge.dst.label)

    def edge_quotient(self):
        max_edges = len(self.nodes) * (len(self.nodes) - 1) / 2
        return len(self.edges) / 2 / max_edges

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
            if node.pos.distance_to(self.nodes[other].pos) < (2 * self.margin):
                return None
        return node

    def draw_edge(self, screen, edge):
            diff = edge.dst.pos - edge.src.pos
            diff.scale_to_length(diff.magnitude() - self.radius)
            pt1 = edge.dst.pos - diff
            pt2 = edge.src.pos + diff
            draw.line(screen, Color(0,0,0), pt1, pt2, 5)

    def draw(self, screen):
        screen.fill("white")
        for n in self.nodes:
            node = self.nodes[n]
            draw.circle(screen, Color(0,0,0), node.pos, self.radius, 5)
            text_rect = self.typeface.get_rect(node.label)
            text_rect.center = node.pos
            self.typeface.render_to(screen, text_rect, node.label)

        for e in self.edges:
            # Only draw edges once.
            if ord(e[0]) >= ord(e[1]):
                continue
            edge = self.edges[e]
            self.draw_edge(screen, edge)
