

from PIL import Image, ImageDraw
import progressbar


class PlaneImage(object):
    """A class for representing a image printed on the 2d plane.

    One can create images based on different rectangles on the plane.
    """

    def __init__(self):
        super(PlaneImage, self).__init__()

        # We sample some points from the rectangle corresponding to the pixel
        # We then average the colors of the sample.
        self.x_samples = 3
        self.y_samples = 3

    def create_plane_image(self, width, height, min_x, min_y, max_x, max_y):
        """Returns a PIL image corresponding to the specified window

        Arguments:
            width {int} --  Width  of input  image in pixels
            height {int} -- Height of output image in pixels
            min_x {float} -- Min x coordinate of the rectangular window
            min_y {float} -- [description]
            max_x {float} -- [description]
            max_y {float} -- [description]

        Returns:
            PIL.Image -- View of the plane image in this window.
        """

        im = Image.new("RGB", (width, height))

        draw = ImageDraw.Draw(im)

        # for i in progressbar.progressbar(range(width)): # With progressbar
        for i in range(width):
            for j in range(height):

                # Get the rectangle on the plane that the pixel corresponds to
                x_min_pixel = min_x + (max_x - min_x) * i / width
                x_max_pixel = min_x + (max_x - min_x) * (i+1) / width
                y_min_pixel = min_y + (max_y - min_y) * (height - j) / height
                y_max_pixel = min_y + (max_y - min_y) * (height - j - 1)/height

                # Average the r, g, b values over a grid of samples within the
                # pixel rectangle.
                r, g, b = 0, 0, 0

                for i_samp in range(self.x_samples):
                    for j_samp in range(self.y_samples):
                        x = x_min_pixel + i_samp * \
                            (x_max_pixel - x_min_pixel) / self.x_samples
                        y = y_min_pixel + j_samp * \
                            (y_max_pixel - y_min_pixel) / self.y_samples
                        dr, dg, db = self.color_func(x, y)
                        r += dr
                        g += dg
                        b += db

                r /= self.x_samples * self.y_samples
                g /= self.x_samples * self.y_samples
                b /= self.x_samples * self.y_samples

                # print(i, j, r, g, b)

                draw.point((i, j), (int(r), int(g), int(b)))

        return im

    def color_func(self, x, y):
        """Abstract method for returning the color at any given point."""

        raise NotImplementedError
