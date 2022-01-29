

import glob
from PIL import Image
import imagegenerator
from collections import Counter
# import cv2
import os

color_list = [
    (0, 0, 0),
    (0, 0, 127),
    (127, 127, 0),
    (255, 0, 255)
]

max_iters = 5000


class SandpileImage(imagegenerator.PlaneImage):

    def __init__(self, pile=Counter()):
        super(SandpileImage, self).__init__()
        self.x_samples = 1
        self.y_samples = 1

        self.pile = pile

    def color_func(self, x, y):
        x, y = round(x), round(y)
        return color_list[self.pile[x, y]]

    # def pile_size(n):
    #     if n == 0:
    #         return {(0, 0): 0}
    #     elif n % 2 == 0:
    #         small_pile = pile_size(n/2)
    #         return add_piles(small_pile, small_pile)
    #     else:
    #         return add_piles(pile_size(n-1), {(0, 0): 1})

    def __add__(self, other):

        if not isinstance(other, SandpileImage):
            raise ValueError("Cannot add sandpile to non sandpile")

        new_pile = SandpileImage(self.pile + other.pile)

        new_pile.collapse()

        return SandpileImage(new_pile)

    def collapse(self, uncollapsed=None):

        if uncollapsed is None:
            uncollapsed = set(self.pile)

        while uncollapsed:

            i, j = uncollapsed.pop()

            if self.pile[i, j] >= 4:

                collapses = self.pile[(i, j)] // 4

                self.pile[(i, j)] -= 4 * collapses

                self.pile[(i+1, j)] += collapses
                self.pile[(i-1, j)] += collapses
                self.pile[(i, j+1)] += collapses
                self.pile[(i, j-1)] += collapses

                uncollapsed.add((i+1, j))
                uncollapsed.add((i-1, j))
                uncollapsed.add((i, j+1))
                uncollapsed.add((i, j-1))

    def add_grain(self, x=0, y=0):
        self.pile[x, y] += 1
        self.collapse()


sandpile = SandpileImage()

imgs = []

for i in range(max_iters):
    im = sandpile.create_plane_image(101, 101, -50, -50, 50, 50)
    imgs.append(im)
    # im.save(f"images/sandpile/sandpile_{i}.png", "PNG")
    sandpile.add_grain()


# Create the frames
frames = []
# imgs = glob.glob("images/sandpile/*.png")
for im in imgs:
    frames.append(im)

# Save into a GIF file that loops forever
frames[0].save('images/sandpile/sandpile.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=30, loop=0)
