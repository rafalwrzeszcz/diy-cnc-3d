from madcad import brick, difference, pi, pierce, rotate, translate, vec3, washer, web, Y, Z
from madcad.io import write

full_turn = 2 * pi

# flat circle base

height = 5
notch_depth = 12
notch_match_margin = 0.1
wing_depth = 47
wing_width = 7

r_out = 120
r_in = 55

ring = washer(r_in * 1.9, r_out * 2, height)["part"]

# external stand notches

notch = brick(
    # without "1" offset in Z we have trouble with edge surface triangulation
    vec3(r_out - notch_depth, -0.5 * height - notch_match_margin, -1),
    vec3(r_out, 0.5 * height + notch_match_margin, height + 1)
)

steps = 3
for i in range(steps):
    ring = difference(ring, notch)
    ring = ring.transform(rotate(full_turn / steps, Z))

# prepare for internal wholes for wings

ring = ring.transform(rotate(full_turn / 7, Z))
hole = brick(
    # without "1" offset in Z we have trouble with edge surface triangulation
    vec3(r_in, -0.5 * wing_width, 0 - 1),
    vec3(r_in + wing_depth, 0.5 * wing_width, height + 1)
)

# 3-hole base

tri_base = ring
steps = 3
for i in range(steps):
    tri_base = difference(tri_base, hole)
    tri_base = tri_base.transform(rotate(full_turn / steps, Z))

# 4-hole base

quad_base = ring
steps = 4
for i in range(steps):
    quad_base = difference(quad_base, hole)
    quad_base = quad_base.transform(rotate(full_turn / steps, Z))

# stand

stand_width = 50
stand_height = 130
support_width = 20

bottom = brick(
    vec3(-stand_width / 2, 0, 0),
    vec3(stand_width / 2, stand_width, height)
)
vertical = brick(
    vec3(-height / 2, 0, 0),
    vec3(height / 2, stand_width, stand_height)
)

notch = brick(
    # without "1" offset in Z we have trouble with edge surface triangulation
    vec3(-stand_width / 2, -1, -notch_match_margin),
    vec3(stand_width / 2, notch_depth, height + notch_match_margin)
)

support = brick(
    vec3(-support_width / 2, 0, -support_width / 2),
    vec3(support_width / 2, stand_width, support_width / 2)
).transform(rotate(full_turn / 8, Y)).transform(translate(vec3(0, 0, support_width)))

# can we cut it cleverer?
cleanup = brick(
    vec3(-support_width / 2 - 1, -1, 0),
    vec3(support_width / 2 + 1, stand_width + 1, support_width)
)
support = difference(support, cleanup).transform(translate(vec3(0, 0, -support_width + height)))

stand = vertical
stand = difference(stand, notch.transform(translate(vec3(0, 0, 40))))
stand = difference(stand, notch.transform(translate(vec3(0, 0, 105))))
stand = stand + bottom + support

write(stand, "stand.stl")
write(tri_base, "tri-wing.stl")
write(quad_base, "quad-wing.stl")
