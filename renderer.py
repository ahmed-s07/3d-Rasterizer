# renderer.py
import settings
import matrix as m
import math
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
    z = v[2]
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

def render_object(pixels, instance):
    A = rotation_matrix(3.14/4)
    B = scale_matrix(0.5)
    C = translation_matrix(instance.position)
    D = projection_matrix(settings.D)
    print("Matrix")
    print(A)
    rotated = []
    for v in instance.verticies:
        rotated.append(m.matrix_vector(A,v))
    print("rotated")
    print(rotated)
    scaled = []
    for v in rotated:
        scaled.append(m.matrix_vector(B,v))
    print("scaled")
    print(scaled)
    shifted = []
    for v in scaled:
        shifted.append(m.matrix_vector(C, v))
    print("shifted")
    print(shifted)
    projected = []
    for i in shifted:
        projected.append(m.no_homo(m.matrix_vector(D, i)))
    print("projected")
    print(projected)
    for e in instance.triangles:
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

    def __init__(self, scale, angle, position):
        self.position = position
        self.scale = scale
        self.angle = angle
        self.triangles = cube.triangles
        v0 = [1, 1, 1,1]
        v1 = [-1, 1, 1,1]
        v2 = [-1, -1, 1,1]
        v3 = [1, -1, 1,1]
        v4 = [1, 1, -1,1]
        v5 = [-1, 1, -1,1]
        v6 = [-1, -1, -1,1]
        v7 = [1, -1, -1,1]
        self.verticies = [v0, v1, v2, v3, v4, v5, v6, v7]
#4X4
def rotation_matrix(angle):
    v1 = [math.cos(angle), 0, -1*math.sin(angle), 0]
    v2 = [0, 1, 0, 0]
    v3 = [math.sin(angle), 0, math.cos(angle), 0]
    v4 = [0, 0, 0, 1]
    return [v1, v2, v3, v4]
#4X4
def scale_matrix(scale):
    v1 = [scale, 0, 0, 0]
    v2 = [0, scale, 0, 0]
    v3 = [0, 0, scale, 0]
    v4 = [0, 0, 0, 1]
    return [v1, v2, v3, v4]
#4X4
def translation_matrix(position):
    v1 = [1, 0, 0, 0]
    v2 = [0, 1, 0, 0]
    v3 = [0, 0, 1, 0]
    v4 = [position[0], position[1], position[2], 1]
    return [v1, v2, v3, v4]
#3X4
def projection_matrix(d):
    v1 = [d, 0, 0]
    v2 = [0, d, 0]  
    v3 = [0, 0, 1]
    v4 = [0, 0, 0]
    return [v1,v2,v3,v4]
def veiw_matrix():
    v1 = [settings.MAX_X//settings.VIEW_X, 0, 0]
    v2 = [0, settings.MAX_Y//settings.VIEW_Y, 0]
    v3 = [0, 0, 0]
    return [v1,v2,v3]
def rotation_z(angle):
    v1 = [math.cos(angle), math.sin(angle), 0, 0]
    v2 = [-1 * math.sin(angle), math.cos(angle), 0, 0]
    v3 = [0, 0, 1, 0]
    v4 = [0, 0, 0, 1]
    return [v1, v2, v3, v4]



def render_instance(pixels, instance):  
    rotation = rotation_matrix(instance.angle)   
    scale = scale_matrix(instance.scale)
    translate = translation_matrix(instance.position)
    project = projection_matrix(settings.D)
    rotateX = rotation_z(0)
    a1 = m.matrix_mult(rotateX, rotation)
    a15 = m. matrix_mult(scale, a1)
    a2 = m.matrix_mult(translate, a15)
    a3 = m.matrix_mult(project, a2)
    
    projected = []
    for x in range(8):
        projected.append(m.no_homo(m.matrix_vector(a3, instance.verticies[x])))
    print(projected)
    print(instance.triangles)
    print(projected[0])
    print(projected[1])
    print(projected[2])
    draw_wireframe_triangle(pixels, projected[0], projected[1], projected[2], settings.red)
    for e in instance.triangles:
        draw_wireframe_triangle(pixels, projected[e[0]], projected[e[1]], projected[e[2]], e[3])




