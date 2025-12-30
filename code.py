# main.py
import pygame
import settings
import renderer as r

# --- Setup ---
pygame.init()
pygame.display.init()

screen = pygame.display.set_mode((settings.MAX_X, settings.MAX_Y))
pygame.display.set_caption("engine")

pixels = pygame.PixelArray(screen)
pixels[:] = (0, 0, 0)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0 , 255) 
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)

def vectorShift(verticies, t):
    for v in verticies:
        v[0] += t[0]
        v[1] += t[1]
        v[2] += t[2]

T = [-1.5, 0, 7]

# --- Data ---
v0 = [1, 1, 1]
v1 = [-1, 1, 1]
v2 = [-1, -1, 1]
v3 = [1, -1, 1]
v4 = [1, 1, -1]
v5 = [-1, 1, -1]
v6 = [-1, -1, -1]
v7 = [1, -1, -1]

t0 = [0, 1, 2, red]
t1 = [0, 2, 3, red]
t2 = [4, 0, 3, green]
t3 = [4, 3, 7, blue]
t4 = [5, 4, 7, blue]
t5 = [5, 7, 6, blue]
t6 = [1, 5, 6, yellow]
t7 = [1, 6, 2, yellow]
t8 = [4, 5, 1, magenta]
t9 = [4, 1, 0, magenta]
t10 = [2, 6, 7, cyan]
t11 = [2, 7, 3, cyan]

verticies = [v0, v1, v2, v3, v4, v5, v6, v7]
triangles = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]


vectorShift(verticies, T)

r.renderObject(verticies, triangles, pixels)


# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 1. Lock the surface to create the PixelArray
    # Locking is required to modify pixels directly and safely
    
    pygame.display.flip()