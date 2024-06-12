# Example file showing a basic pygame "game loop"
import pygame
import pygame.freetype
from pygame import key
from graph import Graph
import random
import search
from pdb import set_trace as bp

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

typeface = pygame.freetype.SysFont("DejaVu Sans", 60)
graph = None
def make_config(node_count, edge_density, seed, initial, goal):
    return {'node_count': node_count, 'edge_density': edge_density, 'seed': seed,
            'initial': initial, 'goal': goal}
config = make_config(3, 0.9, 0, 'A', 'C')

graph_list = [make_config(5, 0.90, 1, 'A', 'C'),
              make_config(6, 0.40, 8, 'E', 'B'),
              make_config(7, 0.40, 21, 'C', 'G'),
              make_config(8, 0.4, 2, 'A', 'H'),
              make_config(9, 0.35, 11, 'F', 'A')]
graph_index = 0

search_state = None

algorithms = {
    'bfs': {
        'init': search.bfs_init,
        'step': search.bfs_step},
    'dijkstra': {
        'init': search.dijkstra_init,
        'step': search.dijkstra_step}}

# Change this to 'dijkstra' to use Dijkstra's Algorithm.
algorithm = 'bfs'
search_init = algorithms[algorithm]['init']
search_step = algorithms[algorithm]['step']

def load_config(config):
    global graph, typeface, search_state
    random.seed(config['seed'])
    print(config)
    graph = Graph(config['node_count'], config['edge_density'], pygame.Surface.get_rect(screen), typeface,
                  config['initial'], config['goal'])
    search_state = search_init(graph)

def reload_graph():
    global config
    if 'initial' not in config:
        config['initial'] = 'A'
        config['terminal'] = chr(ord('A') + config['node_count'] - 1)
    load_config(config)

load_config(graph_list[graph_index])

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                config['seed'] += 1
                reload_graph()
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_k:
                config['node_count'] += 1
                reload_graph()
            elif event.key == pygame.K_j:
                config['node_count'] -= 1
                reload_graph()
            elif event.key == pygame.K_h:
                config['edge_density'] -= 0.05
                reload_graph()
            elif event.key == pygame.K_l:
                config['edge_density'] += 0.05
                reload_graph()
            elif event.key == pygame.K_LEFTBRACKET:
                if graph_index > 0:
                    graph_index -= 1
                load_config(graph_list[graph_index])
            elif event.key == pygame.K_RIGHTBRACKET:
                if graph_index < len(graph_list) - 1:
                    graph_index += 1
                load_config(graph_list[graph_index])
            elif event.key == pygame.K_s:
                if search_state == search.MORE_STEPS_NEEDED:
                   search_state = search_step(graph)

    graph.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
