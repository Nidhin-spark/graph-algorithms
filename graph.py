from pygame import draw, Color, Rect
from pygame.math import Vector2
import random
import math

class Node:
    def __init__(self, pos, label):
        self.pos = pos
        self.label = label

class Edge:
    def __init__(self, src, dst, weight):
        self.src = src
        self.dst = dst
        self.weight = weight
        self.key1 = src.label + dst.label
        self.key2 = dst.label + src.label
    
    def other(self, node):
        if self.src.label != node:
            return self.src.label
        else:
            return self.dst.label

def random_point_in_rect(rect, margin):
    return Vector2(random.randrange(rect.left + margin, rect.right - margin),
                   random.randrange(rect.top + margin, rect.bottom - margin))

class Graph:
    def __init__(self, nodes_count, edge_density, rect, typeface, initial=None, goal=None):
        self.margin = 100
        self.radius = 50
        self.typeface = typeface
        self.rect = rect
        self.nodes = {}
        self.edges = {}
        self.initial = initial
        self.goal = goal
        self.parent = None
        self.visited = None
        self.frontier = None
        self.frontier_set = None
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
    
    def edges_from(self, node):
        for edge in self.edges:
            if edge[0] == node:
                yield self.edges[edge]

    def get_edge(self, nodeA, nodeB):
        label1 = nodeA + nodeB
        return self.edges[label1]

    def generate_node(self, label):
        node = Node(random_point_in_rect(self.rect, self.margin), label)
        for other in self.nodes:
            if node.pos.distance_to(self.nodes[other].pos) < (2 * self.margin):
                return None
        return node

    def draw_arrowhead(self, screen, pt1, pt2, color):
        theta = -(pt2 - pt1).angle_to((0, 0))
        r = 20
        line1 = pt1 + Vector2.from_polar((r, theta + 45))
        line2 = pt1 + Vector2.from_polar((r, theta - 45))
        draw.line(screen, color, pt1, line1, 5)
        draw.line(screen, color, pt1, line2, 5)

    def draw_edge_label(self, screen, edge):
        theta = -(edge.dst.pos - edge.src.pos).angle_to((0, 0))
        line_center = (edge.src.pos + edge.dst.pos) / 2
        label = str(edge.weight)
        text_size = 30
        text_rect = self.typeface.get_rect(label, size=text_size)
        rect_radius = Vector2(text_rect.left - text_rect.right, text_rect.top - text_rect.bottom).distance_to((0,0)) / 2
        text_center = line_center + Vector2.from_polar((rect_radius + 5, theta + 90)) 
        text_rect.center = text_center
        self.typeface.render_to(screen, text_rect, label, Color(255,0,0), size=text_size)

    def draw_edge(self, screen, edge):
        diff = edge.dst.pos - edge.src.pos
        diff.scale_to_length(diff.magnitude() - self.radius)
        pt1 = edge.dst.pos - diff
        pt2 = edge.src.pos + diff
        color = Color(128,128,128) 
        if self.parent.get(edge.src.label) == edge.dst.label:
            color = Color(0, 128, 0)
            self.draw_arrowhead(screen, pt2, pt1, color)
        if self.parent.get(edge.dst.label) == edge.src.label:
            color = Color(0, 128, 0)
            self.draw_arrowhead(screen, pt1, pt2, color)
        draw.line(screen, color, pt1, pt2, 5)
        self.draw_edge_label(screen, edge)

    def draw(self, screen):
        screen.fill("white")
        for n in self.nodes:
            node = self.nodes[n]
            if n == self.goal:
                if n in self.frontier_set:
                    color = Color(0, 255, 255)
                elif n in self.visited:
                    color = Color(128, 255, 0)
                else:
                    color = Color(0, 255, 0) # Green
            elif n in self.frontier_set:
                color = Color(0, 0, 255) # Blue
            elif n in self.visited:
                color = Color(255, 255, 0) # Yellow
            else:
                color = Color(128, 128, 128)
            draw.circle(screen, color, node.pos, self.radius, 5)

            text_rect = self.typeface.get_rect(node.label)
            text_rect.center = node.pos
            self.typeface.render_to(screen, text_rect, node.label)

        for e in self.edges:
            # Only draw edges once.
            if ord(e[0]) >= ord(e[1]):
                continue
            edge = self.edges[e]
            self.draw_edge(screen, edge)
