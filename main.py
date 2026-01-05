# main.py
import pygame
import settings
import renderer as r
import math

# --- Setup ---
pygame.init()
pygame.display.init()

screen = pygame.display.set_mode((settings.MAX_X, settings.MAX_Y))
pygame.display.set_caption("engine")

pixels = pygame.PixelArray(screen)
pixels[:] = (0, 0, 0)


angle = 0.0
rotation_speed = 0.01

T = [-1.5, 0, 7]


bruh = r.cube(1, 0, T)
print(bruh.verticies)
#r.render_object(pixels, bruh)
r.render_instance(pixels, bruh)




# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    angle += rotation_speed
    if angle >= 2 * math.pi:
        angle -= 2 * math.pi

    pixels[:] = (0, 0, 0)
    cube = r.cube(1, angle, T)
    r.render_instance(pixels, cube)

    
    # 1. Lock the surface to create the PixelArray
    # Locking is required to modify pixels directly and safely
    
    pygame.display.flip()