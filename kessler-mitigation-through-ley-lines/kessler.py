from PIL import Image
import math

im = Image.open("images/Albedo.jpeg")

print(im.size)

WIDTH = 2048

earthIm = Image.new("RGB", (WIDTH, WIDTH))

# 128-64 to 128+64

SCALE = 50


# Object at (x, y, z) displays at pixel ()
def where_display(x, y, z):
    # x=2 y=2 z=1 => 0, 0
    return (WIDTH//2 - int(0.866 * (x - y) / SCALE),
            WIDTH//2 - int((z - 0.5 * x - 0.5 * y)/SCALE)
            )


drawn = set()


for a in range(0, im.size[0], 8):
    print(a)
    theta = 2 * math.pi * a / im.size[0] - 1.3
    for b in range(0, im.size[1], 8):
        phi = math.pi * (0.5 - (b / im.size[1]))

        x = math.cos(theta) * math.cos(phi) * 6000
        y = math.sin(theta) * math.cos(phi) * 6000
        z = math.sin(phi) * 6000

        if x + y + z > 0:
            loc = where_display(x, y, z)
            drawn.add(loc)
            earthIm.putpixel(loc, im.getpixel((a, b)))


# ellipse
# c = focus = 10000
# a = semimajor = 17000
# b = semiminor = math.sqrt(17000**2 - 10000**2)
# l = semilatrect = b^2 / a

c = 9000
a = 16000
b = math.sqrt(a**2 - c**2)
rect = b**2 / a

for t in range(WIDTH * 10):
    theta = 2 * math.pi * t / (WIDTH * 10)

    x = math.cos(theta) * rect
    y = math.sin(theta) * rect
    z = 0

    loc = where_display(x, y, z)

    if x + y + z > 0 or loc not in drawn:
        earthIm.putpixel(loc, (256, 0, 0))

for s in range(4):
    phi = math.pi / 4 * s

    for t in range(WIDTH * 10):
        theta = 2 * math.pi * t / (WIDTH * 10)

        x = math.cos(theta) * b * math.sin(phi)
        y = math.cos(theta) * b * math.cos(phi)
        z = c + math.sin(theta) * a

        loc = where_display(x, y, z)

        if x + y + z > 0 or loc not in drawn:
            earthIm.putpixel(loc, (256, 0, 0))

for s in range(4):
    phi = math.pi / 4 * s

    for t in range(WIDTH * 10):
        theta = 2 * math.pi * t / (WIDTH * 10)

        x = math.cos(theta) * b * math.sin(phi)
        y = math.cos(theta) * b * math.cos(phi)
        z = -c + math.sin(theta) * a

        loc = where_display(x, y, z)

        if x + y + z > 0 or loc not in drawn:
            earthIm.putpixel(loc, (256, 0, 0))

# earthIm.show()
earthIm.save("images/leylines2.png")
