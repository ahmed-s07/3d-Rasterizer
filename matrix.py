# we define a matrix by a collevction of vectors v1, v2, v3... in a list where each vector represents a column of the matrix
# we define a vector as a coolection of number x,y,z ... in a list.
#so the identitiy matrix would be e1 = [1,0,0] e2 = [0,1,0] e3 = [0,0,1] so I3 = [e1,e2,e3]

def vector_add(v1, v2):
    v3 = []
    length = len(v1)
    for x in range(length):
        v3.append(v1[x] + v2[x])
    return v3

# to define matrix vector multiplacation say Ax we scale each column of a by A correponding entry in x and add the resulting column vectors together
def matrix_vector(A, x):
    length = len(A)
    a_scaled = []
    for v in range(length):
        scaled = [q * x[v] for q in A[v]]
        a_scaled.append(scaled)
    for v in range(length):
        if v == 0:
            Ax = a_scaled[0]
        else:
            Ax = vector_add(Ax, a_scaled[v])
    return Ax

# now we want to define matrix multiplication as a series of transformation such that A(Bx) is the same a (AB)x
# We can do this by treating each column of AB as the matrix vector product of the matrix A and a column of B
# for example the first column of AB would be the mstrix vector product of A and the first column of B

def matrix_mult(A, B):
    lengthB = len(B)
    AB = []

    for v in range(lengthB):
        AB.append(matrix_vector(A, B[v]))
    return AB

def no_homo(v):
    length = len(v)
    w = v[length-1]
    scaled = []
    for x in range(length-1):
        scaled.append(v[x]//w)
    scaled.append(1.0)
    return scaled

v1 = [0.7073882691671998, 0, -0.706825181105366]
v2 = [0, 1, 0]
v3 = [0.706825181105366, 0, 0.706825181105366]
A = [v1,v2,v3]

v = [1,1,1]


print(matrix_vector(A, v))



