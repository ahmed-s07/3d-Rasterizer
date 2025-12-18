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
    if abs(p1[0] - p0[0]) > abs(p1[1] - p0[1]):
        if p0[0] > p1[0]:
            p0, p1 = p1, p0
        x0, y0 = p0
        x1, y1 = p1
        ys = interpolate(x0, y0, x1, y1)
        for x in range(x0, x1+1):
            putPixel(x, int (ys[x - x0]), color)
    else: 
        if p0[1] > p1[1]:
            p0, p1 = p1, p0
        y0 = p0[1]
        x0 = p0[0]
        y1 = p1[1]
        x1 = p1[0]
        xs = interpolate(y0, x0, y1, x1)
        for y in range (y0, y1+1):
            putPixel(int (xs[y - y0]), y, color)
            



def interpolate(i0, d0, i1, d1):
    if i0 == i1:
        return [d0]
    values = []
    steps = i1 - i0
    a = (d1 - d0) / steps
    d = d0
    i = i0
    while i <= i1:  # include last value
        values.append(d)
        d += a
        i += 1
    return values

pixels[:] = (0,0,0)
point1 = [-200, -100]
point2 = [-100, 300]
drawLine(point1, point2, (255,255,255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()