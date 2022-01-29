

# from PIL import Image, ImageDraw
import colorsys
import math

import imagegenerator


class MandelbrotImage(imagegenerator.PlaneImage):

    def __init__(self):

        super(MandelbrotImage, self).__init__()

    def color_func(self, x, y):
        c = x + y * 1.0j

        z_cur = 0

        iteration = 0

        max_iter = 200

        while abs(z_cur) <= 50 and iteration < max_iter:
            z_cur = z_cur**2 + c
            iteration += 1

        if iteration == max_iter:
            return (0, 0, 0)

        # To provide a smooth color gradient, it is necessary to determine not
        # just which iteration the point escaped in, but also how close to the
        # edge of escaping it was, so to speak.

        # If z escapes, then the sequence
        #   log(|z_i|) / 2^i
        # Converges as i -> infty
        # This can be seen by analyzing the difference between adjacent terms
        #   log(|z_i^2 + c|) / 2^{i+1} - log(|z_i|) / 2^i
        #   = 1/2^{i+1} (log(|z_i^2 + c|) - 2log(|z_i|))
        #   = 1/2^{i+1} (log(|z_i^2 + c|/|z_i|^2))
        #   = 1/2^{i+1} (log(|(z_i^2 + c)/(z_i)|^2))
        #   = 1/2^{i+1} (log(|1 + c/z_i^2|))
        # which decreases exponentially with i when z_i has sufficiently large
        # magnitude.

        # We define the "escape iteration" i_escape to be the extrapolation of
        # the iteration at which we hit |z_escape| = 2 from the value of |z|
        # at a much later time. Since it is an extrapolation, this value is
        # not actually an integer.
        # To do this, we set log(|z_i|) / 2^i to be the same for both the
        # fictitious "escape iteration" and limit iterations.
        # log2(|z_i|) / 2^i = log2(2) / 2^i_escape
        # log2(|z_i|) / 2^i = 1 / 2^i_escape
        # i_escape = -log2(log2(|z_i|) / 2^i)
        # i_escape = i - log2(log2(|z_i|))

        i_escape = iteration - math.log(math.log(abs(z_cur), 2), 2)

        #value = float(iteration)/max_iter

        r, g, b = colorsys.hsv_to_rgb((i_escape / 25 + 0.7) % 1, 0.9, 0.9)

        return int(r * 256), int(g * 256), int(b * 256)


if __name__ == "__main__":

    gen = MandelbrotImage()
    width = 2880
    height = 1800
    im = gen.create_plane_image(width, height, -2.5, -1.25, 1.5, 1.25)

    im.save(f"./images/mandelbrot_{width}_{height}.png", "PNG")
