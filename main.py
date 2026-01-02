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




T = [-1.5, 0, 7]

bruh = r.cube(1, (3.14/4), T)
r.render_instance(pixels, bruh)




# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 1. Lock the surface to create the PixelArray
    # Locking is required to modify pixels directly and safely
    
    pygame.display.flip()