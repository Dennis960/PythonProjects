import numpy as np
import matplotlib.pyplot as plt
import math

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y-other.y)
    def __mul__(self, other):
        if type(other) == Vector:
            return self.x*other.x + self.y*other.y
        else:
            return Vector(self.x*other, self.y*other)
    def __rmul__(self, other):
        if type(other) == Vector:
            return self.x*other.x + self.y*other.y
        else:
            return Vector(self.x*other, self.y*other)
    def np(self):
        return [self.x, self.y]
    def orthogonal(self):
        return Vector(-self.y, self.x)
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)


def draw_vector(vector:Vector, position:Vector):
    origin = np.array([[position.np(), position.np()]])
    return plt.quiver(position.x, position.y, vector.x, vector.y, color='r', scale=50)

def get_position(alpha):
    rad = alpha/360 * 2*math.pi
    return Vector(math.sin(rad)*5, math.cos(rad)*5)

Fg = Vector(0, -9.81)

def draw_fg(alpha):
    return draw_vector(Fg, get_position(alpha))

def get_fp_direction(alpha):
    orthogonal = get_position(alpha).orthogonal()
    return orthogonal/orthogonal.length()

def calc_fp(alpha):
    Fp_dir = get_fp_direction(alpha)
    Fp_length = 10
    return Fp_dir*Fp_length

def draw_fp(alpha):
    return draw_vector(calc_fp(alpha), get_position(alpha))

def draw_ft(alpha):
    return draw_vector(Fg - calc_fp(alpha), get_position(alpha))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.xlim(-10, 10)
plt.ylim(-10, 10)

ax.add_patch(plt.Circle((0, 0), 5, fill=False))

for alpha in range(0,360):
    quiver = draw_fg(alpha)
    quiver2 = draw_fp(alpha)
    quiver3 = draw_ft(alpha)
    plt.pause(0.01)
    quiver.remove()
    quiver2.remove()
    quiver3.remove()

