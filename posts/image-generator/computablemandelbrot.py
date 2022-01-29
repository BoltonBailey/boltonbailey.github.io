
# z0 = 0
# z -> z^2 + c
from fractions import Fraction
import random

from PIL import Image


CANVAS_SIZE = 1200

# Potential improvement:
# reimplement with polynomial and error terms as imports.
# e.g. (z + e)**2 = z^2 + 2ze + e^2


def subset_of(ball0, ball1):

    a0, b0, e0 = ball0
    a1, b1, e1 = ball1

    return e1 >= e0 and (a1 - a0)**2 + (b1 - b0)**2 <= (e1 - e0)**2


def disjoint(ball0, ball1):

    a0, b0, e0 = ball0
    a1, b1, e1 = ball1

    return (a1 - a0)**2 + (b1 - b0)**2 > (e1 + e0)**2


def simplify_expand(ball, n):
    """A simpler superset of the given ball

    Given a ball, returns a ball containing that ball, with a simpler
    description. Larger n means a smaller ball, but with less simple
    description.
    """

    a, b, e = ball

    a = Fraction(a.numerator * n / a.denominator + 1, n)
    b = Fraction(b.numerator * n / b.denominator + 1, n)
    e = Fraction(e.numerator * n / e.denominator + 1, n)

    e += Fraction(3, n)

    assert subset_of(ball, (a, b, e))

    return (a, b, e)


def print_ball(ball):
    a, b, e = ball

    if b < 0:
        print str(float(a)) + str(float(b)) + "i ~" + str(float(e))
    else:
        print str(float(a)) + "+" + str(float(b)) + "i ~" + str(float(e))


def prove_subset_mandelbrot(ball, accuracy):

    escape_ball = (Fraction(0), Fraction(0), Fraction(2))

    ball_set = set()

    a0, b0, e0 = ball

    cur_ball = (Fraction(0), Fraction(0), Fraction(0))

    while True:

        ball_set.add(cur_ball)

        if not subset_of(cur_ball, escape_ball):
            return False

        cur_a, cur_b, cur_e = cur_ball

        # Approximate an upper bound of the norm of the center of the current ball
        cur_norm_squared = cur_a**2 + cur_b**2

        cur_approx_norm = Fraction(1, 1)

        while abs(cur_approx_norm**2 - cur_norm_squared) > Fraction(1, accuracy):
            cur_approx_norm = (cur_approx_norm +
                               cur_norm_squared/cur_approx_norm)/2

        cur_approx_norm = max(
            cur_approx_norm, cur_norm_squared/cur_approx_norm)

        cur_approx_norm = cur_approx_norm.limit_denominator(accuracy)
        cur_approx_norm += Fraction(1, accuracy)

        assert cur_approx_norm**2 > cur_norm_squared

        new_a = cur_a**2 - cur_b**2 + a0
        new_b = 2 * cur_a * cur_b + b0
        new_e = 2 * cur_approx_norm * cur_e + cur_e**2 + e0

        new_ball = simplify_expand((new_a, new_b, new_e), accuracy)

        for ball in list(ball_set):
            if subset_of(new_ball, ball):
                return True
            if subset_of(ball, new_ball):
                ball_set.remove(ball)

        cur_ball = new_ball


def prove_disjoint_mandelbrot(ball, accuracy):

    escape_ball = (Fraction(0), Fraction(0), Fraction(2))

    a0, b0, e0 = ball

    cur_ball = (Fraction(0), Fraction(0), Fraction(0))

    while True:

        if disjoint(cur_ball, escape_ball):
            return True

        if subset_of(escape_ball, cur_ball):
            return False

        cur_a, cur_b, cur_e = cur_ball

        # Approximate an upper bound of the norm of the center of the current ball
        cur_norm_squared = cur_a**2 + cur_b**2

        cur_approx_norm = Fraction(1, 1)

        while abs(cur_approx_norm**2 - cur_norm_squared) > Fraction(1, accuracy):
            cur_approx_norm = (cur_approx_norm +
                               cur_norm_squared/cur_approx_norm)/2

        cur_approx_norm = max(
            cur_approx_norm, cur_norm_squared/cur_approx_norm)

        cur_approx_norm = cur_approx_norm.limit_denominator(accuracy)
        cur_approx_norm += Fraction(1, accuracy)

        assert cur_approx_norm**2 > cur_norm_squared

        new_a = cur_a**2 - cur_b**2 + a0
        new_b = 2 * cur_a * cur_b + b0
        new_e = 2 * cur_approx_norm * cur_e + cur_e**2 + e0

        new_ball = simplify_expand((new_a, new_b, new_e), accuracy)

        cur_ball = new_ball


def display_ball(ball, color, canvas):

    a, b, e = ball

    x0 = float(((a + e) + 2) * CANVAS_SIZE / 4)
    x1 = float(((a - e) + 2) * CANVAS_SIZE / 4)
    y0 = float(((b + e) + 2) * CANVAS_SIZE / 4)
    y1 = float(((b - e) + 2) * CANVAS_SIZE / 4)

    canvas.create_oval(x0, y0, x1, y1, fill=color, outline=color)


def main():

    im = Image.new('RGB', (1024, 1024))
    vector = []
    for _ in range(1024**2):
        color = (random.choice(range(256)), random.choice(
            range(256)), random.choice(range(256)))
        vector.append(color)

    im.putdata(vector)
    im.save('test.png')

    quit()

    unresolved_squares = [
        (Fraction(-2), Fraction(2), Fraction(-2), Fraction(2))]

    while True:

        smaller_unresolved_squares = set()

        for square in unresolved_squares:

            min_x, max_x, min_y, max_y = square

            avg_x = (min_x + max_x)/2
            avg_y = (min_y + max_y)/2

            side_length = (max_x - min_x)
            assert side_length == (max_y - min_y)

            # Find a superset ball
            ball = (avg_x, avg_y, side_length * Fraction(708, 1000))

            refinement = side_length.denominator / \
                max(abs(side_length.numerator), 1) + 1

            if prove_subset_mandelbrot(ball, refinement * 10):
                # If we prove its in
                display_ball(ball, "black", canvas)

            elif prove_disjoint_mandelbrot(ball, refinement * 10):
                # If we prove its out
                display_ball(ball, "grey", canvas)

            else:
                # Neither, look more closely
                smaller_unresolved_squares.add((min_x, avg_x, min_y, avg_y))
                smaller_unresolved_squares.add((avg_x, max_x, min_y, avg_y))
                smaller_unresolved_squares.add((min_x, avg_x, avg_y, max_y))
                smaller_unresolved_squares.add((avg_x, max_x, avg_y, max_y))

            canvas.pack()

            top.update()

        unresolved_squares = smaller_unresolved_squares

    # top.mainloop()


if __name__ == '__main__':
    main()
