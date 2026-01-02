# renderer.py
import settings
def interpolate(i0, d0, i1, d1):
    if i0 == i1:
        return [d0]
    values = []
    steps = i1 - i0
    a = (d1 - d0) / steps
    d = d0
    i = i0
    while i <= i1:
        values.append(d)
        d += a
        i += 1
    return values

def vectorShift(verticies, t):
    for v in verticies:
        v[0] += t[0]
        v[1] += t[1]
        v[2] += t[2]

# Helper to center coordinates
def put_pixel(pixels, x, y, color):
    # Check bounds to prevent crashes
    sx = int((settings.MAX_X / 2) + x)
    sy = int((settings.MAX_Y / 2) - y)
    
    if 0 <= sx < settings.MAX_X and 0 <= sy < settings.MAX_Y:
        pixels[sx, sy] = color

def to_canvas(a):
    x = a[0]
    y = a[1]
    ax = int((x * settings.MAX_X) / settings.VIEW_X)
    ay = int((y * settings.MAX_Y) / settings.VIEW_Y)
    return [ax, ay, 1.0]

def project_vertex(v):
    # Avoid division by zero
    z = v[2] if v[2] != 0 else 1 
    x = int((v[0] * settings.D) / z)
    y = int((v[1] * settings.D) / z)
    return to_canvas([x, y])

def draw_line(pixels, p0, p1, color):
    if abs(p1[0] - p0[0]) > abs(p1[1] - p0[1]):
        if p0[0] > p1[0]:
            p0, p1 = p1, p0
        x0, y0, _ = p0
        x1, y1, _ = p1
        ys = interpolate(x0, y0, x1, y1)
        for x in range(x0, x1 + 1):
            put_pixel(pixels, x, int(ys[x - x0]), color)
    else:
        if p0[1] > p1[1]:
            p0, p1 = p1, p0
        x0, y0, _ = p0
        x1, y1, _ = p1
        ys = interpolate(y0, x0, y1, x1)
        for y in range(y0, y1 + 1):
            put_pixel(pixels, int(ys[y - y0]), y, color)

def draw_wireframe_triangle(pixels, p0, p1, p2, color):
    draw_line(pixels, p0, p1, color)
    draw_line(pixels, p1, p2, color)
    draw_line(pixels, p2, p0, color)

def fill_triangle(pixels, p0, p1, p2, color):
    # Sort vertices by y-coordinate
    if p1[1] < p0[1]: p1, p0 = p0, p1
    if p2[1] < p0[1]: p2, p0 = p0, p2
    if p2[1] < p1[1]: p2, p1 = p1, p2

    x0, y0, h0 = p0
    x1, y1, h1 = p1
    x2, y2, h2 = p2

    long = interpolate(y0, x0, y2, x2)
    longh = interpolate(y0, h0, y2, h2)
    short1 = interpolate(y0, x0, y1, x1)
    short2 = interpolate(y1, x1, y2, x2)
    short1h = interpolate(y0, h0, y1, h1)
    short2h = interpolate(y1, h1, y2, h2)

    short1.pop()
    short1h.pop()
    short = short1 + short2
    shorth = short1h + short2h

    m = int(len(long) / 2)
    if m < len(short) and long[m] < short[m]:
        left, lefth = long, longh
        right, righth = short, shorth
    else:
        left, lefth = short, shorth
        right, righth = long, longh

    for y in range(y0, y2):
        idx = y - y0
        if idx < len(left) and idx < len(right):
            xl = int(left[idx])
            xr = int(right[idx])
            
            # Interpolate color intensity
            hseg = interpolate(xl, lefth[idx], xr, righth[idx])
            
            for x in range(xl, xr):
                if 0 <= x - xl < len(hseg):
                    shaded = tuple(int(t * hseg[x - xl]) for t in color)
                    put_pixel(pixels, x, y, shaded)

def render_object(pixels, verticies, triangles):
    projected = []
    for i in verticies:
        projected.append(project_vertex(i))
    for e in triangles:
        draw_wireframe_triangle(pixels, projected[e[0]], projected[e[1]], projected[e[2]], e[3])

class cube:
    t0 = [0, 1, 2, settings.red]
    t1 = [0, 2, 3, settings.red]
    t2 = [4, 0, 3, settings.green]
    t3 = [4, 3, 7, settings.blue]
    t4 = [5, 4, 7, settings.blue]
    t5 = [5, 7, 6, settings.blue]
    t6 = [1, 5, 6, settings.yellow]
    t7 = [1, 6, 2, settings.yellow]
    t8 = [4, 5, 1, settings.magenta]
    t9 = [4, 1, 0, settings.magenta]
    t10 = [2, 6, 7, settings.cyan]
    t11 = [2, 7, 3, settings.cyan]

    triangles = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]

    def __init__(self, position):
        self.position = position
        self.triangles = cube.triangles
        v0 = [1, 1, 1]
        v1 = [-1, 1, 1]
        v2 = [-1, -1, 1]
        v3 = [1, -1, 1]
        v4 = [1, 1, -1]
        v5 = [-1, 1, -1]
        v6 = [-1, -1, -1]
        v7 = [1, -1, -1]
        self.verticies = [v0, v1, v2, v3, v4, v5, v6, v7]

    

def render_instance(pixels, instance):  
    vectorShift(instance.verticies, instance.position)
    render_object(pixels, instance.verticies, instance.triangles)

