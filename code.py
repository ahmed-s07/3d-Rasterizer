import pygame

pygame.init()
pygame.display.init()
maxX = 750
maxY = 750
screen = pygame.display.set_mode((maxX, maxY))
pygame.display.set_caption("engine")
pixels = pygame.PixelArray(screen)
def putPixel(x, y, color):
    sx = ((int)(maxX / 2) + x)
    sy = ((int)(maxY / 2) - y)
    pixels[sx, sy] = color
def drawLine(p0, p1, color):
    if(p0[0] > p1[0]):
        temp = p0
        p0 = p1
        p1 = temp
    y0 = p0[1]
    x0 = p0[0]
    y1 = p1[1]
    x1 = p1 [0]
    a = (y1 - y0) / (x1 - x0)
    y = y0
    x = x0
    while(x <= x1):
        putPixel(x, int(y), color)
        y += a
        x += 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pixels[:] = (0,0,0)
    point1 = [-50, -200]
    point2 = [60, 240]
    drawLine(point1, point2, (255,255,255))
    pygame.display.flip()