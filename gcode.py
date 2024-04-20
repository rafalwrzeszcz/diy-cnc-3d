margin = 2
x = 290
y = 65
z = 3.1
size = 94.5
notch = 35

def side_a(start_x, start_y):
    x0 = start_x + margin
    y0 = start_y + margin

    return f"""
G00 X{x0} Y{y0}
G01 X{x0} Y{y0} Z-{z}
G01 X{x0 + x} Y{y0}
G01 X{x0 + x} Y{y0 + y}
G01 X{x0 + x - size} Y{y0 + y}
G01 X{x0 + x - size} Y{y0 + y - notch}
G01 X{x0 + x - size - z} Y{y0 + y - notch}
G01 X{x0 + x - size - z} Y{y0 + y}
G01 X{x0 + size + z} Y{y0 + y}
G01 X{x0 + size + z} Y{y0 + y - notch}
G01 X{x0 + size} Y{y0 + y - notch}
G01 X{x0 + size} Y{y0 + y}
G01 X{x0} Y{y0 + y}
G01 X{x0} Y{y0}
G00 X{x0} Y{y0}
G00 X{x0} Y{y0} Z0
"""

def side_b(start_x, start_y):
    x0 = start_x + margin
    y0 = start_y + margin

    return f"""
G00 X{x0} Y{y0}
G01 X{x0} Y{y0} Z-{z}
G01 X{x0 + x} Y{y0}
G01 X{x0 + x} Y{y0 + y - notch}
G01 X{x0 + x - z} Y{y0 + y - notch}
G01 X{x0 + x - z} Y{y0 + y}
G01 X{x0 + z} Y{y0 + y}
G01 X{x0 + z} Y{y0 + y - notch}
G01 X{x0} Y{y0 + y - notch}
G01 X{x0} Y{y0}
G00 X{x0} Y{y0} Z0
"""

print(f"""%
G00
G17
G21
G54
G90
M04
M08
{side_a(0, 0)}
{side_a(0, y + margin)}
{side_b(0, 2 * (y + margin))}
{side_b(0, 3 * (y + margin))}
M05
M09
G28 X0 Y0
M30
%""")
