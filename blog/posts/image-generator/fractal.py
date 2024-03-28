import random
import imagegenerator


def random_condition():
    """ Returns a random set of points, in functional form """

    shape = random.choice(["circle", "rectangle", "triangle"])

    if shape == "circle":
        def in_circle(x, y):


class FractalImageGenerator(imagegenerator.PlaneImage):

    def __init__(self):
        super(FractalImageGenerator, self).__init__()

    def color_func(self):

        for i in range(-100, 100):
            for j in range(-100, 100):
