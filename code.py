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

def drawWireFrameTriangle(p0, p1, p2, color):
    drawLine(p0, p1, color)
    drawLine(p1, p2, color)
    drawLine(p2, p0, color)

def fillTriangle(p0, p1, p2 ,color):
    if p1[1] < p0[1]:
        p1, p0 = p0, p1
    if p2[1] < p0[1]:
        p2, p0 = p0, p2
    if p2[1] < p1[1]:
        p2, p1 = p1, p2
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    long = interpolate(y0, x0, y2, x2)
    short1 = interpolate(y0, x0, y1, x1)
    short2 = interpolate(y1, x1, y2, x2)
    short1.pop()
    short = short1 + short2
    print(long)
    print(short)
    for y in range(y0, y2):
        p3 = [int (short[y-y0]), y]
        p4 = [int(long[y-y0]), y]
        drawLine(p3, p4, color)
    


pixels[:] = (0,0,0)
p1 = [300, 100]
p2 = [-100, 40]
p3 = [100, 100]
drawWireFrameTriangle(p1, p2, p3, (255, 255, 255))
fillTriangle(p1, p2, p3, (255, 0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()