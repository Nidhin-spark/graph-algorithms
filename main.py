# Example file showing a basic pygame "game loop"
import pygame
from graph import Graph
from pdb import set_trace as bp

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

graph = Graph(3, 0.9, pygame.Surface.get_rect(screen))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            graph = Graph(3, 0.9, pygame.Surface.get_rect(screen))

    graph.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
