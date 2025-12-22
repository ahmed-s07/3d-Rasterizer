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
        x0, y0, h0 = p0
        x1, y1, h1 = p1
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
    x0, y0, h0 = p0
    x1, y1, h1 = p1
    x2, y2, h2 = p2
    long = interpolate(y0, x0, y2, x2)
    longh = interpolate(y0, h0, y2, h2)
    short1 = interpolate(y0, x0, y1, x1)
    short2 = interpolate(y1, x1, y2, x2)
    short1h = interpolate(y0, h1, y1, h1)
    short2h = interpolate(y1, h1, y2, h2)
    short1.pop()
    short1h.pop()
    short = short1 + short2
    shorth = short1h + short2h
    m = int (len(long)/2)
    if(long[m] < short[m]):
        left = long
        lefth = longh
        right = short
        righth = shorth
    else:
        left = short
        lefth = shorth
        right = long
        righth = longh
    for y in range(y0, y2):
        x1 = int (left[y-y0])
        xr = int (right[y-y0])
        hseg = interpolate(x1, lefth[y-y0], xr, righth[y-y0])
        for x in range(x1, xr):
            shaded = tuple(t * hseg[x-x1] for t in color)
            putPixel(x,y, shaded)
    


pixels[:] = (0,0,0)
p1 = [100, 50, 0.5]
p2 = [-200, 200, 1.0]
p3 = [5, 300, 0.25]
drawWireFrameTriangle(p1, p2, p3, (255, 255, 255))
fillTriangle(p1, p2, p3, (0, 0, 255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()