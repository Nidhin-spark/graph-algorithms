# Example file showing a basic pygame "game loop"
import pygame
import pygame.freetype
from pygame import key
from graph import Graph
from pdb import set_trace as bp

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

typeface = pygame.freetype.SysFont("DejaVu Sans", 60)
node_count = 3
edge_density = 0.9
graph = None

def reload_graph():
    global graph, node_count, edge_density, typeface
    print("node_count = {node_count}, edge_density = {edge_density}")
    graph = Graph(node_count, edge_density, pygame.Surface.get_rect(screen), typeface)

reload_graph()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                reload_graph()
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_k:
                node_count += 1
                reload_graph()
            elif event.key == pygame.K_j:
                node_count -= 1
                reload_graph()
            elif event.key == pygame.K_h:
                edge_density -= 0.05
                reload_graph()
            elif event.key == pygame.K_l:
                edge_density += 0.05
                reload_graph()

    graph.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
