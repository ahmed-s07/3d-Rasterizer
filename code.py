import pygame

pygame.init()
pygame.display.init()
maxX = 750
maxY = 750
veiwX = 750
veiwY = 750
d = 700
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

def toCanvas(a):
    x = a[0]
    y = a[1]
    ax = int((x * maxX)/veiwX)
    ay = int ((y * maxY)/veiwY)
    return [ax, ay, 1.0] 
            
def projectVertex(v):
    x = int((v[0] * d)/v[2])
    y = int((v[1]* d)/v[2])
    return toCanvas([x,y])



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

#function takes in 3 verticies and a color (r,g,b)
#pixels come in a the form of a list with an x,y, color concentration [0.0,1.0)
def fillTriangle(p0, p1, p2 ,color):
    # this swaps verticies into correct order
    if p1[1] < p0[1]:
        p1, p0 = p0, p1
    if p2[1] < p0[1]:
        p2, p0 = p0, p2
    if p2[1] < p1[1]:
        p2, p1 = p1, p2
    #these lines "unpack" each list into variables for x, y, and concentraiton
    x0, y0, h0 = p0
    x1, y1, h1 = p1
    x2, y2, h2 = p2

    #this creates 2 lists 2 store information on the line from p0 - p2 (long side)
    #long stores the x value as floats of each pixel depending on the y value given by long[y-y0] where y0 is the y coordinate of the lower point
    #longh stores the concetration of each pixel (as a float from [0.0,1.0) ) on the line as a smooth function from h0-h2 where the closer the pixel is to h0 the closer the  concentration is 
    long = interpolate(y0, x0, y2, x2)
    longh = interpolate(y0, h0, y2, h2)
    # the next 4 lines do the same thing that long and longh did but for the 2 shorter sides from h0 - h1 and h1 - h2
    short1 = interpolate(y0, x0, y1, x1)
    short2 = interpolate(y1, x1, y2, x2)
    short1h = interpolate(y0, h0, y1, h1)
    short2h = interpolate(y1, h1, y2, h2)
    #these lines remove the last value of short1 since its a duplicate of the first value of short2 and concatenate the 2 lists
    #this finally leaves us with 2 lists one storing the x values of each pixel on the border of the triangle and one sotring the color concentrations of each pixel 
    short1.pop()
    short1h.pop()
    short = short1 + short2
    shorth = short1h + short2h

    #this checks to see the "middle" pixel of each line to determine whether p0-p2 or p0-p1-p2 is on the left or right and swaps them accordingly
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
    #this is where we actually start filling the triangle
    #the outer for loop loops through each y value from y0 to y2 an is conserned with filling each pixel between the left and right side of y
    for y in range(y0, y2):
        #this initialises the value for the left and right post pixels at each indexed y.
        xl = int (left[y-y0])
        xr = int (right[y-y0])
        #this creates a new list which stores the values of each pixels concentrations (as a float from [0.0,1.0) ) on the line as a smooth function from xl-xr where the closer the pixel is to xl the closer the  concentration is 
        hseg = interpolate(xl, lefth[y-y0], xr, righth[y-y0])
        #this iner for loop loops through each xvalue starting from xl to xr to fill in the pixel and calculate the color
        for x in range(xl, xr):
            #this creates a new color by scaling the color we inputted to the orgiinal function by the concentration of this pixel (found in hseg[x-xl])
            shaded = tuple(int(t * hseg[x-xl]) for t in color)
            #this places the pixel
            putPixel(x,y, shaded)
    


pixels[:] = (0,0,0)

vAf = [-2, -0.5, 5]
vBf = [-2,  0.5, 5]
vCf = [-1,  0.5, 5]
vDf = [-1, -0.5, 5]

vAb = [-2, -0.5, 6]
vBb = [-2,  0.5, 6]
vCb = [-1,  0.5, 6]
vDb = [-1, -0.5, 6]


drawLine(projectVertex(vAf), projectVertex(vBf), (0,0,255))
drawLine(projectVertex(vBf), projectVertex(vCf), (0,0,255))
drawLine(projectVertex(vCf), projectVertex(vDf), (0,0,255))
drawLine(projectVertex(vDf), projectVertex(vAf), (0,0,255))


drawLine(projectVertex(vAb), projectVertex(vBb), (255,0,0))
drawLine(projectVertex(vBb), projectVertex(vCb), (255,0,0))
drawLine(projectVertex(vCb), projectVertex(vDb), (255,0,0))
drawLine(projectVertex(vDb), projectVertex(vAb), (255,0,0))

drawLine(projectVertex(vAf), projectVertex(vAb), (0,255,0))
drawLine(projectVertex(vBf), projectVertex(vBb), (0,255,0))
drawLine(projectVertex(vCf), projectVertex(vCb), (0,255,0))
drawLine(projectVertex(vDf), projectVertex(vDb), (0,255,0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()