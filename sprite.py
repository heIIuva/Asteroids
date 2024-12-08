# sprite.py
import math
import random
from vector import Vector
from config import CANVAS_WIDTH, CANVAS_HEIGHT, ROCK_RADIUS

class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image_name, image_manager, radius, lifespan=None, animated=False):
        self.pos = pos
        self.vel = vel
        self.angle = ang
        self.angle_vel = ang_vel
        self.image_name = image_name
        self.image_manager = image_manager
        self.radius = radius
        self.lifespan = lifespan
        self.animated = animated
        self.age = 0

    def draw(self, canvas, drawn_images):
        angle_degs = math.degrees(self.angle)
        img = self.image_manager.get_rotated_image(self.image_name, angle_degs)
        if img:
            canvas.create_image(self.pos.x, self.pos.y, image=img)
            drawn_images.append(img)  # сохраняем ссылку
        else:
            canvas.create_oval(self.pos.x - self.radius, self.pos.y - self.radius,
                               self.pos.x + self.radius, self.pos.y + self.radius, fill='white')

    def update(self):
        self.angle += self.angle_vel
        self.pos.add(self.vel)
        # Выход за границы
        self.pos.x %= CANVAS_WIDTH
        self.pos.y %= CANVAS_HEIGHT

        if self.lifespan is not None:
            self.age += 1
            return self.age < self.lifespan
        return True

    def collide(self, other):
        dist = math.sqrt((self.pos.x - other.pos.x)**2 + (self.pos.y - other.pos.y)**2)
        return dist <= (self.radius + other.radius)

def random_rock(image_name, image_manager):
    pos = Vector(random.randrange(CANVAS_WIDTH), random.randrange(CANVAS_HEIGHT))
    vel = Vector(random.uniform(-1, 1), random.uniform(-1, 1))
    ang = random.random() * 2 * math.pi
    ang_vel = random.uniform(-0.05, 0.05)
    return Sprite(pos, vel, ang, ang_vel, image_name, image_manager, ROCK_RADIUS)
