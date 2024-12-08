# game_logic.py
from config import LIVES, MISSILE_LIFESPAN, MISSILE_RADIUS, MISSILE_SPEED, ROCK_RADIUS
from sprite import random_rock

class GameLogic:
    def __init__(self, ship, images, image_manager):
        self.ship = ship
        self.images = images
        self.image_manager = image_manager
        self.started = False
        self.rocks = []
        self.missiles = []
        self.score = 0
        self.lives = LIVES

    def start(self):
        self.started = True
        self.score = 0
        self.lives = LIVES
        self.rocks = []
        self.missiles = []

    def add_rock(self):
        if not self.started:
            return

        if len(self.rocks) >= 15:
            return

        # Попытки сгенерировать астероид так, чтобы он не был слишком близко к кораблю
        for _ in range(5):
            rock = random_rock("rock", self.image_manager)
            dist = ((rock.pos.x - self.ship.pos.x)**2 + (rock.pos.y - self.ship.pos.y)**2)**0.5
            if dist > 2 * (ROCK_RADIUS + self.ship.radius):
                self.rocks.append(rock)
                return
        # Если за 5 попыток не получилось - просто пропускаем

    def update(self):
        if not self.started:
            return

        # Обновляем корабль
        self.ship.update()

        # Обновляем камни
        self.rocks = [r for r in self.rocks if r.update()]

        # Обновляем ракеты
        self.missiles = [m for m in self.missiles if m.update()]

        # Проверяем столкновения ракета-камень
        rocks_to_remove = []
        missiles_to_remove = []
        for r in self.rocks:
            for m in self.missiles:
                if r.collide(m):
                    rocks_to_remove.append(r)
                    missiles_to_remove.append(m)
                    self.score += 1
                    break
        self.rocks = [r for r in self.rocks if r not in rocks_to_remove]
        self.missiles = [m for m in self.missiles if m not in missiles_to_remove]

        # Проверяем столкновения корабль-камень
        for r in self.rocks:
            if r.collide(self.ship):
                self.lives -= 1
                self.rocks.remove(r)
                if self.lives <= 0:
                    self.started = False
                break

    def draw(self, canvas, drawn_images):
        # Отрисовать фон
        bg_img = self.image_manager.get_rotated_image("nebula", 0)
        canvas.create_image(400, 300, image=bg_img)
        drawn_images.append(bg_img)

        # Отрисовать корабль
        self.ship.draw(canvas, drawn_images)
        # Отрисовать камни
        for r in self.rocks:
            r.draw(canvas, drawn_images)
        # Отрисовать ракеты
        for m in self.missiles:
            m.draw(canvas, drawn_images)
        # Если игра не запущена - показать splash
        if not self.started:
            splash_img = self.image_manager.get_rotated_image("splash", 0)
            canvas.create_image(400, 300, image=splash_img)
            drawn_images.append(splash_img)

        # Показать счёт и жизни
        canvas.create_text(50, 30, text=f"Lives: {self.lives}", fill="white", font=("Helvetica", 16))
        canvas.create_text(750, 30, text=f"Score: {self.score}", fill="white", font=("Helvetica", 16))

    def shoot(self):
        if self.started:
            missile = self.ship.shoot("missile", MISSILE_SPEED, MISSILE_RADIUS, MISSILE_LIFESPAN)
            self.missiles.append(missile)