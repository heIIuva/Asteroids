# vector.py

import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Vector(self.x, self.y)

    def add(self, other):
        self.x += other.x
        self.y += other.y

    def mul(self, val):
        self.x *= val
        self.y *= val

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def rotate(self, angle):
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        x = self.x * cos_a - self.y * sin_a
        y = self.x * sin_a + self.y * cos_a
        self.x, self.y = x, y
