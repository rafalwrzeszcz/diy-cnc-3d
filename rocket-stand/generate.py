from madcad import Circle, extrusion, flatsurface, web, Z
from madcad.io import write

# flat circle base

height = 5

r_out = 120
r_in = 55

resolution = ("div", r_out * 2)

outer_circle = Circle((0, Z), r_out, resolution=resolution)
inner_circle = Circle((0, Z), r_in, resolution=resolution)

surface = web(outer_circle) + web(inner_circle).flip()

ring = flatsurface(surface)
ring = extrusion(ring, height * Z)

# 4-hole base

# TODO

# 3-hole base

# TODO

# stand

# TODO

write(ring, "stand.stl")
