# ship.py

import math
from vector import Vector
from config import CANVAS_WIDTH, CANVAS_HEIGHT, SHIP_RADIUS

class Ship:
    def __init__(self, pos, vel, angle, image_name, image_thrust_name, image_manager, radius=SHIP_RADIUS):
        self.pos = pos
        self.vel = vel
        self.angle = angle
        self.thrust = False
        self.image_name = image_name
        self.image_thrust_name = image_thrust_name
        self.image_manager = image_manager
        self.radius = radius
        self.angle_vel = 0

    def draw(self, canvas, drawn_images):
        angle_degs = math.degrees(self.angle)
        current_image = self.image_thrust_name if self.thrust else self.image_name
        img = self.image_manager.get_rotated_image(current_image, angle_degs)
        if img:
            canvas.create_image(self.pos.x, self.pos.y, image=img)
            drawn_images.append(img)

    def update(self):
        self.angle += self.angle_vel

        forward = Vector(math.cos(self.angle), math.sin(self.angle))
        if self.thrust:
            self.vel.add(forward)
        self.vel.mul(0.95)

        self.pos.add(self.vel)
        self.pos.x %= CANVAS_WIDTH
        self.pos.y %= CANVAS_HEIGHT

    def set_thrust(self, on):
        self.thrust = on

    def rotate_left(self):
        self.angle_vel -= 0.05

    def rotate_right(self):
        self.angle_vel += 0.05

    def stop_rotate(self):
        self.angle_vel = 0

    def shoot(self, missile_image_name, missile_speed, missile_radius, lifespan):
        forward = Vector(math.cos(self.angle), math.sin(self.angle))
        from sprite import Sprite
        missile_pos = Vector(self.pos.x + forward.x * self.radius, self.pos.y + forward.y * self.radius)
        missile_vel = Vector(self.vel.x + forward.x * missile_speed, self.vel.y + forward.y * missile_speed)
        # Передаём также стартовую позицию снаряда для контроля расстояния
        return Sprite(missile_pos, missile_vel, self.angle, 0, missile_image_name, self.image_manager, missile_radius, lifespan, start_pos=missile_pos.copy())
