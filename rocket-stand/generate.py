import numpy as np
from stl import mesh

height = 5

r_out = 120
r_in = 55
details = 6 / r_out

# vertices generators

def circle_vertices(r, stepping):
    return [[r * np.cos(angle), r * np.sin(angle)] for angle in np.arange(0, 2 * np.pi, stepping)]

# faces generators

def circle_side_faces(offset, steps):
    # each vertex is connected to next one and opposite vertically to it
    bottom_to_top = [[offset + i, offset + i + 1, offset + i + steps] for i in range(steps - 1)]
    top_to_bottom = [[offset + i + steps, offset + i + steps + 1, offset + i + 1] for i in range(steps - 1)]
    # closing gap connecting last one to first one
    bottom_to_top.append([offset + steps - 1, offset, offset + 2 * steps - 1])
    top_to_bottom.append([offset + 2 * steps - 1, offset + steps, offset])
    return bottom_to_top + top_to_bottom

def circle_layer_faces(offset, steps):
    # each vertex is connected to opposite horizontally from out to in and in to out
    out_to_in = [[offset + i, offset + i + 1, offset + i + 2 * steps] for i in range(steps - 1)]
    in_to_out = [[offset + i + 2 * steps, offset + i + 2 * steps + 1, offset + i + 1] for i in range(steps - 1)]
    # closing gap connecting last one to first one
    out_to_in.append([offset + steps - 1, offset, offset + 3 * steps - 1])
    in_to_out.append([offset + 3 * steps - 1, offset + 2 * steps, offset])
    return in_to_out + out_to_in

# order of points:
# - bottom outer ring
# - top outer ring
# - bottom inner ring
# - top inner ring

# outer circle
circle_out = circle_vertices(r_out, details)
circle_steps = len(circle_out)

start = 0
points_out = [[v[0], v[1], z] for z in [0, height] for v in circle_out]

# each vertex is connected to next one and opposite vertically to it
sides_out = circle_side_faces(start, circle_steps)

# inner circle

circle_in = circle_vertices(r_in, details)

# shift after previous part
start = len(points_out)
points_in = [[v[0], v[1], z] for z in [0, height] for v in circle_in]

sides_in = circle_side_faces(start, circle_steps)

# layer faces
sides_top = circle_layer_faces(0, circle_steps)
sides_bottom = circle_layer_faces(circle_steps, circle_steps)

vertices = np.array(points_out + points_in)
faces = np.array(sides_out + sides_in + sides_top + sides_bottom)

# create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for key, f in enumerate(faces):
    for j in range(3):
        cube.vectors[key][j] = vertices[f[j],:]

cube.save("stand.stl")
